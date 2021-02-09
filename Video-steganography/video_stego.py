import cv2,sys,glob
import numpy as np
from image_stego import stego_encode
from image_stego import stego_decode

def stego_encode_video():
    print("create a new txt file and enter your text there ",end="\n")
    loc = input("enter the file location : ")
    loc = loc.replace('\\','/')
    myfile = open(loc, "rt")
    msg = myfile.read()
    myfile.close()
    message = msg
    mm = message
    message = message.replace("\n","||||||||||||")

    imgloc = input('enter location of video in which you want to stego_encode msg : ')
    cap = cv2.VideoCapture(imgloc)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 100000
    

    while(cap.isOpened()):
        ret, frame = cap.read()
        if(ret):
            cv2.imwrite('data/frame{:d}.png'.format(count),frame) 
            count += 1
        else:
            break
    i=100000
    l1 = 0
    l2 = 250
    while(True):
        msg = message[l1:l2]
        imgoc = 'data/frame%d.png'%i
        stego_encode(msg,imgoc)
        if l2==len(message):
            break
        l1=l2
        l2=l2+250
        if l2>=len(message):
            l2=len(message)
        i+=1

    i+=1
    cap.release()
    cv2.destroyAllWindows()

    img_array = []
    for filename in glob.glob('data/*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter('stego_video.mkv',cv2.VideoWriter_fourcc(*'HFYU'), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    print ('output video is stego_video.mkv at the location of this prg')

def stego_decode_video():
    imgloc = input('enter location of video which you want to stego_decode : ')
    cap = cv2.VideoCapture(imgloc)
    count = 100000
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if(ret):
            cv2.imwrite('data/frame{:d}.png'.format(count),frame) 
            count += 1
        else:
            break

    i=100000
    msg,m = '',''
    while(i<count):
        imgoc = 'data/frame%d.png'%i
        m = stego_decode(imgoc)
        mr = m[::-1]
        if(mr==m):
            break
        msg = msg + m
        i+=1

    msg = msg.rstrip()
    msg = msg.replace("||||||||||||","\n")
    print ('Decoded message with stego_decoded is: ')
    print (msg)
    cap.release()
    cv2.destroyAllWindows() 

while (True):
    n = input ("enter 1: to stego_encode a message in video \n      2: to stego_decode a message from video \n      0: to EXIT : ")
    if n=='1' :
        stego_encode_video()
    elif n=='2' :
        stego_decode_video()
    elif n=='0' :
        sys.exit()
    else : 
        print ("please enter correct input OR enter 0 to EXIT")