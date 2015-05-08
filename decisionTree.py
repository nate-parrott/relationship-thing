import csv
from sklearn import tree
from sklearn.externals.six import StringIO
import numpy as np
import copy
import random

def createDecisionTree():
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
	clf = tree.DecisionTreeClassifier()

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

	clf.fit(observations, classes)

	return clf

if __name__ == '__main__':
	classifier = createDecisionTree()
	#with open("tree.dot", "w") as f:
	#	f = tree.export_graphviz(classifier, out_file = f)
