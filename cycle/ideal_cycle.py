import Nodes
import compressor
import condensor
import throttle
import evaporator


"given conditions and initialise nodes"
fluid = 'R134a'
p1 = 500000
p2 = 1600000
T1 = 293
T2 = 350
T3 = 310
T4 = 300
Tw_in = 321
Tw_out = 330
Ta_in = 293
Ta_out = 280
mdot_a = 1.0
mdot_w = 1.0
mdot_r = 1.0



"0-3 Exp nodes, 4-7 Ideal nodes"
nodes = [Nodes.Node() for i in range(8)]
nodes[0].p = p1
nodes[0].x = 1.0
nodes[1].p = p2
nodes[2].p = nodes[1].p
nodes[2].x = 0.0
nodes[3].p = nodes[0].p 

# 2 connect device
c = compressor.Compressor(0, 1, 5)
d = condensor.Condensor(1, 2, 6)
t = throttle.Throttle(2, 3, 7)
e = evaporator.Evaporator(3,0, 8)

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




    


