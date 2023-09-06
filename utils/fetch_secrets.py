import json
import hvac

def fetch_vault_secrets(vault_url, vault_token, secret_path):
    client = hvac.Client(url=vault_url, token=vault_token)
    response = client.secrets.kv.v2.read_secret_version(secret_path, raise_on_deleted_version=False)

    response_data = response['data']['data']
    return response_data
