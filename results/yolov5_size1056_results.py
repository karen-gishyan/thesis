import pandas as pd
from plot import plot


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\csvs\\yolov5_results 1056s.csv"
df=pd.read_csv(path)



# map_05_indices=[10,25,40,55,70,85]    
# map0_095_indices=[11,26,41,56,71,86]
# train_total_loss=[5,20,35,50,65,80] 
# names=["No Augmentation","Blending Sequence","Blurring Sequence","Geometric Sequence","(3x4) Grid Augmentation","(3x5) Grid Augmentation with Transfer Learning"]


map_05_indices=[10,25,40,55,70,85,115]    
map0_095_indices=[11,26,41,56,71,86,116]
train_total_loss=[5,20,35,50,65,80,110] 

names=["No Augmentation","Blending Sequence","Blurring Sequence","Geometric Sequence","(3x4) Grid Augmentation","(3x5) Grid Augmentation with Transfer Learning","Blending Sequence with Transfer Learning"]

#,"Blurring Sequence with Transfer Learning"
	
if __name__=="__main__":


	for index,name in enumerate(df.columns):
		print(index,name)


	for index,(i,j) in enumerate(zip(map_05_indices,map0_095_indices)):		
		maximum=max(df.iloc[:20,i])
		print(index,names[index],maximum,max(df.iloc[:20,j]))


	plot(df,map_05_indices,names,title="mAP 0.5: Yolov5-Large (1056,1056) size",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",percentage=True)		
	plot(df,map0_095_indices,names,title="mAP 0.5:0.95: Yolov5-Large (1056,1056) size",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",percentage=True)
	plot(df,train_total_loss,names,title="Total Training Loss: Yolov5-Large (1056,1056) size",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Value")