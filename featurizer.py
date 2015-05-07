import sys
import csv
from collections import defaultdict

ID_FIELD = 'caseid_new'
NECESSARY_FIELDS = {'s2':True, 'partner_deceased':False}
# a list of the fields in the primary document that are to be extracted
# if you want to add more, just add it to the list
# if the field values need to be converted to integers, add it to the 'enum_mapper.tsv' file
INFO_FIELDS = ['caseid_new',  's2', 'partner_deceased', 'respondent_yrsed', 'partner_yrsed', 'q23', 'hhinc', 'same_sex_couple', 's1a', 'respondent_race', 'partner_race', 'age_difference', 'q21b', 'ppage', 'q9', 'parental_approval', 'w3_q5', 'w3_q1', 'relationship_quality', 'w2w3_combo_breakup', 'w3_broke_up', 'w3_days_elapsed', 'w3_q10', 'q32_internet', 'pppartyid3', 'q12', 'papreligion', 'q7b', 'ppmarit']
SUPP_FIELDS = ['w4_attractive', 'w4_attractive_partner']
INFO_FILE = 'data/projectdata.csv'
SUPP_FILE = 'data/supplement.csv'
MISSING = 'MISSING'
OTHER = 'OTHER'
NOT_APPLICABLE = -1

"""pulls out wanted features from the given files
        filenames - array of strings
        id_field - field name of uuid
        other_fields - array of arrays of fields to be extracted to the corresponding
                       file in filenames
    """
def extract_features(filenames, id_field, other_fields):
    observations = defaultdict(dict) #id -> dict of info
    for i in range(len(filenames)):
        name = filenames[i]
        fields = other_fields[i]
        f = open(name)
        reader = csv.DictReader(f)
        for row in reader:
            has_necessary_fields = True
            key = row[id_field]
            observations[key][id_field] = key
            for field in fields:
                observations[key][field] = row[field] 
    return observations  

def generate_enum_map(enum_file):
    enums = {}
    f = open(enum_file)
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        field = line[0]
        enums[field] = line[1:]
    return enums


""" cleans data by filtering it into enums
     observations - a dictionary (string id -> dictionary) that stores for each 
                    unique id the values for each field
     enum_file - a file path to a csv file where each line represents the different
                 types of strings that can be found under a given field name. The
                 field name is the first column followed by a list of acceptable answers
     returns - observations, but the values of every column specified in the enum file
               will now be the index in the enum file of the value that was extracted 
               in the row the field name is associated to. Any unspecified values will
               be assigned OTHER and any empty string values will be assigned MISSING
    """
def clean(observations, enum_map):
    for obs_key in observations.keys():
        obs = observations[obs_key]
        for field in enum_map.keys():
            vals = enum_map[field]
            converted = False
            if not field in obs.keys():
            	continue
            elif obs[field] == "":
                obs[field] = MISSING
                continue
            for i in range(len(vals)):
                value = vals[i]
                if value == obs[field]:
                    obs[field] = i
                    converted = True
                    break
            if not converted:
                obs[field] = OTHER 
    return observations

"""removes data from the dictionary that does not have appropriate values in specific
   fields
   observations - a dictionary (string id -> dictionary) that stores for each 
                    unique id the values for each field
   necessary_fields - an array of strings of the fields that must be checked
   returns - observations with any entries that contain MISSING or OTHER under a necessary
                column
   """

def filter_data(observations, necessary_fields):
    for obs_key in observations.keys():
        obs = observations[obs_key]
        for field in necessary_fields:
            if obs[field] == MISSING or obs[field] == OTHER:
                del observations[obs_key]
                break
    return observations

""" takes prints the cleaned data to a csv
    observations - a dictionary (string id -> dictionary) that stores for each 
                    unique id the values for each field
     fields - an array of the field names 

"""

def export_features(observations, fields):
    f = open("out.csv", 'w')
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for obs_id in observations.keys():
        writer.writerow(observations[obs_id])
""" binarizes data by using a dictionary of functions that will binarize fields
    observations - a dictionary (string id -> dictionary) that stores for each 
                    unique id the values for each field
    functions - a dictionary (string -> lambda) where the lambda will explain
    		    correctly binarize the value for the field represented by the
    		    key
    returns - observations, but with the value as a dictionary from field to
    		  0/1 value that was determined by the function it was given
"""
def binarize_data(observations, functions):
    new_obs = {}
    for obs_key in observations.keys():
        new_obs[obs_key] = {}
        obs = observations[obs_key]
        for field in functions.keys():
            new_obs[obs_key][field] = functions[field](obs)
    return new_obs

""" labels data according to the label function
    observations - a dictionary (string id -> dictionary) that stores for each 
                    unique id the values for each field
    label_fun - a function that takes in an observation dictionary and labels
    			the observation accordingly (usually 0/1)
    returns - a dictionary from key to label
"""

def label_data(observations, label_fun):
	labels = {}
	for obs_key in observations.keys():
		obs = observations[obs_key]
		labels[key] = label_fun(obs) 

""" prints out the frequency of each answer for a given field so you can compare
	to the frequencies in the data manual to check for accuracy
	observations - a dictionary (string id -> dictionary) that stores for each 
                    unique id the values for each field
    field - the field you want the frequency of
"""

def check_freqs(observations, field):
    counts = {}
    for obs_key in observations.keys():
    	obs = observations[obs_key]
        if obs[field] in counts.keys():
            counts[obs[field]] += 1
        else:
            counts[obs[field]] = 1
    print "Frequencies for:", field
    sort_counts = sorted(counts.keys(), key=lambda x: counts[x]) 
    for ans in sort_counts:
        print counts[ans], ans
        

def main():
    #extract row data from the different input files
    obs = extract_features([INFO_FILE, SUPP_FILE], ID_FIELD, [INFO_FIELDS, SUPP_FIELDS])
    #for multiple choice questions, create a map to number values for acceptable answers
    enum_map = generate_enum_map('enum_mapper.tsv')
    #converts answers to number values
    obs = clean(obs, enum_map)
    #remove any rows with MISSING or OTHER values for "are you in a relationship" and partner_deceased
    obs = filter_data(obs, ['s2', 'partner_deceased'])
    binarize_lam = {
                     'same_sex' : lambda x: x['same_sex_couple'],
                     'same_race' : lambda x: 1 if x['respondent_race'] == x['partner_race'] else 0 ,
                     'parental_approval' : lambda x: x['parental_approval'],
                     'same_pol' : lambda x: 1 if x['pppartyid3'] == x['q12'] else 0,
                     'internet' : lambda x: x['q32_internet'],
                     'same_religion' : lambda x: 1 if x['papreligion'] == x['q7b'] else 0,
                     'age_gap' : lambda x: 1 if x['age_difference'] > 5 else 0
                     }
    #converts the data to the binarized form
    bin_obs = binarize_data(obs, binarize_lam)
    #print bin_obs
    all_fields = list(INFO_FIELDS)
    all_fields.extend(SUPP_FIELDS)
    #print all the fields 
    export_features(obs, all_fields)
    

if __name__ == '__main__': main()
        
