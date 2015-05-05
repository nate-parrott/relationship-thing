import sys
import csv
from collections import defaultdict

ID_FIELD = 'caseid_new'
NECESSARY_FIELDS = {'s2':True, 'partner_deceased':False}
INFO_FIELDS = ['caseid_new', 's2', 'partner_deceased', 'respondent_yrsed', 'partner_yrsed', 'q23', 'hhinc', 'same_sex_couple', 's1a', 'respondent_race', 'partner_race', 'age_difference', 'q21b', 'ppage', 'q9', 'q30', 'w3_q5', 'w3_q1', 'relationship_quality', 'w2w3_combo_breakup', 'w3_broke_up', 'w3_days_elapsed', 'w3_q10', 'w3_q10', 'q32_internet', 'pppartyid3', 'q12']
SUPP_FIELDS = []
INFO_FILE = 'data/projectdata.csv'
SUPP_FILE = 'data/supplement.csv'
MISSING = 'MISSING'
OTHER = 'OTHER'

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

def clean(observations, enum_file):
    enums = {}
    f = open(enum_file)
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        field = line[0]
        enums[field] = line[1:]
    for obs_key in observations.keys():
        obs = observations[obs_key]
        for field in enums.keys():
            vals = enums[field]
            converted = False
            if obs[field] == "":
                obs[field] = MISSING
                continue
            for i in range(len(vals)):
                value = vals[i]
                if value == obs[field]:
                    obs[field] = i
                    converted = True
                    break
            if not converted:
                #print field, obs[field]
                #print ""
                obs[field] = OTHER 
    return observations

def filter_data(observations, necessary_fields):
    for obs_key in observations.keys():
        obs = observations[obs_key]
        for field in necessary_fields:
            if obs[field] == MISSING or obs[field] == OTHER:
                del observations[obs_key]
                break
    return observations

def export_features(observations, fields):
    f = open("out.txt", 'w')
    writer = csv.DictWriter(f, fieldnames=fields)
    for obs_id in observations.keys():
        writer.writerow(observations[obs_id])

def main():
    obs = extract_features([INFO_FILE, SUPP_FILE], ID_FIELD, [INFO_FIELDS, SUPP_FIELDS]) 
    obs = clean(obs, 'enum_mapper.tsv')
    obs = filter_data(obs, ['s2', 'partner_deceased'])
    export_features(obs, INFO_FIELDS)
    

if __name__ == '__main__': main()
        
