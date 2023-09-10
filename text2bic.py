import numpy as np
from PIL import Image
from os.path import isfile
from math import ceil

import typing as tp
from io import TextIOWrapper


def string2bic(string_or_file: str | TextIOWrapper, 
               row_length=104, 
               col_length=104
               ) -> Image.Image | list[Image.Image]:
    '''
    Converts a string into one or more BIC (Binary Image Code).
    
    Params:
        string_or_file: A string, a path-like (Pointing at a text file), or a text file wrapper.
        row_length: The width of the BIC in pixels.
        col_lenght: The height of the BIC in pixels.
    Return:
        PIL.Image.Image: An Pillow image instance.
        list[PIL.Image.Image]: A list of Pillow images instances.
    '''
    
    if row_length * col_length % 8 != 0:
        raise ValueError('The BIC total size must be divisible by 8.')
    
    if isinstance(string_or_file, TextIOWrapper):
        string_or_file = string_or_file.read()
    elif isfile(string_or_file):
        with open(string_or_file, 'r', encoding='utf-8') as file:
            string_or_file = file.read()
    

    binaries = _string2binary(string_or_file)
    binaries = np.hsplit(binaries, ceil(binaries.size / (row_length * col_length))) # !

    output_bin = list()
    for binary in binaries:
        complement = np.zeros(row_length * col_length - binary.size, dtype=np.uint8)

        full_array = np.concatenate((binary, complement), dtype=np.uint8)
        full_array = full_array.reshape(row_length, col_length)
        
        image = Image.fromarray(full_array, mode='L')
        output_bin.append(image)
    
    return output_bin if len(output_bin) != 1 else output_bin[0]

    
def bic2string(image: Image.Image | str | tp.Sequence[Image.Image]):
    '''
    Converts one or more BIC (Binary Image Code) into a string.
    
    Params:
        image: A Pillow image instance, a path pointing at a image file
        or a sequence of Pillow images instances.
    Return:
        str: A string with the content of the BIC's.
    '''
    # It's getting converted into a tuple so it can be
    # iterated afterwards.
    if isinstance(image, str):
        image = (Image.open(image),)
    elif isinstance(image, Image.Image):
        image = (image,)
        
    splited_text = list()
    for img in image:
        binary = np.asarray(img).flatten()
        binary //= 255
        binary = ''.join([str(x) for x in binary])
        splited_text.append(_binary2string(binary))
    
    return ''.join(splited_text)
    
    
def _string2binary(string: str):
    binary_full = ''.join(format(ord(x), '08b') for x in string)

    final_binary = np.array(list(binary_full), dtype=np.uint)
    final_binary *= 255
    return final_binary


def _binary2string(binary: str):
    binary = binary.replace(' ', '')
    
    # Getting sets of 8 binary digits (That's equivalent to one decimal number)
    # and translating them to the decimal base to be used in the chr() function.
    decimal = list()
    for i in range(0, len(binary), 8):
        set = int(binary[i:i + 8], 2)
        decimal.append(set)

    return ''.join([chr(x) for x in decimal])


if __name__ == '__main__':
    test = string2bic(string_or_file='Hello world!')
    test.show()
    print(bic2string(test))