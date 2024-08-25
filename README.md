# Image_Steganography using Python 
[https://www.geeksforgeeks.org/image-based-steganography-using-python/]
Using PIL library to access pixel information of given image.

# What is image steganography?
Steganography refers to the method of concealing binary data within an image. The hidden data is undetectable as the change is very subtle and difficult to notice.

# How is the data encoded?
Tldr; data is encoded by manipulating the LSB of the pixel values 
The data is encoded by converting each byte of data to be encoded into 8-bit binary code using its corresponding ASCII values. The pixels of the image in which the data is to be encoded is read from left to right in groups of three. Each pixel has 3 values (RGB) so a group of pixels has 9 values (8 of which contain data, 1 to indicate whether the message is over or not)
The value of the pixel is made odd to denote 1 and even to denote a 0.

# How is data decoded?
The image is read from left to right in groups of 3 pixels till the last value is odd. (Odd last pixel indicates the end of the message)

# How many pixels are required for n bytes of data?
For every 8 bits (1 byte) of data, 3 pixels are req to store those 8 bits, and 3 pixels for the continuation bit, making it 3 pixels per byte.
Pixels required=n×3
