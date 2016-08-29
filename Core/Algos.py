
# Algorithms to change
# ========== == ======

__algos = {

	'Decision Tree' : [['Decision Tree'], ['Classification']],
	
	'K-Nearest Neighbors' : [['K-Nearest Neighbors'], ['Classification']],
	
	'Linear Discriminant Analysis' : [['Linear Discriminant Analysis'],
		['Classification']],
	
	'Support Vector Classifier' : [['Support Vector Classifier'],
		['Classification']],
	
	'Gaussian Naive Bayes' : [['Gaussian Naive Bayes'], ['Classification']],

    
    'Linear' : [['Polynomial Features', 'Linear'],
		['Pre-Processing', 'Regression']],
    
    'Lasso'  : [['Polynomial Features', 'Lasso'],
    	['Pre-Processing', 'Regression']],
    
    'Ridge'  : [['Polynomial Features', 'Ridge'],
    	['Pre-Processing', 'Regression']],


	'K-Means' : [['K-Means'], ['Clustering']]
}


#-----------------------------------------------------------------------------#

# Change Engine
# ====== ======

def algoEngine(algo):
    return __algos[algo]


#-----------------------------------------------------------------------------#
