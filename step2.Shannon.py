import math
import re

def calculate_entropy(window):
    symbol_count = {}
    for symbol in window:
        if symbol in symbol_count:
            symbol_count[symbol] += 1
        else:
            symbol_count[symbol] = 1
    
    entropy = 0.0
    window_length = len(window)
    for count in symbol_count.values():
        probability = count / window_length
        entropy -= probability * math.log2(probability)
    
    return entropy

# File paths
input_windows_file = 'output_windows1.txt'
output_entropy_file = 'entropy_values.txt'

# Read the windows from the file
with open(input_windows_file, 'r') as file:
    window_lines = file.readlines()

# Calculate entropy for each window
with open(output_entropy_file, 'w') as output_file:
    for window_line in window_lines:
        window_match = re.search(r'Window \d+: ([01]+)', window_line)
        if window_match:
            window = window_match.group(1)
            entropy = calculate_entropy(window)
            output_file.write(f"Entropy: {entropy}\n")
