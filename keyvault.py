from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = "https://keyvaultforurlshortener.vault.azure.net/"

_credential = DefaultAzureCredential()
_client = SecretClient(vault_url = VAULT_URL, credential=_credential)

def get_secret(secret_name: str) -> str:
    """Fetch a secret value from Azure key vault by name."""
    secret = _client.get_secret(secret_name)
    return secret.value