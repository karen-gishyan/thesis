
import numpy as np
import pandas as pd
import os


def make_new_labels(txt_path,labels_to_drop=None): 
	"""
	Reads the VisDrone text files, renames categories. Desired labels can also be dropped.
	# The converted text files are written into a new cateogory.
	"""
	
	new_directory="yolo_annotations_separated"
	folder_path=os.path.split(txt_path)[0] 
	path=os.path.join(folder_path,new_directory) 
	print(path)	
	
	if not os.path.exists(path):
		os.makedirs(path) #create a folder.
	
	count=0
	for file in os.listdir(txt_path):
		
		if file.endswith(".txt"):
				
			
			t = os.path.join(path,file)	
					
			
			
			df=pd.read_csv(os.path.join(txt_path,file),sep=" ",header=None,index_col=None)														  
			df[0]=list(map(lambda v: 3 if (v in [3,7,8]) else (4 if v in [4,5,6,9,10] else v), df[0]))
			
			
			if labels_to_drop!=None:
			
				for index, row in df.iterrows():
					if row[0] in labels_to_drop:
						df.drop(df[df[0]==row[0]].index,inplace=True,axis=0)


			with open(t,"wt", encoding='ascii') as stream: # this creates the file, t is the path.
				np.savetxt(stream, df.values, fmt='%f')
				
			count+=1
			print("{0} Converted.".format(count))


#print(len(os.listdir(txt_p))/3)
#txt_p="C:\\Users\\Կարեն\\Desktop\\Bath Thesis\\VisDrone2019-DET-train\\annotations_plus_images_yolo"
sample_path="C:\\Users\\Կարեն\\Desktop\\Bath Thesis"
#make_new_labels(txt_p)
make_new_labels(sample_path,[1,2,3])


