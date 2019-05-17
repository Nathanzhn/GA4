import Nodes
import compressor
import condensor
import throttle
import evaporator




"given conditions and initialise nodes"
fluid = 'R134a'
p1 = 100000
p2 = 800000

nodes = [Nodes.Node() for i in range(4)]
nodes[0].p = p1
nodes[0].x = 1.0
nodes[1].p = p2
nodes[2].p = nodes[1].p
nodes[2].x = 0.0
nodes[3].p = nodes[0].p 

# 2 connect device
c = compressor.Compressor(0, 1)
d = condensor.Condensor(1, 2)
t = throttle.Throttle(2, 3)
e = evaporator.Evaporator(3,0)

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




    


