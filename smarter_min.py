H='Kadabra'
D='Abra'
F=float
from abc import ABC,abstractmethod as J
from random import choice as K
import numpy as A
from ..bot_control import Move as B
__all__=[D,H]
def I(s,v,z,y,id):
	M='-inf';J=y;G=z;D=s;B=v;C=B[-1]
	if C[0]<0 or C[1]<0 or C[0]>=D.shape[1]or C[1]>=D.shape[0]:return F(M)
	G+=D[(B[-1][1],B[-1][0])]
	if J==0:K=G
	else:
		H=F(M)
		for N in E.values():
			L=C+N
			if[B for B in reversed(B[1:])if A.array_equal(L,B)]:continue
			H=max(H,I(D,B+[L],G,J-1,id))
		K=H
	return K
def L(x,position,r,id):A=position;C=M(x,id);return[(B,I(C,[A,A+B],0,r,id))for B in E.values()]
def M(x,id):B=x;C=A.zeros_like(B,dtype=F);D=(id-B)%3;C[B==0]=1;C[(B!=id)&(D==2)]=1;C[(B!=id)&(B!=0)&(D!=0)]+=1e-06;return C
E={B.UP:A.array([0,1],dtype=A.int16),B.RIGHT:A.array([1,0],dtype=A.int16),B.LEFT:A.array([-1,0],dtype=A.int16),B.DOWN:A.array([0,-1],dtype=A.int16)}
G=object()
def N(it,*,key):
	it=iter(it);A=next(it,G)
	if A is G:raise ValueError('max() arg is an empty sequence')
	B=key(A);C=[A]
	for D in it:
		E=key(D)
		if E>B:C=[D];B=E
		elif E==B:C.append(D)
	return K(C)
def O(direction):return next((B for(B,C)in E.items()if A.array_equal(C,direction)))
class C(ABC):
	def __init__(A,r):A.r=r;A.id=None;A.position=None
	@J
	def get_name(self):raise NotImplementedError()
	def get_contributor(A):return'Rayman'
	def determine_next_move(A,x,enemies,game_info):B,C=N(L(x,A.position,A.r,A.id),key=lambda m:m[1]);return O(B)
class Abra(C):
	def __init__(A):super().__init__(0)
	def get_name(A):return D
class Kadabra(C):
	def __init__(A):super().__init__(1)
	def get_name(A):return H
class P(C):
	def __init__(A):super().__init__(2)
	def get_name(A):return'Alakazam'