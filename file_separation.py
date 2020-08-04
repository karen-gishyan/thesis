import os
from PIL import Image


def separate_file(path_to_dir,sep_file="xml",custom_save_path=None,remove_file=False):

	"""
	Can separate with mixed annotations as well, image in xml and image with txt.
	"""


	folder_name="Seperated images" if (sep_file=="jpg" or sep_file=="png") else ("Seperated txt" if sep_file=="txt" else "Seperated xml")  
	
	path=custom_save_path if custom_save_path != None else os.path.join(os.path.split(path_to_dir)[0],folder_name)
		

	if not os.path.exists(path):
		os.makedirs(path)

	for file in os.listdir(path_to_dir):

		
		if (sep_file=="txt" and file.endswith(".txt")) or (sep_file=="xml" and file.endswith(".xml")):	
			
			with open(os.path.join(path_to_dir,file),"rt") as lines:
				with open(os.path.join(path,file),"wt") as stream:
					
					for line in lines:
						stream.write(line)
			
			if remove_file:
				os.remove(os.path.join(path_to_dir,file))


		if sep_file in ["jpg","png"] and (file.endswith(".jpg") or file.endswith(".png")):
		
			img = Image.open(os.path.join(path_to_dir,file))
			img_path=os.path.join(path,file)
			img=img.save(img_path)
		
			if remove_file:
				os.remove(os.path.join(path_to_dir,file))

class Separate_Images_on_Quality:

	"""
	Separates images based on the height.Acts as a quality measure.
	"""

	def __init__(self,path):
		
		self.path=path
		self.main_path=os.path.split(self.path)[0]
		self.low_quality_image_folder_path=os.path.join(self.main_path,"Images smaller than 720p")
		self.high_quality_image_folder_path=os.path.join(self.main_path,"Images higherorequal 1080p")


	def make_dirs(self):

		if not os.path.exists(self.low_quality_image_folder_path): 
			os.makedirs(self.low_quality_image_folder_path)

		if not os.path.exists(self.high_quality_image_folder_path):
			os.makedirs(self.high_quality_image_folder_path)


	def separate(self):

		
		for image in os.listdir(self.path):

			img=Image.open(os.path.join(self.path,image))
			img_width,img_height=img.size

			#img.save(os.path.join(self.low_quality_image_folder_path,image)) if img_height<720 else 
			if img_height <=720:
				img.save(os.path.join(self.low_quality_image_folder_path,image))
			
			elif img_height>= 1080:
				img.save(os.path.join(self.high_quality_image_folder_path,image))


class Separate_Images_and_Annotations_on_Quality(Separate_Images_on_Quality):
	"""
	Image and annotation need to follow each other.
	The dir should contain only one annotation, txt or xml.
	"""
	
	#class variable to be accessed from instance method, needs to be in self again, cannot be directly accessed.
	annot_list=[".xml",".txt"]
	img_list=[".jpg",".png"] 


	def make_dirs(self):
		super().make_dirs() # needs to be inside a function. or self.make_dir(), again inside a function.

	def separate_image_and_annotation_same_dir(self):
		

		path_to_iterate=os.listdir(self.path)

		for file_index in range(0,len(path_to_iterate)-1,2):

			file_name=os.path.splitext(path_to_iterate[file_index])[0]
			file_type=os.path.splitext(path_to_iterate[file_index])[1]

			file_name_next=os.path.splitext(path_to_iterate[file_index+1])[0]			
			file_type_next=os.path.splitext(path_to_iterate[file_index+1])[1]
			
			if file_name==file_name_next and ((file_type in self.annot_list and file_type_next in self.img_list) or \
						  (file_type in self.img_list and file_type_next in self.annot_list)):

				#print("reached")
				#if path_to_iterate[file_index].endswith(".jpg"):
				if os.path.splitext(path_to_iterate[file_index])[1] in self.img_list:
							
					img_name=path_to_iterate[file_index]
					ann_name=path_to_iterate[file_index+1]
					
				else:
					img_name=path_to_iterate[file_index+1]
					ann_name=path_to_iterate[file_index]

				
				img = Image.open(os.path.join(self.path,img_name))
				img_width,img_height=img.size
				
				annot_file=open(os.path.join(self.path,ann_name),"rt")
				
				if img_height<=720:

					img.save(os.path.join(self.low_quality_image_folder_path,img_name)) 
					
					new_file=open(os.path.join(self.low_quality_image_folder_path,ann_name),"wt")
					
					for line in annot_file: #equivalent to with open.
					
						new_file.write(line)
					annot_file.close()

				elif img_height>=1080: 
					
					img.save(os.path.join(self.high_quality_image_folder_path,img_name))
					
					new_file=open(os.path.join(self.high_quality_image_folder_path,ann_name),"wt")
					
					for line in annot_file:
						
						new_file.write(line)
					annot_file.close()

	
	def separate__different_dirs(self,image_path,annot_path):

		self.img_path=image_path
		self.annot_path=annot_path

		iterable= zip(os.listdir(image_path),os.listdir(annot_path))

		for image, annot in iterable:


			if os.path.splitext(image)[1] in [".jpg",".png"] and os.path.splitext(annot)[1] in [".txt",".xml"]\
			 and os.path.splitext(image)[0]== os.path.splitext(annot)[0]: 


				img = Image.open(os.path.join(self.img_path,image))
				
				img_width,img_height=img.size
				
				annot_file=open(os.path.join(self.annot_path,annot),"rt")
				
				if img_height<=720:

					
					img.save(os.path.join(self.low_quality_image_folder_path,image)) 
					
					new_file=open(os.path.join(self.low_quality_image_folder_path,annot),"wt")
					
					for line in annot_file: #equivalent to with open.
					
						new_file.write(line)
					annot_file.close()

				elif img_height>=1080: 
					
					img.save(os.path.join(self.high_quality_image_folder_path,image))
					
					new_file=open(os.path.join(self.high_quality_image_folder_path,annot),"wt")
					
					for line in annot_file:
						
						new_file.write(line)
					annot_file.close()



if __name__=="__main__":
	
	sample_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\sample1"
	

	imaged="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\VisDrone2019-DET-train\\Visdrone Default\\images"
	annotd="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\Final\\yolo labels- 0,7,8,10 removed and  9 becomes 7"
	#a=Separate_Images_and_Annotations_on_Quality(sample_path)	
	#a.make_dirs()
	#a.separate__different_dirs(imaged,annotd)	

	path2="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\Final\\3.High Quality Visdrone with correct labels"
	separate_file(path2,sep_file="txt",remove_file=True)	
