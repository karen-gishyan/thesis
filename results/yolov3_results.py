import pandas as pd
from plot import plot

#path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\final csvs\\yolov3 final results.csv"

path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final_results\\yolov3_final.csv"
df=pd.read_csv(path)


#map_05_indices=[0,16,24,32,8,40,48,56,64]
map_05_indices352=[0,16,24,32,48]
map_05_indices1056=[8,40,56,64]

f1_indices_352=[1,17,25,33,49]
f1_indices_1056=[9,41,57,65]

train_obj_loss_352=[3,19,27,35,51]
train_obj_loss_1056=[11,43,59,67]

train_cls_loss_352=[4,20,28,36,52]
train_cls_loss_1056=[12,44,60,68]


names352=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation","(3,4) Grid Augmentation"]
names1056=["No Augmentation","(3,4) Grid Augmentation","(3,5) Grid Augmentation","(3,5) Grid Augmentation:Size 1056-Transfer Learning"]

if __name__=="__main__":


	# for i in map_05_indices:
	# 	print(max(df.iloc[:,i]))


	for index,name in enumerate(df.columns):
		print(index,name)

	plot(df,map_05_indices352,names352,title="MaP 0.5 results: Yolo Version 3",xlabel="Epochs",ylabel="MaP")		
	plot(df,map_05_indices1056,names1056,title="MaP 0.5 results: Yolo Version 3",xlabel="Epochs",ylabel="MaP")
	
	# plot(df,f1_indices_352,names352,title="F1 Score: Yolo version 3",xlabel="Epochs",ylabel="Value")
	# plot(df,f1_indices_1056,names1056,title="F1 Score: Yolo version 3",xlabel="Epochs",ylabel="Value")
	
	# plot(df,train_cls_loss_352,names352,title="Training Classification Loss: Yolo Version 3",xlabel="Epochs",ylabel="Loss Value")
	# plot(df,train_cls_loss_1056,names1056,title="Training Classification Loss: Yolo Version 3",xlabel="Epochs",ylabel="Loss Value")
	
	# plot(df,train_obj_loss_352,names352,title="Training Objective Loss: Yolo Version 3",xlabel="Epochs",ylabel="Loss Value")
	# plot(df,train_obj_loss_1056,names1056,title="Training Objective Loss: Yolo Version 3",xlabel="Epochs",ylabel="Loss Value")
	
