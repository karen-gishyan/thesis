import numpy as np
import os
from PIL import Image
import torch
import torchvision
import torch
import shutil
import sys
torch.manual_seed(1)


class TrainTestValid:
	
	"""
	The images and annotations should be either stored in a single directory or in seperate directories, 
	where in both cases each image should match its corresponding annotation.
	The annotations can be yolo pytorch, yolo darknet, and pascal voc formats.
	The class allows to divide the images and annotations into train,test, valide sets, and besides the given annotations, save in coco
	json as well.
	In the directory image and annotation should follow each other.
	"""

	def __init__(self,train_size,test_size,valid_size=None):
		"""
		Splits based on numpy random.
		"""
		self.train_size=train_size
		self.test_size=test_size
		self.valid_size=valid_size


	def make_dirs(self,main_path):

		#go one level back and create these repo names.

		train=os.path.join(os.path.split(main_path)[0],"train")
		test= os.path.join(os.path.split(main_path)[0],"test")

		if not os.path.exists(train):
			os.makedirs(train)

		if not os.path.exists(test):
			os.makedirs(test)

		if self.valid_size is not None: 
			
			valid = os.path.join(os.path.split(main_path)[0],"valid")
		
			if not os.path.exists(valid): os.makedirs(valid)

			return train,test, valid
		else:

			return train,test,None 


	def split(self,path):
		
		"""
		instance method, meant to be called from train_test_split and methods.
		"""

		train,test,valid =self.make_dirs(path)

		if self.valid_size is None:

			dirr=train if np.random.uniform()<self.train_size else test
		
		if self.valid_size is not None:

			if np.random.uniform()<=self.train_size: 
				dirr=train		

			elif self.train_size < np.random.uniform() <=self.train_size+self.test_size: 
				dirr=test # test always comes low, check.
			
			else:
				dirr=valid		

		return dirr	


	def train_test_split_single_path(self,single_path,format=".txt"):

		self.single_path=single_path
	
		path_to_iterate=os.listdir(self.single_path)
		
		#in a single file checks each file and the corresponding file.
		for file_index in range(0,len(path_to_iterate)-1,2):
	
			if path_to_iterate[file_index].strip(".jpg")== path_to_iterate[file_index+1].strip(format) \
			or path_to_iterate[file_index].strip(format)== path_to_iterate[file_index+1].strip(".jpg"):

				dirr=self.split(self.single_path)				

				if path_to_iterate[file_index].endswith(".jpg"):
						
					img_branch=path_to_iterate[file_index]
					ann_branch=path_to_iterate[file_index+1]
				
				else:
					img_branch=path_to_iterate[file_index+1]
					ann_branch=path_to_iterate[file_index]
						
					
				img = Image.open(os.path.join(self.single_path,img_branch))		
				path= os.path.join(dirr,img_branch)
				print(path)
				img=img.save(path)

				with open(os.path.join(self.single_path,ann_branch),"rt") as lines:
					with open(os.path.join(dirr,ann_branch),"wt") as stream: 
						for line in lines:
							stream.write(line)						


	def train_test_split_different_paths(self,img_path,annot_path):

		self.img_path=img_path
		self.annot_path=annot_path

		iterable= zip(os.listdir(self.img_path),os.listdir(self.annot_path))

		for image, annot in iterable:

			if os.path.splitext(image)[1] in [".jpg",".png"] and os.path.splitext(annot)[1] in [".txt",".xml"]\
			 and os.path.splitext(image)[0]== os.path.splitext(annot)[0]: 

				dirr=self.split(self.img_path) #can be annot_path as well.

				img = Image.open(os.path.join(self.img_path,image))		
				path= os.path.join(dirr,image)
				img=img.save(path)

				with open(os.path.join(self.annot_path,annot),"rt") as lines:
					with open(os.path.join(dirr,annot),"wt") as stream: 
						
						for line in lines:
							stream.write(line)	




def pytorch_split(path_to_images,path_to_annotations,train_prop=0.7,test_prop=0.1,valid_prop=0.2,annot_type="txt"):

	
	"""
	images and annotations are stored separately.
	annot_type either txt or xml.
	"""

	n_images=sum([1 for image in os.listdir(path_to_images)])
	train_size=int(n_images*train_prop)
	test_size=int(n_images*test_prop)
	valid_size=int(n_images*valid_prop)

	diff=n_images-(train_size+test_size+valid_size)
	train_size+=diff
	

	print("The number of images is {}.".format(n_images))

	pytorch_path=os.path.dirname(path_to_images)
	root_dir=os.path.split(path_to_annotations)[0] #equivalent to the one above.
	#print(root_dir)
	train_annotations= os.path.join(root_dir,"train_annotations")
	test_annotations=  os.path.join(root_dir,"test_annotations")
	valid_annotations= os.path.join(root_dir,"valid_annotations")

	train_images=os.path.join(root_dir,"train_images")
	test_images=os.path.join(root_dir,"test_images")
	valid_images=os.path.join(root_dir,"valid_images")

	
	dir_list=[train_annotations,test_annotations,valid_annotations,train_images,test_images,valid_images]

	for dirr in dir_list:
		if not os.path.exists(dirr):
			os.makedirs(dirr)

	full_dataset = torchvision.datasets.ImageFolder(root=pytorch_path)
	train_dataset, test_dataset,valid_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size,valid_size])

		
	for index, image in enumerate(os.listdir(path_to_images)):
		
		assert(os.path.splitext(image)[1] in [".png",".jpg"])

		full_img_path=os.path.join(path_to_images,image)
		#print(full_img_path)
		
		if annot_type=="txt":
			full_ann_path=os.path.join(path_to_annotations,os.path.splitext(image)[0])+".txt"
		
		elif annot_type=="xml":
			full_ann_path=os.path.join(path_to_annotations,os.path.splitext(image)[0])+".xml"	
		
		else:
			raise TypeError ("Incorrect extension type.")


		if index in train_dataset.indices:
			
			shutil.copy(full_ann_path,train_annotations) 
			shutil.copy(full_img_path,train_images)
			
		elif index in test_dataset.indices:

			shutil.copy(full_ann_path,test_annotations)
			shutil.copy(full_img_path,test_images)
		
		else:
			shutil.copy(full_ann_path,valid_annotations)
			shutil.copy(full_img_path,valid_images)

	n_train_images=len(os.listdir(train_images))
	n_test_images=len(os.listdir(test_images))
	n_val_images=len(os.listdir(valid_images))

	print("There are {} train, {} test, and {} valid_images.".format(n_train_images,n_test_images,n_val_images)) 
				
im_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\own images\\img\\images"
annot_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\own images\\annotations_correct"

pytorch_split(im_path,annot_path,train_prop=0.5,test_prop=0.05,valid_prop=0.45,annot_type="txt")




