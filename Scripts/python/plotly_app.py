import matplotlib.pyplot as plt
import pandas as pd

# Read the data from the CSV file and store it in a data frame
df = pd.read_csv(r'D:\workspace\Sample.csv')
print(df)
melted_df = df.melt(id_vars=['RiskType', 'RiskClassification'], var_name="ReportingPeriod")
print(melted_df)
melted_df.plot(kind='bar')
# plt.show()
#
# # Group the data by RiskType and RiskClassification
# grouped = df.groupby(['RiskType', 'RiskClassification'])
#
# # Use unstack to reshape the data into a format suitable for a stacked bar chart
# unstacked = grouped.sum().unstack()
#
# # Create a stacked bar chart with the data
# unstacked.plot(kind='bar', stacked=False)
#
# # Add labels, titles, and other elements to customize the plot
# plt.xlabel('Risk Type')
# plt.ylabel('Risk Classification')
# plt.title('Stacked Bar Chart of Risk Classifications by Risk Type')
#
# plt.show()