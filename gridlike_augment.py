#https://eecs.oregonstate.edu/ecampus-video/CS161/template/chapter_5/nested.html#:~:text=Using%20break%20in%20a%20nested,all%20of%20the%20looping%20stops.
#break in  nested loop behaves differently, the outer loop keeps on executing.


import os
import sys
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from lxml import etree
from visualize import visualize_bounding_box

	

def horizontal_grid_augment(annot_path,imgs_path,combine_img_number,desired_augment_number=None,min_width=False,decrease_width_size=1,im_save_path=None,xml_save_path=None):

	"""
	combine_img_number=number of images to combine horizontally.
	min_width=if True, all the images are resized to the mininum existing image width.Default-their original widths are adjusted with height.
	desired_augment_number-how many gridlike images to generate,cannot exceed the number of original images.
	decrease_width_size=how many times to decrease the width before saving.
	"""


	new_xml_dir_path= im_save_path if im_save_path!=None else os.path.join(os.path.dirname(annot_path),"grid_horizontal_xmls") 
	new_img_dir_path= xml_save_path if xml_save_path!=None else os.path.join(os.path.dirname(annot_path),"grid_horizontal_images")


	if not os.path.exists(new_img_dir_path):
		os.makedirs(new_img_dir_path)

	if not os.path.exists(new_xml_dir_path):
		os.makedirs(new_xml_dir_path)

	sum_images=len(os.listdir(imgs_path))
	half=sum_images//2
	quarter=sum_images//4

	#generators up to the number of dir images.
	img_generator=(image for image in os.listdir(imgs_path))
	img_generator_rev=(image for image in reversed(os.listdir(imgs_path)))
	img_generator_upper=(image for image in os.listdir(imgs_path)[half:])
	img_generator_lower=(image for image in os.listdir(imgs_path)[:half])
	img_generator_middle=(image for image in os.listdir(imgs_path)[quarter:quarter])
	img_generator_middle_rev=(image for image in reversed(os.listdir(imgs_path)[quarter:quarter]))

	# This exhausts the generator.
	#gen_sum=sum(1 for i in img_generator)
	new_images_list=[]
	new_annots_list=[]
	iter_num=sum_images//combine_img_number if desired_augment_number==None else desired_augment_number

	
	for index, _ in enumerate(range(iter_num)):
		
		img_list=[]
		annot_names=[]

		for _ in range(combine_img_number): # every iteration generetas a combined image and an annotation.

			try:
				img=next(img_generator) # if this generator is exhausted, takes images from the reversed generator.
			except Exception as e:
				pass
				try:
					img=next(img_generator_rev)
				except Exception as e:
					pass
					try:
						img=next(img_generator_upper)
					except Exception as e:
						pass
						try:
							img=next(img_generator_lower)
						except Exception as e:
							pass
							try:
								img=next(img_generator_middle)
							except Exception as e:
								pass
								
								try:
									img=next(img_generator_middle_rev)
								except Exception as e:
									print(e)
									sys.exit("Not enough images to unpack vertically, consider decreasing the desired_augment_number to less than {}.".format(desired_augment_number))

						
			img_full_path=os.path.join(imgs_path,img)
			img_list.append(Image.open(img_full_path))

			annot=os.path.splitext(img)[0]+".xml"
			annot_names.append(annot)
			
		min_height = min(im.height for im in img_list)
			
		
		if min_width:
			
			min_width=min(im.width for im in img_list)
			im_list_resize = [im.resize((min_width, min_height),resample=Image.BICUBIC)
						  for im in img_list]
						  
		else:
			im_list_resize = [im.resize((int(im.width * min_height /im.height),min_height),resample=Image.BICUBIC)
						  for im in img_list]
			

		size_diff=[i.size[0]/j.size[0] for i,j in zip(img_list,im_list_resize)] #both width and height are resized by the same amount.

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
				
				#resize bounding boxes of resize images before shifting.
				xmin=int(xmin//size_diff[i])
				xmax=int(xmax//size_diff[i])
				ymin=int(ymin//size_diff[i])
				ymax=int(ymax//size_diff[i])
					

				shift=x_position-img.width
				
				write_xml.add_object(r,xmin+shift,ymin,xmax+shift,ymax,name)
	
		
		new_image=new_image.resize((new_image.width//decrease_width_size,new_image.height))
		
		new_images_list.append(new_image)
		new_annots_list.append(r)		
				
		new_image.save(new_img_path)
		write_xml.save_xml(r,new_xml_dir_path,new_image_name)

	print("{} images horizontally combined and {} annotations have been transformed.".format(len(new_images_list),len(new_annots_list)))
	return new_img_dir_path,new_xml_dir_path




def vertical_grid_augment(annot_path,imgs_path,combine_img_number,desired_augment_number=None,min_height=False,decrease_height_size=1,im_save_path=None,xml_save_path=None):

	"""
	You either provide an imgs_path or a list of horizontal
	"""

	new_xml_dir_path= xml_save_path if im_save_path!=None else os.path.join(os.path.dirname(annot_path),"grid_vertical_xmls") 
	new_img_dir_path= im_save_path  if xml_save_path!=None else os.path.join(os.path.dirname(annot_path),"grid_vertical_images")


	if not os.path.exists(new_img_dir_path):
		os.makedirs(new_img_dir_path)

	if not os.path.exists(new_xml_dir_path):
		os.makedirs(new_xml_dir_path)

	
	sum_images=len(os.listdir(imgs_path))
	half=sum_images//2
	quarter=sum_images//4

	img_generator=(image for image in os.listdir(imgs_path))
	img_generator_rev=(image for image in reversed(os.listdir(imgs_path)))
	img_generator_upper=(image for image in os.listdir(imgs_path)[half:])
	
	img_generator_lower=(image for image in os.listdir(imgs_path)[:half])
	img_generator_middle=(image for image in os.listdir(imgs_path)[quarter:quarter])
	img_generator_middle_rev=(image for image in reversed(os.listdir(imgs_path)[quarter:quarter]))	

	new_images_list=[]
	new_annots_list=[]

	iter_num=sum_images//combine_img_number if desired_augment_number==None else desired_augment_number

	
	for index, _ in enumerate(range(iter_num)):
		
		img_list=[]
		annot_names=[]

		for _ in range(combine_img_number):

			try:

				img=next(img_generator) 
			except Exception as e:
				pass
				try:
					img=next(img_generator_rev)
				except Exception as e:
					pass
					try:
						img=next(img_generator_upper)
					except Exception as e:
						pass
						try:
							img=next(img_generator_lower)
						except Exception as e:
							pass
							try:
								img=next(img_generator_middle)
							except Exception as e:
								pass
								
								try:
									img=next(img_generator_middle_rev)
								except Exception as e:
									print(e)
									sys.exit("Not enough images to unpack vertically, consider decreasing the desired_augment_number to less than {}.".format(desired_augment_number))



			img_full_path=os.path.join(imgs_path,img)
			img_list.append(Image.open(img_full_path))

			annot=os.path.splitext(img)[0]+".xml"
			annot_names.append(annot)
			
		min_width = min(im.width for im in img_list)

		#resize the weights based on the mininum height.

		if min_height:
			
			min_height=min(im.height for im in img_list)
			im_list_resize = [im.resize((min_width, min_height),resample=Image.BICUBIC)
						  for im in img_list]
		
		else:	
			im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=Image.BICUBIC)
					  for im in img_list]



		size_diff=[i.size[0]/j.size[0] for i,j in zip(img_list,im_list_resize)]

		total_height = sum(im.height for im in im_list_resize)
		
		new_image=Image.new('RGB', (min_width, total_height))
		
		np_image = np.array(new_image) # for depth

		new_image_name="grid_augment"+str(index+1)+".jpg"
		
		new_img_path=os.path.join(new_img_dir_path,new_image_name)

		
		write_xml=XML_Writer(new_image_name,new_img_path,new_image.width,new_image.height,np_image.shape[2])
		r=write_xml.create_tag()

		y_position=0

		for i, (img,annot) in enumerate(zip(im_list_resize,annot_names)): # the first one need to be the

			new_image.paste(img,(0,y_position))
			y_position+=img.height
			
		 
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
				
				xmin=int(xmin//size_diff[i])
				xmax=int(xmax//size_diff[i])
				ymin=int(ymin//size_diff[i])
				ymax=int(ymax//size_diff[i])

					
				shift=y_position-img.height
				write_xml.add_object(r,xmin,ymin+shift,xmax,ymax+shift,name)
			
		
		new_image=new_image.resize((new_image.width,new_image.height//decrease_height_size))	
		new_images_list.append(new_image)
		new_annots_list.append(r)		
		
		
		new_image.save(new_img_path)

	
		write_xml.save_xml(r,new_xml_dir_path,new_image_name)

	print("{} images and {} annotations have been  vertically combined.".format(len(new_images_list),len(new_annots_list)))

	return new_img_dir_path,new_xml_dir_path



def mosaic_augment(annot_path,imgs_path,size=(3,4),
	mininum_width=False,mininum_height=False, dec_width=1,dec_height=1,
	total_images=None):

	new_xml_dir_path=os.path.join(os.path.dirname(annot_path),"grid_mosaic_xmls")
	new_img_dir_path=os.path.join(os.path.dirname(imgs_path),"grid_mosaic_images")

	if not os.path.exists(new_img_dir_path):
		os.makedirs(new_img_dir_path)

	if not os.path.exists(new_xml_dir_path):
		os.makedirs(new_xml_dir_path)



	horiz_im_dir_path,horiz_xml_dir_path=horizontal_grid_augment(annot_path,imgs_path,combine_img_number=size[0],
		desired_augment_number=200,min_width=mininum_width,decrease_width_size=dec_width)

	vertical_grid_augment(horiz_xml_dir_path,horiz_im_dir_path,combine_img_number=size[1],
		xml_save_path=new_xml_dir_path,im_save_path=new_img_dir_path,decrease_height_size=dec_height,desired_augment_number=100)




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


if __name__ == '__main__':

	#annot_path="C:/Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\trials\\train_annots_sample"
	#images_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\trials\\train_img_sample"

	#annot_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Not Augmented\\train_annotations_xml"
	#images_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Not Augmented\\train_images"
	
	mosaic_augment(annot_path,images_path,size=(3,4))

	annot_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Not Augmented\\grid_mosaic_xmls"
	images_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Not Augmented\\grid_mosaic_images"
	
	visualize_bounding_box(annot_path,images_path)




