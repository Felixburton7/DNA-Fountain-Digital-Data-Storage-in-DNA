'''Summary of the process (my attempt)

The script decodes DNA droplet information back to its original message. It  loads the luby_blocks.csv file to identify which blocks of information are encoded in each droplet. It then decodes the DNA sequences from the droplet_sequences.txt (fasta) file into binary format using a specified encoding scheme (A -> 00, G -> 01, C -> 10, T -> 11). Each droplet's binary sequence is divided into three parts: Luby Index, Droplet Message, and Error Correction Code. The Luby Index, Droplet Message, and Error Correction Code are extracted and stored.

Using the Luby Transform, the script reconstructs the original blocks from the droplet messages by performing XOR operations where necessary. During the reconstruction, any unexpected DNA bases are ignored, ensuring only valid sequences are processed. The script handles cases where block indices are out of range by skipping those droplets. After decoding each droplet's message, the script combines the blocks to form the final binary message.

Finally, the binary message is converted back to text, completing the decoding process. The script prints intermediate steps and final results for verification, including the decoded binary sequences and the final text message. This comprehensive approach ensures accurate reconstruction of the original message from the encoded DNA droplets.

Task:

Goal: Decode the DNA droplet information back to the original message by reversing the Luby Transform.

Input Files:
luby_blocks.csv: Identifies which blocks of information are encoded in each droplet.
droplet_sequences.txt: Contains the sequencing results of the DNA droplets (the fasta file that you gave us). 

Encoding Scheme:
A -> 00
G -> 01
C -> 10
T -> 11
Droplet Structure: Each droplet consists of:
Luby Index (16 bits)
Droplet Message (256 bits)
Error Correction Code (16 bits)'''


# Import necessary libraries
import pandas as pd

# Load the CSV file into a DataFrame with correct splitting
csv_file_path = 'luby_blocks.csv'
df = pd.read_csv(csv_file_path, header=None, names=['drop'])

# Split the 'drop' column into separate 'drop' and 'blocks' columns
df['blocks'] = df['drop'].apply(lambda x: x.split(' - blocks: ')[1])
df['drop'] = df['drop'].apply(lambda x: x.split(' - blocks: ')[0])

# Display the first few rows and column names of the DataFrame to verify the structure
print(df.head())
print(df.columns)

# Define function to convert DNA sequence to binary


def dna_to_binary(dna_sequence):
    encoding = {'A': '00', 'G': '01', 'C': '10', 'T': '11'}
    binary_sequence = []
    for base in dna_sequence:
        if base in encoding:
            binary_sequence.append(encoding[base])
        else:
            print(
                f"Warning: Unexpected base '{base}' found. Ignoring this base.")
    return ''.join(binary_sequence)


# Load and parse the droplet_sequences.fasta file
sequences = {}
# Ensure the correct path is specified
fasta_file_path = 'droplet_sequences.txt'
try:
    with open(fasta_file_path, mode='r') as file:
        droplet_number = ''
        for line in file:
            if line.startswith('>'):
                header = line.strip()
                droplet_number = header.split('_')[1][1:]
            else:
                sequence = line.strip()
                binary_sequence = dna_to_binary(sequence)
                sequences[droplet_number] = binary_sequence

    # Display a few decoded sequences for verification
    for key, value in list(sequences.items())[:5]:
        # Print the first 64 bits for brevity
        print(f"Droplet {key}: {value[:64]}...")
except FileNotFoundError:
    print(f"File not found: {fasta_file_path}")

# Define function to extract parts from binary sequence


def extract_parts(binary_sequence):
    luby_index = binary_sequence[:16]
    droplet_message = binary_sequence[16:272]
    error_correction_code = binary_sequence[272:288]
    return luby_index, droplet_message, error_correction_code


# Create a dictionary to hold the extracted parts for each droplet
droplet_data = {}
for droplet_number, binary_sequence in sequences.items():
    luby_index, droplet_message, error_correction_code = extract_parts(
        binary_sequence)
    droplet_data[droplet_number] = {
        'luby_index': luby_index,
        'droplet_message': droplet_message,
        'error_correction_code': error_correction_code
    }

# Display a few extracted parts for verification
for key, value in list(droplet_data.items())[:5]:
    print(
        f"Droplet {key}: Luby Index - {value['luby_index']}, Droplet Message - {value['droplet_message'][:64]}..., Error Correction Code - {value['error_correction_code']}")

# Initialize an array to hold the blocks
n_blocks = 56  # Number of unique blocks of information
blocks = [None] * n_blocks

# Define function to XOR two binary strings


def xor_binary_strings(str1, str2):
    return ''.join(['0' if bit1 == bit2 else '1' for bit1, bit2 in zip(str1, str2)])


# Decode the blocks using the droplet data
for droplet_number, data in droplet_data.items():
    try:
        # Debug print to check the droplet number being processed
        print(f"Processing droplet: {droplet_number}")

        block_indices_str = df[df['drop'] ==
                               f'drop_n{droplet_number}']['blocks'].values
        if len(block_indices_str) == 0:
            raise IndexError(
                f"No block indices found for droplet {droplet_number}")

        block_indices = list(
            map(int, block_indices_str[0].strip('[]').split(', ')))
        print(f"Droplet {droplet_number}: Blocks {block_indices}")
    except IndexError as e:
        print(f"Error processing droplet {droplet_number}: {e}")
        continue

    decoded_message = data['droplet_message']

    for index in block_indices:
        if index >= n_blocks:
            print(
                f"Error: Block index {index} is out of range for droplet {droplet_number}")
            continue

        if blocks[index] is None:
            blocks[index] = decoded_message
        else:
            blocks[index] = xor_binary_strings(blocks[index], decoded_message)

# Combine the blocks to form the final message
final_message_binary = ''.join(block for block in blocks if block is not None)
print("Final Message in Binary:", final_message_binary)

# Convert the final binary message to text


def binary_to_text(binary_str):
    n = int(binary_str, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()


try:
    final_message_text = binary_to_text(final_message_binary)
    print("Final Decoded Message:", final_message_text)
except ValueError:
    print("Invalid binary string for text conversion")
