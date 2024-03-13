import json
import requests
import os

"""
Web URL: https://projects.rusarchives.ru/rgani_db/kendo_gpl/Kenju/examples/web/grid/mygrid.html
"""

FONDY_URL = "https://projects.rusarchives.ru/rgani_db/data/fonds.php"

OPISI_URL = "https://projects.rusarchives.ru/rgani_db/data/opices.php?filter%5Blogic%5D=and&filter%5Bfilters%5D%5B0%5D%5Bfield%5D=id_fonds&filter%5Bfilters%5D%5B0%5D%5Boperator%5D=eq&filter%5Bfilters%5D%5B0%5D%5Bvalue%5D="

OPIS_BASE_URL = "https://projects.rusarchives.ru/rgani_db/data/opices_cz.php?filter[logic]=and&filter[filters][0][field]=id_opices&filter[filters][0][operator]=eq&filter[filters][0][value]="


def parse_json(url):  
    """Parse json from a given URL"""
    # set verify=False because of an certificate error on projects.rusarchives.ru
    json_string = json.loads(requests.get(url, verify=False).text)    
    return list(json_string.items())[0][1], json_string

def get_opis_url(opis_base_url, number):
    """construct the url for an specific opis"""
    return f"{opis_base_url}{number}"

def write_string_to_csv(opis_string, dir_name, opis_data): 
    """write data to a csv file"""   
    csv_filename = f"{dir_name}{os.sep}{opis_data.get('num_fond')}.{opis_data.get('num_opic')}.csv"
    with open(csv_filename, 'w', encoding='utf-8') as csvfile:
        csvfile.write(opis_string)

def write_json_file(opis_json, json_filename):
    """write data to a json file"""  
    with open(json_filename, "w", encoding='utf-8') as json_file:
        json.dump(opis_json, json_file, indent=4, separators=(", ", ": "), sort_keys=True)

# get the fondy data
fondy_data, fondy_json = parse_json(FONDY_URL)

for fond in fondy_data:
    fond_number = fond.get('num_fond')
    fond_id = fond.get('id')
    fond_name = fond.get('name_fond')
    fond_keys = ['num_fond', 'name_fond']
    fond_general_data = {k:v for k,v in fond.items() if k in fond_keys}

    # for every fond create a folder with json and csv subfolders
    json_dir_name = f"{fond_number}{os.sep}json"
    os.makedirs(json_dir_name, exist_ok=True)
    csv_dir_name = f"{fond_number}{os.sep}csv"
    os.makedirs(csv_dir_name, exist_ok=True)

    opisi_data = None    
    opisi_data, opisi_json = parse_json(OPISI_URL + str(fond_id))
    opis_keys = ['id_fonds', 'num_opic', 'name_opic', 'beg_end_dates', 'op_beg_data', 'op_end_data']

    if opisi_data:
        for opis in opisi_data:        
            opis_general_data = {k:v for k,v in opis.items() if k in opis_keys}
            opis_fond_data = fond_general_data| opis_general_data 
            opis_url = get_opis_url(OPIS_BASE_URL, opis.get('id'))

            opis_specific_data, opis_json = parse_json(opis_url)
            key_dict = opis_fond_data | opis_specific_data[0]
            data_string = ";".join(key_dict.keys()) + '\n'

            opis_data_list = list()
            for elem in opis_specific_data:
                opis_data = opis_fond_data | elem       
                data_string += ';'.join(f'"{w}"' for w in opis_data.values()) + '\n'
                opis_data_list.append(opis_data)

            
            json_filename = f"{json_dir_name}{os.sep}{opis_fond_data.get('num_fond')}.{opis_general_data.get('num_opic')}.json"
            write_json_file(opis_data_list, json_filename)
            write_string_to_csv(data_string, csv_dir_name, opis_data)
            
            print(opis_fond_data)
            print(f"f{opis_fond_data.get('num_fond')} op{opis_general_data.get('num_opic')} csv/json files written.")
            print("-------------------")

