import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def convert_to_numeric(sequence):
    mapping = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
    return np.array([mapping.get(base, -1) for base in sequence], dtype=np.int32)

def create_spectrogram(sequence):
    numeric_sequence = convert_to_numeric(sequence)

    # Use scipy's spectrogram function
    frequencies, times, Sxx = signal.spectrogram(
        numeric_sequence, fs=1.0, window='hamming', nperseg=100, noverlap=50)

    # Plot the spectrogram
    plt.figure(figsize=(8, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
    plt.ylabel('Frequency')
    plt.xlabel('Time')
    plt.title('DNA Sequence Spectrogram')
    plt.colorbar(label='Intensity (dB)')
    plt.show()

# Read the DNA sequence from a file
file_path = 'exons_introns.txt'  # Replace with your file path
with open(file_path, 'r') as file:
    dna_sequence = file.read().strip()  # Assuming the sequence is in one line

# Create spectrogram
create_spectrogram(dna_sequence)
























