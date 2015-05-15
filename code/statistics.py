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

	attractive_diff, relationship_qualities = arrays_for_comparison(couples, 'attractive_diff', 'relationship_quality')
	correlation, p_val = pearsonr(map(float, attractive_diff), map(float, relationship_qualities))
	print "difference in partner attractiveness is correlated with self-assessed relqtionship quality with pearson coefficient {0} and p-value {1}".format(correlation, p_val)

	# parental_approval, age_diff = arrays_for_comparison(couples, 'same_race',  'relationship_quality')
	# correlation, p_val = pearsonr(map(float, parental_approval), map(float, age_diff))
	# print "religion correlated with self-assessed parental approval with pearson coefficient {0} and p-value {1}".format(correlation, p_val)

	together, married = arrays_for_comparison(couples, 'w3_q5',  'w3_q5')
	together = np.array(map(float,together))
	married = np.array(map(float,married))
	a = len(together[together==1])
	b = len(together[together==0])
	print a, b
	print (a/float(len(together))*100)

	# q32, relationship_qualities = arrays_for_comparison(couples, 'q32_internet', 'relationship_quality')
	# q32 = np.array(map(float, q32))
	# relationship_qualities = np.array(map(float, relationship_qualities))
	# yes_internet = relationship_qualities[q32 == 0]
	# no_internet = relationship_qualities[q32 == 1]
	# t_stat, p_val = ttest_ind(yes_internet, no_internet, equal_var=False)
	# print "averages: internet {0} and not {1}".format(np.mean(yes_internet), np.mean(no_internet))
	# print "The likelihood of couples met on the internet and not having different relationship qualities has a p_value of {0}".format(p_val)
	# correlation, p_val = pearsonr(q32, relationship_qualities)
	# print "Internet meeting is correlated with self-assessed relationship quality with pearson coefficient {0} and p-value {1}".format(correlation, p_val)

	political1, relationship_qualities = arrays_for_comparison(couples, 'pppartyid3', 'relationship_quality')
	political2, relationship_qualities = arrays_for_comparison(couples, 'q12', 'relationship_quality')
	political1 = np.array(map(float, political1))
	political2 = np.array(map(float, political2))
	relationship_qualities = np.array(map(float, relationship_qualities))
	same = (political1 == political2)
	not_same = (political1 != political2)
	t_stat, p_val = ttest_ind(same, not_same, equal_var = False)
	print "averages: same {0} and not{1}".format(np.mean(same), np.mean(not_same))
	print len(same), len(not_same)
	print "The likelihood of same and not same (politically) couples having different average relationship qualities has a p_value of {0}".format(p_val)


	# approval, married = arrays_for_comparison(couples, 'parental_approval', 'ppmarit')
	# married = np.array(map(float,married))
	# approval = np.array(map(float, approval))
	# is_married = approval[(married < 4)]
	# not_married = approval[(married > 3)]
	# t_stat, p_val = ttest_ind(is_married, not_married, equal_var = False)
	# print "averages: married {0} and non-married {1}".format(np.mean(is_married), np.mean(not_married))
	# print "The likelihood of married and not married couples having different average parental approvals has a p_value of {0}".format(p_val)

	# attractiveness, earnings = arrays_for_comparison(couples, 'w4_attractive_partner', 'q23')
	# earnings = np.array(map(float,earnings))
	# attractiveness = np.array(map(float, attractiveness))
	# print attractiveness
	# more = attractiveness[(earnings == 0)]
	# less = attractiveness[(earnings == 2)]
	# t_stat, p_val = ttest_ind(more, less, equal_var = False)
	# print "averages: partner earns less {0} and partner earns more {1}".format(np.mean(more), np.mean(less))
	# print "The likelihood of partners who make more or less having different perceptions of the attractiveness of their partner has a p_value of {0}".format(p_val)

	

if __name__ == '__main__':
	main()
