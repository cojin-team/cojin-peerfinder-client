from core.utils import Empty

class parser(object):
    def __init__(self) -> None:
        self.reset() # avoid writing 2 times the same code
        
    def reset(self) -> None:
        """Set the instance properties to default"""
        self.rpc = Empty()
        self.rpc.enabled = False
        self.rpc.user = None
        self.rpc.password = None
        self.rpc.port = None
        self.walletport = 18327

    def read(self, file: str):
        """
        Parse the config file
        
        Args:
            file (str): File path
        """
        with open(file, 'r') as f:
            self.lines = f.readlines()
        
        for line in self.lines:
            if line.startswith('#'): continue #skip comments
            pair = line.removesuffix('\n').split('=') #remove \n at the end of line before splitting
            #pair[0] is the instruction
            #pair[1] is the value
            if pair[0] == 'server':
                if pair[1] == '1': self.rpc.enabled = True
                else: self.rpc.enabled = False

            if pair[0] == 'rpcuser':
                self.rpc.user = pair[1]
            
            if pair[0] == 'rpcpassword':
                self.rpc.password = pair[1]

            if pair[0] == 'rpcport':
                self.rpc.port = pair[1]
            
    def rpcOK(self) -> bool:
        """Check if the RPC is enabled and ready"""
        if not self.rpc.enabled: return False
        if not self.rpc.user: return False
        if not self.rpc.password: return False
        if not self.rpc.port: return False
        return True
