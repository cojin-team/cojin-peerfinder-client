# Local files
from core.configparser import parser
from core.api import wrapper
from core.rpc import RPC
from core.uncolor import uncolor

# External libraries
from pyngrok import ngrok

# Internal python libraries
from os import getenv, path
from platform import system
from sys import exit #sometimes exit is not defined
from time import sleep


cfg = parser()

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
cfg.read(cojinpath)

# Test wallet rpc

if not cfg.rpcOK():
    print(uncolor('The wallet RPC is not configured, please configure it and restart the wallet', ['red']))
    input('press enter to exit')
    exit()

try:
    rpc = RPC(
        'http://127.0.0.1:' + cfg.rpc.port, #maybe i'll add support for remote wallets in the future
        cfg.rpc.user,
        cfg.rpc.password
    )
except Exception as e:
    print(uncolor('The wallet RPC refuses the connection, try restarting the wallet', ['red']))
    input('press enter to exit')
    exit()

# Actual peer finding code

print(uncolor('Trying connection with server', ['yellow']))
server = wrapper('https://cojin-peerfinder.glitch.me')
print(uncolor('Connected with server', ['green']))

peers = server.getPeers()
for peer in peers:
    if peer == None: continue
    print('Trying connection to:', uncolor(peer, ['green']))
    rpc.request('addnode', [peer, 'onetry']) # use onetry bc instantly attempts the connection
    sleep(1) # avoid accidental DOS attack


if True: #replace with programconfig.enablePortFoward (if program config is added)
    print(uncolor('Posting peer on peerfinding server', ['yellow']))
    tunnel = ngrok.connect(cfg.walletport, 'tcp')
    server.postPeer(tunnel.data['public_url'])

    try:
        process = ngrok.get_ngrok_process()
        print(uncolor('Peer posted, press ctrol + C to kill ngrok', ['green']))
        process.proc.wait()
    except KeyboardInterrupt:
        print(uncolor('Shutting down', ['yellow']))
        ngrok.kill()
