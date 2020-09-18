import os


def count_annotations(annot_path):
	count=0
	
	for txt in os.listdir(annot_path):
		
		txt=os.path.join(annot_path,txt)
		with open(txt,"r") as file:
			for line in file:
				count+=1


	return count



no_aug="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Not Augmented\\train_annotations_yolo"
aug_1="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Augmentation 1\\train_annotations_yolo"
aug_2="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Augmentation 2\\train_annotations_yolo"
aug_3="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Augmentation 3\\train_labels"
mosaic_only="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Augmentation (3,4)\\mosaic only\\gird_mosaic_yolo"
aug_3x5="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Augmentation (3,5) with blurred images\\train_labels"

no_aug_3x4_blur="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Augmentation default_(3x4)_then_blurr\\train_labels"
combined_700="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\main\\main\\main experiments\\Augmentation_blend_blur_geometric_700\\train_labels"


#geometric annotations-original-159547, after conversion-146358.

print("Number of annotations without augmentation is",count_annotations(no_aug))
print("Number of annotations after augmentation 1 is",count_annotations(aug_1))
print("Number of annotations after augmentation 2 is",count_annotations(aug_2))
print("Number of annotations after augmentation 3 is",count_annotations(aug_3))
print("Number of annotations only mosaic is ",count_annotations(mosaic_only))
print("Number of annotations after (3,5) is ",count_annotations(aug_3x5))
print("Number of annotations after no_aug+(3x4) then blur is ",count_annotations(no_aug_3x4_blur))
print("Number of annotations, blend,blur and geometric on grid",count_annotations(combined_700))

