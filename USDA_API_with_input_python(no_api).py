import requests
import bs4
import pandas as pd
import time

USDA_API_KEY = '' # Your API goes here
base_url = 'https://api.nal.usda.gov/fdc/v1/food/'
headers = {"X-Api-Key": USDA_API_KEY, "Content-type": "application/json"}

def get_json(fdc_id):
    FDC_ID = fdc_id
    full_url = base_url + FDC_ID
    res = requests.get(full_url,headers=headers)
    json = res.json()
    return json

def gather_data_to_df(json):
    all_nutrient_data = []
    for num in range(len(json['foodNutrients'])):
        amount = ''
        nutrient = json['foodNutrients'][num]['nutrient']['name']
        try:
            amount = json['foodNutrients'][num]['amount']
        except:
            pass
        unit = json['foodNutrients'][num]['nutrient']['unitName']
        nutrient_data ={
            'food_id': json['fdcId'],
            'food-item': json['description'],
            'ndb_number': json['ndbNumber'],
            'nutrient': nutrient,
            'amount': amount,
            'unit': unit
        }
        all_nutrient_data.append(nutrient_data)
        food_item_df = pd.DataFrame(all_nutrient_data)

    return food_item_df


def specific_nutrients(full_item_df):
    specific_nutrients_df = full_item_df[(full_item_df['nutrient'] == 'Protein') |
              ((full_item_df['nutrient'] == 'Energy') & (full_item_df['unit'] == 'kcal')) |
              (full_item_df['nutrient'] == 'Calcium, Ca') |
              (full_item_df['nutrient'] == 'Carbohydrate, by difference') |
              (full_item_df['nutrient'] == 'Cholesterol') |
              (full_item_df['nutrient'] == 'Fatty acids, total saturated') |
              (full_item_df['nutrient'] == 'Fatty acids, total trans') |
              (full_item_df['nutrient'] == 'Iron, Fe') |
              (full_item_df['nutrient'] == 'Potassium, K') |
              (full_item_df['nutrient'] == 'Sodium, Na') |
              (full_item_df['nutrient'] == 'Fatty acids, total trans') |
              (full_item_df['nutrient'] == 'Sugars, total including NLEA') |
              (full_item_df['nutrient'] == 'Sugars, added') |
              (full_item_df['nutrient'] == 'Total lipid (fat)') |
              (full_item_df['nutrient'] == 'Vitamin A, IU') |
              (full_item_df['nutrient'] == 'Vitamin A, RAE') |
              (full_item_df['nutrient'] == 'Vitamin C, total ascorbic acid') |
              (full_item_df['nutrient'] == 'Vitamin D (D2 + D3), International Units') |
              (full_item_df['nutrient'] == 'Vitamin D (D2 + D3)') |
              (full_item_df['nutrient'] == 'Fiber, total dietary')
             ]
    return specific_nutrients_df

# Re-indexing by nutrient
def new_index_order(clean_df):
    new_index_df = clean_df.set_index(['nutrient'])
    final_df = new_index_df.reindex(['Calcium, Ca', 'Energy', 'Carbohydrate, by difference', 'Cholesterol',
                             'Fatty acids, total saturated', 'Fatty acids, total trans', 'Fiber, total dietary',
                             'Iron, Fe', 'Potassium, K', 'Protein', 'Sodium, Na', 'Sugars, added',
                             'Sugars, total including NLEA', 'Total lipid (fat)', 'Vitamin A, IU',
                             'Vitamin A, RAE', 'Vitamin C, total ascorbic acid',
                             'Vitamin D (D2 + D3), International Units', 'Vitamin D (D2 + D3)'])
    return final_df


# Now to put it all together
more_fdc_id = True

while more_fdc_id:
    all_dataframes = []
    fdc_id = input("What is your FDC ID? ")
    print(f"Getting json for FDC ID: {fdc_id}")
    json = get_json(fdc_id)
    food_item = json['description']
    print(f"Now getting all nutrients for '{food_item}'")
    full_nutrients = gather_data_to_df(json)
    print("Removing unnecessary nutrients")
    specific_nutrients_df = specific_nutrients(full_nutrients)
    print("Re-ordering nutrients")
    final_df = new_index_order(specific_nutrients_df)
    all_dataframes.append(final_df)
    print(f"'{food_item}' done!")
    final_df = final_df.reset_index()
    print(final_df[['nutrient', 'amount', 'unit']])

    answer = input("Will you like more nutrition info? (Y/N)  > ")

    if answer[0].lower() == 'y':
        more_fdc_id = True
        print()
        print("-"*100)
        print()
    else:
        print("*"*100)
        print('Great! See you next time!')
        more_fdc_id = False
        break
