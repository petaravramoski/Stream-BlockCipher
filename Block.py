import time
import secrets
import random
import string

from sbox import S_box

#INPUT STRING
x = "This is the secret messagethat is going to be encryprted with a block cipher: SGKLSNDFSFLKSFNDS"

#debug check size 
#print(len(x))

print("text that is going to be encrypted: ", x)
#input block size
blockSize = 8 #Size of block
num_rounds = 3 #number of rounds that we will encrypt/decrypt 
asciiNum = 97

# Order of chars in block (index order) for first permutation
permutationOrderOne = [3, 5, 1, 2, 6, 0, 4, 7]

#Where each encrypted block is stored 
encryptedBlock = []

#Where the key for each block will be stored 
keyForEachBlock = []

#Where substituted blocks will be stored
subBlocks = []


#Function to pad the last block if needed, eg. if block[-1] is 6 chars long then pad it so its 8 
def pad_last_block(block, block_size, padding_char='a'):
    if len(block) < block_size:
        padded_block = block + (padding_char * (block_size - len(block)))
    else:
        padded_block = block
    return padded_block

#Update blockExtract to use the padded last block
#using Pad function to pad last block if its not size 8
blockExtract = [pad_last_block(x[i:i+blockSize], blockSize) for i in range(0, len(x), blockSize)]

#This function generates a random key for 
def generate_random_key(length):
    # Define the set of characters from which the key will be composed
    characters = string.ascii_letters.lower()
    
    # Generate random key
    key = ''.join(secrets.choice(characters) for _ in range(length))
    
    return key

def generate_key_for_each_block(blockExtract):
    keyForEachBlock = []  # Initialize the list to store keys for each block
    for block in blockExtract: 
        #Debugging print statement
        #print("Block length:", len(block))
        
        #Generate a random key of the appropriate length for the block
        key = generate_random_key(len(block))
        
        #Store the key for later use during decryption
        keyForEachBlock.append(key)
    return keyForEachBlock


#Where the keys are generated for each block and stored in keyForEachBlock
keyForEachBlock = generate_key_for_each_block(blockExtract)

print("Key For Each Block: ", keyForEachBlock)


#This function takes care of the permutation part of the encryption process
def initialPermutation(bExtract, fPermutation):

    result = [] #Where the permuted blocks are stored in the function 

    for block in bExtract: 
        temp = "" #temporary empty string var to make sure block is a string and then to append to array
        for index in fPermutation[:len(block)]:  #Adjust permutation order based on block length
            temp += block[index] #
        result.append(temp)
    
    return result

initialPermutationResult = initialPermutation(blockExtract, permutationOrderOne)

print("Initial Permutation", initialPermutationResult)



#This function here takes care of the Substitution part of the encryption process
def substitution(input_block, S_box):
    result = [] #Where the substituted blocks will be stored and returned 
    for block in input_block:
        #Perform substitution for each character in the block
        substituted_block = ''.join(S_box[char] for char in block)
        result.append(substituted_block)
    return result

#Where the substitution chars are stored and passed down 
subBlocks = substitution(initialPermutationResult, S_box)

print("Sub blocks:", subBlocks)


#how this one works: 
#It iterates and takes the first value from initial perm which is M 
#it then iterates again this time over perOrderOne and gets first values which is 3 
#it then puts M in index position 3 and so on... 
def inversePermutation(initialPerm, perOrderOne):
    result = []
    for bChar in initialPerm: 
        # Pad block with spaces if needed to ensure it's long enough
        temp = [''] * len(bChar)
        for i, perm_value in enumerate(perOrderOne):
            temp[perm_value] = bChar[i]
        result.append(''.join(temp))
    return result

inversePermutationResult = inversePermutation(initialPermutationResult, permutationOrderOne)


#Here we reverse the sbox so then we can use it for decryption. 
# instead of a -> z it will be z -> a etc.. 
inverse_S_box = {value: key for key, value in S_box.items()}

def inverse_substitution(input_block, inverse_S_box):
    result = []
    for block in input_block:
        # Perform inverse substitution for each character in the block
        substituted_block = ''
        for char in block:
            if char in inverse_S_box:
                substituted_block += inverse_S_box[char]
            else:
                substituted_block += char
        result.append(substituted_block)
    return result

# Example usage:
plaintext_after_inverse_substitution = inverse_substitution(subBlocks, inverse_S_box)


def encrypt_with_key_mixing(blocks, permutation_order, keys, num_rounds):
    encrypted_blocks = blocks[:]  #Making a copy of the original blocks
    
    for _ in range(num_rounds):
        round_encrypted_blocks = []  # Temporary list to store the blocks after each round
        
        for i, block in enumerate(encrypted_blocks):
            # Apply initial permutation
            permuted_block = ''.join(block[index] for index in permutation_order) 
            
            # Perform substitution using the S-box
            substituted_block = ''.join(S_box[char] for char in permuted_block)
            
            # Mix the block with the corresponding key using modular addition
            mixed_block = ''
            for char, key_char in zip(substituted_block, keys[i]):
                if char.islower():
                    x_char = ord(char) - ord('a')
                    key_char = ord(key_char) - ord('a')
                elif char.isupper():
                    x_char = ord(char) - ord('A')
                    key_char = ord(key_char) - ord('A')
                elif char.isdigit():
                    x_char = ord(char) - ord('0')
                    key_char = ord(key_char) - ord('0')
                else:
                    # Handle other characters (e.g., digits, punctuation, whitespace)
                    mixed_block += char
                    continue

                if char.isalpha():
                    encrypted_char = (x_char + key_char) % 26
                else:
                    encrypted_char = (x_char + key_char) % 10

                mixed_block += (chr(encrypted_char + ord('a')) if char.islower() else 
                                chr(encrypted_char + ord('A')) if char.isupper() else 
                                chr(encrypted_char + ord('0')))
            
            # Append the mixed block to the list of encrypted blocks for this round
            round_encrypted_blocks.append(mixed_block)
        
        # Update the encrypted_blocks list for the next round
        encrypted_blocks = round_encrypted_blocks
    
    return encrypted_blocks

# Perform encryption with key mixing using keys stored in keyForEachBlock
encryptedBlock = encrypt_with_key_mixing(blockExtract, permutationOrderOne, keyForEachBlock, num_rounds)

# Print the encrypted blocks
print('Encrypted Blocks with Key Mixing:')
for block in encryptedBlock:
    print(block) 


def decrypt_with_key_mixing(encrypted_blocks, keys, inverse_S_box, permutation_order, num_rounds):
    decrypted_blocks = encrypted_blocks[:] #Making a copy of the encrypted blocks
    
    for _ in range(num_rounds):
        round_decrypted_blocks = []  # Temporary list to store the blocks after each round
        
        for i, block in enumerate(decrypted_blocks):
            # Decrypt the block with the corresponding key using bitwise XOR
            decrypted_block = ''
            for char, key_char in zip(block, keys[i]):
                if char.islower():
                    result = (ord(char) - ord(key_char)) % 26 + 97
                elif char.isupper():
                    result = (ord(char) - ord(key_char)) % 26 + 65
                elif char.isdigit():
                    result = (ord(char) - ord(key_char)) % 10 + 48
                else:
                    # Handle other characters (e.g., punctuation, whitespace)
                    result = ord(char)
                decrypted_block += chr(result)
            
            # Apply inverse substitution
            substituted_block = inverse_substitution([decrypted_block], inverse_S_box)[0]
            
            # Apply inverse permutation
            inv_permuted_block = inversePermutation([substituted_block], permutation_order)[0]
            
            # Append the block to the list of decrypted blocks for this round
            round_decrypted_blocks.append(inv_permuted_block)
        
        # Update the decrypted_blocks list for the next round
        decrypted_blocks = round_decrypted_blocks
    
    return decrypted_blocks

# Perform decryption with key mixing using keys stored in keyForEachBlock
decrypted_blocks = decrypt_with_key_mixing(encryptedBlock, keyForEachBlock, inverse_S_box, permutationOrderOne, num_rounds)

print('Decrypted Blocks with Key Mixing:', *[block for block in decrypted_blocks])





