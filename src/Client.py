import xmlrpc.client
import random
import math


def hash(inp):
    _input = str(inp)
    return int(len(_input)%(math.exp(len(_input))))
def main():
    with xmlrpc.client.ServerProxy("http://localhost:7001/") as proxy:
        #multicall.getCourse(addr,code)
        k=3
        N=2*int(input('Prime number: '))+1
        s = ''.join([random.choice('qwertyuioplkjhgfdsazxcvbnm') for _ in range(random.randint(1,10))])
        I=str(input('Username: '))
        p=str(input('Password: '))
        g = 11
        print('Generator g = ', g)
        x=hash(s+p)
        print('x=',x)
        v=(g^x)%N
        print('v=',v)
        #FirstPhase
        print('Sending to server I,s,v,N')
        proxy.firstPhase(I,s,v,N)
        print('Data send')
        a=random.randint(1,1000)
        print('Generating a=',a)
        A=pow(g,a)%N
        print('Calculating A=g^a mod N=',A)
        print('Sending to server I,A')
        tempst = str(proxy.sendRand(I,A))
        tempst = tempst.split('!')
        B=int(tempst[0])
        print('Recieving from server B=',B)
        u=hash(str(A)+str(B))
        print('Calculating U=h(A,B)=',u)
        if u!=0:
            proxy.countKey()
            S=(pow((B-k*((pow(g,x))%N)),(a+u*x)))%N
            K=hash(S)
            print('Calculating K=h(((B-k*(g^x mod N))^a+u*x) mod N = ',K)
        #SecondPhase
        M = hash(str((hash(N)^hash(g)))+str(hash(I))+s+str(A)+str(B)+str(K))
        print('Calculating M=',M)
        if(hash(str(A)+str(M)+str(K))==proxy.secondPhase(M)):
            print('Sucsess!')
        else:
            print('Error!')
if __name__ =='__main__':
    main()