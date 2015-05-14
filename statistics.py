import csv
import numpy as np
from scipy.stats import pearsonr, ttest_ind

def arrays_for_comparison(couples, key1, key2):
	arrays = []
	keys = [key1, key2]
	def include_couple(couple):
		return all(couple[key] not in ('MISSING', '') for key in keys)
	couples = filter(include_couple, couples)
	return [[couple[k] for couple in couples] for k in keys]

def main():
	couples = list(csv.DictReader(open('cleaned_data.csv')))
	
	relationship_qualities, age_diffs = arrays_for_comparison(couples, 'relationship_quality', 'age_difference')
	age_diff_correlation, age_diff_p_val = pearsonr(map(float, age_diffs), map(float, relationship_qualities))
	print "Age difference is correlated with relationship quality with pearson coefficient {0} and p-value {1}".format(age_diff_correlation, age_diff_p_val)
	
	resp_edu, partner_edu = arrays_for_comparison(couples, 'respondent_yrsed', 'partner_yrsed')
	edu_correlation, edu_p_val = pearsonr(map(float, resp_edu), map(float, partner_edu))
	print "One partner's years of education is correlated with the other partner's pearson coefficient {0} and p-value {1}".format(edu_correlation, edu_p_val)
	
	years, relationship_qualities = arrays_for_comparison(couples, 'how_long_ago_first_romantic', 'relationship_quality')
	correlation, p_val = pearsonr(map(float, years), map(float, relationship_qualities))
	print "Duration of relationship is correlated with self-assessed relationship quality with pearson coefficient {0} and p-value {1}".format(correlation, p_val)

	incomes, relationship_qualities = arrays_for_comparison(couples, 'hhinc', 'relationship_quality')
	correlation, p_val = pearsonr(map(float, incomes), map(float, relationship_qualities))
	print "Household income is correlated with self-assessed relationship quality with pearson coefficient {0} and p-value {1}".format(correlation, p_val)

	approval, relationship_qualities = arrays_for_comparison(couples, 'parental_approval', 'relationship_quality')
	correlation, p_val = pearsonr(map(float, approval), map(float, relationship_qualities))
	print "Parental approval is correlated with self-assessed relationship quality with pearson coefficient {0} and p-value {1}".format(correlation, p_val)

	approval, married = arrays_for_comparison(couples, 'parental_approval', 'ppmarit')
	married = np.array(map(float,married))
	approval = np.array(map(float, approval))
	is_married = approval[(married < 4)]
	not_married = approval[(married > 3)]
	t_stat, p_val = ttest_ind(is_married, not_married, equal_var = False)
	print "The likelihood of married and not married couples having different average parental approvals has a p_value of {0}".format(p_val)


	attractiveness, earnings = arrays_for_comparison(couples, 'w4_attractive_partner', 'q23')
	earnings = np.array(map(float,earnings))
	attractiveness = np.array(map(float, attractiveness))
	more = attractiveness[(earnings == 0)]
	less = attractiveness[(earnings == 2)]
	t_stat, p_val = ttest_ind(more, less, equal_var = False)
	print "The likelihood of partners who make more or less having different perceptions of the attractiveness of their partner has a p_value of {0}".format(p_val)

	

if __name__ == '__main__':
	main()
