""" Separability index: An index to assess how separable two two-component datasets are. 
"""

import numpy as np
from scipy.stats import multivariate_normal
from pingouin import multivariate_normality as mvn
from scipy.optimize import minimize

__author__ = 'A. Renmin Pretell Ductram', 'Scott J. Brandenberg'


#===================================================================================================
# Get separability index
#===================================================================================================
def get_SI(x1,y1,x2,y2):

	C1 = multivariate_normal(mean=np.asarray([np.mean(x1),np.mean(y1)]), cov=np.cov(x1,y1))
	C2 = multivariate_normal(mean=np.asarray([np.mean(x2),np.mean(y2)]), cov=np.cov(x2,y2))
	f12 = C2.pdf(np.vstack((x1,y1)).T)
	f21 = C1.pdf(np.vstack((x2,y2)).T)
	f11 = C1.pdf(np.vstack((x1,y1)).T)
	f22 = C2.pdf(np.vstack((x2,y2)).T)
	return 1-(f12.sum()+f21.sum())/(f11.sum()+f22.sum())

#===================================================================================================
# Get Henze-Zirkler test statistic
#===================================================================================================
def get_HZ(lamda,ARGS):
	X1      = ARGS[0]
	X2      = ARGS[1]
	lamda_x = lamda[0]
	lamda_y = lamda[1]

	if(lamda_x!=0):
		X1_box_x = (X1[:,0]**lamda_x-1)/lamda_x
		X2_box_x = (X2[:,0]**lamda_x-1)/lamda_x
	else:
		X1_box_x = np.log(X1[:,0])
		X2_box_x = np.log(X2[:,0])

	if(lamda_y!=0):
		X1_box_y = (X1[:,1]**lamda_y-1)/lamda_y
		X2_box_y = (X2[:,1]**lamda_y-1)/lamda_y
	else:
		X1_box_y = np.log(X1[:,1])
		X2_box_y = np.log(X2[:,1])

	X1_box = np.vstack((X1_box_x,X1_box_y))
	X2_box = np.vstack((X2_box_x,X2_box_y))
	X1_box = X1_box.T
	X2_box = X2_box.T
	return np.sqrt(mvn(X1_box,alpha=0.05)[0]**2 + mvn(X2_box,alpha=0.05)[0]**2)

#===================================================================================================
# Get Box-Cox transform lambda coefficient
#===================================================================================================
def get_lambda(X1,X2):
	ARGS = [X1,X2]
	return minimize(get_HZ,[1.0,1.0],ARGS)['x']
