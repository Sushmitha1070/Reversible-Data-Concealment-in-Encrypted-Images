

def encrypt_image(image_path):

    from PIL import Image
    import numpy as np
    import os
    from cryptography.fernet import Fernet
    import numpy as np
    import random


    if not os.path.exists("send"):
        os.makedirs("send")
    if not os.path.exists("out"):
        os.makedirs("out")
    
    image = Image.open(image_path).convert("L")

    pixel_values = list(image.getdata())

    width = image.width
    height = image.height

    pixel_array = [pixel_values[i:i+image.width] for i in range(0, len(pixel_values), image.width)]
    output_file = r"send/pixel_values.txt"
    with open(output_file, "w") as file:
        for row in pixel_array:
            file.write(' '.join(map(str, row)) + '\n')

    print(f"Pixel values saved to {output_file}")

    # Load pixel values from the text file
    with open("send/pixel_values.txt", "r") as file:
        lines = file.readlines()
        pixel_values = [[int(value) for value in line.strip().split()] for line in lines]

    # Convert pixel values to 2x2 matrices
    block_size = 2
    blocks = []
    block_number = 1
    for i in range(0, len(pixel_values), block_size):
        for j in range(0, len(pixel_values[0]), block_size):
            block = np.array(pixel_values[i:i+block_size])[:, j:j+block_size]
            if block.shape == (block_size, block_size):
                blocks.append((block, block_number))
                block_number += 1

    # Save the 2x2 matrices to a text file
    output_file = "send/blocks.txt"
    with open(output_file, "w") as file:
        for block, number in blocks:
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write(f"Block Number: {number}\n\n")

    print(f"2x2 matrices with block numbers saved to {output_file}")

    # Generate a key for AES encryption
    def generate_aes_key():
        return Fernet.generate_key()

    # Encrypt a block using AES
    def encrypt_block(block, key):
        cipher = Fernet(key)
        encrypted_block = cipher.encrypt(block.tobytes())
        return encrypted_block

    # Function to shuffle the blocks using a key
    def shuffle_blocks(blocks, key):
        np.random.seed(int.from_bytes(key, "big") % (2**32 - 1))
        shuffled_blocks = blocks.copy()
        np.random.shuffle(shuffled_blocks)
        return shuffled_blocks

    # Load the 2x2 matrices from the text file
    blocks = []
    with open("send/blocks.txt", "r") as file:
        lines = file.readlines()
        block = []
        temp_block = []
        block_number = None
        _temp = 0
        for line in lines:
            if line.strip() == "":
                if block:
                    blocks.append((block, block_number))
                    block = []
                    block_number = None
            elif line.startswith("Block Number:"):
                block_number = int(line.split(":")[1])
            else:
                try:
                    a, b  = [int(value) for value in line.strip().split()]
                    block.append([a, b])
                except ValueError:
                    pass

        if block:
            blocks.append((block, block_number))
            

    # Generate AES key
    aes_key = generate_aes_key()
    print("Key for block shuffling: ", aes_key)
    # Shuffle the blocks using the AES key
    shuffled_blocks = shuffle_blocks(blocks, aes_key)

    # Save the shuffled blocks to a text file
    shuffled_blocks_file = "send/shuffled_blocks_aes.txt"
    with open(shuffled_blocks_file, "w") as file:
        for block, block_number in shuffled_blocks:
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write(f"Block Number: {block_number}\n\n")
    print(f"Shuffled blocks saved to {shuffled_blocks_file}")

    blocks = []
    with open("send/shuffled_blocks_aes.txt", "r") as file:
        lines = file.readlines()
        block = []
        temp_block = []
        block_number = None
        for line in lines:
            if line.strip() == "":
                if block:
                    blocks.append((block, block_number))
                    block = []
                    block_number = None
            elif line.startswith("Block Number:"):
                block_number = int(line.split(":")[1])
            else:
                try:
                    block.append([int(value) for value in line.strip().split()] )
                except ValueError:
                    pass

        if block:
            blocks.append((block, block_number))  
    aes_key_2 = generate_aes_key()
    print("Key for within block shuffling: ", aes_key_2)

    new_blocks = []
    for i in blocks:
        temp = [i[0][0][0], i[0][0][1], i[0][1][0], i[0][1][1]]
        temp = shuffle_blocks(temp, aes_key_2)
        # print(temp, temp_)
        new_tup = ([[temp[0], temp[1]], [temp[2], temp[3]]], i[1])
        new_blocks.append(new_tup)

    shuffled_blocks_file = "send/shuffled_blocks_aes_after_block_shuffling.txt"
    with open(shuffled_blocks_file, "w") as file:
        for block, block_number in new_blocks:
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write(f"Block Number: {block_number}\n\n")

    print(f"Permutated blocks saved to {shuffled_blocks_file}")


    image = np.zeros((height, width))

    ind = 0
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            image[i][j] = new_blocks[ind][0][0][0]
            image[i][j+1] = new_blocks[ind][0][0][1]
            image[i+1][j] = new_blocks[ind][0][1][0]
            image[i+1][j+1] = new_blocks[ind][0][1][1]
            ind += 1
        
    with open("send/encrypted_pixels.txt", "w") as f:
        for i in image:
            for j in i:
                f.write(str(int(j)) + " ")
            f.write("\n")

    im = Image.fromarray(np.uint8(np.array(image)))
    im.save("encrypted_image.png")

    with open("out/keys.txt", "w") as f:
        f.write(aes_key.decode()+"\n")
        f.write(aes_key_2.decode()+"\n")
        