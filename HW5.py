#import layout
#import types, time, random, os, 
import sys, pdb, linecache, traceback

#Clockwise Q sub k
va_clock, vb_clock, vc_clock = -7.3 ,	-2.4 ,	-3.0 

#Counterclockwise Q sub k
va_wise, vb_wise, vc_wise = -4.6 ,	4.0 ,	-0.5 

t_a_b_clock, r_a_b_clock = 0.2, 0

t_a_c_clock, r_a_c_clock = 0.8, -10

#---------------

t_a_b_wise, r_a_b_wise = 0.400 	,0.000

t_a_c_wise, r_a_c_wise = 0.600, 	-10.000

#################
t_b_a_clock, r_b_a_clock =0.200 	,-9.000

t_b_c_clock, r_b_c_clock = 0.800 ,	0.000

#---------------

t_b_a_wise, r_b_a_wise = 1.000 ,	7.000

t_b_c_wise, r_b_c_wise = 0,0

###############

t_c_a_clock, r_c_a_clock = 1,0

t_c_b_clock, r_c_b_clock = 0,0

#---------------

t_c_a_wise, r_c_a_wise = 0,0

t_c_b_wise, r_c_b_wise = 1,-4

gamma = 0.5


# q_a_clock = t_a_b_clock*(r_a_b_clock + gamma*vb_wise) + t_a_c_clock*(r_a_c_clock + gamma*vc_wise)
# q_a_wise = t_a_b_wise*(r_a_b_wise + gamma*vb_wise) + t_a_c_wise*(r_a_c_wise + gamma*vc_wise)

# q_b_clock = t_b_a_clock*(r_b_a_clock + gamma*va_wise) + t_b_c_clock*(r_b_c_clock + gamma*vc_wise)
# q_b_wise = t_b_a_wise*(r_b_a_wise + gamma*va_wise) + t_b_c_wise*(r_b_c_wise + gamma*vc_wise)

# q_c_clock = t_c_a_clock*(r_c_a_clock + gamma*va_wise) + t_c_b_clock*(r_c_b_clock + gamma*vb_wise)
# q_c_wise = t_c_a_wise*(r_c_a_wise + gamma*va_wise) + t_c_b_wise*(r_c_b_wise + gamma*vb_wise)


q_a_clock = 
q_a_wise = 

q_b_clock = 
q_b_wise = 

q_c_clock = 
q_c_wise = 


#pdb.set_trace()

print "q_a_clock = " + str(q_a_clock)
print "q_a_wise = " + str(q_a_wise)

print "q_b_clock = " + str(q_b_clock)
print "q_b_wise = " + str(q_b_wise)

print "q_c_clock = " + str(q_c_clock)
print "q_c_wise = " + str(q_c_wise)
