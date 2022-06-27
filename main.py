# Local files
from core.configparser import parser
from core.api import wrapper
from core.rpc import RPC

# External libraries
from pyngrok import ngrok
from pymsgbox import alert

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
    alert('The cojin configuration file does not exists, please create and fill it', 'Cojin Configuration Error')
    exit()

cfg.read(cojinpath)

# Test wallet rpc

if not cfg.rpcOK():
    alert('The wallet RPC is not configured, please configure it and restart the wallet', 'Wallet RPC Error')
    exit()

try:
    rpc = RPC(
        'http://127.0.0.1:' + cfg.rpc.port, #maybe i'll add support for remote wallets in the future
        cfg.rpc.user,
        cfg.rpc.password
    )
except Exception as e:
    alert('The wallet RPC refuses the connection, try restarting the wallet', 'Wallet RPC Error')
    exit()

# Actual peer finding code

server = wrapper('https://cojin-peerfinder.glitch.me')

peers = server.getPeers()
for peer in peers:
    if peer == None: continue
    rpc.request('addnode', [peer, 'onetry']) # use onetry bc instantly attempts the connection
    sleep(1) # avoid accidental DOS attack


if True: #replace with programconfig.enablePortFoward (if program config is added)
    print('Posting peer on peerfinding server')
    tunnel = ngrok.connect(cfg.walletport, 'tcp')
    server.postPeer(tunnel.data['public_url'])

    try:
        process = ngrok.get_ngrok_process()
        print('Peer posted, press ctrol + C to kill ngrok')
        process.proc.wait()
    except KeyboardInterrupt:
        print('Shutting down')
        ngrok.kill()
