import json
from pymongo import MongoClient 
import math

def open_file(path_to_file):
    '''Open a file using path argument'''
    with open(path_to_file, 'r') as file:
        return json.load(file)
    
def get_config():
    '''Get configuration values from config.json'''
    profile = open_file ('django/invman/etl/config.json')
    return profile

def transform_boolean(value):
    '''We could use mongoengine to do these, but we would have to create mongo models, in addition to our Django models'''
    if value == 'true':
        return 'True'
    elif value == 'false':
        return 'False'
    else:
        return value
    
def set_mapped_values(document, row, mapping):
    '''Sets every field in the Django model that has a mapping in the <model>.json file'''
    for mongo_field, postgres_field in mapping.items():
        if mongo_field in document:
            value = document[mongo_field]
        
        if isinstance(value, dict):
            for mongo_field_2, postgres_field_2 in mapping[mongo_field].items():
                sub_value_2 = value[mongo_field_2]
                if isinstance(sub_value_2, dict):
                    for mongo_field_3, postgres_field_3 in mapping[mongo_field][mongo_field_2].items():
                        if mongo_field_3 == 'standard_item':
                            if 'n' in sub_value_2.values():
                                row.support_11n = True
                            if 'ac' in sub_value_2.values():
                                row.support_11ac = True
                            if 'ax' in sub_value_2.values():
                                row.support_11ax = True
                            if 'ag' in sub_value_2.values():
                                row.support_11ag = True
                            if '6e' in sub_value_2.values():
                                row.support_6e = True
                            if '7' in sub_value_2.values():
                                row.support_7 = True
                        else:
                            sub_value_3 = sub_value_2[mongo_field_3]
                            set_value(row, postgres_field_3, sub_value_3)

                # sub_value = value[mongo_field_2]
                if not isinstance(sub_value_2, dict):
                    set_value(row, postgres_field_2, sub_value_2)
            
            continue

        if mongo_field == 'useType' and not isinstance(value, type(None)):

            if 'res' in value:
                value = 'residential'
            
            if value == 'retail':
                value = 'enterprise'

        if mongo_field == '':
            if value == 'Qualcomm':
                value = 'qualcomm'
            elif value == 'Broadcom':
                value = 'broadcom'
            else:
                value = ''

        # if isinstance(row._meta.get_field(mapping[mongo_field]), models.BooleanField):
        set_value(row, postgres_field, value)
        # except KeyError as e:
        #     print("Continuing on version is None")

def connect_to_mongodb():
    '''Get a mongo client for collection finds'''
    config = get_config().get('mongodb')
    try:
        mongo_client = MongoClient(host=config['host'], username=config['username'], password=config['password'])
        return mongo_client
    except Exception as e:
        print(f'Unable to establish mongo connection: {str(e)}')

def extract_collection(mongo_client, collection_name, query):
    '''Get all data from collection'''
    mongo_db = mongo_client['automation']
    mongo_collection = mongo_db[collection_name]
    return list(mongo_collection.find(query))

def set_value(row, postgres_field, value):
    value = transform_boolean(value)

    if isinstance (value, float):
        if math.isnan(value):
            print("Skipping NaN")
            return

    if value != '': # Enforces Postgres default value
        if value != 'NaN':
            if not isinstance(postgres_field, dict):
                try:
                    setattr(row, postgres_field, value)
                except:
                    print("row")