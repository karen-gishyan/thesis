import pandas as pd
from plot import plot


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\final csvs\\efficientdet final results.csv"


df=pd.read_csv(path)


iou_05_indexes=[1,15,23,31]
iou_095_indexes=[2,16,24,32]
train_losses=[5,11,19,27,35]
classifcation_losses=[3,9,17,25,33]

names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]
#names=["No Augmentation","Transfer Learning-No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]

if __name__=="__main__":

	for index,name in enumerate(df.columns):
		print(index,name)

	plot(df,iou_05_indexes,names,title="MaP 0.5 results: Efficientdet",xlabel="Epochs",ylabel="MaP")
	#plot(df,classifcation_losses,names)