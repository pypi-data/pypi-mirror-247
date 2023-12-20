"""
Get the environment object
"""
import os
import sys
import copy
import yaml
import json
import logging

logger = logging.getLogger()

class Context:
    def __init__(self, config=None, *args, **kwargs):

        self.context = {}

        if config is None:
            if "ENRICH_CONTEXT" in os.environ:
                config = os.environ["ENRICH_CONTEXT"]
                if not os.path.exists(config):
                    raise Exception("Context file missing: {}".format(config))
            elif os.path.exists('context.yml'):
                config = "context.yml"
            elif os.path.exists('context.yaml'):
                config = "context.yaml"

        if config is not None:
            if isinstance(config, str):
                try:
                    if config.endswith(".json"):
                        config = json.load(open(config))
                    elif (config.endswith(".yaml") or config.endswith(".yml")):
                        config = yaml.load(open(config), Loader=yaml.FullLoader)
                    else:
                        raise Exception("Unknown input format")
                except:
                    raise
                self.context = config
            elif isinstance(config, dict):
                self.context = config
            else:
                raise Exception("Invalid context file")

        # => Priority yaml config -> environment variables..
        # Root has to be specified
        if "ENRICH_ROOT" not in self.context:
            if "ENRICH_ROOT" in os.environ:
                self.context["ENRICH_ROOT"] = os.environ["ENRICH_ROOT"]
            else:
                logger.warning(
                    "ENRICH_ROOT must ideally be specified in context file or environment. Using default /tmp/enrich")
                self.context['ENRICH_ROOT'] = os.environ['ENRICH_ROOT'] = '/tmp/enrich'

        defaults = {
            "ENRICH_RUN_ROOT": "%(ENRICH_ROOT)s",
            "ENRICH_DATA": "%(ENRICH_ROOT)s/data",
            "ENRICH_ETC": "%(ENRICH_ROOT)s/etc",
            "ENRICH_SHARED": "%(ENRICH_ROOT)s/shared",
            "ENRICH_VAR": "%(ENRICH_ROOT)s/var",
            "ENRICH_LIB": "%(ENRICH_ROOT)s/lib",
            "ENRICH_OPT": "%(ENRICH_ROOT)s/opt",
            "ENRICH_LOGS": "%(ENRICH_ROOT)s/logs",
            "ENRICH_CUSTOMERS": "%(ENRICH_ROOT)s/customers",
            "ENRICH_RELEASES": "%(ENRICH_ROOT)s/releases",
            "ENRICH_TEST": "%(ENRICH_ROOT)s/test",
            "ENRICH_MANAGE": "%(ENRICH_ROOT)s/manage",
            "versionmap": "%(ENRICH_ROOT)s/etc/versionmap.json",
            "django-env": "%(ENRICH_ROOT)s/etc/django-env",
            "EMAIL_HOST": "unknown",
            "EMAIL_HOST_USER": "notset",
            "EMAIL_HOST_PASSWORD": "notset",
            "EMAIL_PORT": "9999",
            "EMAIL_USE_TLS": "TRUE",
        }

        for k, v in defaults.items():
            if k not in self.context:
                # If specified in the environment
                if k in os.environ:
                    self.context[k] = os.environ[k]
                else:
                    self.context[k] = v

        # For siteconf check the available alternatives. If none
        # present, then dont add the entry.
        k = "siteconf"
        if k not in self.context:
            if k in os.environ:
                self.context[k] = os.environ[k]
            else:
                for s in [
                    "%(ENRICH_ROOT)s/etc/siteconf.jsonx",
                    "%(ENRICH_ROOT)s/etc/siteconf.json",
                ]:
                    try:
                        s = s % self.context
                        if os.path.exists(s):
                            self.context[k] = s
                            break
                    except:
                        pass

        # Resolve all of them...
        for k, v in self.context.items():
            if isinstance(v, str):
                v = v % self.context
                self.context[k] = v

        if "ENRICH_ROOT" not in self.context:
            print("Please define ENRICH_ROOT or provide a environmental context file")
            raise Exception("Missing ENRICH_ROOT. Cant build context")

    def set_var(self, k, v):
        """
        Update the value for given context variable
        """
        self.context[k] = v

    def get_var(self, k):
        """
        Get the value for given context variable
        """
        return self.context.get(k, None)

    def validate(self):

        for attr in ["ENRICH_ROOT", "ENRICH_DATA", "ENRICH_CUSTOMERS", "ENRICH_ETC"]:
            if attr not in self.context:
                raise Exception("Incomplete context")

    def set_env(self):
        """
        Set the environment using the context
        """
        update = {k: v for k, v in self.context.items() if k.isupper()}
        os.environ.update(update)

    def asdict(self):
        return copy.copy(self.context)
