import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# Load the CSV data into a DataFrame
df = pd.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_SepiaTone_all_res.csv')

# Convert 'Time Taken (ms)' to seconds
df['Time Taken (ms)'] = df['Time Taken (ms)'] / 1000

# Group the data by 'Resolution Category' and 'Method', and calculate the mean 'Time Taken (ms)'
grouped = df.groupby(['Resolution Category', 'Method'])['Time Taken (ms)'].mean().reset_index()

# Create a helper function to map resolution categories to a numerical value
resolution_map = {'720p': 1, '1080p': 2, '2K': 3, '4K': 4, '8K': 5}
grouped['Resolution_Rank'] = grouped['Resolution Category'].map(resolution_map)

# Sort the data by 'Resolution_Rank'
grouped = grouped.sort_values('Resolution_Rank')

# Create a line plot with two separate lines for JS and WASM
plt.figure(figsize=(10, 6))
plt.subplots_adjust(left=0.1, right=0.8, top=0.95, bottom=0.1)  # Adjust plot margins

for method, color in [('JS', 'darkorange'), ('WASM', 'dodgerblue')]:
    subset = grouped[grouped['Method'] == method]
    plt.plot(subset['Resolution_Rank'], subset['Time Taken (ms)'], marker='o', label=method, color=color)

# Calculate the timing differences between JS and WASM for each resolution
js_times = grouped[grouped['Method'] == 'JS'].set_index('Resolution Category')['Time Taken (ms)']
wasm_times = grouped[grouped['Method'] == 'WASM'].set_index('Resolution Category')['Time Taken (ms)']
timing_diffs = js_times - wasm_times

# Add the timing differences as a dotted black line
for res_rank in grouped['Resolution_Rank'].unique():
    res_cat = grouped[grouped['Resolution_Rank'] == res_rank]['Resolution Category'].iloc[0]
    js_time = js_times[res_cat]
    wasm_time = wasm_times[res_cat]
    plt.plot([res_rank, res_rank], [js_time, wasm_time], linestyle='--', color='black', linewidth=1)
    
    # Add the timing difference as text annotation on the right side of the dotted line (except for 720p)
    diff = timing_diffs[res_cat]
    if res_cat == '720p':
        plt.text(res_rank - 0.025, (js_time + wasm_time) / 2, f'{diff:.2f}s', fontsize=10, ha='right', va='center')
    else:
        plt.text(res_rank + 0.025, (js_time + wasm_time) / 2, f'{diff:.2f}s', fontsize=10, ha='left', va='center')

# Set labels and title
plt.xlabel('Resolution (Ascending Order)', fontsize=14)
plt.ylabel('Average Time Taken (s)', fontsize=14)  # Change label to 's' for seconds
plt.title('Sepia Tone - Average Time Taken by Resolution for JS and WASM', fontsize=16)
plt.xticks(ticks=range(1, 6), labels=['720p', '1080p', '2K', '4K', '8K'])
plt.legend()

# Format y-axis to show one decimal place
formatter = FuncFormatter(lambda y, _: '{:.1f}'.format(y))
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)
plt.tight_layout()
plt.show()