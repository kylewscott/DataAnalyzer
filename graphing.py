
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('../Datasets/user_behavior_dataset.csv')

plt.figure(figsize=(10,6))
plt.bar(range(50), data.iloc[:50, 7].values)
plt.xlabel('User ID')
plt.ylabel('Screen On Time (hours/day)')
plt.title('Screen time for the first 50 users')
plt.show()

