import subprocess
from prettytable import PrettyTable
import hvac


def get_secrets(vault_url, vault_token, secret_path):
    client = hvac.Client(url=vault_url, token=vault_token)
    response = client.secrets.kv.v2.read_secret_version(
        secret_path, raise_on_deleted_version=False)
    response_data = response['data']['data']
    result = ""
    for k, v in response_data.items():
        result += f"{k}: {v}\n"
    return result


def get_k8s_pods():
    # Run the kubectl command to get pods in a custom format
    cmd = [
        'kubectl', 'get', 'pods',
        '-o=custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName,IP:.status.podIP'
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
        return

    # Split the output into lines
    lines = result.stdout.splitlines()

    # Create a table with the headers from the first line of the command output
    table = PrettyTable(lines[0].split())

    # Add rows to the table from the rest of the command output
    for line in lines[1:]:
        table.add_row(line.split())

    return str(table)


def get_k8s_events():
    # Run the kubectl command to get events in a custom format
    cmd = [
        'kubectl', 'get', 'events',
        '-o=custom-columns=LAST SEEN:.lastTimestamp,TYPE:.type,REASON:.reason,OBJECT:.involvedObject.kind/.involvedObject.name,MESSAGE:.message'
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
        return

    # Split the output into lines
    lines = result.stdout.splitlines()

    # Create a table with the headers from the first line of the command output
    table = PrettyTable(lines[0].split())

    # Add rows to the table from the rest of the command output
    for line in lines[1:]:
        table.add_row(line.split())

    return str(table)


def get_k8s_namespaces():
    try:
        result = subprocess.run(['kubectl', 'get', 'namespaces',
                                '-o=jsonpath={.items[*].metadata.name}'], check=True, capture_output=True, text=True)
        namespaces = result.stdout.split()
        formatted_output = "\n".join(namespaces)
        return formatted_output

    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command: {e}")
        return "could not connect to your cluster"


def create_ssh_user(username, serverIP, sshPubKey):
    print(f"***********create_ssh_user was called")
    return "user is created"
