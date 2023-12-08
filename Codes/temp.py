import matplotlib.pyplot as plt

wall_length = 0.5
plt.plot(10,10) 
plt.plot([5-wall_length,5+wall_length],[5,5])
plt.plot([5,5],[5-wall_length,5+wall_length])
plt.show()