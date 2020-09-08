from PIL import Image
import pandas as pd
import numpy as np
import os



def make_new_labels(path_to_dir,separate_txt=True,separate_images=False,
	labels_to_drop=None, change_labels_function=None,number_of_txt_to_convert=None,number_of_img_to_separate=None): 
	
	"""
	labels_to_drop=takes a list and drops all labels that belong to the list.
	
	change_labels_function:, takes a lambda function :
		eg: lambda x: x/2,  each label is halfed. eg:16 label becomes 8.
	
	separate_txt=if True, creates a directory for separated yolo files.
	seperarate_images= if True, creates a directory for seperated images.

	number_of_txt_to_convert=The number of files to convert.
	number_of_img_to_separate=The number of images to be separated. Separate_images has to be True.

	"""

	folder_path=os.path.split(path_to_dir)[0] 
	
	count_txt=0
	count_img=0
	halfway=True

	for file in os.listdir(path_to_dir):
		
		if separate_txt:

			txt_directory="yolo_labels_converted"
			txt_path=os.path.join(folder_path,txt_directory)

			if not os.path.exists(txt_path):
				os.makedirs(txt_path)			

			if file.endswith(".txt"): 
								
				t = os.path.join(txt_path,file)	
				
				try:						
					df=pd.read_csv(os.path.join(path_to_dir,file),sep=" ",header=None,index_col=None)														  
				
				except:
					print("Empty file")
					file_name=os.path.splitext(file)[0]+".jpg"
					
					#delete the corresponding image of the empty txt file.
					os.remove(os.path.join("C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\images\\Images",file_name))
					continue
				
				if change_labels_function !=None:

					df[0]=list(map(change_labels_function,df[0]))

				if labels_to_drop!=None:
				
					for index, row in df.iterrows():
						
						if row[0] in labels_to_drop:
							
							df.drop(df[df[0]==row[0]].index,inplace=True,axis=0)

				with open(t,"wt", encoding='ascii') as stream: 

					#creates a new path and save the converted txt to that location.

					fmt= '%d', '%1.6f', '%1.6f', '%1.6f','%1.6f' 
					np.savetxt(stream, df.values, fmt=fmt)

				count_txt+=1

		if not separate_txt and number_of_txt_to_convert!=None:
			raise TypeError("seperate_txt is set to False.")
					
		if separate_images:

			image_directory="images_separated"
			image_path=os.path.join(folder_path,image_directory)

			if not os.path.exists(image_path):
				os.makedirs(image_path)

			if file.endswith(".jpg"): 
				
				img = Image.open(os.path.join(path_to_dir,file))
				img=img.save(os.path.join(image_path,file))

				count_img+=1

		if not separate_images and number_of_img_to_separate!=None:
			raise TypeError("separate_images is set to False.")

		# From here bellow, mostly deals with the printing variations.
		if number_of_txt_to_convert!=None and separate_txt and separate_images!=True: # int object.
			
			if count_txt==number_of_txt_to_convert:
				print("txt File convertion finished!")
				break
				
			if count_txt==number_of_txt_to_convert/2:
				
				# halfway makes sure there are no multiple print statements, if png and txt do not follow each other.
				if halfway: print("txt file Conversion halfway done!") #  no else.
				halfway=False

		elif number_of_img_to_separate!=None and separate_txt!=True and separate_images:
			
			if count_img==number_of_img_to_separate:
				print("Image convertion finished!")
				break

			if count_img==number_of_img_to_separate/2:
				
				if halfway:print("Image convertion halfway done!")
				halfway=False
				
		elif (number_of_img_to_separate!=None or number_of_txt_to_convert!=None) and separate_txt and separate_images: # if both are converted, converts with equal number.
			
			if (count_txt==number_of_txt_to_convert or count_txt==number_of_img_to_separate) and count_txt==count_img:
				
				print("File convertion finished!")
				break

			if number_of_txt_to_convert!=None:	

				if count_txt==count_img and (count_txt==number_of_txt_to_convert/2):
					
					if halfway: print("File conversion halfway done!")
					halfway=False

			if img_to_convert!=None:

				if count_txt==count_img and (count_txt==img_to_convert/2):
			
					if halfway: print("File conversion halfway done!")  
					halfway=False

	print("Number of txt files converted:{0}.".format(count_txt))
	print("Number of images converted:{0}.".format(count_img))

	
lambda_function= lambda x : x-1

path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\own images\\annotations"

make_new_labels(path,change_labels_function=lambda_function)