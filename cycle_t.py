from Nodes import *
from compressor import *
from condensor import *
from throttle import *
from evaporator import *




"given conditions and initialise nodes"
fluid = 'R134a'
p1 = 100000
p2 = 800000

nodes = [Node() for i in range(4)]
nodes[0].p = p1
nodes[0].x = 1.0
nodes[1].p = p2
nodes[2].p = nodes[1].p
nodes[2].x = 0.0
nodes[3].p = nodes[0].p 

# 2 connect device
c = Compressor(0, 1)
d = Condensor(1, 2)
t = Throttle(2, 3)
e = Evaporator(3,0)

nodes[0].px() 

c.simulate(nodes)    

d.simulate(nodes) 
print(nodes[2].p)
t.simulate(nodes)      

#e.simulate(nodes)

nodes[1].ps()      
nodes[2].px()
#    myobj = attributes = [attr for attr in dir(nodes[2]) if not attr.startswith('__')]
 


nodes[3].ph()




    


