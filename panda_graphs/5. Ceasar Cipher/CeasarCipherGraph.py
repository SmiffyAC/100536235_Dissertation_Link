import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV data into a DataFrame
df = pd.read_csv('panda_graphs/5. Ceasar Cipher/CaesarCipher.csv')

# Convert 'TimeTaken (ms)' to seconds
df['TimeTaken (ms)'] = df['TimeTaken (ms)'] / 1000

# Group the data by 'FileID' and 'Method', and calculate the mean 'TimeTaken (ms)'
grouped = df.groupby(['FileID', 'Method'])['TimeTaken (ms)'].mean().reset_index()

# Create a line plot with two separate lines for JS and WASM
plt.figure(figsize=(10, 6))  # Increase the figure height to accommodate the text below
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.15)  # Adjust plot margins

for method, color in [('JS', 'darkorange'), ('WASM', 'dodgerblue')]:
    subset = grouped[grouped['Method'] == method]
    plt.plot(subset['FileID'], subset['TimeTaken (ms)'], marker='o', label=method, color=color)
    
    # Calculate the mean value for the current method
    mean_value = subset['TimeTaken (ms)'].mean()
    
    # Add a horizontal line for the mean value
    plt.axhline(mean_value, color=color, linestyle='--', linewidth=1, alpha=0.7)
    
    # Add the mean value as text annotation on the right or left side of the graph with a small offset
    if method == 'JS':
        plt.text(plt.xlim()[1] + 0.1, mean_value, f'Mean ({method}): {mean_value:.2f}s', 
                 color=color, verticalalignment='center', horizontalalignment='left')
    else:
        plt.text(plt.xlim()[0] - 0.1, mean_value, f'Mean ({method}): {mean_value:.2f}s', 
                 color=color, verticalalignment='center', horizontalalignment='right')

# Set labels and title
plt.xlabel('File ID', fontsize=14)
plt.ylabel('Average Time Taken (s)', fontsize=14)  # Change label to 's' for seconds
plt.title('Caesar Cipher - Average Time Taken by File ID for JS and WASM', fontsize=16)
plt.xticks(range(1, 11))  # Adjust the range based on the number of unique file IDs
plt.legend()

# Format y-axis to show one decimal place
formatter = FuncFormatter(lambda y, _: '{:.1f}'.format(y))
plt.gca().yaxis.set_major_formatter(formatter)

# Calculate key values
js_mean = grouped[grouped['Method'] == 'JS']['TimeTaken (ms)'].mean()
wasm_mean = grouped[grouped['Method'] == 'WASM']['TimeTaken (ms)'].mean()

js_std = grouped[grouped['Method'] == 'JS']['TimeTaken (ms)'].std()
wasm_std = grouped[grouped['Method'] == 'WASM']['TimeTaken (ms)'].std()

js_max = grouped[grouped['Method'] == 'JS']['TimeTaken (ms)'].max()
wasm_max = grouped[grouped['Method'] == 'WASM']['TimeTaken (ms)'].max()

js_min = grouped[grouped['Method'] == 'JS']['TimeTaken (ms)'].min()
wasm_min = grouped[grouped['Method'] == 'WASM']['TimeTaken (ms)'].min()

# Add key values below the graph
plt.figtext(0.1, 0.05, 'JavaScript:', fontsize=12)
plt.figtext(0.1, 0.03, f'  Mean: {js_mean:.3f} seconds', fontsize=10)
plt.figtext(0.1, 0.01, f'  Std Dev: {js_std:.3f} seconds', fontsize=10)
plt.figtext(0.3, 0.03, f'  Max: {js_max:.3f} seconds', fontsize=10)
plt.figtext(0.3, 0.01, f'  Min: {js_min:.3f} seconds', fontsize=10)

plt.figtext(0.6, 0.05, 'WebAssembly:', fontsize=12)
plt.figtext(0.6, 0.03, f'  Mean: {wasm_mean:.3f} seconds', fontsize=10)
plt.figtext(0.6, 0.01, f'  Std Dev: {wasm_std:.3f} seconds', fontsize=10)
plt.figtext(0.8, 0.03, f'  Max: {wasm_max:.3f} seconds', fontsize=10)
plt.figtext(0.8, 0.01, f'  Min: {wasm_min:.3f} seconds', fontsize=10)

plt.grid(True)
plt.tight_layout()
plt.show()