from sys import argv
import SocketServer
import gmpy2
from hashlib import sha256
from Crypto.Util.number import long_to_bytes,bytes_to_long,getStrongPrime

e = ?
assert e <= 65535

def genParams():
    while 1:
        p = getStrongPrime(1024)
        q = getStrongPrime(1024)
        n = p * q
        phi = (p-1) * (q-1)
        try:
            d = gmpy2.invert(e, phi)
            return (n, phi, d)
        except ZeroDivisionError:
            genParams()

def signature(params, r):
    n = params[0]
    phi = params[1]
    d = params[2]
    M = r * bytes_to_long('hctf{' + sha256(open('./flag').read()).hexdigest() + '}')
    S = pow(M, d, n)
    return S

class handler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.tries = 0
        self.params = genParams()

    def handle(self):
        self.request.send("Welcome Our RSA Signature Generate System! :-)\n")
        self.request.send("Please input your team token> ")
        token = self.request.recv(32+1).rstrip()
        if len(token) != 32:
            self.request.send("Invalid token!\n")
            exit()
        self.request.send("N is {}\n\n".format(self.params[0]))   
        for i in range(1000):
            self.request.send("Please tell me your secret number> ")
            ans = int(self.request.recv(1000))
            if ans > 1:
                sig = signature(self.params, ans)
                self.request.send("Alright, here is your signature: {}\n\n".format(sig))
            else:
                self.request.send("This is not allowed.\n")
                break
        self.request.send("Bye!\n")

def main():
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    if len(argv) < 2:
        print("Usage: {} <PORT>".format(argv[0]))
    else:
        LOCAL_PORT = int(argv[1])
        s = SocketServer.ThreadingTCPServer(("", LOCAL_PORT), handler)
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("shutting down")
            s.shutdown()
            s.socket.close()

if __name__ == "__main__":
    main()