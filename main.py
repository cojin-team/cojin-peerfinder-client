# Local files
## Cojin API
from core.cojin.configparser import parser as cojinparser
from core.cojin.rpc import RPC
## Local libraries
from core.peerfinder import wrapper
from core.uncolor import uncolor
from core.config import config

# External libraries
from pyngrok import ngrok

# Internal python libraries
from os import getenv, path
from platform import system
from sys import exit #sometimes exit is not defined
from time import sleep


cojincfg = cojinparser()

# Detect cojin config file
if system() == 'Windows':
    cojinpath = path.join(getenv('USERPROFILE'), '.cojin/cojin.conf')
else:
    cojinpath = path.join(getenv('HOME'), '.cojin/cojin.conf')

# Error msg if cojin file doesn't exists
if not path.isfile(cojinpath):
    print(uncolor('The cojin configuration file does not exists, please create and fill it', ['red']))
    input('press enter to exit')
    exit()

print(uncolor('Parsing cojin.conf file', ['yellow']))
cojincfg.read(cojinpath)

# Test wallet rpc

if not cojincfg.rpcOK():
    print(uncolor('The wallet RPC is not configured, please configure it and restart the wallet', ['red']))
    input('press enter to exit')
    exit()

try:
    rpc = RPC(
        'http://127.0.0.1:' + cojincfg.rpc.port, #maybe i'll add support for remote wallets in the future
        cojincfg.rpc.user,
        cojincfg.rpc.password
    )
except Exception as e:
    print(uncolor('The wallet RPC refuses the connection, try restarting the wallet', ['red']))
    input('press enter to exit')
    exit()

# Actual peer finding code

print(uncolor('Trying connection with server', ['yellow']))
server = wrapper(config['peerfinder']['server'])
print(uncolor('Connected with server', ['green']))

peers = server.getPeers()
for peer in peers:
    if peer == None: continue
    print('Trying connection to:', uncolor(peer, ['green']))
    rpc.request('addnode', [peer, 'onetry']) # use onetry bc instantly attempts the connection
    sleep(int(config['RPC']['wait'])) # avoid accidental DOS attack


if config['ngrok']['enabled']:
    tunnel = ngrok.connect(cojincfg.walletport, 'tcp')
    print(uncolor('Wallet exposed to ' + tunnel.data['public_url'], ['green']))
    print(uncolor('Posting peer on peerfinding server', ['yellow']))
    server.postPeer(tunnel.data['public_url'])
    try:
        process = ngrok.get_ngrok_process()
        print(uncolor('Peer posted, press ctrol + C to kill ngrok', ['green']))
        process.proc.wait()
    except KeyboardInterrupt:
        print(uncolor('Shutting down', ['yellow']))
        ngrok.kill()
