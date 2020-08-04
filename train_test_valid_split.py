import numpy as np
import os
from PIL import Image



class TrainTestValid:
	
	"""
	The images and annotations should be either stored in a single directory or in seperate directories, 
	where in both cases each image should match its corresponding annotation.
	The annotations can be yolo pytorch, yolo darknet, and pascal voc formats.
	The class allows to divide the images and annotations into train,test, valide sets, and besides the given annotations, save in coco
	json as well.
	In the directory image and annotation should follow each other.
	"""

	def __init__(self,train_size,test_size,img_path,valid_size=None,annot_path=None):
		"""
		img_path assumes images and annotations are stored in a single directory.
		If different directories, pass the path to annot_path seperately.
		train_size default,test_size take fractions, like 0.7,0.3 etc.
		"""
		self.train_size=train_size
		self.test_size=test_size
		self.img_path=img_path
		self.annot_path=annot_path
		self.valid_size=valid_size

	def train_test_split(self,format=".txt"):


		if self.annot_path is None:

			#go one level back and create these repo names.
			train=os.path.join(os.path.split(self.img_path)[0],"train")
			test= os.path.join(os.path.split(self.img_path)[0],"test")

			if not os.path.exists(train):
				os.makedirs(train)

			if not os.path.exists(test):
				os.makedirs(test)

			if self.valid_size is not None: valid = os.path.join(os.path.split(self.img_path)[0],"valid")
			if self.valid_size is not None and not os.path.exists(valid): os.makedirs(valid)

			
			path_to_iterate=os.listdir(self.img_path)
			
			#in a single file checks each file and the corresponding file.
			for file_index in range(0,len(path_to_iterate)-1,2):

				
				if path_to_iterate[file_index].strip(".jpg")== path_to_iterate[file_index+1].strip(format) \
				or path_to_iterate[file_index].strip(format)== path_to_iterate[file_index+1].strip(".jpg"):
				
					
					if self.valid_size is None:

						dirr=train if np.random.uniform()<self.train_size else test
					
					if self.valid_size is not None:

						if np.random.uniform()<=self.train_size: 
							dirr=train		

						elif self.train_size < np.random.uniform() <=self.train_size+self.test_size: 
							dirr=test
						else:
							dirr=valid	

						print("This is",dirr)

					if path_to_iterate[file_index].endswith(".jpg"):
							
						img_branch=path_to_iterate[file_index]
						ann_branch=path_to_iterate[file_index+1]
					
					else:
						img_branch=path_to_iterate[file_index+1]
						ann_branch=path_to_iterate[file_index]
							
						
					img = Image.open(os.path.join(self.img_path,img_branch))		
					path= os.path.join(dirr,img_branch)
					print(path)
					img=img.save(path)

					with open(os.path.join(self.img_path,ann_branch),"rt") as lines:
						with open(os.path.join(dirr,ann_branch),"wt") as stream: # creates a new file and iteratively writes.
							for line in lines:
								stream.write(line)						
				else:
					continue




path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\sample\\practice\\Images and Annotations XML"
#path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\sample\\practice\\Images and Annotations YOLO"
#inst=TrainTestValid(0.7,0.2,path,valid_size=0.1).train_test_split(format=".xml")