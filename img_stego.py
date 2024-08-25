from PIL import Image #for image processing

def bi_data(data): #function to return the binary rep of data to be encoded
    lst = [] 
    for i in data:
        lst.append(format(ord(i), '08b')) #'08b' makes sure the output is exactly 8 bits long
    return lst #list in which each element is the binary representation of each character in data

def modifypix(pix, data):
    datalist = bi_data(data)
    lendata = len(data)
    imgdata = iter(pix)
    for i in range (lendata): 
        #to extract 9 colour values (3 per pixel) from a group of 3 pixels at a time
        pix = [value for value in imgdata.__next__()[:3]+imgdata.__next__()[:3]+imgdata.__next__()[:3]]
        #pix_chunk = imgdata[i*3:(i+1)*3]??
        for j in range (0, 8): #for each bit in the binary string
            #1 = odd, 0 = even
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                #if the bit is 0, and if the pixel value is odd
                pix[j] -= 1 #make it even
            elif (datalist[i][j] == '1' and pix[j]%2 == 0):
                if (pix[j]!=0):
                    pix[j] -= 1 #make it odd
                else:
                    pix[j] += 1

    #eighth value of each group tells us whether the message is over or not
    #0 = not over, 1 = message over
    #check for the last index using negative indexing
    if (i == lendata - 1):#reaches the last element
        if (pix[-1] % 2 == 0): #if its even 
            if(pix[-1] != 0):
                pix[-1] -= 1 #make it odd to indicate that the message is over
            else:
                pix[-1] += 1 #if = 0 add 1 to make it odd
    
    else: #not the last element, continue reading (move on to next group)
        if (pix[-1] % 2 != 0): 
            pix[-1] -= 1 #make it even otherwise it will indicate end of the message
                
    pix = tuple(pix) #makes the data immutable
    #using yield does not terminate the function but pauses it
    #returns the RGB values of the grouped 3 pixels
    #yield returns one slice of data at a time rather than all at once
    yield pix[0:3]
    yield pix[3:6]
    yield pix[6:9]


#embeds the data into the image by modifying the pixel data
def encode_enc(new_img, data):
    #x.size() returns (width, height)
    w = new_img.size[0] #stores the width of the image
    (x, y) = (0, 0) #starting coordinates top left corner

    for pixel in modifypix(new_img.getdata(),data):
        new_img.putpixel((x, y), pixel) #replaces the pixel value at coords (x,y) with new piexl values
        if (x == w - 1): #end of the pic horizontally
            x = 0 #resets x 
            y += 1 #next row
        else:
            x += 1 #moves to next pixel in the same row

#prepares the image for embedding & to save final image
def encode():
    img = input("Enter image name with extension : ")
    image = Image.open(img, 'r') #read mode - default tho ig so not really needed here

    data = input ("Data to be encoded : ")
    # if (len(data) == 0):
    #     raise ValueError('Empty data.')

    new_img = image.copy() #duplicate

    # Check if the image is large enough to encode the data
    if len(data) * 3 > new_img.size[0] * new_img.size[1]:
        raise ValueError("Image is too small to encode the data.")
    
    encode_enc(new_img, data)

    new_img_name = input("Enter the name of the new encoded image(with extension) : ")
    new_img.save(new_img_name, str(new_img_name.split(".")[1].upper()))


def decode():
    img = input("Enter image name with extension : ")
    image = Image.open(img, 'r') 

    data = '' #temp string
    imgdata = iter(image.getdata())

    while(True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        binstr = '' #string of binary data
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def main():
    a = int(input(":: Steganography ::\n1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()
    elif (a == 2):
        print("Decoded Word :  " + decode())
    else:
        raise Exception("Invalid input.")
 
# Driver Code
if __name__ == '__main__' :
 
    # Calling main function
    main()
