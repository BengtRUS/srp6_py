from xmlrpc.server import SimpleXMLRPCServer
import random
import math

k=3
g=123
I=''
s=''
v=0
N=0 
A=0
def hash(inp):
    _input = str(inp)
    return int(len(_input)%(math.exp(len(_input))))
def main():
    server = SimpleXMLRPCServer(('127.0.0.1', 7001))
    server.register_introspection_functions()
    server.register_multicall_functions()
    server.register_function(firstPhase)
    server.register_function(sendRand)
    server.register_function(countKey)
    server.register_function(secondPhase)
    print("Server ready")
    server.serve_forever()
def firstPhase(name,salt,_hash,prime):
    global I
    global s
    global v
    global N
    global g
    I =name    
    s=salt    
    v=int(_hash)    
    N=int(prime)
    g = 11
    print('Got from client I,s,v,N!')
    return True
def sendRand(name,Aa):
    global I
    global s
    global v
    global N
    global A
    global B
    A=Aa
    b=random.randint(1,1000)
    B=k*v+pow(g,b)%N
    sr = str(B)+'!'+str(s)
    print('Got from client I and A; calculating b=%d and B=%f; sending data to client...' %(b,B))
    return (sr)
def countKey():
    u=hash(str(A)+str(B))
    S=((A*(pow(v,u)%N))^B)%N
    global K
    K=hash(S)
    print('Calculating and sending to client K=',K)
    return K
def secondPhase(M):
    print('Got from client M. Cheching...')
    if M == hash(str((hash(N)^hash(g)))+str(hash(I))+s+str(A)+str(B)+str(K)):
        print('OK!')
        return hash(str(A)+str(M)+str(K))
    else:
        print('Not OK -_-')
        return -1

main()