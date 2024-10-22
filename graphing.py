
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('../Datasets/user_behavior_dataset.csv')

plt.figure(figsize=(10,6))
plt.plot(data['Screen On Time (hours/day)'].head(50), marker='o')
plt.xlabel('User ID')
plt.ylabel('Screen On Time (hours/day)')
plt.title('Screen Time of the First 50 Users')
plt.show()

