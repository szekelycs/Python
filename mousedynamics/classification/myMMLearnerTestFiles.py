import pandas
from mousedynamics.utils import settings as st
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB


def myMMLearnerTestFiles():

	names = st.csvOutHeaders
	dataset = pandas.read_csv(st.workDir + 'mouse_action_summary.csv', skiprows = 1, names = names)
	array = dataset.values

	X_train = array[:,5:]
	Y_train = array[:,0]

	testdataset = pandas.read_csv(st.workDir + 'test_mouse_action_summary.csv', skiprows = 1, names = names)
	testarray = testdataset.values

	X_validation = testarray[:,5:]
	Y_validation = testarray[:,0]


	# validation_size = 0.10
	seed = 7
	scoring = 'accuracy'
	# X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
	models = []
	models.append(('LR', LogisticRegression()))
	models.append(('LDA', LinearDiscriminantAnalysis()))
	models.append(('KNN', KNeighborsClassifier()))
	models.append(('CART', DecisionTreeClassifier()))
	models.append(('NB', GaussianNB()))
	models.append(('RF', RandomForestClassifier()))
	# n_estimators = 500
	# models.append(('SVM', SVC()))
	# evaluate each model in turn
	results = []
	names = []

	for name, model in models:
		kfold = model_selection.KFold(n_splits=10, random_state=seed)
		cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
		results.append(cv_results)
		names.append(name)
		msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
		print(msg)

		# Compare Algorithms
	fig = plt.figure()
	fig.suptitle('Algorithm Comparison')
	ax = fig.add_subplot(111)
	plt.boxplot(results)
	ax.set_xticklabels(names)
	plt.show()

	# Make predictions on validation dataset
	knn = KNeighborsClassifier()
	knn.fit(X_train, Y_train)
	predictions = knn.predict(X_validation)
	print(accuracy_score(Y_validation, predictions))
	print(confusion_matrix(Y_validation, predictions))
	print(classification_report(Y_validation, predictions))


	# shape
	# print(dataset.shape)

	# head
	# print(dataset.head(20))

	# descriptions
	# print(dataset.describe())

	# class distribution
	# print(dataset.groupby('class').size())

	# box and whisker plots
	# dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
	# plt.show()

	# histograms
	# dataset.hist()
	# plt.show()

	# scatter plot matrix
	# scatter_matrix(dataset)
	# plt.show()
	return

myMMLearnerTestFiles()