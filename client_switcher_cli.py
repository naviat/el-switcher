# Acknowledgments
# client-switcher is branched from client-switcher written by Accidental-green: https://github.com/accidental-green/client-switcher

import os
import requests
import re
import json
import tarfile
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from consolemenu import *
from consolemenu.items import *

# Customize Default Values if desired
EL_P2P_PORT=30303
EL_RPC_PORT=8545
EL_MAX_PEER_COUNT=50
JWTSECRET_PATH="/secrets/jwtsecret"

# Change to the home folder
os.chdir(os.path.expanduser("~"))

# Check sudo privileges
print("Checking sudo privileges")
try:
    subprocess.run(['sudo', '-v'], check=True)
    print("Sudo credentials authenticated.")
except subprocess.CalledProcessError:
    print("Failed to verify sudo credentials.")
    exit(1)

############# CLI CODE #######################

# Define valid execution clients and networks
valid_clients = ['BESU', 'NETHERMIND', 'ERIGON', 'RETH', 'GETH', 'NONE']
valid_networks = ['MAINNET', 'HOLESKY', 'SEPOLIA']

# Ask the user for Ethereum network
index = SelectionMenu.get_selection(valid_networks,title=':: Execution Client Switcher :: by CoinCashew.eth',subtitle='Select Ethereum network:')

# Exit selected
if index == 3:
    sys.exit()

eth_network=valid_networks[index]

# Ask the user for the execution client to DELETE
execution_client_delete = ""
index = SelectionMenu.get_selection(valid_clients,title='Select Execution Client to REMOVE:',show_exit_option=False)
execution_client_delete=valid_clients[index]

# Ask the user for the execution client to INSTALL
execution_client_install = ""
index = SelectionMenu.get_selection(valid_clients,title='Select Execution Client to INSTALL:',subtitle='Consider choosing a minority client. \nRecommendation: Nethermind - super fast sync time',show_exit_option=False)
execution_client_install=valid_clients[index]


def set_p2p():
    global EL_P2P_PORT
    EL_P2P_PORT = Screen().input(f'Current P2P Port: {EL_P2P_PORT} \nEnter the new value: ')

def set_rpc():
    global EL_RPC_PORT
    EL_RPC_PORT = Screen().input(f'Current RPC Port: {EL_RPC_PORT} \nEnter the new value: ')

def set_max():
    global EL_MAX_PEER_COUNT
    EL_MAX_PEER_COUNT = Screen().input(f'Current Max Peer Count: {EL_MAX_PEER_COUNT} \nEnter the new value: ')

def set_jwt():
    global JWTSECRET_PATH
    JWTSECRET_PATH = Screen().input(f'Current JWTSECRET_PATH: {JWTSECRET_PATH} \nEnter the new value: ')

def refresh_prologue():
    return f'P2P Port: {EL_P2P_PORT}\nRPC Port: {EL_RPC_PORT}\nMax Peer Count: {EL_MAX_PEER_COUNT}\nJWTSECRET_PATH: {JWTSECRET_PATH}'

menu = ConsoleMenu("Customize Default Values", "Update values to match your node configuration.", prologue_text=refresh_prologue)

# These menu items are using static text.
item1 = FunctionItem("Change P2P Port", set_p2p)
item2 = FunctionItem("Change RPC Port", set_rpc)
item3 = FunctionItem("Change Max Peer Count", set_max)
item4 = FunctionItem("Change JWT Secret Path", set_jwt)


# Add all the items to the root menu
menu.append_item(item1)
menu.append_item(item2)
menu.append_item(item3)
menu.append_item(item4)

answer=PromptUtils(Screen()).prompt_for_yes_or_no(f"Use default values for Ports, Max Peer Count, and JWT Secret?")

if not answer:
    # Show the menu
    menu.start()
    menu.join()

# Confirmation
answer= PromptUtils(Screen()).prompt_for_yes_or_no(f"You have selected to REMOVE {execution_client_delete} and INSTALL {execution_client_install} on NETWORK {eth_network}. Is this correct?")

if not answer:
    print("Operation cancelled by the user.")
    sys.exit()

# Print User Input Variables
print("\n##### User Selected Inputs #####")
print(f"Ethereum Network: {eth_network}")
print(f"Execution Client to DELETE: {execution_client_delete}")
print(f"Execution Client to INSTALL: {execution_client_install}\n")

######### REMOVE OLD CLIENT ###################
# Removal commands for different clients
geth_cmds = [
    "sudo systemctl stop execution",
    "sudo rm -rf /usr/local/bin/geth",
    "sudo rm -rf /var/lib/geth",
    "sudo rm -rf /etc/systemd/system/execution.service",
    "sudo userdel -r execution || true",
]

besu_cmds = [
    "sudo systemctl stop execution",
    "sudo rm -rf /usr/local/bin/besu",
    "sudo rm -rf /var/lib/besu",
    "sudo rm -rf /etc/systemd/system/execution.service",
    "sudo userdel -r execution || true",
]

nethermind_cmds = [
    "sudo systemctl stop execution",
    "sudo rm -rf /usr/local/bin/nethermind",
    "sudo rm -rf /var/lib/nethermind",
    "sudo rm -rf /etc/systemd/system/execution.service",
    "sudo userdel -r execution || true",
]

reth_cmds = [
    "sudo systemctl stop execution",
    "sudo rm -rf /usr/local/bin/reth",
    "sudo rm -rf /var/lib/reth",
    "sudo rm -rf /etc/systemd/system/execution.service",
    "sudo userdel -r execution || true",
]

erigon_cmds = [
    "sudo systemctl stop execution",
    "sudo rm -rf /usr/local/bin/erigon",
    "sudo rm -rf /var/lib/erigon",
    "sudo rm -rf /etc/systemd/system/execution.service",
    "sudo userdel -r execution || true",
]

# Convert inputs to lowercase
eth_network = eth_network.lower()
execution_client_delete = execution_client_delete.lower()
execution_client_install = execution_client_install.lower()

# Execute removal commands for execution_client_delete
print(f"Removing execution client: {execution_client_delete}")

if execution_client_delete == 'geth':
    for cmd in geth_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'besu':
    for cmd in besu_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'nethermind':
    for cmd in nethermind_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'reth':
    for cmd in reth_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'erigon':
    for cmd in erigon_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'none':
    print("No client selected for deletion")

# Update and upgrade packages
subprocess.run(['sudo', 'apt', '-y', 'update'])
subprocess.run(['sudo', 'apt', '-y', 'upgrade'])

# Install New Client
print(f"\nInstalling execution client: {execution_client_install}\n")
print(f"Creating usernames, directories, and service files...\n")
print(execution_client_install.lower())

############ GETH INSTALL##################
if execution_client_install == 'geth':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'execution'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/geth'])
    subprocess.run(['sudo', 'chown', '-R', 'execution:execution', '/var/lib/geth'])

    # Define the URL of the Geth download page
    url = 'https://geth.ethereum.org/downloads/'

    # Send a GET request to the download page and retrieve the HTML response
    response = requests.get(url)
    html = response.text

    # Use regex to extract the URL of the latest Geth binary for Linux (amd64)
    match = re.search(r'href="(https://gethstore\.blob\.core\.windows\.net/builds/geth-linux-amd64-[0-9]+\.[0-9]+\.[0-9]+-[0-9a-f]+\.tar\.gz)"', html)
    if match:
        download_url = match.group(1)
        filename = os.path.expanduser('~/geth.tar.gz')
        print(f'Downloading {download_url}...')
        response = requests.get(download_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Done! Binary saved to {filename}.')

        # Extract the contents of the tarball to the user's home folder
        with tarfile.open(filename, 'r:gz') as tar:
            dirname = tar.getnames()[0].split('/')[0]
            tar.extractall(os.path.expanduser('~'))

        # Remove the existing geth executable from /usr/local/bin if it exists
        if os.path.exists('/usr/local/bin/geth'):
            subprocess.run(['sudo', 'rm', '/usr/local/bin/geth'])
            print('Existing geth executable removed from /usr/local/bin.')

        # Copy the geth executable to /usr/local/bin
        src = os.path.expanduser(f'~/{dirname}/geth')
        subprocess.run(['sudo', 'cp', src, '/usr/local/bin/'])
        print('Geth executable copied to /usr/local/bin.')

        # Remove the downloaded file and extracted directory
        os.remove(filename)
        shutil.rmtree(os.path.expanduser(f'~/{dirname}'))
        print(f'Removed {filename} and directory {dirname}.')
    else:
        print('Error: could not find download URL.')

############ BESU INSTALL ##################
if execution_client_install == 'besu':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'execution'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/besu'])
    subprocess.run(['sudo', 'chown', '-R', 'execution:execution', '/var/lib/besu'])

    # Get the latest version number
    url = "https://api.github.com/repos/hyperledger/besu/releases/latest"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    latest_version = data['tag_name']

    besu_version = latest_version

    # Download the latest version
    download_url = f"https://github.com/hyperledger/besu/releases/download/{latest_version}/besu-{latest_version}.tar.gz"
    urllib.request.urlretrieve(download_url, f"besu-{latest_version}.tar.gz")

    # Extract the tar.gz file
    with tarfile.open(f"besu-{latest_version}.tar.gz", "r:gz") as tar:
        tar.extractall()
        tar.close()

    # Copy the extracted besu folder to /usr/local/bin/besu
    subprocess.run(["sudo", "cp", "-a", f"besu-{latest_version}", "/usr/local/bin/besu"], check=True)

    # Remove the downloaded .tar.gz file
    os.remove(f"besu-{latest_version}.tar.gz")

    # Install OpenJDK-17-JRE
    subprocess.run(["sudo", "apt", "-y", "install", "openjdk-17-jre"])

    # Install libjemalloc-dev
    subprocess.run(["sudo", "apt", "install", "-y", "libjemalloc-dev"])

############ NETHERMIND INSTALL ##################
if execution_client_install == 'nethermind':
    # Create User and directories
    subprocess.run(["sudo", "useradd", "--no-create-home", "--shell", "/bin/false", "execution"])
    subprocess.run(["sudo", "mkdir", "-p", "/var/lib/nethermind"])
    subprocess.run(["sudo", "chown", "-R", "execution:execution", "/var/lib/nethermind"])
    subprocess.run(["sudo", "apt-get", "install", "libsnappy-dev", "libc6-dev", "libc6", "unzip", "-y"], check=True)

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/NethermindEth/nethermind/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Search for the asset with the name that ends in linux-x64.zip
    assets = response.json()['assets']
    download_url = None
    zip_filename = None
    for asset in assets:
        if asset['name'].endswith('linux-x64.zip'):
            download_url = asset['browser_download_url']
            zip_filename = asset['name']
            break

    if download_url is None or zip_filename is None:
        print("Error: Could not find the download URL for the latest release.")
        exit(1)

    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to a temporary file
    with tempfile.NamedTemporaryFile('wb', suffix='.zip', delete=False) as temp_file:
        temp_file.write(response.content)
        temp_path = temp_file.name

    # Create a temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the binary to the temporary directory
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Copy the contents of the temporary directory to /usr/local/bin/nethermind using sudo
        subprocess.run(["sudo", "cp", "-a", f"{temp_dir}/.", "/usr/local/bin/nethermind"])

    # chown -R execution:execution /usr/local/bin/nethermind
    subprocess.run(["sudo", "chown", "-R", "execution:execution", "/usr/local/bin/nethermind"])

    # chmod a+x /usr/local/bin/nethermind/nethermind
    subprocess.run(["sudo", "chmod", "a+x", "/usr/local/bin/nethermind/nethermind"])

    # Remove the temporary zip file
    os.remove(temp_path)

    nethermind_version = os.path.splitext(zip_filename)[0]

############ RETH INSTALL ##################
if execution_client_install == 'reth':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'execution'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/reth'])
    subprocess.run(['sudo', 'chown', '-R', 'execution:execution', '/var/lib/reth'])

    # Define the Github API endpoint to get the latest release
    url = "https://api.github.com/repos/paradigmxyz/reth/releases/latest"

    # Send a GET request to the API endpoint
    response = requests.get(url)
    reth_version = response.json()['tag_name']

    # Search for the asset with the name that ends in linux-x64.zip
    assets = response.json()['assets']
    download_url = None
    tar_filename = None
    for asset in assets:
        if asset['name'].endswith('x86_64-unknown-linux-gnu.tar.gz'):
            download_url = asset['browser_download_url']
            tar_filename = asset['name']
            break

    if download_url is None or tar_filename is None:
        print("Error: Could not find the download URL for the latest release.")
        exit(1)

    # Download the latest release binary
    urllib.request.urlretrieve(download_url, f"{tar_filename}")

    # Extract the tar.gz file
    with tarfile.open(f"{tar_filename}", "r:gz") as tar:
        tar.extractall(path='/usr/local/bin')
        tar.close()

    # chown execution:execution /usr/local/bin/reth
    subprocess.run(["sudo", "chown", "execution:execution", "/usr/local/bin/reth"])

    # Remove the downloaded .tar.gz file
    os.remove(f"{tar_filename}")



############ ERIGON INSTALL ##################
if execution_client_install == 'erigon':
   # Create User and directories
   subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'execution'])
   subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/erigon'])
   subprocess.run(['sudo', 'chown', '-R', 'execution:execution', '/var/lib/erigon'])

   # Define the Github API endpoint to get the latest release
   url = "https://api.github.com/repos/ledgerwatch/erigon/releases/latest"

   # Send a GET request to the API endpoint
   response = requests.get(url)
   erigon_version = response.json()['tag_name']

   # Search for the asset with the name that ends in linux-x64.zip
   assets = response.json()['assets']
   download_url = None
   tar_filename = None
   for asset in assets:
       if asset['name'].endswith('linux_amd64.tar.gz'):
           download_url = asset['browser_download_url']
           tar_filename = asset['name']
           break

   if download_url is None or tar_filename is None:
       print("Error: Could not find the download URL for the latest release.")
       exit(1)

   # Download the latest release binary
   urllib.request.urlretrieve(download_url, f"{tar_filename}")

   # Extract the tar.gz file
   with tarfile.open(f"{tar_filename}", "r:gz") as tar:
       tar.extractall(path='/usr/local/bin')
       tar.close()

   # chown execution:execution /usr/local/bin/erigon
   subprocess.run(["sudo", "chown", "execution:execution", "/usr/local/bin/erigon"])

   # Remove the downloaded .tar.gz file
   os.remove(f"{tar_filename}")

###### GETH SERVICE FILE #############
if execution_client_install == 'geth':
    geth_service_file_lines = [
'[Unit]',
f'Description=Geth Execution Layer Client service for {eth_network.upper()}',
'After=network-online.target',
'Documentation=https://www.coincashew.com',
'',
'[Service]',
'Type=simple',
'User=execution',
'Group=execution',
'Restart=on-failure',
'RestartSec=3',
'KillSignal=SIGINT',
'TimeoutStopSec=900',
f'ExecStart=/usr/local/bin/geth --{eth_network} --port {EL_P2P_PORT} --http.port {EL_RPC_PORT} --maxpeers {EL_MAX_PEER_COUNT} --metrics --http --datadir=/var/lib/geth --pprof --state.scheme=path --authrpc.jwtsecret={JWTSECRET_PATH}',
'',
'[Install]',
'WantedBy=multi-user.target',
    ]

    geth_service_file = '\n'.join(geth_service_file_lines)

    geth_temp_file = 'geth_temp.service'
    geth_service_file_path = '/etc/systemd/system/execution.service'

    with open(geth_temp_file, 'w') as f:
        f.write(geth_service_file)

    os.system(f'sudo cp {geth_temp_file} {geth_service_file_path}')
    os.remove(geth_temp_file)

############ BESU SERVICE FILE ###############

if execution_client_install == 'besu':
    try:
        output = subprocess.check_output(["bash", "-c", "free -m | grep Mem: | awk '{print $2}'"], universal_newlines=True)
        total_mem = int(output)
        print(total_mem)
        if total_mem > 30 * 1024:
            print("More than 30GB RAM. Enabling rocksdb high spec.")
            _highspec='--Xplugin-rocksdb-high-spec-enabled'
        else:
            _highspec=''
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

    besu_service_file_lines = [
'[Unit]',
f'Description=Besu Execution Layer Client service for {eth_network.upper()}',
'Wants=network-online.target',
'After=network-online.target',
'Documentation=https://www.coincashew.com',
'',
'[Service]',
'Type=simple',
'User=execution',
'Group=execution',
'Restart=on-failure',
'RestartSec=3',
'KillSignal=SIGINT',
'TimeoutStopSec=900',
'Environment="JAVA_OPTS=-Xmx5g"',
f'ExecStart=/usr/local/bin/besu/bin/besu --network={eth_network} --p2p-port={EL_P2P_PORT} --rpc-http-port={EL_RPC_PORT} --max-peers={EL_MAX_PEER_COUNT} --metrics-enabled=true --metrics-port=6060 --rpc-http-enabled=true --sync-mode=SNAP --data-storage-format=BONSAI --data-path="/var/lib/besu" --engine-jwt-secret={JWTSECRET_PATH} {_highspec}',
''
'[Install]',
'WantedBy=multi-user.target',
    ]

    besu_service_file = '\n'.join(besu_service_file_lines)

    besu_temp_file = 'besu_temp.service'
    besu_service_file_path = '/etc/systemd/system/execution.service'

    with open(besu_temp_file, 'w') as f:
        f.write(besu_service_file)

    os.system(f'sudo cp {besu_temp_file} {besu_service_file_path}')
    os.remove(besu_temp_file)

####### RETH SERVICE FILE ###########
if execution_client_install == 'reth':
    EL_MAX_PEER_COUNT=int(EL_MAX_PEER_COUNT)//2

    reth_service_file_lines = [
'[Unit]',
f'Description=Reth Execution Layer Client service for {eth_network.upper()}',
'Wants=network-online.target',
'After=network-online.target',
'Documentation=https://www.coincashew.com',
'',
'[Service]',
'Type=simple',
'User=execution',
'Group=execution',
'Restart=on-failure',
'RestartSec=3',
'KillSignal=SIGINT',
'TimeoutStopSec=900',
'Environment=RUST_LOG=info',
f'ExecStart=/usr/local/bin/reth node --full --chain {eth_network} --datadir=/var/lib/reth --metrics 127.0.0.1:6060 --port {EL_P2P_PORT} --http --http.port {EL_RPC_PORT} --http.api="rpc,eth,web3,net,debug" --log.file.directory=/var/lib/reth/logs --authrpc.jwtsecret={JWTSECRET_PATH} --max-outbound-peers {EL_MAX_PEER_COUNT} --max-inbound-peers {EL_MAX_PEER_COUNT}',
'',
'[Install]',
'WantedBy=multi-user.target',
    ]

    reth_service_file = '\n'.join(reth_service_file_lines)

    reth_temp_file = 'reth_temp.service'
    reth_service_file_path = '/etc/systemd/system/execution.service'

    with open(reth_temp_file, 'w') as f:
        f.write(reth_service_file)

    os.system(f'sudo cp {reth_temp_file} {reth_service_file_path}')

    os.remove(reth_temp_file)

####### NETHERMIND SERVICE FILE ###########
if execution_client_install == 'nethermind':
    nethermind_service_file_lines = [
'[Unit]',
f'Description=Nethermind Execution Layer Client service for {eth_network.upper()}',
'Wants=network-online.target',
'After=network-online.target',
'Documentation=https://www.coincashew.com',
'',
'[Service]',
'Type=simple',
'User=execution',
'Group=execution',
'Restart=on-failure',
'RestartSec=3',
'KillSignal=SIGINT',
'TimeoutStopSec=900',
'WorkingDirectory=/var/lib/nethermind',
'Environment="DOTNET_BUNDLE_EXTRACT_BASE_DIR=/var/lib/nethermind"',
f'ExecStart=/usr/local/bin/nethermind/nethermind --config {eth_network} --datadir="/var/lib/nethermind" --Network.DiscoveryPort {EL_P2P_PORT} --Network.P2PPort {EL_P2P_PORT} --Network.MaxActivePeers {EL_MAX_PEER_COUNT} --JsonRpc.Port {EL_RPC_PORT} --Metrics.Enabled true --Metrics.ExposePort 6060 --JsonRpc.JwtSecretFile {JWTSECRET_PATH}',
'',
'[Install]',
'WantedBy=multi-user.target',
    ]

    nethermind_service_file = '\n'.join(nethermind_service_file_lines)

    nethermind_temp_file = 'nethermind_temp.service'
    nethermind_service_file_path = '/etc/systemd/system/execution.service'

    with open(nethermind_temp_file, 'w') as f:
        f.write(nethermind_service_file)

    os.system(f'sudo cp {nethermind_temp_file} {nethermind_service_file_path}')

    os.remove(nethermind_temp_file)

####### ERIGON SERVICE FILE ###########
if execution_client_install == 'erigon':
    erigon_service_file_lines = [
'[Unit]',
f'Description=Erigon Execution Layer Client service for {eth_network.upper()}',
'Wants=network-online.target',
'After=network-online.target',
'Documentation=https://www.coincashew.com',
'',
'[Service]',
'Type=simple',
'User=execution',
'Group=execution',
'Restart=on-failure',
'RestartSec=3',
'KillSignal=SIGINT',
'TimeoutStopSec=900',
'Environment=RUST_LOG=info',
f'ExecStart=/usr/local/bin/erigon --datadir /var/lib/erigon --chain {eth_network} --port {EL_P2P_PORT} --torrent.port 42069 --http.port {EL_RPC_PORT} --maxpeers {EL_MAX_PEER_COUNT} --metrics --pprof --prune htc --authrpc.jwtsecret={JWTSECRET_PATH}',
'',
'[Install]',
'WantedBy=multi-user.target',
    ]

    erigon_service_file = '\n'.join(erigon_service_file_lines)

    erigon_temp_file = 'erigon_temp.service'
    erigon_service_file_path = '/etc/systemd/system/execution.service'

    with open(erigon_temp_file, 'w') as f:
        f.write(erigon_service_file)

    os.system(f'sudo cp {erigon_temp_file} {erigon_service_file_path}')

    os.remove(erigon_temp_file)

#### END SERVICE FILES #####

# Reload system daemon
subprocess.run(f"sudo systemctl daemon-reload", shell=True, check=False)

# Enable systemd to autostart at boot
subprocess.run(f"sudo systemctl enable execution", shell=True, check=False)

############ PRINT FINAL OUTPUT ###############
print("\n########### CLIENT SWITCH DETAILS #############\n")

print(f'Removed: {execution_client_delete.upper()}\n')
print(f'Installed: {execution_client_install.upper()}\n')

# Check & Print Installed Versions
if execution_client_install == 'geth':
    geth_version = subprocess.run(["geth", "--version"], stdout=subprocess.PIPE).stdout
    if geth_version is not None:
        geth_version = geth_version.decode()
        geth_version = geth_version.split(" ")[-1].strip()
    else:
        geth_version = ""
    print(f'Geth Version: v{geth_version}\n')

if execution_client_install == 'besu':
    print(f'Besu Version: v{besu_version}\n')

if execution_client_install == 'nethermind':
    print(f'Nethermind Version: \n{nethermind_version}\n')

if execution_client_install == 'erigon':
    print(f'Erigon Version: \n{erigon_version}\n')

if execution_client_install == 'reth':
    print(f'Reth Version: \n{reth_version}\n')

print(f"Client switch complete!\n")

# Ask the user if they want to start the execution client
answer=PromptUtils(Screen()).prompt_for_yes_or_no(f"Start {execution_client_install.upper()} and begin syncing?")

print("\n########### NEXT STEPS #############\n")
print(f'\nFor more information, refer to https://www.coincashew.com/coins/overview-eth/guide-or-how-to-setup-a-validator-on-eth2-mainnet');
if not answer:
    print(f'\nWhen ready, run the following command to start {execution_client_install.upper()}')
    print(f'\nsudo systemctl start execution')
    print(f'\nView Logs: \njournalctl -fu execution')
    sys.exit()
else:
    subprocess.run(f"sudo systemctl start execution", shell=True, check=False)
    print(f'\nStarted {execution_client_install.upper()}! Sync can take a few hours, or up to a day.')
    print(f'\nView Logs: journalctl -fu execution | ccze')