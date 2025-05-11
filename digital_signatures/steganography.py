import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class Steganography:
    @staticmethod
    def encrypt_data(data, key=None):
        """Encrypt data using AES"""
        if key is None:
            # Generate a random 32 byte key if none provided
            key = get_random_bytes(32)
        
        # Create cipher object and perform encryption
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        
        # Combine IV and ciphertext
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        encrypted_data = f"{iv}:{ct}"
        
        return encrypted_data, key

    @staticmethod
    def decrypt_data(encrypted_data, key):
        """Decrypt data using AES"""
        try:
            # Split IV and ciphertext
            iv, ct = encrypted_data.split(':')
            iv = base64.b64decode(iv)
            ct = base64.b64decode(ct)
            
            # Create cipher object and perform decryption
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except (ValueError, KeyError) as e:
            raise ValueError("Invalid decryption") from e

    @staticmethod
    def embed(image, data, encryption_key=None):
        """Embed encrypted data in image using LSB steganography"""
        # Encrypt the data first
        encrypted_data, key = Steganography.encrypt_data(data, encryption_key)
        
        # Convert image to numpy array
        img_array = np.array(image)
        
        # Convert encrypted data to binary string
        binary = ''.join([format(ord(i), '08b') for i in encrypted_data])
        binary += '1111111111111110'  # EOF marker
        
        data_len = len(binary)
        
        # Check if image can hold the data
        if data_len > img_array.shape[0] * img_array.shape[1] * 3:
            raise ValueError("Image too small to hold this data")

        # Embed data
        data_index = 0
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                for k in range(3):  # RGB channels
                    if data_index < data_len:
                        img_array[i, j, k] = (img_array[i, j, k] & ~1) | int(binary[data_index])
                        data_index += 1

        return Image.fromarray(img_array), key

    @staticmethod
    def extract(image, decryption_key):
        """Extract and decrypt data from image using LSB steganography"""
        # Convert image to numpy array
        img_array = np.array(image)
        
        # Extract binary data
        binary = ''
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                for k in range(3):  # RGB channels
                    binary += str(img_array[i, j, k] & 1)

        # Find EOF marker
        eof_marker = '1111111111111110'
        eof_index = binary.find(eof_marker)
        if eof_index == -1:
            raise ValueError("No embedded data found")
        
        binary = binary[:eof_index]
        
        # Convert binary to encrypted text
        encrypted_data = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            encrypted_data += chr(int(byte, 2))

        # Decrypt the extracted data
        try:
            decrypted_data = Steganography.decrypt_data(encrypted_data, decryption_key)
            return decrypted_data
        except ValueError:
            raise ValueError("Invalid encryption key or corrupted data")