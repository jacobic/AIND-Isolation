import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

results = pd.DataFrame.from_csv('/Users/jacobic/ai-nanodegree/t1/AIND-Isolation/heuristic_data.csv')
results = results.T
sns.heatmap(results, annot=True, fmt='.2f', cmap="YlGnBu", 
                cbar_kws={'label': 'Win-rate'})
# plt.title('Heuristic Evaluation Function Analysis - {} Games'
#           .format((2*NUM_MATCHES)))
plt.ylabel('Test Agents')
plt.xlabel('CPU Agents')
plt.yticks(rotation=0)
#plt.savefig('/Users/jacobic/ai-nanodegree/t1/AIND-Isolation/heuristic_plot.png')
plt.show()
    
    