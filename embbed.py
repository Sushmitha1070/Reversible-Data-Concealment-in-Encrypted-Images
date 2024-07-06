



def  embed_data(reconstructed_image_path,sec_image_path):
    El=26
    import zlib
    import os
    from PIL import Image
    import numpy as np
    from cryptography.fernet import Fernet
    from PIL import Image
    if not os.path.exists("embed"):
        os.makedirs("embed")
        
    # Load the encryped image
    
    reconstructed_image = Image.open(reconstructed_image_path)

    # Get the pixel values
    reconstructed_pixel_values = list(reconstructed_image.getdata())

    # Convert pixel values to array format
    reconstructed_pixel_array = [reconstructed_pixel_values[i:i+reconstructed_image.width] for i in range(0, len(reconstructed_pixel_values), reconstructed_image.width)]

    # Convert pixel values to 2x2 matrices
    block_size = 2
    reconstructed_blocks = []
    block_number = 1
    for i in range(0, len(reconstructed_pixel_array), block_size):
        for j in range(0, len(reconstructed_pixel_array[0]), block_size):
            block = np.array(reconstructed_pixel_array[i:i+block_size])[:, j:j+block_size]
            if block.shape == (block_size, block_size):
                reconstructed_blocks.append((block, block_number))
                block_number += 1

    # Save the extracted 2x2 blocks to a file
    output_file = "embed/reconstructed_blocks.txt"
    with open(output_file, "w") as file:
        for block, block_number in reconstructed_blocks:
            file.write(f"Block Number: {block_number}\n")
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write("\n")

    print(f"Extracted 2x2 blocks saved to {output_file}")




    import numpy as np

    # Load the reconstructed image
    reconstructed_image_path = "encrypted_image.png"
    reconstructed_image = Image.open(reconstructed_image_path)

    # Get the pixel values
    reconstructed_pixel_values = list(reconstructed_image.getdata())

    # Convert pixel values to array format
    reconstructed_pixel_array = [reconstructed_pixel_values[i:i+reconstructed_image.width] for i in range(0, len(reconstructed_pixel_values), reconstructed_image.width)]

    # Save pixel values to a text file
    output_file = "embed/reconstructed_pixel_values.txt"
    with open(output_file, "w") as file:
        for row in reconstructed_pixel_array:
            file.write(' '.join(map(str, row)) + '\n')

    print(f"Pixel values saved to {output_file}")

    # Load pixel values from the text file
    with open(output_file, "r") as file:
        lines = file.readlines()
        reconstructed_pixel_values = [[int(value) for value in line.strip().split()] for line in lines]

    # Sort pixel values within each 2x2 block in ascending order
    sorted_blocks = []
    for i in range(0, len(reconstructed_pixel_values), 2):
        for j in range(0, len(reconstructed_pixel_values[0]), 2):
            block = np.array(reconstructed_pixel_values[i:i+2])[:, j:j+2].reshape(4)
            sorted_block = np.sort(block).tolist()
            sorted_blocks.append(sorted_block)

    # Save the sorted blocks to a text file
    sorted_blocks_file = "embed/sorted_blocks.txt"
    with open(sorted_blocks_file, "w") as file:
        for sorted_block in sorted_blocks:
            file.write(" ".join(str(pixel) for pixel in sorted_block) + "\n")

    print(f"Sorted blocks saved to {sorted_blocks_file}")


    
    # sorting the elements
    
    import numpy as np
    from PIL import Image

    # Load the sorted blocks from the text file
    sorted_blocks = []
    with open("embed/sorted_blocks.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            sorted_block = [int(value) for value in line.strip().split()]
            sorted_blocks.append(sorted_block)

    # Reshape the sorted pixel values into 2x2 blocks
    blocks_2x2 = []
    block_number = 1
    for sorted_block in sorted_blocks:
        block = np.array(sorted_block).reshape(2, 2)
        blocks_2x2.append((block, block_number))
        block_number += 1

    # Save the 2x2 blocks with block numbers to a text file
    output_file = "embed/blocks_2x2.txt"
    with open(output_file, "w") as file:
        for block, block_number in blocks_2x2:
            file.write(f"Block Number: {block_number}\n")
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write("\n")

    print(f"2x2 blocks saved to {output_file}")



    #binary matrix

    m=reconstructed_image.width
    n=reconstructed_image.height

    height =n
    width = m

    newarray=np.zeros((n//2,m//2))
    index=0

    for i in range(n//2):
        for j in range(m//2):
            temp=blocks_2x2[index][0][1][1]
            tem=blocks_2x2[index][0][0][0]
            if temp+El>254 or tem-El<1:
                newarray[i][j]=1
            else:
                newarray[i][j]=0
            index = index + 1

    with open("out/binary_matrix.txt", "w") as f:
        for i in newarray:
            for j in i:
                f.write(str(int(j))+" ")
            f.write("\n")


    binary_matrix__ = newarray


    image = Image.open(sec_image_path).convert("L")

    pixel_values = list(image.getdata())

    width = image.width
    height = image.height

    print("Secret image dims: ", width, height)

    pixel_array = [pixel_values[i:i+image.width] for i in range(0, len(pixel_values), image.width)]

    bin_data = ''
    for i in pixel_array:
        for j in i:
            temp = f'{j:08b}'
            bin_data = bin_data + temp

    with open("embed/sec.txt", 'w') as f:
        f.write(" ".join(str(i) for i in pixel_values))
        f.write("\n-------------\n")
        f.write(" ".join(str(i) for i in pixel_array))


    # Generate a key for AES encryption
    def generate_aes_key():
        return Fernet.generate_key()

    # Function to shuffle the blocks using a key
    def shuffle_blocks(blocks, key):
        np.random.seed(int.from_bytes(key, "big") % (2**32 - 1))
        shuffled_blocks = blocks.copy()
        np.random.shuffle(shuffled_blocks)
        return shuffled_blocks


    # Generate AES key
    aes_key_image = generate_aes_key()

    print("Key for block shuffling: ", aes_key_image)

    # Shuffle the blocks using the AES key
    shuffled_blocks = shuffle_blocks(list(bin_data), aes_key_image)

    bin_data="".join(shuffled_blocks)

    with open("out/keys.txt", "a") as f:
        f.write("\n"+aes_key_image.decode())

    #data embedding
    

    def compress_coding(matrix):
        cdata = zlib.compress(matrix)
        binary_string = ''.join(format(byte, '08b') for byte in cdata)
        return binary_string

    with open("out/binary_matrix.txt", "rb") as file:
        matrix = file.read()

    # matrix = (matrix)
    compressed = compress_coding(bytes(matrix))
    # print(compressed)

    leng = len(compressed)

    print("Length of compressed Mc is: ", leng)
    print("Length of compressed Mc is: ", (leng/8))

    leng = f'{leng:016b}'
    leng2 = f'{len(bin_data):032b}'
    leng3 = f'{width:010b}'

    print("Length of secret data: ", len(bin_data))
    print("Binary leng: ", leng)
    print("Binary length sec: ", leng2)

    ol = len(bin_data)
    bin_data = leng+compressed+leng2+leng3+bin_data

    print("Total data being embbedded is: ", len(bin_data), ol)
    with open("embed/compressed.txt", "w") as f:
        f.write(leng+'\n')
        f.write(compressed)

    ind = 0
    di = 0
    for i in range(n//2):
        for j in range(m//2):
            if(newarray[i][j] == 0):
                dmin = blocks_2x2[ind][0][0][0] - blocks_2x2[ind][0][0][1]
                dmax = blocks_2x2[ind][0][1][1] - blocks_2x2[ind][0][1][0]
                if(dmax <= El):
                    if(di <len(bin_data) and bin_data[di] == '1'):
                        blocks_2x2[ind][0][1][1] = blocks_2x2[ind][0][1][1]+El+1
                    di += 1
                elif(dmax > El):
                    blocks_2x2[ind][0][1][1] = blocks_2x2[ind][0][1][1]+El+1
                else:
                    print(i, ind)
                if(dmin >= -El):
                    if(di <len(bin_data) and bin_data[di] == '1'):
                        blocks_2x2[ind][0][0][0] = blocks_2x2[ind][0][0][0]-El-1
                    di += 1
                elif(dmin < -El):
                    blocks_2x2[ind][0][0][0] = blocks_2x2[ind][0][0][0]-El-1
                else:
                    print(i, ind)

            ind = ind + 1

    if di < len(bin_data):
        print(f"Only embbedded {di} bits out of {len(bin_data)}")
    else:
        print(f"Complete data is embedded.{di}")

    with open("out/blocks_after_embbedding.txt", "w") as file:
        for block, block_number in blocks_2x2:
            file.write(f"Block Number: {block_number}\n")
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write("\n")

    print(f"Blocks after embedding are saved to blocks_after_embbedding.txt")



    width = m
    height = n

    image = np.zeros((height, width))

    ind = 0
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            image[i][j] = blocks_2x2[ind][0][0][0]
            image[i][j+1] = blocks_2x2[ind][0][0][1]
            image[i+1][j] = blocks_2x2[ind][0][1][0]
            image[i+1][j+1] = blocks_2x2[ind][0][1][1]
            ind += 1

    im = Image.fromarray(np.uint8(np.array(image)))
    im.save("out/embbedded_image.png")



    index=0
    nonover=[]
    overflow=[]
    final=[]

    for i in range(0,n//2):
        for j in range(0,m//2):
            if newarray[i][j]==0:
                nonover.append(blocks_2x2[index])
            else:
                overflow.append(blocks_2x2[index])   
            index=index+1

    final=nonover+overflow[::-1]

    print("nonoverflow :",len(nonover))
    output_file = "embed/rearrangeblocks_2x2.txt"
    with open(output_file, "w") as file:
        for block, block_number in final:
            file.write(f"Block Number: {block_number}\n")
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write("\n")



    image = np.zeros((height, width))

    ind = 0
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            image[i][j] = final[ind][0][0][0]
            image[i][j+1] = final[ind][0][0][1]
            image[i+1][j] = final[ind][0][1][0]
            image[i+1][j+1] = final[ind][0][1][1]
            ind += 1
        
    with open("embed/reaarranged_pixels.txt", "w") as f:
        for i in image:
            for j in i:
                f.write(str(int(j)) + " ")
            f.write("\n")

    im = Image.fromarray(np.uint8(np.array(image)))
    im.save("reembbedded_image.png")


    #secret image and data hiding key 
