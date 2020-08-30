#https://eecs.oregonstate.edu/ecampus-video/CS161/template/chapter_5/nested.html#:~:text=Using%20break%20in%20a%20nested,all%20of%20the%20looping%20stops.
#break in  nested loop behaves differently, the outer loop keeps on executing.


import os
import sys
import xml.etree.ElementTree as ET
from tqdm import tqdm
import numpy as np
from PIL import Image
from lxml import etree
import cv2


	

def grid_augment(annot_path,imgs_path):


	new_xml_dir_path=os.path.join(os.path.dirname(annot_path),"grid_augmented_xmls")
	new_img_dir_path=os.path.join(os.path.dirname(annot_path),"grid_augmented_images")

	if not os.path.exists(new_img_dir_path):
		os.makedirs(new_img_dir_path)

	if not os.path.exists(new_xml_dir_path):
		os.makedirs(new_xml_dir_path)

	img_generator=(image for image in os.listdir(imgs_path))
	img_generator_rev=(image for image in reversed(os.listdir(imgs_path)))

	sum_images=len(os.listdir(imgs_path))
	# This exhausts the generator.
	#gen_sum=sum(1 for i in img_generator)
	

	
	for index, _ in enumerate(range(sum_images//3)):
		
		img_list=[]
		annot_names=[]

		for _ in range(3):


			img=next(img_generator)
			img_full_path=os.path.join(imgs_path,img)
			img_list.append(Image.open(img_full_path))

			annot=os.path.splitext(img)[0]+".xml"
			annot_names.append(annot)
			
		min_height = min(im.height for im in img_list)

		#resize the weights based on the mininum height.
		im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=Image.BICUBIC)
						  for im in img_list]

		total_width = sum(im.width for im in im_list_resize)
		
		new_image=Image.new('RGB', (total_width, min_height))
		
		np_image = np.array(new_image) # for depth

		new_image_name="grid_augment"+str(index+1)+".jpg"
		
		new_img_path=os.path.join(new_img_dir_path,new_image_name)

		

		write_xml=XML_Writer(new_image_name,new_img_path,new_image.width,new_image.height,np_image.shape[2])
		r=write_xml.create_tag()

		x_position=0

		for i, (img,annot) in enumerate(zip(im_list_resize,annot_names)): # the first one need to be the

			new_image.paste(img,(x_position,0))
			x_position+=img.width
			
		 
			full_path=os.path.join(annot_path,annot)
			tree=ET.parse(full_path)
			root=tree.getroot()


			for object in root.iter("object"): 
					
				voc_list=[]

				name=str(object.find("name").text)		
				box= object.find("bndbox")

				xmin=int(box.find("xmin").text)
				ymin=int(box.find("ymin").text)
				xmax=int(box.find("xmax").text)
				ymax=int(box.find("ymax").text)
				
						
		
				shift=x_position-img.width
				write_xml.add_object(r,xmin+shift,ymin,xmax+shift,ymax,name)
	
				
		new_image.resize((new_image.width,new_image.height)).save(new_img_path)			
		write_xml.save_xml(r,new_xml_dir_path,new_image_name)



class XML_Writer:


	def __init__(self,file_name,img_path,img_width,img_height,img_depth):
		
		self.file_name=file_name
		self.img_path=img_path
		self.img_width=img_width
		self.img_height=img_height
		self.img_depth=img_depth

	def create_tag(self):

		self.root = etree.Element('annotation')

		self.folder=etree.SubElement(self.root,'folder').text='annotations'
		self.filename=etree.SubElement(self.root,"filename").text="{}".format(self.file_name)
		self.path=etree.SubElement(self.root,"path").text="{}".format(self.img_path)
		self.source=etree.SubElement(self.root,"source")		
		self.database=etree.SubElement(self.source,"database").text='Visdrone Dataset'
		self.size=etree.SubElement(self.root,"size")
		self.width=etree.SubElement(self.size,"width").text="{}".format(self.img_width)
		self.height=etree.SubElement(self.size,"height").text="{}".format(self.img_height)
		self.depth=etree.SubElement(self.size,"depth").text="{}".format(self.img_depth)
		self.segmented=etree.SubElement(self.root,"segmented").text="0"

		return self.root


	def add_object(self,root,xmin,ymin,xmax,ymax,name):
		
		

		self.obj = etree.Element('object')
		self.name=etree.SubElement(self.obj,'name').text="{}".format(name)
		self.pose=etree.SubElement(self.obj,'pose').text="Unspecified"
		self.truncated=etree.SubElement(self.obj,'truncated').text="0"
		self.diff=etree.SubElement(self.obj,'difficult').text="0"
		self.bnd=etree.SubElement(self.obj,'bndbox')
		self.xmin=etree.SubElement(self.bnd,"xmin").text="{}".format(xmin)
		self.ymin=etree.SubElement(self.bnd,"ymin").text="{}".format(ymin)
		self.xmax=etree.SubElement(self.bnd,"xmax").text="{}".format(xmax)
		self.ymax=etree.SubElement(self.bnd,"ymax").text="{}".format(ymax)

		
		root.append(self.obj)
		


	def save_xml(self,root,new_xml_dir_path,img_name):

		s = etree.tostring(root, pretty_print=True)

		name=os.path.splitext(img_name)[0]+".xml"
		save_path=os.path.join(new_xml_dir_path,name)

		with open(save_path,"wb") as file:
			file.write(s)




annot_path="C:/Users/gishy/Dropbox/My PC (LAPTOP-SQRN8N46)/Desktop/sample_annotations_xml - Copy"
images_path="C:/Users/gishy/Dropbox/My PC (LAPTOP-SQRN8N46)/Desktop/sample_images"

grid_augment(annot_path,images_path)

# for element in root.iter():
# 	print(element.tag,element.text)







