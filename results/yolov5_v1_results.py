import pandas as pd
from plot import plot

path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\final csvs\\yolov5l v1 final results.csv"
df=pd.read_csv(path)

map_05_indices=[0,8,16,24]
map0_05_095_indices=[1,9,17,25]
train_cls_loss=[4,12,20,28]
val_obj_loss=[6,14,22,30]
val_cls_loss=[7,15,23,31]



names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]




if __name__=="__main__":

	for index,name in enumerate(df.columns):
		print(index,name)

	plot(df,map_05_indices,names,title="MaP 0.5 results: Yolo Version 5",xlabel="Epochs",ylabel="MaP")
	#plot(df,map0_05_095_indices,names,title="Yolov5 v1 MaP 0.5:0.95")
	#plot(df,train_cls_loss,names,title="Classification Loss")
	#plot(df,val_obj_loss,names,title="Yolov5 v1 Validation Objective Loss")
