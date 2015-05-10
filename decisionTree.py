import csv
from sklearn import tree
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.externals.six import StringIO
import numpy as np
import copy
import random

def createObservations():
	"""
	bashCommand = "wc -l out.csv"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	n = int(output.split()[0])
	"""

	csv_reader = list(csv.DictReader(open('binary_data.csv')))
	mydict = copy.copy(csv_reader[0])
	del mydict["caseid_new"]
	del mydict["broken_up"]
	features = sorted(mydict.keys())
	print features

	observations = []
	classes = []
	for row in csv_reader:
		# deal with class attribution
		if row["broken_up"] == '0':
			classes.append(1)
		elif row["broken_up"] == "MISSING":
			rand = random.random()
			if rand < 0.5:
				classes.append(1)
			else:
				classes.append(0)
		else:
			classes.append(0)
		
		obs = []
		# process observations
		for feature in features:
			if row[feature] == "MISSING" or row[feature] == "":
				rand = random.random()
				if rand < 0.5:
					obs.append(1)
				else:
					obs.append(0)
			else:
				obs.append(int(row[feature]))
		observations.append(obs)

	return (observations, classes)


def compareClassifiers():
	(observations, classes) = createObservations()
	observations = np.array(observations)
	classes = np.array(classes)

	# make tree classifier
	my_tree = tree.DecisionTreeClassifier()
	my_tree.fit(observations, classes)
	tree_score = my_tree.score(observations, classes)
	tree_cv = cross_validation.cross_val_score(my_tree, observations, classes, scoring='accuracy', cv=10)
	print "tree score:", tree_score, "tree cv", np.mean(tree_cv)

	# make naive classifier
	naive = BernoulliNB(binarize=None)
	naive.fit(observations, classes)
	naive_score = naive.score(observations, classes)
	naive_cv = cross_validation.cross_val_score(naive, observations, classes, scoring='accuracy', cv=10)
	print "naive score:", naive_score, "naive cv", np.mean(naive_cv)

	# make SVM classifier
	svm = LinearSVC()
	svm.fit(observations, classes)
	svm_score = svm.score(observations, classes)
	svm_cv = cross_validation.cross_val_score(svm, observations, classes, scoring='accuracy', cv=10)
	print "svm score:", svm_score, "svm cv", np.mean(svm_cv)

	# make Log classifier
	log = LogisticRegression()
	log.fit(observations, classes)
	log_score = log.score(observations, classes)
	log_cv = cross_validation.cross_val_score(log, observations, classes, scoring='accuracy', cv=10)
	print "log score:", log_score, "log cv", np.mean(log_cv)


if __name__ == '__main__':
	compareClassifiers()
