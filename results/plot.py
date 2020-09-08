import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import pandas as pdd
import sys



def plot(dataset,list_indices,label_names_list,rolling_mean_windows_size=None,number_of_rows=None,title=None,
	xlabel=None,ylabel=None,percentage=False,legend_outside=True):
	

	for i in list_indices:

		series=dataset.iloc[:,i]

		if rolling_mean_windows_size!=None:

			series=series.rolling(window=rolling_mean_windows_size).mean()

		if number_of_rows!=None:

			series=dataset.iloc[:number_of_rows,i]
		
		
		plt.plot(series*100,label=dataset.columns[i]) if percentage else plt.plot(series,label=dataset.columns[i])

	#l=plt.legend(loc="best",fontsize=7, title_fontsize=7)
	l=plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1)) if legend_outside else plt.legend()


	names=label_names_list
	
	[l.get_texts()[i].set_text(j) for i,j in zip(range(len(l.get_texts())),names)]
	plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))	
	
	if title!=None:  plt.title(title)
	if xlabel!=None: plt.xlabel(xlabel)
	if ylabel!=None: plt.ylabel(ylabel)

	plt.show()
	plt.clf()