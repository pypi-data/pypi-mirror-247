import simple_salesforce
# from apollo import ApolloClient
from prefect.blocks.system import Secret

class ClientMgr:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self._available_tools = ["apollo", "salseforce"]

    def health(self):
        print("health check")
        return "health check"

    def get_client(self, tool):
        if tool not in self._available_tools:
            raise Exception("not available tool")

        if tool == "salesforce":
            return self._get_client_salesforce

        # if tool == "apollo":
        #     return self._get_client_apollo

    def _get_client_salesforce(self):
        # Salesforce credentials
        sf_username, sf_password, sf_security_token = self._get_salesforce_credentials()
        sf = simple_salesforce.Salesforce(username=sf_username, password=sf_password, security_token=sf_security_token)
        return sf

    def _get_salesforce_credentials(self):
        sf_username = Secret.load(f"{self.tenant_id}_SF_USERNAME").get()
        sf_password = Secret.load(f"{self.tenant_id}_SF_PASSWORD").get()
        sf_security_token = Secret.load(f"{self.tenant_id}_SF_SECURITY_TOKEN").get()
        return sf_username, sf_password, sf_security_token

    # def _get_client_apollo(self):
    #     apollo_api_key = self._get_apollo_credentials
    #     apollo = ApolloClient(apollo_api_key)
    #     return apollo

    # def _get_apollo_credentials(self):
    #     apollo_api_key = Secret.load(f"{self.tenant_id}_APOLLO_API_KEY").get()
    #     return apollo_api_key




