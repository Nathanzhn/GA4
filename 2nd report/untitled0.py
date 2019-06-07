import csv

with open('state.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        
        
        
##output state
with open('state.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['State','P','T','h','s','x'])
    for i in range(4):
        s_list = [i,states[i].p,states[i].t,states[i].h,states[i].s,states[i].x]
        writer.writerow(s_list)
        
#### output system parameters 
##with open('state.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(['qc','qh','COPR','COPcar'])
#    writer.writerow([d.qc,b.qh,COP_inner,COP_carnot])