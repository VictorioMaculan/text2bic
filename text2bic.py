from PIL import Image
import numpy as np


def string2bic(string: str, precise_size=False, 
               row_length=100, col_length=100):
    '''
    Converts a string into a BIC (Binary Image Code).
    '''
    binary = _string2binary(string)    
    complement = np.zeros(row_length * col_length - binary.size, dtype=np.uint32)
    
    full_array = np.concatenate((binary, complement), dtype=np.uint8)
    full_array = full_array.reshape(row_length, col_length)
    
    return Image.fromarray(full_array, mode='L')

    
def bic2string(image: Image.Image):
    '''
    Converts a BIC (Binary Image Code) image into a string.
    '''
    
    # ! Just testing this part, it'll be changed afterwards
    binary = np.asarray(image).flatten()
    binary_str = ''.join([str(x).replace('255', '1') for x in binary])
    return _binary2string(binary_str)
    
    
def _string2binary(string: str):
    binary_full = ''.join(format(ord(x), '08b') for x in string)

    # TODO: Upgrade this part
    final_binary = list()
    for digit in binary_full:
        if digit == ' ':
            continue
        final_binary.append(0) if digit == '0' else final_binary.append(255)
            
    return np.array(final_binary, dtype=np.uint8)


def _binary2string(binary: str | list): # TODO
    binary = binary.replace(' ', '')
    decimal_full = list()
    
    for i in range(0, len(binary), 8):
        set = int(binary[i:i + 8], 2)
        decimal_full.append(set)
            
    return ''.join([chr(x) for x in decimal_full])


if __name__ == '__main__':
    a = string2bic('Hello, World!')
    b = print(bic2string(a))