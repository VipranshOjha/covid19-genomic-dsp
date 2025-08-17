import os
import re
import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# --- Digitalization logic (from digitalizing sequence from atcg.py) ---
def convert_to_binary(sequence):
    mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
    return ''.join([mapping.get(base, base) for base in sequence])

def convert_fasta_to_binary(fasta_file):
    sequences = {}
    with open(fasta_file, 'r') as file:
        sequence_id = ""
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if sequence_id != "":
                    sequences[sequence_id] = convert_to_binary(sequence)
                sequence_id = line[1:]
                sequence = ""
            else:
                sequence += line.upper()
        if sequence_id != "":
            sequences[sequence_id] = convert_to_binary(sequence)
    return sequences

def save_binary_sequences(sequences, output_file):
    with open(output_file, 'w') as out:
        for seq_id, binary_seq in sequences.items():
            out.write(f"Sequence ID: {seq_id}\n")
            out.write(f"Binary Sequence: {binary_seq}\n\n")

# --- Windowing logic (if needed) ---
def create_windows(binary_sequence, window_size=100, step=10):
    windows = []
    for i in range(0, len(binary_sequence) - window_size + 1, step):
        windows.append(binary_sequence[i:i+window_size])
    return windows

def save_windows(windows, output_file):
    with open(output_file, 'w') as f:
        for idx, window in enumerate(windows):
            f.write(f"Window {idx+1}: {window}\n")

# --- Entropy calculation (from step2.Shannon.py) ---
def calculate_entropy(window):
    symbol_count = {}
    for symbol in window:
        symbol_count[symbol] = symbol_count.get(symbol, 0) + 1
    entropy = 0.0
    window_length = len(window)
    for count in symbol_count.values():
        probability = count / window_length
        entropy -= probability * math.log2(probability)
    return entropy

def calculate_entropy_for_windows(windows, output_file):
    with open(output_file, 'w') as output_file:
        for window in windows:
            entropy = calculate_entropy(window)
            output_file.write(f"Entropy: {entropy}\n")

# --- Plotting (from step3plotting.py) ---
def plot_entropy(entropy_file):
    with open(entropy_file, 'r') as file:
        entropy_values = [float(line.strip().split(': ')[1]) for line in file]
    plt.figure(figsize=(10, 6))
    plt.plot(entropy_values, marker='o', linestyle='-')
    plt.title('Information Entropy Spectra')
    plt.xlabel('Window Position')
    plt.ylabel('Shannon Entropy')
    plt.grid(True)
    plt.show()

# --- Spectrogram (from spectogram.py) ---
def convert_to_numeric(sequence):
    mapping = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
    return np.array([mapping.get(base, -1) for base in sequence], dtype=np.int32)

def create_spectrogram(sequence):
    numeric_sequence = convert_to_numeric(sequence)
    frequencies, times, Sxx = signal.spectrogram(
        numeric_sequence, fs=1.0, window='hamming', nperseg=100, noverlap=50)
    plt.figure(figsize=(8, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
    plt.ylabel('Frequency')
    plt.xlabel('Time')
    plt.title('DNA Sequence Spectrogram')
    plt.colorbar(label='Intensity (dB)')
    plt.show()

# --- Main pipeline orchestration ---
def main():
    fasta_file = 'coronavirus.fasta'
    binary_sequences_file = 'binary_sequences.txt'
    windows_file = 'output_windows1.txt'
    entropy_file = 'entropy_values.txt'

    # Step 1: Digitalize FASTA
    print('Converting FASTA to binary...')
    binary_sequences = convert_fasta_to_binary(fasta_file)
    save_binary_sequences(binary_sequences, binary_sequences_file)
    print(f'Binary sequences saved to {binary_sequences_file}')

    # Step 2: Create windows for the first sequence (as an example)
    first_seq_id = next(iter(binary_sequences))
    first_binary_seq = binary_sequences[first_seq_id]
    print(f'Creating windows for sequence {first_seq_id}...')
    windows = create_windows(first_binary_seq, window_size=100, step=10)
    save_windows(windows, windows_file)
    print(f'Windows saved to {windows_file}')

    # Step 3: Calculate entropy for each window
    print('Calculating entropy for each window...')
    calculate_entropy_for_windows(windows, entropy_file)
    print(f'Entropy values saved to {entropy_file}')

    # Step 4: Plot entropy
    print('Plotting entropy values...')
    plot_entropy(entropy_file)

    # Step 5: Create spectrogram for the first sequence (original ATCG, not binary)
    print('Creating spectrogram for the first sequence...')
    # Re-read the original sequence from FASTA
    with open(fasta_file, 'r') as file:
        sequence = ''
        for line in file:
            if not line.startswith('>'):
                sequence += line.strip().upper()
    create_spectrogram(sequence)

if __name__ == '__main__':
    main()
