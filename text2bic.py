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
    
    if (row_length * col_length) % 8 != 0:
        raise ValueError('The BIC total size must be divisible by 8.')
    
    if isinstance(string_or_file, TextIOWrapper):
        string_or_file = string_or_file.read()
    elif isfile(string_or_file):
        with open(string_or_file, 'r', encoding='utf-8') as file:
            string_or_file = file.read()
    
    bits = _string2bits(string_or_file)
    
    # * Creating a array for each image
    images_arrays = np.array_split(bits, ceil(bits.size / (row_length * col_length)))

    images = list()
    for img_array in images_arrays:
        complement = np.zeros(row_length * col_length - img_array.size, dtype=np.uint8)

        full_array = np.concatenate((img_array, complement), dtype=np.uint8)
        full_array = full_array.reshape(row_length, col_length)
        
        image = Image.fromarray(full_array, mode='L')
        images.append(image)
    
    return images if len(images) != 1 else images[0]

    
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
        splited_text.append(_binary2utf8(binary))
    
    return ''.join(splited_text)
    
    
def _string2bits(string: str):
    '''Create a flat np.ndarray with each bit separated'''
    # TODO: Convert the character in more than one byte (If needed) to use utf-8 
    binary_full = ''.join(format(ord(x), '08b') for x in string)

    bits = np.array(list(binary_full), dtype=np.uint)
    bits *= 255
    return bits


def _binary2utf8(binary: str):
    '''Translate a binary string into text with encoding utf-8'''
    binary = binary.replace(' ', '')
    
    byte_string = bytearray()
    for i in range(0, len(binary), 8):
        byte = int(binary[i:i+8], 2)
        byte_string.append(byte)
    return byte_string.decode('utf-8')
    


if __name__ == '__main__':
    test = string2bic(string_or_file='Hello, world!')
    test.show()
    print(bic2string(test))
    
