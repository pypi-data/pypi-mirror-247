import os
import sys
import json
import requests
import logging
import time
import csv
import re
import traceback

from django.urls import reverse, resolve
from django.conf.urls import url, include
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse

from dateutil import parser as dateparser

from enrichsdk.app.utils import clean_and_validate_widgets
from enrichsdk.lib import get_credentials_by_name

logger = logging.getLogger("app")

class SalesforceClient:

    def __init__(self, cred):

        if isinstance(cred, str):
            self.cred = get_credentials_by_name(cred)
        else:
            self.cred = cred
        self.baseurl = self.cred['url']
        self.token = None
        self.salesforce_version = "v58.0"
        
    def get_token(self, force=False):
        """
        Get access token...
        """
        sample_token = {
            'access_token': '00D7j000000H9Ht!AR...',
            'instance_url': 'https://acmecompanycompany--preprod.sandbox.my.salesforce.com',
            'id': 'https://test.salesforce.com/id/00D7j000000H9HtEAK/0057j0000053bRfAAI',
            'token_type': 'Bearer',
            'issued_at': '1697972695996',
            'signature': 'BQ+dEwXSrqZcZtqXYGSYR2B+9+3eftIeBjT92Dv2YYI='
        }

        # Assumption. We dont know when the token will expire. It is
        # said to be 2 hours in documentation
        timeout = 3600*1000
        now = int(1000*time.time())
        if ((not force) and
            (self.token is not None) and
            (isinstance(self.token, dict)) and
            ('access_token' in self.token) and
            (now < (int(self.token['issued_at']) + timeout))):
            return self.token['access_token']

        tokenurl = self.baseurl + "/services/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Construct the oauth request
        cred = self.cred
        data = {
            "grant_type": "password",
            "client_id": cred['client_id'],
            "client_secret": cred['client_secret'],
            "username": cred['username'],
            "password": cred['password'] + cred['client_security_token']
        }

        msg = ""
        msg += f"Token URL: {tokenurl}\n"
        for k, v in data.items():
            if k != "password":
                msg += f"{k}: {str(v)[:8]}...\n"
            else:
                msg += f"{k}: ****...\n"
            result = requests.post(tokenurl, data=data, headers=headers)
        try:
            self.token = result.json()
            if result.status_code == 200:
                logger.debug("Salesforce token obtained",
                             extra={
                                 'data': msg
                             })
            else:
                logger.error("Failed to obtained Salesforce token",
                             extra={
                             'data': msg + str(result.content)
                             })
        except:
                logger.exception("Failed to obtained Salesforce token",
                             extra={
                             'data': msg + str(result.content)
                             })

        return self.token['access_token']

    def access_salesforce(self, url, method="get",
                          params={}, data={},
                          request=None):

        token = self.get_token()
        url = self.baseurl + url
        headers = {
            'Authorization': f"Bearer {token}"
        }

        if method == "get":
            result = requests.get(url, params=params, headers=headers)
        elif method == "post":
            result = requests.post(url, params=params, headers=headers, json=data)
        elif method == "patch":
            result = requests.patch(url, params=params, headers=headers, json=data)
        else:
            raise Exception(f"Unknown access method: {method}")

        if result.status_code >= 400:
            logger.error("Failed to access Salesforce",
                         extra={

                             'data': f"URL: {url}\nOutput: {result.content}"
                         })
        try:
            if method != "patch":
                status, result = result.status_code, result.json()
            else:
                status, result = result.status_code, {}

            # [{"message":"Jurisdiction: bad value for restricted picklist field: State of Washington","errorCode":"INVALID_OR_NULL_FOR_RESTRICTED_PICKLIST","fields":["Jurisdiction__c"]}]
            if ((request is not None) and
                (isinstance(result, (dict, list))) and
                (len(result) > 0)):
                res = result
                if isinstance(res, list):
                    res = res[0]
                if isinstance(res, dict) and ("message" in res):
                    messages.error(request, "Salesforce message: " + res['message'])

            if 'nextRecordsUrl' in result:
                messages.error(request, "Internal error. A few search results were not processed. Please contact support")

            return status, result
        except:
            logger.exception("Failed to access Salesforce",
                             extra={
                                 'data': f"URL: {url}\n"
                             })

        raise Exception("Failed to access Salesforce")

    def run_query(self, query, request=None):

        query = re.split(r"\s+", query)
        query = "+".join(query)
        opurl = f"/services/data/{self.salesforce_version}/query/?q={query}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to run query")
        return result

    def get_opportunity_by_id(self, oppid, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/{oppid}"
        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to get opportunity")
        return result

    def describe_opportunity(self, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/describe"
        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to describe opportunity")
        return result

    def get_opportunities(self, limit=200, columns=None, request=None):

        fields = "FIELDS(ALL)"
        if columns is not None:
            fields = ",".join(columns)

        opurl = f"/services/data/{self.salesforce_version}/query/?q=SELECT+{fields}+FROM+Opportunity+ORDER+BY+LastModifiedDate+DESC+LIMIT+{limit}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to query for opportunities")
        return result

    def get_opportunity_detail(self, oppid, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/{oppid}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to get opportunity detail")
        return result

    def add_opportunity(self, data, request=None):
        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity"
        status, result = self.access_salesforce(opurl, method="post", data=data, request=request)
        if status >= 400:
            raise Exception("Failed to add opportunity")
        return result

    def update_opportunity(self, oppid, data, request=None):
        opurl = f"/services/data/{self.salesforce_version}/sobjects/Opportunity/{oppid}"
        status, result = self.access_salesforce(opurl,
                                                method="patch",
                                                data=data,
                                                request=request)
        if status >= 400:
            raise Exception("Failed to add opportunity")
        return result

    def get_accounts(self, limit=200, columns=None, request=None):

        fields = "FIELDS(ALL)"
        if columns is not None:
            fields = ",".join(columns)

        opurl = f"/services/data/{self.salesforce_version}/query/?q=SELECT+{fields}+FROM+Account+ORDER+BY+LastModifiedDate+DESC+LIMIT+{limit}"

        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception("Failed to query for opportunities")
        return result

    def add_account(self, data, request=None):
        opurl = f"/services/data/{self.salesforce_version}/sobjects/Account"
        status, result = self.access_salesforce(opurl,
                                                method="post",
                                                data=data, request=request)
        if status >= 400:
            raise Exception("Failed to add account")
        return result

    def get_account_by_id(self, accid, request=None):

        opurl = f"/services/data/{self.salesforce_version}/sobjects/Account/{accid}"
        status, result = self.access_salesforce(opurl, request=request)
        if status >= 400:
            raise Exception(f"Failed to get account details: {accid}")
        return result

#############################################
#=> Fields in Salesforce Opportunity Object
#############################################
# Account_Name__c: null,
# Account_Region__c: null,
# Active_Headcount__c: null,
# Amount: 4810308.0,
# Amount_Lost__c: 0.0,
# Amount_M__c: 5.0,
# LastActivityDate: null,
# LastAmountChangedHistoryId: null,
# LastCloseDateChangedHistoryId: null,
# LastModifiedById: 0057j0000053bRfAAI,
# LastModifiedDate: 2023-10-19T17:37:53.000+0000,
# ....

class SalesforceBaseMixin:

    def salesforce_update_urlpatterns(self, prefix, urlpatterns):
        urlpatterns.extend([
            url(f'^{prefix}[/]?$', self.salesforce_index, name="salesforce_index"),
            url(f'^{prefix}/detail/(?P<oppid>[a-zA-Z0-9]+)[/]?$', self.salesforce_detail, name="salesforce_detail"),
        ])

    def salesforce_update_templates(self, templates):
        templates.update({
            'salesforce_index': 'sharedapp/generic_index.html',
            'salesforce_detail': 'sharedapp/generic_index.html',
        })

    def get_client(self, request, spec):

        # Get the salesforce client...
        cred = spec['cred']
        cred = get_credentials_by_name(cred)
        if hasattr(self, "salesforce_client"):
            client = self.salesforce_client
        else:
            client = self.salesforce_client = SalesforceClient(cred)

        return cred, client

    #################################################################
    # All Salesforce
    #################################################################
    def salesforce_index_get_extra_header_components(self, request, spec):

        r = resolve(request.path)
        return []

    def salesforce_index_finalize_entry(self, request, spec, opportunity, entry):
        return entry

    def salesforce_index_finalize_widgets(self, request, spec,
                                          opportunities, widgets):
        return widgets

    def salesforce_index_get_extra_actions(self, request, spec,
                                           opportunity,
                                           entry):
        return {}, []

    def salesforce_index_get_opportunities(self, request, spec):

        cred, client = self.get_client(request, spec)

        opportunities = client.get_opportunities(columns=[
            "Name",
            "Amount",
            "Id",
            "CreatedDate"
        ], request=request)

        return opportunities
    
    def salesforce_index_get_columns(self, request, spec, data):

        columns = [
            "Added", 'Name', "Amount (M$)",
        ]

        workflowcols = []
        detailcols = []
        
        if len(data) > 0: 
            for k in data[0].keys():
                if k in columns:
                    continue
                if k.startswith("ACTION_"):
                    detailcols.append(k)
                else:
                    workflowcols.append(k)
        columns += [
            ('Workflow', workflowcols),
            ('Details', detailcols)
        ]
        return columns

    def salesforce_index_finalize_data(self, request, spec, data):
        return data
    
    def salesforce_index(self, request, spec):

        r = resolve(request.path)

        usecase = spec['usecase']
        namespace = spec['namespace']
        cred = get_credentials_by_name(spec['cred'])
        
        # First get the opportunities
        opportunities = self.salesforce_index_get_opportunities(request, spec)
        
        workflowcols = []
        data = []
        for o in opportunities.get('records',[]):

            amount = o['Amount']
            if amount is None:
                amount = 0
            amount = round(amount/10**6, 1)
            
            dt = dateparser.parse(o['CreatedDate'])
            detailurl = reverse(r.namespace + ":salesforce_detail",
                                kwargs={
                                    'oppid': o['Id']
                                })
            entry = {
                "Added": dt.replace(microsecond=0).strftime("%Y-%m-%d"),
                "Amount (M$)": amount,
                "ACTION_SALESFORCE": {
                    "title": "Details",
                    "alt": "",
                    "class": "",
                    "template": "action_icon_compact",
                    "target": "_blank",
                    "icon": "salesforce_24x24",
                    "url": f"{cred['url']}/{o['Id']}"
                },
            }

            # Any cleanup before adding extra actions...
            entry = self.salesforce_index_finalize_entry(request, spec, o, entry)

            # Now add actions...
            extra, order = self.salesforce_index_get_extra_actions(request, spec, o, entry)
            entry.update(extra)

            data.append(entry)


        # How should I structure the output columns
        columns = self.salesforce_index_get_columns(request, spec, data)
        
        # Any header actions..
        extra_header_components = self.salesforce_index_get_extra_header_components(request, spec)

        widget = {
            "name": "Opportunities in Salesforce",
            "description": f"Recent entries and not the complete list",
            "type": "full_width_table_compact_actions",
            "columns": columns,
            "search": True,
            "rows": data,
            "order": [[0, "desc"]],
            "td_class": "white-space-normal wordwrap",
            "thead_th_class": "",
            "header_components": {
                "components": [
                    {
                        "template": "action_search"
                    }
                ]
            }
        }

        widgets = [widget]

        # Do any extra cleanup
        widgets = self.salesforce_index_finalize_widgets(request, spec,
                                                         opportunities,
                                                         widgets)

        clean_and_validate_widgets(widgets)

        data = {
            "title": "Salesforce",
            "sidebar_targets": self.get_sidebar(request, spec),
            "breadcrumb": "Salesforce",
            "widgets": widgets
        }

        # Cleanup and add any final note..
        data = self.salesforce_index_finalize_data(request, spec, data)
        
        template = self.get_template(spec, 'salesforce_index')
        return render(request,
                      template,
                      {
                          'app': self,
                          'usecase': usecase,
                          'spec': spec,
                          'basenamespace': r.namespace,
                          'data': data
                      })

    def salesforce_detail(self, request, spec, oppid):

        cred, client = self.get_client(request, spec)

        r = resolve(request.path)

        usecase = spec['usecase']
        namespace = spec['namespace']

        widgetspecs = []

        # => Get the opportunity object...
        detail = client.get_opportunity_by_id(oppid, request=request)
        accounts = {}
        data = []
        for name, value in detail.items():
            if not isinstance(value, str):
                value = str(value)
            data.append({
                "Attribute": name,
                "Value": value
            })

        plan_name = detail['Plan_Names_and_Registration_Numbers__c']
        plan_name = str(plan_name)
        widgetspecs.append({
            "name": plan_name,
            "description": "Opportunity detail in Salesforce",
            "data": data
        })

        # Get the consultant and plan sponsor objects as well..
        for name, label in [
                ['AccountId', "Plan Sponsor"],
                ['Intermediary__c', "Consultant"]
        ]:
            idval = detail[name]
            if idval is None:
                continue
            accdetail = client.get_account_by_id(idval, request)
            data = []
            for name, value in accdetail.items():
                if not isinstance(value, str):
                    value = str(value)
                data.append({
                    "Attribute": name,
                    "Value": value
                })
            widgetspecs.append({
                "name": f"{label} - {accdetail['Account_Short_Name__c']}",
                "description": "Details of account",
                "data": data
            })

        columns = [
            "Attribute", "Value"
        ]

        widgets = []
        for widgetspec in widgetspecs:
            widget = {
                "name": widgetspec['name'],
                "description": widgetspec['description'],
                "type": "full_width_table_compact_actions",
                "columns": columns,
                "search": True,
                "rows": widgetspec['data'],
                "order": [[0, "asc"]],
                "td_class": "white-space-normal wordwrap",
                "thead_th_class": "",
                "header_components": {
                    "components": [
                        {
                            "template": "action_search"
                        }
                    ]
                }
            }
            widgets.append(widget)

        clean_and_validate_widgets(widgets)

        data = {
            "title": "Salesforce",
            "sidebar_targets": self.get_sidebar(request, spec),
            "breadcrumbs": [
                {
                    "name": "Salesforce",
                    "url": reverse(r.namespace + ":salesforce_index"),
                },
                {
                    "name": "Detail"
                }
            ],
            "widgets": widgets
        }

        template = self.get_template(spec, 'salesforce_detail')
        return render(request,
                      template,
                      {
                          'app': self,
                          'usecase': usecase,
                          'spec': spec,
                          'basenamespace': r.namespace,
                          'data': data
                      })


if __name__ == "__main__":

    salesforce = SalesforceClient(cred="acme-salesforce")

    results = salesforce.get_opportunities()
    print(json.dumps(results, indent=4))

    #results = salesforce.describe_opportunity()
    #print(json.dumps(results, indent=4))

