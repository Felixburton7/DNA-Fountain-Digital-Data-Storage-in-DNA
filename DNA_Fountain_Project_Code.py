#!/usr/bin/env python
# coding: utf-8

# # Challenge 1 - DNA Fountain
# 
# Felix Burton 

# ## Imports


from Bio import SeqIO
import pandas as pd
import re
import nltk
from nltk.corpus import words

# ## Reading Files

# ### Reading sequence records from fasta


records = [r  for r in SeqIO.parse("droplet_sequences.fasta", "fasta")]
records[0:3]


# ### Reading block encodings

# In[21]:


# Read the CSV file and extract the blocks column
blocks_raw = pd.read_csv('luby_blocks.csv', header=None)[0]

# Define a function to extract blocks from each entry
def extract_blocks(entry):
    return re.findall(r'\b\d+\b', entry)

# Extract blocks from each entry using the defined function
blocks = [list(set(extract_blocks(entry))) for entry in blocks_raw]

print(blocks_raw[0:3])
blocks[0:3] 

# ### Checking consistency between imports

# In[22]:


degrees_csv = [len(b) -  1 for b in blocks]
degrees_fasta = [list(re.split('d', r.name))[-1] for r in records]

print(f"Consistent: {degrees_csv == degrees_fasta}")
[[degrees_csv[i],degrees_fasta[i]] for i in range(len(degrees_csv))][0:6]

# ## Decoding droplets

# ### Double-checking reduncancy and counting number of blocks


#Finding the total number of blocks encoded
number_of_blocks = max([int(i) for j in blocks for i in j]) + 1
print(f"{number_of_blocks} total blocks encoded")

#Finding the total number of droplets used
number_of_drops = len(blocks)
print(f"{number_of_drops} droplets created\n"f"{number_of_drops/number_of_blocks}-fold redundancy")


# ### Decoding 0-degree blocks as a sanity check 

#Finding which droplets have index degree
zero_deg_inds = [i for i in range(len(degrees_csv)) if degrees_csv[i] == 0]
print(f"Indices of droplets with degree-0: {zero_deg_inds}")

#A helper function for slicing arrays using a list of indices
def slc(lst, inds):
    rArray = []
    for i in inds:
        rArray += [lst[i]]
    return rArray
    

#A dictionary for decoding sequences into binary
decode_dict = {
    'A' : '00',
    'G' : '01',
    'C' : '10',
    'T' : '11'
}

#Starting by decoding these droplets directly
zero_deg_drops = [s.seq for s in slc(records, zero_deg_inds)]
decoded_blocks = [int(i[0]) for i in slc(blocks, zero_deg_inds)]

#Helper for converting a DNA seq to binary
def decode(s):
    return "".join([decode_dict[c] for c in s])

# Converting each sequence to binary
zero_deg_binary = [decode(s) for s in zero_deg_drops]

#Function for Xor of strings for decoding
def xor(str1, str2):
    # Convert binary strings to integers
    int1 = int(str1, 2)
    int2 = int(str2, 2)
    
    # Perform XOR operation
    result_int = int1 ^ int2
    
    # Convert result back to binary string
    result_str = bin(result_int)[2:]  # Remove '0b' prefix
    
    # Pad with leading zeros if necessary
    result_str = result_str.zfill(max(len(str1), len(str2)))
    
    return result_str

#Function for decoding a binary string
def decode_luby_drop(s):
    
    payload = s[16:len(s)-16]
    payload_size = (len(s)-32)//8



    return ''.join(chr(int(payload[8*i : 8*i + 8],2)) for i in range(payload_size))

#Get luby index of a droplet
def get_index(d):
    
    payload = d[0:16]

    return int(payload,2)


print(decoded_blocks)
zero_deg_messages = [decode_luby_drop(s) for s in zero_deg_binary]
zero_deg_messages


# How should I deal with broken reads? Checking for the presence of '\x00' will be a sufficient heuristic. (It turns out i also needed a heuristic to rule out some that didnt have null characters and had gibberish words by comparing against an english word dictionary)

# ## Decoding blocks based on queue of non-processed droplets


#Storing the fully decoded binaries in a dictionary
decoded = {decoded_blocks[i] : zero_deg_binary[i] for i in range(len(decoded_blocks))}
bad_droplets = []


#A heuristic function that checks for english words
def contains_word(sentence):
    ret = any([wrd in words.words()for wrd in sentence.split()])
    return ret

#check for any broken decryptions
deletes = []
for i,k in enumerate(decoded.keys()):
        if '\x00' in decode_luby_drop(decoded[k]):
            deletes += [k]
            bad_droplets += [zero_deg_inds[i]]
for d in deletes:
    del decoded[d]

#Converting text to int in list
def to_int(l):
    return([int(i) for i in l])


#Loop for decoding droplets based on the decoding of smaller order droplets
while len(decoded) < number_of_blocks :
#while len(possible) > 0:    
#for i in range(100):
    #Get the list of droplets that are already decoded
    decoded_block_nums = [int(i) for i in list(decoded.keys())]

    #Determine which blocks are able to be decoded based on whats already been decoded
    
    possible = [[e,[i for i in to_int(blocks[e]) if i in (set(to_int(blocks[e])) & set(decoded_block_nums))],[i for i in to_int(blocks[e]) if not(i in decoded_block_nums)][0]] for e in range(number_of_drops) if len([i for i in to_int(blocks[e]) if not(i in decoded_block_nums)]) == 1 and not list(set(to_int(blocks[e])) - set(decoded_block_nums))[0] in decoded_block_nums and not(e in bad_droplets)]

    for e in possible:
        drop = records[e[0]].seq
        binary = decode(drop)
        for pair in e[1]:
            binary = xor(binary, decoded[pair])
        decoded[e[2]] = binary
        if '\x00' in decode_luby_drop(binary)or not(contains_word(decode_luby_drop(binary))):
            print(e[2])
            print('bad',e)
            print(decode_luby_drop(binary))
            print('-------')
            bad_droplets += [e[0]]


    #Clean up any mis-decoded droplets
    deletes = []
    for k in decoded.keys():       
        if ('\x00' in decode_luby_drop(decoded[k]) and not('technology'in decode_luby_drop(decoded[k]))) or not(contains_word(decode_luby_drop(decoded[k]))):
            deletes += [k]
    print(deletes)
    for d in deletes:
        del decoded[d]

    print(f"*{len(decoded)}*")


x = list(decoded.keys())
x.sort()
print([i for i in range(number_of_blocks) if not i in x])


# ## Assembling message

message = ""

for i in range(len(decoded)):
    chunk = decode_luby_drop(decoded[i])
    print(i,chunk)
    message += chunk
message = message.replace('\x00', '')
# Open the file in write mode ('w'), this will overwrite the file if it already exists
with open('decoded_message.txt', 'wt', encoding='utf-8') as file:
    # Write the string to the file
    file.write(message)





