import PIL
import cv2
import numpy as np
from PIL import Image
import skimage.io
import skimage.transform
import skimage.color
import skimage
import sys

image=cv2.imread("C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\go\\0000100_02616_d_0000012.jpg")
#cv2.imshow("123",image)
#cv2.waitKey(0)

common_size=512
h=960
w=540
scale=common_size/w
resize_h=int(h*scale)
resize_w=common_size


#1056, 608.

#print(image.shape)

scale=608/540
print(w*scale>1024)
scale=1024/960 # scales based on the smallest difference. retinanet, efficientdet old makes everything 512,512.

image = cv2.resize(image, (int(round((w*scale))),(int(round(h*scale)))),interpolation=cv2.INTER_LINEAR)
rows, cols, cns = image.shape
#print(rows,cols)
pad_w = 32 - rows%32
pad_h = 32 - cols%32


new_image = np.zeros((rows + pad_w, cols + pad_h, cns),dtype=np.uint8)
print(new_image.shape)


new_image[:rows, :cols] = image
img=Image.fromarray(new_image,"RGB")
img.show()



##efficientdet-512.

# image = cv2.resize(image, (resize_w, resize_h), interpolation=cv2.INTER_LINEAR)
# new_image=np.zeros((common_size,common_size,3),dtype=np.uint8)
# new_image[0:resize_h, 0:resize_w] = image
# img=Image.fromarray(new_image,"RGB")
# print(img.size)
# img.show()


#resized all to 512,512