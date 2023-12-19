import simple_salesforce
from prefect.blocks.system import Secret
import requests

class ClientMgr:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self._available_tools = ["apollo", "salesforce"]
        self.apollo_base_url = "https://api.apollo.io/v1"
    def health(self):
        print("health check")
        return "health check"

    def get_client(self, tool):
        if tool not in self._available_tools:
            raise Exception("not available tool")

        if tool == "salesforce":
            return self._get_client_salesforce()

        if tool == "apollo":
            return self._get_http_client_apollo()

    def _get_client_salesforce(self):
        # Salesforce credentials
        sf_username, sf_password, sf_security_token = self._get_salesforce_credentials()
        sf = simple_salesforce.Salesforce(username=sf_username, password=sf_password, security_token=sf_security_token)
        return sf

    def _get_salesforce_credentials(self):
        sf_username = Secret.load(f"{self.tenant_id}-sf-username").get()
        sf_password = Secret.load(f"{self.tenant_id}-sf-password").get()
        sf_security_token = Secret.load(f"{self.tenant_id}-sf-security-token").get()
        return sf_username, sf_password, sf_security_token

    def _get_http_client_apollo(self):
        self.apollo_api_key = self._get_apollo_credentials()
        return self._apollo_http_request

    def _get_apollo_credentials(self):
        apollo_api_key = Secret.load(f"{self.tenant_id}-apollo-api-key").get()
        return apollo_api_key

    def _apollo_http_request(self, method, path, params = {}, body = {}, raw = False):
        available_http_method = ["get", "post", "patch", "put", "delete"]
        method = method.lower()
        apollo_api_key = self.apollo_api_key
        if method not in available_http_method:
            raise Exception(f"not available method {method}")
        request_method = getattr(requests, method)

        base_url = self.apollo_base_url
        url = base_url + ('/' + path if not path.startswith('/') else path)

        if method.lower() == 'get':
            params['api_key'] = apollo_api_key
            response = request_method(url, params=params)
        else:
            body['api_key'] = apollo_api_key
            response = request_method(url, params=params, json=body)
        if raw:
            return response
        return response.json()

# Example
# if __name__ == "__main__":
#     client = ClientMgr('db77420a-f943-4408-afe2-bd269a92ea63')
#     apollo = client.get_client("apollo")
#     result = apollo(method="get",path="auth/health")
#     print(result)
