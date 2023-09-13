import numpy as np
from PIL import Image
from os.path import isfile

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
        raise ValueError('The BIC total size must be divisible by eight')
    
    if isinstance(string_or_file, TextIOWrapper):
        string_or_file = string_or_file.read()
    elif isfile(string_or_file):
        with open(string_or_file, 'r', encoding='utf-8') as file:
            string_or_file = file.read()
    
    bits = _string2bits(string_or_file)
    
    # * Creating each image
    images = list()
    for bytes in range(0, len(bits), (row_length * col_length)):
        img_array = bits[bytes:bytes + (row_length * col_length)]
        
        complement = np.zeros(row_length * col_length - img_array.size, dtype=np.uint8)

        full_array = np.concatenate((img_array, complement), dtype=np.uint8)
        full_array = full_array.reshape(row_length, col_length)
        
        image = Image.fromarray(full_array, mode='L')
        images.append(image)
    
    return images if len(images) != 1 else images[0]

    
def bic2string(image: Image.Image | str | tp.Sequence[Image.Image]
               ) -> str:
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
        binary //= 255 # * Converting the white pixels (255) to 1
        binary = ''.join([str(x) for x in binary])
        splited_text.append(_binary2utf8(binary))
    
    return ''.join(splited_text)
    
    
def _string2bits(string: str):
    '''Create a flat np.ndarray with each bit separated'''
    
    bytes_ = bytes(string, 'utf-8')
    bytes_ = [int(b, 16) for b in bytes_.hex(' ').split()]
    
    binary_full = ''.join([format(h, '08b') for h in bytes_])
    
    bits = np.array(list(binary_full), dtype=np.uint)
    bits *= 255
    return bits


def _binary2utf8(binary: str):
    '''Translate a binary string into text with encoding utf-8'''
    binary = binary.replace(' ', '')

    bytes_ = bytearray()
    for i in range(0, len(binary), 8):
        
        byte = int(binary[i:i + 8], 2)
        
        if byte != 0: # * Removing the U+0000 characters after the text
            bytes_.append(byte)
    
    return bytes_.decode('utf-8', errors='replace')


if __name__ == '__main__':
    test = string2bic(string_or_file='scr/utf_testing_file.txt')
    print(len(bic2string(test)))
    
