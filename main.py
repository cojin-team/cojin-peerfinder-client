from core.configparser import parser
from pyngrok import ngrok
from pymsgbox import alert
from core.api import wrapper #still in pseudocode
from core.rpc import RPC

from sys import exit #sometimes exit is not defined

cfg = parser()
#cfg.read('filepath')

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

server = wrapper('serverURL')
if True: #replace with programconfig.enablePortFoward
    tunnel = ngrok.connect(cfg.walletport, 'tcp')
    server.post(tunnel.data['public_url'])

peers = wrapper.getPeers()
for peer in peers:
    rpc.request('addnode', [peer, 'onetry'])

totalpeers = rpc.request('getpeerinfo')
print('Discovered', len(peers), 'peers, connected succesfully with', len(totalpeers), 'peers')
