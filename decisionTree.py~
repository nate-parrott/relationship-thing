import csv
from sklearn import tree
import numpy as np

def createDecisionTree():
	"""
	bashCommand = "wc -l out.csv"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	n = int(output.split()[0])
	"""

	csv_reader = list(csv.DictReader(open('out.csv')))
	features = csv_reader[0].keys()
	clf = tree.DecisionTreeClassifier()

	observations = []
	classes = []
	for row in csv_reader:
		del row["caseid_new"]
		observations.append(row.values())
		classes.append(row["broken_up"==0])

	clf.fit(observations, classes)

	return clf

if __name__ == '__main__':
	getBestFeature()
