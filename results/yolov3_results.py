import pandas as pd
from plot import plot

path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\final csvs\\yolov3 final results.csv"
df=pd.read_csv(path)


map_05_indices=[0,8,16,24]
f1_indices=[1,9,17,25]
train_cls_loss=[4,12,20,28]
val_obj_loss=[6,14,22,30]
val_cls_loss=[7,15,23,31]

names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]


if __name__=="__main__":

	for index,name in enumerate(df.columns):
		print(index,name)

	#plot(df,map_05_indices,names,title="MaP 0.5 results: Yolo Version 3",xlabel="Epochs",ylabel="MaP")
	#plot(df,f1_indices,names)
	#plot(df,train_cls_loss,names)
	#plot(df,val_obj_loss,names)
	#plot(df,val_cls_loss,names,title="Valid_cls_loss")