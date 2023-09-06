from utils.fetch_secrets import fetch_vault_secrets
import subprocess

vault_url = 'http://127.0.0.1:8200'
vault_token = ''
secret_path = 'gitlab'  
def get_secrets():
    data = fetch_vault_secrets(vault_url, vault_token, secret_path)
    for k,v in data.items():
        return f"key: {k} and value: {v}"
 
def get_events():
    print("******** getting kubernetes events")
    try:
        result = subprocess.run(['kubectl', 'get', 'events', '-o=jsonpath={.items[*].metadata.name}'], check=True, capture_output=True, text=True)
        events = result.stdout.split()
        formatted_output = "\n".join(events)
        return formatted_output
    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command: {e}")
        return "could not connect to your cluster"

def get_namespaces():
    try:
        result = subprocess.run(['kubectl', 'get', 'namespaces', '-o=jsonpath={.items[*].metadata.name}'], check=True, capture_output=True, text=True)
        namespaces = result.stdout.split()
        formatted_output = "\n".join(namespaces)
        return formatted_output
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command: {e}")
        return "could not connect to your cluster"

def create_ssh_user(username, serverIP, sshPubKey):
    print(f"***********create_ssh_user was called")
    return "user is created"