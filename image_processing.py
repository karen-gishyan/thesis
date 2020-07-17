import os
import imageio
import imgaug as ia
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug import augmenters as iaa 
ia.seed(1)
from collections import defaultdict
import math
import numpy as np
from PIL import Image
from skimage import io as sk_io


#print(os.getcwd())

# # # this happens with a pascal voc format.
# # #path="C:\\Users\\Կարեն\\Desktop\\0000084_02139_d_0000007.jpg"
# # image = imageio.imread(path)
# # image = ia.imresize_single_image(image, (540, 960))
# print(image.shape)

# bbs = BoundingBoxesOnImage([
# 	BoundingBox(x1=258, x2=298, y1=326, y2=420),
# 	BoundingBox(x1=733, x2=771, y1=269, y2=342),
# 	BoundingBox(x1=475, x2=501, y1=213, y2=296)], shape=image.shape)

# ia.imshow(bbs.draw_on_image(image, size=3))

# seq = iaa.Sequential([
# 	iaa.GammaContrast(1.5),
# 	iaa.Affine(translate_percent={"x": 0.1}, scale=0.8),
# 	iaa.AdditiveGaussianNoise(scale=(10, 60)),
# 	iaa.Affine(rotate=(-30, 30))
# ])


# image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
# #ia.imshow(bbs_aug.draw_on_image(image_aug, size=2))

# print(bbs.bounding_boxes)

# for i in range(len(bbs.bounding_boxes)):
# 	before=bbs.bounding_boxes[i]
# 	after=bbs_aug.bounding_boxes[i]
# 	print("BB %d: (%.4f, %.4f, %.4f, %.4f) -> (%.4f, %.4f, %.4f, %.4f)" % (
# 		i,
# 		before.x1, before.y1, before.x2, before.y2,
# 		after.x1, after.y1, after.x2, after.y2)
# 	)


image = imageio.imread(os.path.join(os.getcwd(),"0000002_00448_d_0000015.jpg"))
def conversion():

	path=os.getcwd()
	file=open(os.path.join(path,'0000002_00448_d_0000015.txt'))


	bb_list=[]
	l=[]
	for line in file.readlines():	
		label=int(line.split()[0])
		new_line=line.split()[1:] # create a list, then remove the class label.
	
		xmin = max(float(new_line[0]) - float(new_line[2]) / 2, 0)
		xmax = min(float(new_line[0]) + float(new_line[2]) / 2, 1)
		ymin = max(float(new_line[1]) - float(new_line[3]) / 2, 0)
		ymax = min(float(new_line[1]) + float(new_line[3]) / 2, 1)

		xmin = float(960 * xmin)
		xmax = float(960 * xmax)
		ymin = float(540 * ymin)
		ymax = float(540 * ymax)
		
		
		bb=BoundingBox(x1=xmin, x2=xmax, y1=ymin, y2=ymax)
		bb_list.append(bb)

	bbs = BoundingBoxesOnImage(bb_list,shape=(540, 960, 3))
	#ia.imshow(bbs.draw_on_image(image, size=3))
	
	seq = iaa.Sequential([
		iaa.GammaContrast(1.5),
		iaa.AdditiveGaussianNoise(scale=(10, 60)),
		iaa.Affine(rotate=(-30, 30))])

	image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)

	for i in range(len(bbs.bounding_boxes)):
		
		after=bbs_aug.bounding_boxes[i]
		xcen = float((after.x1 + after.x2)) / 2 / 960
		ycen = float((after.y1 + after.y2)) / 2 / 540

		w = float((after.x2 - after.x1)) / 960
		h = float((after.y2 - after.y1)) / 540

		l1=[label,xcen, ycen, w, h] # label.

		l.append(l1)

	with open(os.path.join(os.getcwd(),"imp.txt"),"wt", encoding='ascii') as stream: 		
		np.savetxt(stream, np.array(l), fmt='%f')	

	file_path = os.path.join(os.getcwd(), "imp.png")
	print(file_path)
	sk_io.imsave(file_path, image_aug)
	ia.imshow(image_aug)
	
if __name__=="__main__":		
	conversion()