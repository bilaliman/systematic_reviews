import krippendorff
import numpy as np

#Experiment 2.1
ann1 = [[2,0,1,0],[2,1,0,0],[1,0,0,2],[0,0,0,2],[1,0,0,2],[0,0,0,2],[2,0,1,0],[0,0,0,2],[1,0,0,2],[0,0,0,0]]
ann2 = [[2,0,1,0],[2,1,0,0],[1,0,0,2],[0,1,0,2],[2,0,0,1],[1,0,0,2],[2,0,0,1],[1,0,0,2],[1,0,0,2],[1,0,0,2]]
ann3 = [[2,0,1,0],[1,2,0,0],[1,0,0,2],[0,0,1,2],[1,0,0,2],[2,0,0,1],[2,0,0,1],[1,0,0,2],[1,0,0,2],[1,0,0,2]]

s = 0
for i in range(10):
    reliability_data = [ann1[i],ann2[i],ann3[i]]
    s += krippendorff.alpha(reliability_data=reliability_data,level_of_measurement="ordinal")

print('Experiment 2.1 agreement: ',s/10)




#Experiment 2.2
ann1 = [[0,2,0],[2,2,0],[0,2,1],[0,2,1],[2,1,0],[0,1,2],[1,0,2],[0,2,1],[0,1,2],[1,0,2]]
ann2 = [[0,2,0],[2,1,0],[0,2,1],[0,2,1],[1,1,2],[0,1,2],[1,0,2],[0,1,2],[0,1,2],[1,0,2]]
ann3 = [[1,2,0],[1,2,0],[0,2,1],[1,2,2],[0,2,1],[1,2,0],[1,0,2],[0,1,2],[0,1,2],[1,0,2]]

s = 0
for i in range(10):
    reliability_data = [ann1[i],ann2[i],ann3[i]]
    s += krippendorff.alpha(reliability_data=reliability_data,level_of_measurement="ordinal")

print('Experiment 2.2 agreement: ',s/10)