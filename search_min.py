M='Alakazam'
L='Kadabra'
K='Abra'
J=float
C=None
from abc import ABC,abstractmethod as N
from collections import deque
from heapq import heappush as O,heappop as P
from random import choice as Q
import numpy as A
from ..bot_control import Move as B
__all__=[K,L,M]
def R(x,position,u,id,r=C):
	I=position;F=r
	if F is C:F=[]
	K=S(x,id)
	for (L,N) in T(I,F):K[(L[1],L[0])]-=N
	E=U();E.push(H(y=u+1,z=0.0,v=A.array([I]),q=K));D=J('-inf');G=[]
	while E:
		B=E.pop()
		if B.y==0:
			if B.p>D:D=B.p;G=[B]
			elif B.z==D:G.append(B)
		if B.p<D:break
		for M in B.t():
			if M.p<D:continue
			E.push(M)
	for B in G:yield(B.v[1]-B.v[0],B.z)
class H:
	__slots__='y','z','v','q','p'
	def __init__(A,y,z,v,q):C=z;B=y;A.y=B;A.z=C;A.v=v;A.q=q;A.p=C+B
	def t(A):
		if A.y>0:
			B=A.v[-1]
			if B[0]>0:yield from A.s(B+G)
			if B[1]>0:yield from A.s(B+I)
			if B[0]<A.q.shape[1]-1:yield from A.s(B+F)
			if B[1]<A.q.shape[0]-1:yield from A.s(B+E)
	def s(B,next_position):
		C=next_position
		if (B.v[1:]==C).all(axis=1).any():return
		D=B.z+B.q[(C[1],C[0])];yield H(B.y-1,D,A.concatenate((B.v,C[(A.newaxis,...)])),B.q)
	def __lt__(A,other):return A.p>other.p
	def __repr__(A):return f"{A.__class__.__name__}(y={A.y} z={A.z:.2f} v={A.v.tolist()})"
def S(x,id):
	B=x;E=dict(zip(*A.unique(B,return_counts=True)));E.pop(0,C);D=A.zeros_like(B,dtype=J);H=(id-B)%3;D[B==0]=1;D[(B!=id)&(H==2)]=1;G=10;I=max(E.values())if E else 1
	for (F,K) in E.items():
		if F==id or(id-F)%3==0:continue
		D[B==F]+=K/I/G
	D/=1+1/G;return D
def T(position,r):
	B=r
	if not B:return
	D,E=A.unique(A.vstack((position,B)),axis=0,return_counts=True)
	for (F,C) in enumerate(E):
		if C>1:yield(D[F],C)
class U:
	__slots__='w',
	def __init__(A):A.w=[]
	def push(A,item):O(A.w,item)
	def pop(A):return P(A.w)
	def __bool__(A):return bool(A.w)
E=A.array([0,1],dtype=A.int16)
F=A.array([1,0],dtype=A.int16)
G=A.array([-1,0],dtype=A.int16)
I=A.array([0,-1],dtype=A.int16)
V={B.UP:E,B.RIGHT:F,B.LEFT:G,B.DOWN:I}
def W(direction):return next((B for(B,C)in V.items()if A.array_equal(C,direction)))
X=C
class D(ABC):
	def __init__(A,u):A.u=u;A.id=C;A.position=C;A.r=deque([],maxlen=8)
	@N
	def get_name(self):raise NotImplementedError()
	def get_contributor(A):return'Rayman'
	def determine_next_move(A,x,enemies,game_info):B,D=Q(list(R(x,A.position,A.u,A.id,A.r)));A.r.appendleft(A.position);C=W(B);return C
class Abra(D):
	def __init__(A):super().__init__(0)
	def get_name(A):return K
class Kadabra(D):
	def __init__(A):super().__init__(1)
	def get_name(A):return L
class Alakazam(D):
	def __init__(A):super().__init__(5)
	def get_name(A):return M