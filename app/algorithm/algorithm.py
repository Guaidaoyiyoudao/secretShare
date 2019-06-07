from PIL import Image
from app.algorithm.shamir import *

#点值抽象
def GetvalueOfpoint(coordinate, im):
	if im.getpixel(coordinate) == 255:
		return 1
	else:
		return 0
		
#2*2矩阵转化
def GetmatrixBlock(imageUrl):
	im = Image.open(imageUrl).convert('1')
	c, d = im.size
	blockSet = []
	for x in range(0,int(c/2)):
		x = 2*x
		for y in range(0,int(d/2)):
			y = 2*y
			valueOfblock = 0
			valueOfblock = (8*GetvalueOfpoint((x,y),im)+4*GetvalueOfpoint((x+1,y),im)
							+2*GetvalueOfpoint((x,y+1),im)+GetvalueOfpoint((x+1,y+1),im))
			blockSet.append(valueOfblock)
	return blockSet
	
#秘密图像还原
def DematrixBlock(blockSet, length, width):
	set_length = len(blockSet)
	newIm= Image.new('1', (length, width))
	count = 0
	for x in range(0,int(length/2)):
		x = 2*x
		for y in range(0,int(width/2)):
			y = 2*y
			value_str = '{:04b}'.format(blockSet[count])
			a = int(value_str[0])
			b = int(value_str[1])
			c = int(value_str[2])
			d = int(value_str[3])
			newIm.putpixel((x,y), a)
			newIm.putpixel((x+1,y), b)
			newIm.putpixel((x,y+1), c)
			newIm.putpixel((x+1,y+1), d)
			count = count+1
	return newIm


def LSB(imageUrl_carrier,secret_list,subNum):
	im_carrier = Image.open(imageUrl_carrier)
	pic_length = len(secret_list)
	c, d = im_carrier.size
	# print(pic_length)
	#最低位隐写
	count = 0
	for x in range(0,c):
		for y in range(0,int(d/2)):
			y = y*2
			pix = im_carrier.getpixel((x,y))
			pix = pix - pix%16 + int(secret_list[count][subNum][0])
			im_carrier.putpixel((x,y),pix)
			pix = im_carrier.getpixel((x,y+1))
			pix = pix - pix%16 + int(secret_list[count][subNum][1])
			im_carrier.putpixel((x,y+1),pix)
			count = count+1
			if count == pic_length:
				break
		else:
			continue
		break			
	# carrier_newurl = "/Users/zhangyuhang/Desktop/Sys/carrier_new.png"
	# im_carrier.save(carrier_newurl)
	return im_carrier


#获取载体图像隐藏信息
def deLSB(im_carrier, pic_length):
	length, wide = im_carrier.size
	secretSet = []
	count = 0
	for x in range(0,length):
		for y in range(0,int(wide/2)):
			y = y*2
			pix = im_carrier.getpixel((x,y))
			secret_x = pix%16
			pix = im_carrier.getpixel((x,y+1))
			secret_y = pix%16 
			secretSet.append((secret_x,secret_y))
			count = count+1
			if count == pic_length/4:
				break
		else:
			continue
		break
	# print(len(secretSet))	
	return secretSet




def Getsubimage(secret_ImageUrl, n, k,im_carrierUrlSet):
	blockset = GetmatrixBlock(secret_ImageUrl)
	secret_list = []
	image_set = []
	# print(blockset)
	# print(len(blockset))
	for x in range(len(blockset)):
		tmp = Shamir(n, k, blockset[x])
		list_xy = tmp.GetPloy()
		secret_list.append(list_xy)
	count = 0
	for url in im_carrierUrlSet:
		im = LSB(url, secret_list, count)
		count = count+1
		image_set.append(im)
	return image_set                                              




def Getsecretimage(setOfsubImageUrl,secret_leng,secret_wide):
	secret_set = []
	secret_length = secret_leng*secret_wide
	# print(secret_length)
	n = len(setOfsubImageUrl)
	for url in setOfsubImageUrl:
		im = Image.open(url)
		secret_set.append(deLSB(im, secret_length))
	# print(secret_set)
	# print(len(secret_set[0]))
	desecret = []
	count = 0
	# print(len(secret_set[0]))
	for i in range(len(secret_set[0])):
		# print(count)
		count = count+1
		tmp = []
		for j in range(n):
			tmp.append(secret_set[j][i])
		# print("***************************************")
		# print(tmp)
		secret =  dePloy(17, tmp)
		desecret.append(secret)
	newIm= Image.new('1', (secret_length, secret_wide))
	im_secret = DematrixBlock(desecret, secret_leng, secret_wide)
	return im_secret

			

if __name__ == '__main__': 
	



	uris = ['../image/45baa9dac85cecfaf9f4b1d7527ab6e40.bmp','../image/45baa9dac85cecfaf9f4b1d7527ab6e41.bmp',
	'../image/45baa9dac85cecfaf9f4b1d7527ab6e42.bmp']


	res = Getsecretimage(uris, 256, 256)
	res.show()

		