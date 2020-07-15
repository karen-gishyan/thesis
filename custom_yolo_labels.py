
import numpy as np
import pandas as pd
import os
from PIL import Image


def make_new_labels(dirr,txt_dir_name,img_dir_name,labels_to_drop=None, reduce_categories=True,
	separate_txt=True,separate_images=True,txt_to_convert=None,img_to_convert=None): 
	"""
	Reads the VisDrone text files, renames categories. Desired labels can also be dropped.
	# The converted text files are written into a new cateogory.

	txt_to_convert parameter works when separate_txt is True.
	img_to_convert parameter works when separate_images is True.
	"""


	txt_directory=txt_dir_name
	image_directory=img_dir_name
	

	folder_path=os.path.split(dirr)[0] 

	txt_path=os.path.join(folder_path,txt_directory) 
	image_path=os.path.join(folder_path,image_directory)
		
	if not os.path.exists(txt_path):
		os.makedirs(txt_path) #create a folder.
	
	if not os.path.exists(image_path):
		os.makedirs(image_path)

	count_txt=0
	count_img=0
	halfway=True

	for file in os.listdir(dirr):
		
		if separate_txt:

			if file.endswith(".txt"): # harcy ene vor karoxa arajiny png exni, u miangamic convert ene txt chhasni.
								
				t = os.path.join(txt_path,file)	
										
				df=pd.read_csv(os.path.join(dirr,file),sep=" ",header=None,index_col=None)														  
				
				if reduce_categories:
					
					df[0]=list(map(lambda v: 3 if (v in [3,7,8]) else (4 if v in [4,5,6,9,10] else v), df[0]))
				
				if labels_to_drop!=None:
				
					for index, row in df.iterrows():
						
						if row[0] in labels_to_drop:
							
							df.drop(df[df[0]==row[0]].index,inplace=True,axis=0)

				with open(t,"wt", encoding='ascii') as stream: # this creates the file, t is the path.
					
					np.savetxt(stream, df.values, fmt='%f')

				count_txt+=1

		if not separate_txt and txt_to_convert!=None:
			raise TypeError("seperate_txt is set to False.")
					
		if separate_images:

			if file.endswith(".jpg"): 
				
				img = Image.open(os.path.join(dirr,file))
				img=img.save(os.path.join(image_path,file))

				count_img+=1

		if not separate_images and img_to_convert!=None:
			raise TypeError("separate_images is set to False.")


		if txt_to_convert!=None and separate_txt and separate_images!=True: # int object.
			
			if count_txt==txt_to_convert:
				print("txt File convertion finished!")
				break
				
			if count_txt==txt_to_convert/2:
				
				# halfway makes sure there are no multiple print statements, if png and txt do not follow each other.
				if halfway: print("txt file Conversion halfway done!") # when there is no else.
				halfway=False

		elif img_to_convert!=None and separate_txt!=True and separate_images:
			
			if count_img==img_to_convert:
				print("Image convertion finished!")
				break

			if count_img==img_to_convert/2:
				
				if halfway:print("Image convertion halfway done!")
				halfway=False
				
		elif (img_to_convert!=None or txt_to_convert!=None) and separate_txt and separate_images: # if both are converted, converts with equal number.
			
			if (count_txt==txt_to_convert or count_txt==img_to_convert) and count_txt==count_img:
				
				print("File convertion finished!")
				break

			if txt_to_convert!=None:	

				if count_txt==count_img and (count_txt==txt_to_convert/2):
					
					if halfway: print("File conversion halfway done!")
					halfway=False

			if img_to_convert!=None:

				if count_txt==count_img and (count_txt==img_to_convert/2):
			
					if halfway: print("File conversion halfway done!")  
					halfway=False

	print("Number of txt files converted:{0}.".format(count_txt))
	print("Number of images converted:{0}.".format(count_img))

	
p1="C:\\Users\\Կարեն\\Desktop\\Bath Thesis\\VisDrone2019-DET-train\\annotations_plus_images_yolo"
#sample_path="C:\\Users\\Կարեն\\Desktop\\Bath Thesis"
txt_directory="yolo_annotations_pedestrian"
image_directory="images_seperated_pedestrian"
make_new_labels(p1,txt_directory,image_directory,txt_to_convert=500,labels_to_drop=[0,2,3,4,5,6,7,8,9,10,11]) # keep only pedestrian

