import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV data into DataFrames
caesar_df = pd.read_csv('panda_graphs/5. Ceasar Cipher/CaesarCipher.csv')
vigenere_df = pd.read_csv('panda_graphs/6. Vigenere Cipher/VigenereCipher.csv')

# Combine the DataFrames into a single DataFrame
combined_df = pd.concat([caesar_df, vigenere_df])

# Convert 'TimeTaken (ms)' to seconds
combined_df['TimeTaken (ms)'] = combined_df['TimeTaken (ms)'] / 1000

# Group the data by 'FileID', 'Method', and 'EncryptionMethod', and calculate the mean 'TimeTaken (ms)'
grouped = combined_df.groupby(['FileID', 'Method', 'EncryptionMethod'])['TimeTaken (ms)'].mean().reset_index()

# Create a line plot with separate lines for each cipher and method
plt.figure(figsize=(10, 6))
colors = ['darkorange', 'dodgerblue']
ciphers = ['caesar', 'vigenere']

for cipher, shade in zip(ciphers, [0.3, 0.6]):
    for method, color in zip(['JS', 'WASM'], colors):
        subset = grouped[(grouped['EncryptionMethod'] == cipher) & (grouped['Method'] == method)]
        plt.plot(subset['FileID'], subset['TimeTaken (ms)'], marker='o', label=f'{cipher.capitalize()} - {method}',
                 color=color, alpha=shade)

# Set labels and title
plt.xlabel('File ID')
plt.ylabel('Average Time Taken (s)')  # Change label to 's' for seconds
plt.title('Caesar and Vigenere Ciphers - Average Time Taken by File ID for JS and WASM')
plt.xticks(range(1, 11))  # Adjust the range based on the number of unique file IDs
plt.legend()

# Format y-axis to show one decimal place
formatter = FuncFormatter(lambda y, _: '{:.1f}'.format(y))
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)
plt.show()