from PIL import Image
import numpy as np

class Steganography:
    @staticmethod
    def embed(image, data):
        # Convert image to numpy array
        img_array = np.array(image)
        
        # Convert data to binary
        binary = ''.join(format(ord(i), '08b') for i in data)
        
        # Embed data in least significant bits
        data_index = 0
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                for k in range(3):  # RGB channels
                    if data_index < len(binary):
                        img_array[i, j, k] = img_array[i, j, k] & ~1 | int(binary[data_index])
                        data_index += 1
        
        return Image.fromarray(img_array)

    @staticmethod
    def extract(image):
        # Extract hidden data from image
        img_array = np.array(image)
        binary = ''
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                for k in range(3):
                    binary += str(img_array[i, j, k] & 1)
        
        # Convert binary to text
        data = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            data += chr(int(byte, 2))
            if data.endswith('\0'):
                return data[:-1]
        
        return data