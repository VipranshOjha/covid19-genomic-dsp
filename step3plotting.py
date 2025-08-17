import matplotlib.pyplot as plt

# File path for entropy values
entropy_values_file = 'entropy_values.txt'

# Read entropy values from the file
with open(entropy_values_file, 'r') as file:
    entropy_values = [float(line.strip().split(': ')[1]) for line in file]

# Plotting the entropy spectra
plt.figure(figsize=(10, 6))
plt.plot(entropy_values, marker='o', linestyle='-')
plt.title('Information Entropy Spectra')
plt.xlabel('Window Position')
plt.ylabel('Shannon Entropy')
plt.grid(True)
plt.show()




