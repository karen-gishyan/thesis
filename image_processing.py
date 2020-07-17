import os
import imageio
import imgaug as ia
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug import augmenters as iaa 
from collections import defaultdict
ia.seed(1)
import numpy as np
from skimage import io as sk_io


# #path="C:\\Users\\Կարեն\\Desktop\\0000084_02139_d_0000007.jpg"
# image = imageio.imread(path)
# image = ia.imresize_single_image(image, (540, 960))

# ia.imshow(bbs.draw_on_image(image, size=3))

# image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
# #ia.imshow(bbs_aug.draw_on_image(image_aug, size=2))


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