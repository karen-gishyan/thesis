import pandas as pd
from plot import plot


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\final csvs\\yolov5l v2 final results.csv"
df=pd.read_csv(path)

map_05_indices=[0,8,16,24,32]
map0_05_095_indices=[1,9,17,25,33]
train_cls_loss=[4,12,20,28,36]
val_obj_loss=[6,14,22,30,38]
val_cls_loss=[7,15,23,31,39]
val_gio_loss=[5,13,21,29,37]
train_gio_loss=[2,10,18,26,34]

names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]
names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation","(3,4)-Gridlike Augmentation"]


if __name__=="__main__":

	for index,name in enumerate(df.columns):
		print(index,name)

	plot(df,map_05_indices,names,title="MaP 0.5 results: Yolo version 5l",xlabel="Epochs",ylabel="MaP")	
	#plot(df,map0_05_095_indices,names,title="Yolov5 v1 MaP 0.5:0.95")
	#plot(df,train_cls_loss,names,title="Training Classification Loss:Yolov5")
	#plot(df,val_obj_loss,names,title="Yolov5 v1 Validation Objective Loss")	
	#plot(df,val_gio_loss,names,title="Val Gio Loss")
	#plot(df,train_gio_loss,names)