import matplotlib.pyplot as plt
import sys



def plot(dataset,list_indices,label_names_list,number_of_rows=None,title=None,xlabel=None,ylabel=None):

	for i in list_indices:

		if number_of_rows!=None:
			plt.plot(dataset.iloc[:number_of_rows,i]*100,label=dataset.columns[i])
		else:
			plt.plot(dataset.iloc[:,i]*100,label=dataset.columns[i])

	l=plt.legend()
	names=label_names_list
	[l.get_texts()[i].set_text(j) for i,j in zip(range(len(l.get_texts())),names)]
	
	if title!=None:  plt.title(title)
	if xlabel!=None: plt.xlabel(xlabel)
	if ylabel!=None: plt.ylabel(ylabel)
	plt.show()
	plt.clf()