import matplotlib.pyplot as plt 
  
# x axis values 
x = [8, 8, 32, 32, 32, 360, 360, 360, 3312, 3312, 7856, 12416, 12416, 12416, 12416, 12416 , 8, 8, 292112, 292112, 584224  , 7736640]

# corresponding y axis values 
y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0 , 0, 98]
  
# plotting the points  
plt.scatter(x, y, label= "stars", color= "green", marker= ".", s=30) 
# plt.plot(x,y)

  
# naming the x axis 
plt.xlabel('x - Nombre de bits envoyés') 
# naming the y axis 
plt.ylabel('y - Nombre de bits éronnés') 
  
# giving a title to my graph 
plt.title('Noise analysis') 
  
# function to show the plot 
plt.show() 

