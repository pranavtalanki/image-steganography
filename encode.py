
'''
Import Packages:
'''
from PIL import Image
import math

#----------------------------------------------------------------------------#
'''
Image Selection
'''
original_image_file = "images/VIT.png"

input_image = Image.open(original_image_file)

input_image_rgb=input_image.convert("RGB")
width, height = input_image.size
print("width=",width,"height=",height)
pixel_map = input_image.load()

#----------------------------------------------------------------------------#

'''
Functions:

    Function to select the pixels in a spiral manner. Pixel selection Starts from the middle.
'''
def spiral(N):
    hw,hh = int(width/2),int(height/2)
    x,y = hw,hh   
    dx, dy = 0, -5

    for d in range(N):
        if abs(hw-x) == abs(hh-y) and [dx,dy] != [5,0] or x>hw and hh-y == abs(hw-abs(5-x)):  
            dx, dy = -dy, dx            # corner, change direction
            #print('\t\t',dx,dy)
        yield x, y
        
        x, y = x+dx, y+dy
        


def co_prime(x,y):
    while y!=0:
        x,y = y,x%y
    if(x == 1):
        return True
    return False

def check_p(i):
    if(i%2 == 1):
        return True
    return False

def DectoBin(i):
    binary_v = bin(i).replace("0b","")
    temp_bin = binary_v[::-1]
    while len(temp_bin) < 8:
        temp_bin += '0'
    binary_v = temp_bin[::-1]
    return binary_v
    #return bin(i).replace("0b","")

def BintoDec(i):
    return int(i,2)
    
#-----------------------------------------------------------------------------#

'''
Step-1: Receive Message and encrypted it and get the binary representation
'''


f = open("demo1.txt","r")
msg = f.read()
print(msg)



p = 11#int(input("Enter p:"))
q = 17#int(input("Enter q:"))
if(check_p(p) and check_p(q)):
    n = p*q
    phi_n = (p-1)*(q-1)

    #co_p = []
    e = 0
    for i in range(2,phi_n):
        if(co_prime(i,phi_n)):
            e = i
            break
            #co_p.append(i)
    
    
    #print("Co_p val:",co_p)
    #e = co_p[2] 
    temp = 1
    d = 0
    for temp in range(1,10):
        temp2 = 1+temp*phi_n
        if temp2%e == 0:
            d = int(temp2/e)
            break;
    print("\np:",p,"q:",q,"n:",n,"phi:",phi_n,"e:",e,"d:",d)
    #msg = "This is sample"
    msg_ascii = [ord(i) for i in msg]#msg_ascii = [ord(i) for i in msg]
    print("Msg Ascii:",msg_ascii)
    encoded_msg = []
    for i in msg_ascii:
        encoded_msg.append(i**e % n)
    print("\nEncoded_msg:",encoded_msg)
    encrypted_msg = ''.join([chr(i) for i in encoded_msg])
    print("\nEncrypted Msg : ",encrypted_msg)
    encoded_msg_bin = [DectoBin(i) for i in encoded_msg]
    print("\nEncoded msg in bin:",encoded_msg_bin)
    encoded_msg_bin_str = "".join(encoded_msg_bin)

    l=len(encoded_msg_bin_str)
    le=l/3
    le=math.ceil(le)
else:
    print('ISSUE!')
#----------------------------------------------------------------------------#
'''
Step-2: Get the pixel values from Image:
'''
index=0
#print('Spiral 3x3:')
for a,b in spiral(le):
    #print ("pixel co-ordinates =",a,b)
    pixel_value=input_image_rgb.getpixel((a,b))
    #print("rgb values of pixel = ",pixel_value)
    
    
    r=int(DectoBin(pixel_value[0])[:7]+encoded_msg_bin_str[index],2)
    #print("r=",r)
    #print(r,pixel_value[1],pixel_value[2])
    pixel_map[a,b]=(r,pixel_value[1],pixel_value[2])
    input_image_rgb=input_image.convert("RGB")
    #print("after encoding ",index,"bit rgb has been changed to",input_image_rgb.getpixel((a,b)))
    index+=1
    #print("index = ",index)
    if index>=l:
        #print("breaking after r")
        break

    
    g=int(DectoBin(pixel_value[1])[:7]+encoded_msg_bin_str[index],2)
    #print("g=",g)
    #print(r,g,pixel_value[2]) 
    pixel_map[a,b]=(r,g,pixel_value[2])
    input_image_rgb=input_image.convert("RGB")
    #print("after encoding ",index,"bit rgb has been changed to",input_image_rgb.getpixel((a,b)))
    index+=1
    #print("index = ",index)
    if index>=l:
        #print("breaking after g")
        break

    
    b1=int(DectoBin(pixel_value[2])[:7]+encoded_msg_bin_str[index],2)
    #print("b=",b1)
    #print(r,g,b)
    pixel_map[a,b]=(r,g,b1)
    input_image_rgb=input_image.convert("RGB")
    #print("after encoding ",index,"bit rgb has been changed to",input_image_rgb.getpixel((a,b)))
    index+=1
    #print("index = ",index)
    if index>=l:
        #print("breaking after b")
        break





input_image.save("output.png", format="png")
input_image.show()
output_image=Image.open("output.png")
output_image_rgb=output_image.convert("RGB")


print('--------------------------------------------------------------------')

msg1=""
for a,b in spiral(le):
    #print ("pixel co-ordinates =",a,b)
    pixel_value=output_image_rgb.getpixel((a,b))
    #print(pixel_value)
    for i in pixel_value:
        msg1=msg1+str(DectoBin(i)[7])



m = len(msg1)%8
msg2 = msg1[:(len(msg1) - (m))]



msg_length = 8
msg2_array = [msg2[i:i+msg_length] for i in range(0,len(msg2),msg_length)]

print(msg2_array)




decode_msg = [BintoDec(i) for i in msg2_array]
print("\ndecoded msg from bin to dec:",decode_msg,type(decode_msg[1]))
final_Ascii_msg = []
    
for i in decode_msg:
    final_Ascii_msg.append(i**d % n)
    
print("\nDecoded msg after RSA:",final_Ascii_msg)
    
    
final_msg = ''.join([chr(i) for i in final_Ascii_msg])
print("\n")
    
print(final_msg)
