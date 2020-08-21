import os


def writetxt_for_json(path_to_xml):
	
	dir_name=os.path.dirname(path_to_xml)
	save_path=os.path.join(dir_name,"ids.txt")
	
	with open(save_path,"wt") as file:

		for number,xml in enumerate(os.listdir(path_to_xml)):
			file.write(xml+"\n")
			count=number

		print("Number of files written is {}.".format(count+1))

path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Augmentation 3\\train_annotations_xml"
writetxt_for_json(path)
