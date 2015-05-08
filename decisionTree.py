import csv
import subprocess
import math

def getBestFeature():
	bashCommand = "wc -l out.csv"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	n = int(output.split()[0])

	csv_reader = list(csv.DictReader(open('out.csv')))
	features = csv_reader[0].keys()
	entropySplitThreshold = 0.7219

	feature_order = {}
	print features

	for x in range(len(features)):
		bestEntropy = 0
		bestFeature = None

		for i in range(len(features)):

			# calculate probability that feature is true across all lines
			for row in csv_reader:
				sumv = 0
				if row["w3_broke_up"] == 1:
					sumv += 1
			p_pos = sumv/float(n)
			p_neg = 1-p_pos
			if p_pos == 0:
				p_pos = 0.0000001
			if p_neg == 0:
				p_neg = 0.0000001

			# calculate entropy
	        entropy = (-1)*p_pos*math.log(p_pos,2) + (-1)*p_neg*math.log(p_neg,2)

	        # determine best entropy
	        if entropy >= entropySplitThreshold and entropy > bestEntropy:
	            bestEntropy = entropy
	            bestFeature = i

		feature_order[features[i]] = x
		features.pop(i)

	print feature_order

if __name__ == '__main__':
	getBestFeature()