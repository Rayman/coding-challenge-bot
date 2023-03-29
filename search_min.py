I='Alakazam'
H='Kadabra'
G='Abra'
F=float
from abc import ABC,abstractmethod as J
from heapq import heappush as K,heappop as L
from random import choice as M
import numpy as A
from ..bot_control import Move as B
__all__=[G,H,I]
def N(x,position,r,id):
	H=O(x,id);C=P();C.push(E(y=r+1,z=0,v=[position],s=H));B=F('-inf');D=[]
	while C:
		A=C.pop()
		if A.y==0:
			if A.r()>B:B=A.r();D=[A]
			elif A.z==B:D.append(A)
		if A.r()<B:break
		for G in A.u():
			if G.r()<B:continue
			C.push(G)
	return[(A.v[1]-A.v[0],A.z)for A in D]
class E:
	def __init__(A,y,z,v,s):A.y=y;A.z=z;A.v=v;A.s=s
	def u(B):
		if B.y>0:
			F=B.v[-1]
			for G in D.values():
				C=F+G
				if C[0]<0 or C[1]<0 or C[0]>=B.s.shape[1]or C[1]>=B.s.shape[0]:continue
				if[B for B in reversed(B.v[1:])if A.array_equal(C,B)]:continue
				H=B.z+B.s[(C[1],C[0])];yield E(B.y-1,H,B.v+[C],B.s)
	def r(A):return A.z+A.y
	def __lt__(A,other):return A.r()>other.r()
	def __repr__(A):return f"{A.__class__.__name__}({', '.join((f'{A}={B!r}'for(A,B)in A.__dict__.items()if A!='s'))})"
def O(x,id):B=x;C=A.zeros_like(B,dtype=F);D=(id-B)%3;C[B==0]=1;C[(B!=id)&(D==2)]=1;C[(B!=id)&(B!=0)&(D!=0)]+=1e-06;return C
class P:
	def __init__(A):A.w=[]
	def push(A,item):K(A.w,item)
	def pop(A):return L(A.w)
	def __len__(A):return len(A.w)
D={B.UP:A.array([0,1],dtype=A.int16),B.RIGHT:A.array([1,0],dtype=A.int16),B.LEFT:A.array([-1,0],dtype=A.int16),B.DOWN:A.array([0,-1],dtype=A.int16)}
def Q(direction):return next((B for(B,C)in D.items()if A.array_equal(C,direction)))
class C(ABC):
	def __init__(A,r):A.r=r;A.id=None;A.position=None
	@J
	def get_name(self):raise NotImplementedError()
	def get_contributor(A):return'Rayman'
	def determine_next_move(A,x,enemies,game_info):B,C=M(N(x,A.position,A.r,A.id));return Q(B)
class Abra(C):
	def __init__(A):super().__init__(0)
	def get_name(A):return G
class Kadabra(C):
	def __init__(A):super().__init__(1)
	def get_name(A):return H
class Alakazam(C):
	def __init__(A):super().__init__(3)
	def get_name(A):return I