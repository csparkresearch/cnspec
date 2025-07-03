import math 

C1 = 310679 #Count for source 1
C2 = 335564 #Count 2
C12 = 603910 #Combined count
T = 900. #Seconds
CB = 4164

m1=C1/T
m2=C2/T
m12=C12/T
mb = CB/T

def non_paralyzable():
	global m1,m2,m12,mb
	X = m1*m2 - mb*m12
	Y = m1*m2*(m12+mb) - mb*m12*(m1+m2)
	Z = Y*(m1+m2-m12-mb)/(X*X)
	print('non paralyzable: %e'%(X*(1-math.sqrt(1-Z))/Y))

def paralyzable():
	global m1,m2,m12,mb
	print('paralyzable: %e'%((m1+m2-m12-mb)/(m12**2 - m1**2 -m2**2))  )

non_paralyzable()
paralyzable()
