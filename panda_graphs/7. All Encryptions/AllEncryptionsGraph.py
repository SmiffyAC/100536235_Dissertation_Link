import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV data into DataFrames
df_caesar = pd.read_csv('panda_graphs/5. Ceasar Cipher/CaesarCipher.csv')
df_vigenere = pd.read_csv('panda_graphs/6. Vigenere Cipher/VigenereCipher.csv')

# Convert 'TimeTaken (ms)' to seconds for both DataFrames
df_caesar['TimeTaken (ms)'] = df_caesar['TimeTaken (ms)'] / 1000
df_vigenere['TimeTaken (ms)'] = df_vigenere['TimeTaken (ms)'] / 1000

# Group the data by 'FileID' and 'Method', and calculate the mean 'TimeTaken (ms)' for both DataFrames
grouped_caesar = df_caesar.groupby(['FileID', 'Method'])['TimeTaken (ms)'].mean().reset_index()
grouped_vigenere = df_vigenere.groupby(['FileID', 'Method'])['TimeTaken (ms)'].mean().reset_index()

# Create a single figure with all plots and lines
fig, ax = plt.subplots(figsize=(10, 8))  # Increase the figure height
fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.25)  # Increase the bottom margin

# Plot Caesar Cipher data
for method, color, linestyle in [('JS', 'darkorange', '-'), ('WASM', 'dodgerblue', '-')]:
    subset = grouped_caesar[grouped_caesar['Method'] == method]
    ax.plot(subset['FileID'], subset['TimeTaken (ms)'], marker='o', label=f'Caesar Cipher - {method}',
            color=color, linestyle=linestyle)

# Plot Vigenere Cipher data
for method, color, linestyle in [('JS', 'darkorange', '--'), ('WASM', 'dodgerblue', '--')]:
    subset = grouped_vigenere[grouped_vigenere['Method'] == method]
    ax.plot(subset['FileID'], subset['TimeTaken (ms)'], marker='o', label=f'Vigenère Cipher - {method}',
            color=color, linestyle=linestyle)

ax.set_xlabel('File ID', fontsize=14)
ax.set_ylabel('Average Time Taken (s)', fontsize=14)  # Change label to 's' for seconds
ax.set_title('Caesar Cipher and Vigenère Cipher - Average Time Taken by File ID for JS and WASM', fontsize=16)
ax.set_xticks(range(1, 11))  # Adjust the range based on the number of unique file IDs
ax.legend(fontsize=10)

# Format y-axis to show one decimal place
formatter = FuncFormatter(lambda y, _: '{:.1f}'.format(y))
ax.yaxis.set_major_formatter(formatter)

# Calculate key values for Caesar Cipher
js_mean_caesar = grouped_caesar[grouped_caesar['Method'] == 'JS']['TimeTaken (ms)'].mean()
wasm_mean_caesar = grouped_caesar[grouped_caesar['Method'] == 'WASM']['TimeTaken (ms)'].mean()

js_std_caesar = grouped_caesar[grouped_caesar['Method'] == 'JS']['TimeTaken (ms)'].std()
wasm_std_caesar = grouped_caesar[grouped_caesar['Method'] == 'WASM']['TimeTaken (ms)'].std()

js_max_caesar = grouped_caesar[grouped_caesar['Method'] == 'JS']['TimeTaken (ms)'].max()
wasm_max_caesar = grouped_caesar[grouped_caesar['Method'] == 'WASM']['TimeTaken (ms)'].max()

js_min_caesar = grouped_caesar[grouped_caesar['Method'] == 'JS']['TimeTaken (ms)'].min()
wasm_min_caesar = grouped_caesar[grouped_caesar['Method'] == 'WASM']['TimeTaken (ms)'].min()

# Calculate key values for Vigenere Cipher
js_mean_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'JS']['TimeTaken (ms)'].mean()
wasm_mean_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'WASM']['TimeTaken (ms)'].mean()

js_std_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'JS']['TimeTaken (ms)'].std()
wasm_std_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'WASM']['TimeTaken (ms)'].std()

js_max_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'JS']['TimeTaken (ms)'].max()
wasm_max_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'WASM']['TimeTaken (ms)'].max()

js_min_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'JS']['TimeTaken (ms)'].min()
wasm_min_vigenere = grouped_vigenere[grouped_vigenere['Method'] == 'WASM']['TimeTaken (ms)'].min()

# Add key values below the graph for Caesar Cipher
plt.figtext(0.05, 0.16, 'Caesar Cipher - JavaScript:', fontsize=12)
plt.figtext(0.05, 0.13, f'  Mean: {js_mean_caesar:.3f} seconds', fontsize=10)
plt.figtext(0.05, 0.11, f'  Std Dev: {js_std_caesar:.3f} seconds', fontsize=10)
plt.figtext(0.2, 0.13, f'  Max: {js_max_caesar:.3f} seconds', fontsize=10)
plt.figtext(0.2, 0.11, f'  Min: {js_min_caesar:.3f} seconds', fontsize=10)

plt.figtext(0.05, 0.08, 'Caesar Cipher - WebAssembly:', fontsize=12)
plt.figtext(0.05, 0.05, f'  Mean: {wasm_mean_caesar:.3f} seconds', fontsize=10)
plt.figtext(0.05, 0.03, f'  Std Dev: {wasm_std_caesar:.3f} seconds', fontsize=10)
plt.figtext(0.2, 0.05, f'  Max: {wasm_max_caesar:.3f} seconds', fontsize=10)
plt.figtext(0.2, 0.03, f'  Min: {wasm_min_caesar:.3f} seconds', fontsize=10)

# Add key values below the graph for Vigenere Cipher
plt.figtext(0.55, 0.16, 'Vigenère Cipher - JavaScript:', fontsize=12)
plt.figtext(0.55, 0.13, f'  Mean: {js_mean_vigenere:.3f} seconds', fontsize=10)
plt.figtext(0.55, 0.11, f'  Std Dev: {js_std_vigenere:.3f} seconds', fontsize=10)
plt.figtext(0.7, 0.13, f'  Max: {js_max_vigenere:.3f} seconds', fontsize=10)
plt.figtext(0.7, 0.11, f'  Min: {js_min_vigenere:.3f} seconds', fontsize=10)

plt.figtext(0.55, 0.08, 'Vigenère Cipher - WebAssembly:', fontsize=12)
plt.figtext(0.55, 0.05, f'  Mean: {wasm_mean_vigenere:.3f} seconds', fontsize=10)
plt.figtext(0.55, 0.03, f'  Std Dev: {wasm_std_vigenere:.3f} seconds', fontsize=10)
plt.figtext(0.7, 0.05, f'  Max: {wasm_max_vigenere:.3f} seconds', fontsize=10)
plt.figtext(0.7, 0.03, f'  Min: {wasm_min_vigenere:.3f} seconds', fontsize=10)

plt.grid(True)
plt.show()