# text2bic
 A simple program that converts text into a ``BIC (Binary Image Code)``.

 A BIC is an image composed by black and white pixels (Zeros and Ones) that represents a binary code. Take a look at the example above (That shows a BIC
 image of "Hello World!" in english, portuguese, spanish, russian and greek):
 
![hello_world](https://github.com/VictorioMaculan/text2bic/assets/123396267/852fbcdf-e7ee-4b48-9a06-950682ef9237)

 The ``text2bic`` library uses the [UTF-8 encoding](https://pt.wikipedia.org/wiki/UTF-8), and that's why we can use it with characteres from latin, russian and greek (And bassicaly, with every single character from the UTF-8 Table). To decode the image just download it and use the ``bic2string`` function:

 ```py
 import text2bic as t2b

 decoded_str = t2b.bic2string('Path to the image here')
 print(decoded_str)
 ```
 For more information about the functions (``string2bic`` and ``bic2string``) read their docstrings.
 
