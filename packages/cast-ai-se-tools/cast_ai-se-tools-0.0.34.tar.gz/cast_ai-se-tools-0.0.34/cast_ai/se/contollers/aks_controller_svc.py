import logging
from azure.mgmt.containerservice import ContainerServiceClient


from cast_ai.se.models.cloud_confs import AksConfig
from cast_ai.se.models.execution_status import ExecutionStatus
from cast_ai.se.contollers.cloud_controller_svc import CloudController


class AKSController(CloudController):
    def __init__(self, azure_conf: AksConfig):
        try:
            self._conf = azure_conf
            self._logger = logging.getLogger(__name__)
            self._client = ContainerServiceClient(self._conf.credential, self._conf.subscription_id)
            self._cluster = self._client.managed_clusters.get(self._conf.resource_group, self._conf.cluster_name)
            self.scale(2)
        except Exception as e:
            self._logger.critical(f"An error occurred during EKSController initialization: {str(e)}")
            raise RuntimeError(f"An error occurred during EKSController initialization: {str(e)}")

    def scale(self, node_count: int) -> ExecutionStatus:

        self._logger.info(f"{'-' * 70}[ Scaling AKS Node Pool to {node_count} nodes ]")
        try:
            node_pool = next(pool for pool in self._cluster.agent_pool_profiles if pool.name == self._conf.node_pool)
            node_pool.count = node_count
            update_operation = self._client.managed_clusters.begin_create_or_update(self._conf.resource_group,
                                                                                    self._conf.cluster_name,
                                                                                    self._cluster)
            return ExecutionStatus()
        except Exception as e:
            self._logger.exception(f"Error trying to set Demo Nodes capacity: {str(e)}")
            raise RuntimeError(f"Error trying to set Demo Nodes capacity: {str(e)}")
