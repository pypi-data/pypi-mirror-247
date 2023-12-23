import logging

from spaceone.core.connector.space_connector import SpaceConnector
from spaceone.core.manager import BaseManager

_LOGGER = logging.getLogger(__name__)

_GET_RESOURCE_METHODS = {
    "identity.Project": "get_project",
    "identity.ServiceAccount": "get_service_account",
}


class IdentityManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identity_connector: SpaceConnector = self.locator.get_connector(
            "SpaceConnector", service="identity"
        )

    def get_domain(self, domain_id):
        return self.identity_connector.dispatch("Domain.get", {"domain_id": domain_id})

    def get_user(self, user_id, domain_id):
        return self.identity_connector.dispatch(
            "User.get", {"user_id": user_id, "domain_id": domain_id}
        )

    def get_project(self, project_id: str, domain_id: str = None) -> dict:
        conditions = {"project_id": project_id}

        if domain_id:
            conditions["domain_id"] = domain_id

        return self.identity_connector.dispatch("Project.get", conditions)

    def check_workspace(self, workspace_id: str, domain_id: str) -> dict:
        return self.identity_connector.dispatch(
            "Workspace.check", {"workspace_id": workspace_id, "domain_id": domain_id}
        )

    def get_service_account(self, service_account_id, domain_id):
        return self.identity_connector.dispatch(
            "ServiceAccount.get",
            {"service_account_id": service_account_id, "domain_id": domain_id},
        )

    def get_resource(self, resource_type, resource_id, domain_id):
        if resource_type == "identity.Project":
            return self.get_project(resource_id)
        elif resource_type == "identity.ServiceAccount":
            return self.get_service_account(resource_id, domain_id)

    def list_service_accounts(self, query, domain_id):
        return self.identity_connector.dispatch(
            "ServiceAccount.list", {"query": query, "domain_id": domain_id}
        )
