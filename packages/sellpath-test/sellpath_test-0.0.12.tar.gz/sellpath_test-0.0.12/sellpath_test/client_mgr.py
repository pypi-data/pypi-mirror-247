import simple_salesforce
from prefect.blocks.system import Secret
import requests
from cryptography.fernet import Fernet
import base64
import shortuuid


class ClientMgr:
    def __init__(self, tenant_id):
        """
        Initialize the Client Manager with a specific tenant ID and available tools.
        """
        self.tenant_id = tenant_id
        self._available_tools = ["apollo", "salesforce"]
        self.apollo_base_url = "https://api.apollo.io/v1"

    def health(self):
        """
        Perform a health check and print a message.
        """
        print("health check")
        return "health check"

    def get_client(self, tool_id: str, tool: str):
        """
        Get a client based on the specified tool.
        Args:
            tool_id (str): The short uuid from task detail context.
            tool (str): The tool for which the client is requested.
        Returns:
            object: The client instance for the specified tool.
        Raises:
            Exception: If the tool is not available.
        """
        self.secret_block_header = self._decode_short_uuid(tool_id)
        tool = tool.lower()
        if tool not in self._available_tools:
            raise Exception("not available tool")

        if tool == "salesforce":
            return self._get_client_salesforce()

        if tool == "apollo":
            return self._get_http_client_apollo()

    def _decode_short_uuid(self, short_uuid):
        return shortuuid.decode(short_uuid)

    def _decrypt_data(self, encoded_data):
        key = self.tenant_id
        uuid_key = key.replace("-", "")
        fernet_key = base64.urlsafe_b64encode(uuid_key.encode())
        cipher_suite = Fernet(fernet_key)
        plain_text = cipher_suite.decrypt(encoded_data)
        result = plain_text.decode("utf-8")

        return result

    def _get_client_salesforce(self):
        """
        Get a Salesforce client using the stored credentials.

        Returns:
            simple_salesforce.Salesforce: The Salesforce client instance.
        """
        sf_username, sf_password, sf_security_token = self._get_salesforce_credentials()
        sf = simple_salesforce.Salesforce(
            username=sf_username, password=sf_password, security_token=sf_security_token
        )
        return sf

    def _get_salesforce_credentials(self):
        """
        Get Salesforce credentials from Prefect Secrets.

        Returns:
            tuple: Tuple containing Salesforce username, password, and security token.
        """
        sf_username = Secret.load(f"{self.secret_block_header}-sf-username").get()
        sf_username = self._decrypt_data(sf_username)

        sf_password = Secret.load(f"{self.secret_block_header}-sf-password").get()
        sf_password = self._decrypt_data(sf_password)

        sf_security_token = Secret.load(f"{self.secret_block_header}-sf-security-token").get()
        sf_security_token = self._decrypt_data(sf_security_token)

        return sf_username, sf_password, sf_security_token

    def _get_http_client_apollo(self):
        """
        Get an HTTP client for Apollo using the stored API key.

        Returns:
            function: The Apollo HTTP request function.
        """
        self.apollo_api_key = self._get_apollo_credentials()
        return self._apollo_http_request

    def _get_apollo_credentials(self):
        """
        Get Apollo API key from Prefect Secrets.

        Returns:
            str: Apollo API key.
        """
        apollo_api_key = Secret.load(f"{self.secret_block_header}-apollo-api-key").get()
        apollo_api_key = self._decrypt_data(apollo_api_key)

        return apollo_api_key

    def _apollo_http_request(self, method, path, params={}, body={}, raw=False):
        """
        Perform an HTTP request to the Apollo API.

        Args:
            method (str): HTTP method (get, post, patch, put, delete).
            path (str): API endpoint path.
            params (dict): Query parameters.
            body (dict): Request body.
            raw (bool): Flag indicating whether to return raw response or JSON.
        Returns:
            dict or requests.Response: JSON response or raw response.
        Raises:
            Exception: If an invalid HTTP method is provided.
        """
        available_http_method = ["get", "post", "patch", "put", "delete"]
        method = method.lower()
        apollo_api_key = self.apollo_api_key
        if method not in available_http_method:
            raise Exception(f"not available method {method}")
        request_method = getattr(requests, method)

        base_url = self.apollo_base_url
        url = base_url + ("/" + path if not path.startswith("/") else path)

        if method.lower() == "get":
            params["api_key"] = apollo_api_key
            response = request_method(url, params=params)
        else:
            body["api_key"] = apollo_api_key
            response = request_method(url, params=params, json=body)
        if raw:
            return response
        return response.json()


# Example
# if __name__ == "__main__":
#     client = ClientMgr("2c0e49a6-28f1-4dd2-80b8-372c03982b8d")
#     apollo = client.get_client("fb9113ca-1e20-4fa5-831c-d458c0d82354", "apollo")
#     result = apollo(method="get", path="auth/health")
#     print(result)
