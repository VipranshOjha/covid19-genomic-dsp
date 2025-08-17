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

# Read the DNA sequences from a FASTA file
file_path = 'coronavirus.fasta'  # Replace with your FASTA file path

sequences = []
current_sequence = ''
with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('>'):  # Header line
            if current_sequence:
                sequences.append(current_sequence)
                current_sequence = ''
        else:
            current_sequence += line

    if current_sequence:  # Append the last sequence
        sequences.append(current_sequence)

# Process and create spectrogram for each sequence
for seq_idx, dna_sequence in enumerate(sequences, start=1):
    create_spectrogram(dna_sequence)
