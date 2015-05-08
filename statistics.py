import csv
from scipy.stats import pearsonr

def arrays_for_comparison(couples, key1, key2):
	arrays = []
	keys = [key1, key2]
	def include_couple(couple):
		return all(couple[key] not in ('MISSING', '') for key in keys)
	couples = filter(include_couple, couples)
	return [[couple[k] for couple in couples] for k in keys]

def main():
	couples = list(csv.DictReader(open('out.csv')))
	
	relationship_qualities, age_diffs = arrays_for_comparison(couples, 'relationship_quality', 'age_difference')
	age_diff_correlation, age_diff_p_val = pearsonr(map(float, age_diffs), map(float, relationship_qualities))
	print "Age difference is correlated with relationship quality with pearson coefficient {0} and p-value {1}".format(age_diff_correlation, age_diff_p_val)

if __name__ == '__main__':
	main()
