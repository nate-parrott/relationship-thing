import csv
import numpy as np
from scipy.stats import pearsonr, ttest_ind

def arrays_for_comparison(couples, key1, key2, key3):
	arrays = []
	keys = [key1, key2, key3]
	def include_couple(couple):
		return all(couple[key] not in ('MISSING', '') for key in keys)
	couples = filter(include_couple, couples)
	return [[couple[k] for couple in couples] for k in keys]

def main():
	couples = list(csv.DictReader(open('cleaned_data.csv')))
	

	attractiveness, racer, racep = arrays_for_comparison(couples, 'w4_attractive_partner', 'respondent_race','partner_race')
	attractiveness = np.array(map(float,attractiveness))
	racer = np.array(map(float, racer))
	racep = np.array(map(float, racep))
	same = attractiveness[(racer == racep)]
	diff = attractiveness[(racer != racep)]
	t_stat, p_val = ttest_ind(same, diff, equal_var = False)
	print "The likelihood of partners who are of of the same or different races having different perceptions of the attractiveness of their partner has a p_value of {0}".format(p_val)

	attractiveness, religionr, religionp = arrays_for_comparison(couples, 'w4_attractive_partner', 'papreligion','q7b')
	attractiveness = np.array(map(float,attractiveness))
	religionr = np.array(map(float, religionr))
	religionp = np.array(map(float, religionp))
	same = attractiveness[(religionr == religionp)]
	diff = attractiveness[(religionr != religionp)]
	t_stat, p_val = ttest_ind(same, diff, equal_var = False)
	print "The likelihood of partners who are of of the same or different religion having different perceptions of the attractiveness of their partner has a p_value of {0}".format(p_val)

	

if __name__ == '__main__':
	main()
