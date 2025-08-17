def convert_to_binary(sequence):
    binary_sequence = ""
    mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}

    for base in sequence:
        if base in mapping:
            binary_sequence += mapping[base]
        else:
            # Handle other characters, if any
            binary_sequence += base

    return binary_sequence

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

# Replace 'your_file.fasta' with the path to your FASTA file
fasta_file = 'coronavirus.fasta'

# Convert FASTA sequences to binary
binary_sequences = convert_fasta_to_binary(fasta_file)

# Save binary sequences to a text file
output_file = 'binary_sequences.txt'
with open(output_file, 'w') as out:
    for seq_id, binary_seq in binary_sequences.items():
        out.write(f"Sequence ID: {seq_id}\n")
        out.write(f"Binary Sequence: {binary_seq}\n\n")

print(f"Binary sequences saved to {output_file}")
