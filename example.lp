\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 x[0,3] + 0 x[0,4] + 0 x[0,5] + 0 x[0,6] + 0 x[0,7] + 0 x[1,3] + 0 x[1,4]
   + 0 x[1,5] + 0 x[1,6] + 0 x[1,7] + 0 x[2,3] + 0 x[2,4] + 0 x[2,5]
   + 0 x[2,6] + 0 x[2,7] + 0 x[3,3] + 0 x[3,4] + 0 x[3,5] + 0 x[3,6]
   + 0 x[3,7] + 0 x[4,0] + 0 x[4,1] + 0 x[4,2] + 0 x[4,3] + 0 x[4,4]
   + 0 x[4,5] + 0 x[4,6] + 0 x[4,7] + 0 x[5,0] + 0 x[5,1] + 0 x[5,2]
   + 0 x[5,3] + 0 x[5,4] + 0 x[5,5] + 0 x[5,6] + 0 y
Subject To
 con[0,0]: x[0,0] <= 1
 con[0,1]: x[0,1] <= 1
 con[0,2]: x[0,2] <= 1
 con[1,0]: x[1,0] <= 1
 con[1,1]: x[1,1] <= 1
 con[1,2]: x[1,2] <= 1
 con[2,0]: x[2,0] <= 1
 con[2,1]: x[2,1] <= 1
 con[2,2]: x[2,2] <= 1
 con[3,0]: x[3,0] <= 1
 con[3,1]: x[3,1] <= 1
 con[3,2]: x[3,2] <= 1
 con: x[0,1] + x[0,2] + x[5,7] <= 100
Bounds
End
