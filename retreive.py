




def retreive_data(image_path,aes_key,aes_key_2,key):
    
    
    
    #!/usr/bin/env python
    import zlib
    import os
    from PIL import Image
    import numpy as np
    if not os.path.exists("ret"):
        os.makedirs("ret")
    El=26

   
    image = Image.open(image_path).convert("L")

    pixel_values = list(image.getdata())

    width = image.width
    height = image.height

    pixel_array = [pixel_values[i:i+image.width] for i in range(0, len(pixel_values), image.width)]


    output_file = r"ret/pixel_values.txt"
    with open(output_file, "w") as file:
        for row in pixel_array:
            file.write(' '.join(map(str, row)) + '\n')

    print(f"Pixel values saved to {output_file}")


    import numpy as np

    # Load pixel values from the text file
    with open("ret/pixel_values.txt", "r") as file:
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
    output_file = "ret/blocks.txt"
    with open(output_file, "w") as file:
        for block, number in blocks:
            for row in block:
                file.write(" ".join(str(pixel) for pixel in row) + "\n")
            file.write(f"Block Number: {number}\n\n")

    print(f"2x2 matrices with block numbers saved to {output_file}")


    complete = ""
    ind = 0
    i = 0
    while ind < len(blocks):
        dmin = blocks[ind][0][0][0] - blocks[ind][0][0][1]
        dmax = blocks[ind][0][1][1] - blocks[ind][0][1][0]
        if(dmax <= (2* El) + 1 and dmax >= El+1):
            complete += '1'
        elif(dmax >=0 and dmax <= El):
            complete += '0'
        if(i< 16 and dmin <=0 and dmin >= -El):
            complete += '0'
        elif(i < 16 and dmin <= -El-1 and dmin >= (-2*El) -1):
            complete += '1'
        ind = ind + 1



    def decompress_coding(binary_string):
        compressed_data = bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
        dcdata = zlib.decompress(compressed_data)
        # dcdata = ''.join(format(byte, '08b') for byte in dcdata)
        dcdata = dcdata.decode()
        with open('ret/bin_matrix.txt', "w") as f:
            f.write(dcdata)
        lis = dcdata.strip().split('\n')
        matrix = []
        for i in lis:
            temp = []
            for j in i.strip().split(' '):
                temp.append(j)
            if temp != [] :
                matrix.append(temp)
        return matrix



    # Function to shuffle the blocks using a key
    def shuffle_blocks(shuffled_list, key):
        np.random.seed(int.from_bytes(key, "big") % (2**32 - 1))

        shuf_order = np.arange(len(shuffled_list))
        np.random.shuffle(shuf_order)
        
        unshuffled_list = [0] * len(shuffled_list)
        for i, j in enumerate(shuf_order):
            unshuffled_list[j] = shuffled_list[i]
        return unshuffled_list

    lm = int(complete[:16], 2)
    complete = complete[16:]

    bin_map = complete[:lm]
    complete = complete[lm:]

    sec_length = int(complete[:32], 2)
    complete = complete[32:]

    sec_image_dim = int(complete[:10], 2)
    complete = complete[10:]

    sec_data = complete[:sec_length]

    bin_matrix = decompress_coding(bin_map)

    new_blocks = []
    front = 0
    back = -1

    for i in bin_matrix:
        for j in i:
            if int(j) == 0:
                new_blocks.append(blocks[front])
                front += 1
            else:
                new_blocks.append(blocks[back])
                back -= 1


  
    aes_key = aes_key.encode()


    aes_key_2 = aes_key_2.encode()

    if(aes_key != '' and aes_key_2 != ''):
        # Shuffle the blocks using the AES key
        shuffled_blocks = shuffle_blocks(new_blocks, aes_key)

        # Save the shuffled blocks to a text file
        shuffled_blocks_file = "ret/shuffled_blocks_aes.txt"
        with open(shuffled_blocks_file, "w") as file:
            for block, block_number in shuffled_blocks:
                for row in block:
                    file.write(" ".join(str(pixel) for pixel in row) + "\n")
                file.write(f"Block Number: {block_number}\n\n")

        print(f"Shuffled blocks saved to {shuffled_blocks_file}")

        blocks = []
        with open("ret/shuffled_blocks_aes.txt", "r") as file:
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

        new_blocks = []
        for i in blocks:
            temp = [i[0][0][0], i[0][0][1], i[0][1][0], i[0][1][1]]
            temp = shuffle_blocks(temp, aes_key_2)
            # print(temp, temp_)
            new_tup = ([[temp[0], temp[1]], [temp[2], temp[3]]], i[1])
            new_blocks.append(new_tup)

        shuffled_blocks_file = "ret/shuffled_blocks_aes_after_block_shuffling.txt"
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

        im = Image.fromarray(np.uint8(np.array(image)))
        im.save("constructed_image.png")
    

        
        print("Retreived image is saved to reconstructed_image.py")


    key =key.encode()

    if key != '':
        data = shuffle_blocks(list(sec_data), key)
        data = "".join(str(i) for i in data)
        image = []

        ind = 0
        for i in range(sec_image_dim):
            temp = []
            for j in range(sec_image_dim):
                f = data[ind:ind+8]
                if f!= '':
                    temp.append(int(data[ind:ind+8], 2))
                else:
                    temp.append(0)
                ind += 8
            image.append(temp)

        im = Image.fromarray(np.uint8(np.array(image)))
        im.save("ret_secret_image.png")



    #accuracy




def accuracy(original_image_path, decrypted_image_path):
    # Open the original and decrypted images using Pillow
    from PIL import Image
    import numpy as np
    try:
        with Image.open(original_image_path) as img_orig, Image.open(decrypted_image_path) as img_dec:
            # Convert images to grayscale
            img_orig_gray = img_orig.convert('L')
            img_dec_gray = img_dec.convert('L')
            # Convert images to NumPy arrays
            original_image = np.array(img_orig_gray)
            decrypted_image = np.array(img_dec_gray)
    except IOError:
        print("Unable to open image files.")
        return None

    # Ensure images have the same dimensions
    if original_image.shape != decrypted_image.shape:
        raise ValueError("Images must have the same dimensions")

    # Calculate the RMSE
    mse = np.mean((original_image - decrypted_image) ** 2)
    rmse = np.sqrt(mse)

    return rmse




    #print("RMSE between original and decrypted images:", rmse)
    #print("Percentage RMSE:", percentage_rmse,"%")





def calentropy(encrypted_image_path):
    from PIL import Image
    import numpy as np
    import math
    # Open the encrypted image
    try:
        with Image.open(encrypted_image_path) as img:
            # Convert the image to grayscale
            img_gray = img.convert('L')
            # Convert the image to a NumPy array
            encrypted_image = np.array(img_gray)
    except IOError:
        print("Unable to open image file:", encrypted_image_path)
        return None

    # Calculate the histogram of pixel intensity values
    histogram, _ = np.histogram(encrypted_image.flatten(), bins=256, range=(0, 256))

    # Calculate the probability distribution
    probability_distribution = histogram / float(np.sum(histogram))

    # Calculate entropy
    entropy = -np.sum([p * math.log2(p + 1e-10) for p in probability_distribution])
    return entropy
