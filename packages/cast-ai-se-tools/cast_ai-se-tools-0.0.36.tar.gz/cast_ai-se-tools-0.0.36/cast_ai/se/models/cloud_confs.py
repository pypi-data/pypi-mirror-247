import logging
from azure.identity import ClientSecretCredential


class EksConfig:
    def __init__(self, aws_conf: dict):
        self._logger = self._logger = logging.getLogger(__name__)
        try:
            self.region = aws_conf["REGION"]
            self.asg = aws_conf["AUTOSCALING_GROUP"]
            self.access_key = aws_conf["ACCESS_KEY"]
            self.access_secret_key = aws_conf["ACCESS_SECRET_KEY"]
        except Exception as e:
            self._logger.critical(f"Was not able to initialize aws config:{str(e)}")
            raise RuntimeError(f"Was not able to initialize aws config:{str(e)}")


class AksConfig:
    def __init__(self, azure_conf: dict):
        self._logger = self._logger = logging.getLogger(__name__)
        try:
            self.tenant_id = azure_conf["TENANT_ID"]
            self.node_pool = azure_conf["NODE_POOL"]
            self.client_id = azure_conf["CLIENT_ID"]
            self.client_secret = azure_conf["CLIENT_SECRET"]
            self.credential = ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)
            self.subscription_id = azure_conf["SUBSCRIPTION_ID"]
            self.cluster_name = azure_conf["CLUSTER_NAME"]
            self.resource_group = azure_conf["RESOURCE_GROUP"]
        except Exception as e:
            self._logger.critical(f"Was not able to initialize azure config:{str(e)}")
            raise RuntimeError(f"Was not able to initialize azure config:{str(e)}")
