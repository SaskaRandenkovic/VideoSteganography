import cv2, sys
import numpy as np

def stego_encode(msg,imgloc): 
	img = cv2.imread(imgloc)
	h = img.shape[0]
	w = img.shape[1]
	channels = img.shape[2]
	pixel = []
	
	for m in range(1,h):
	    for n in range(1,w):
	        if (img[m,n][0]!=0) & (img[m,n][1]!=0) & (img[m,n][2] != 0) :
	            pixel.append(img[m,n])

	i,j,k=0,0,0
	while (i<=len(msg)):
		if i==len(msg):
			b='11111111'
		else :
			no = ord(msg[i])
			b = '0'+"{0:b}".format(no)
		if (len(b)==7):
			b='0'+b
		elif (len(b)==6):
			b='00'+b
		x=0
		while (x<len(b)):
			if (b[x]=='0'):
				if (pixel[j][k]%2!=0):
					pixel[j][k]-=1
			elif (b[x]=='1'):
				if (pixel[j][k]%2==0):
					pixel[j][k]-=1
			if k==2:
				k=0
				j+=1
			else :
				k+=1
			x+=1
		j+=1
		k=0
		i+=1
	j=0
	for m in range(1,h):
		for n in range(1,w):
		    if (img[m,n][0]!=0) & (img[m,n][1]!=0) & (img[m,n][2] != 0) & (j<len(pixel)) :
		        img[m][n]=pixel[j]
		        j+=1
	enc_img = img
	cv2.imwrite(imgloc,img)


def stego_decode(imgloc):
	img = cv2.imread(imgloc)
	h = img.shape[0]
	w = img.shape[1]
	pixel = []
	
	for m in range(1,h):
	    for n in range(1,w):
	        if (img[m,n][0]!=0) & (img[m,n][1]!=0) & (img[m,n][2] != 0) :
	            pixel.append(img[m,n])
  
	j,x=0,0
	data,b='',''
	while (j<len(pixel)):
		k=0
		while(x!=8):
			if(pixel[j][k]%2==0):
				b=b+'0'
			else:
				b=b+'1'
			x+=1
			if(k==2):
				k=0
				j+=1
			else:
				k+=1

		j+=1
		no = int(b,2)
		if (b=='11111111') | (no>127) | (no<0) :
			break
		else :
			pass
		data+=str(chr(no))

		b=''
		x=0

	return data
