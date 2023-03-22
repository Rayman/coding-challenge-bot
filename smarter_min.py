I='Kadabra'
H='Abra'
G=float
from abc import ABC,abstractmethod as J
from random import choice as K
import numpy as A
from ..bot_control import Move as B
__all__=[H,I]
def L(floor_colour,bot_colour):
	B=bot_colour;A=floor_colour
	if A==0:return B
	return(A,0,B)[(B-A)%3]
C={B.UP:A.array([0,1],dtype=A.int16),B.RIGHT:A.array([1,0],dtype=A.int16),B.LEFT:A.array([-1,0],dtype=A.int16),B.DOWN:A.array([0,-1],dtype=A.int16)}
def M(position):return next((B for(B,C)in C.items()if A.array_equal(C,position)))
F=object()
def N(it,*,key):
	it=iter(it);A=next(it,F)
	if A is F:raise ValueError('max() arg is an empty sequence')
	B=key(A);C=[A]
	for D in it:
		E=key(D)
		if E>B:C=[D];B=E
		elif E==B:C.append(D)
	return K(C)
class D(ABC):
	def __init__(A,max_depth):A.max_depth=max_depth;A.id=None;A.position=None
	@J
	def get_name(self):raise NotImplementedError()
	def get_contributor(A):return'Rayman'
	def determine_next_move(A,grid,enemies,game_info):B=N(C.values(),key=lambda move:E(grid,[A.position+move],A.max_depth,A.id));D=M(B);return D
class Abra(D):
	def __init__(A):super().__init__(0)
	def get_name(A):return H
class Kadabra(D):
	def __init__(A):super().__init__(1)
	def get_name(A):return I
class P(D):
	def __init__(A):super().__init__(2)
	def get_name(A):return'Alakazam'
def O(grid,history,id):
	E='-inf';B=0
	for A in history:
		if A[0]<0 or A[1]<0:return G(E)
		try:C=grid[(A[1],A[0])]
		except IndexError:return G(E)
		if C!=id:
			D=L(C,id)
			if D==id:B+=1
			elif D==0:B+=1e-06
	return B
def E(grid,history,depth,id):
	D=depth;B=history
	if D==0:A=O(grid,B,id)
	else:
		F=[]
		for (H,G) in C.items():A=E(grid,B+[B[-1]+G],D-1,id);F.append(A)
		A=max(F)
	return A