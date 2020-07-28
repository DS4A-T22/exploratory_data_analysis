import pandas as pd
import numpy as np
import os
from pathlib import Path

# DATASET_PATH = os.path.abspath('../exploratory_data_analysis/data/cleansed')
DATASET_PATH = Path(__file__).parent / "./data/cleansed"
ACT = f'{DATASET_PATH}/...'
ACT_DISAG = f'{DATASET_PATH}/...'
ADHERENCE = f'{DATASET_PATH}/Adher.csv' # -> TO DO: In the notebook use standard file name format and place file into the 'cleansed' directory
BASIC_DATA = f'{DATASET_PATH}/datos_basicos.csv'
BIO_MEDS = f'{DATASET_PATH}/...'
DYSPNEA = f'{DATASET_PATH}/disnea.csv'
EMERGENCIES = f'{DATASET_PATH}/...'
FAMILY_RECORD = f'{DATASET_PATH}/antecedentes_familiares.csv'
HABITS = f'{DATASET_PATH}/...'
HEIGHT_WEIGHT = f'{DATASET_PATH}/...'
HOSPITALIZATIONS = f'{DATASET_PATH}/Hosp.csv' # -> TO DO: In the notebook use standard file name format and place file into the 'cleansed' directory
MEDICAL_TREATMENTS = f'{DATASET_PATH}/...'
MEDS_COLLECTING_ISSUES = f'{DATASET_PATH}/...'
PARACLINICAL = f'{DATASET_PATH}/...'
PATHOLOGICAL_RECORD = f'{DATASET_PATH}/Pato.csv' # -> TO DO: In the notebook use standard file name format and place file into the 'cleansed' directory
PHARMA_VIGILANCE = f'{DATASET_PATH}/...'
VACCINATION = f'{DATASET_PATH}/...'
WELLBEING_INDEX = f'{DATASET_PATH}/calidad_de_vida.csv'

def get_basic_info_dataset():
    basic_info = pd.read_csv(BASIC_DATA, sep='|')
    # set datatype and explicit category sorting for categorical data
    basic_info['gender'] = basic_info['gender'].astype('category')
    basic_info['education'] = basic_info['education'].astype('category')
    basic_info['education'].cat.reorder_categories(['ANALFABETA', 'EDAD PREESCOLAR', 'PRIMARIA', \
                                                      'SECUNDARIA', 'TECNICO', 'TECNOLOGO', 'UNIVERSITARIO', \
                                                      'POSGRADO'], ordered=True, inplace=True)
    basic_info['civil_status'] = basic_info['civil_status'].astype('category')
    basic_info['zone'] = basic_info['zone'].astype('category')
    basic_info['socioeconomic_level'] = basic_info['socioeconomic_level'].astype('category')
    basic_info['socioeconomic_level'].cat.reorder_categories(['NIVEL 0 DEL SISBEN', 'NIVEL 1 DEL SISBEN', \
                                                               'NIVEL 2 DEL SISBEN', 'A', 'B', 'C'], \
                                                              ordered=True, inplace=True)
    basic_info['occupation'] = basic_info['occupation'].astype('category')
    basic_info['social_security_regime'] = basic_info['social_security_regime'].astype('category')
    basic_info['social_security_affiliation_type'] = basic_info['social_security_affiliation_type'].astype('category')
    basic_info['employment_type'] = basic_info['employment_type'].astype('category')
    basic_info['birthdate'] = pd.to_datetime(basic_info['birthdate'])
    return basic_info

def get_family_records_dataset():
    familiar_records = pd.read_csv(FAMILY_RECORD, sep='|')
    # set datatype and explicit category sorting for categorical data
    familiar_records['health_provider'] = familiar_records['health_provider'].astype('category')
    familiar_records['diagnosis'] = familiar_records['diagnosis'].astype('category')
    familiar_records['diagnosis_code'] = familiar_records['diagnosis_code'].astype('category')
    familiar_records['relationship'] = familiar_records['relationship'].astype('category')
    familiar_records['creation_date'] = pd.to_datetime(familiar_records['creation_date'])
    return familiar_records

def get_wellbeing_index_dataset():
    life_quality = pd.read_csv(WELLBEING_INDEX, sep='|')
    # set datatype and explicit category sorting for categorical data
    life_quality['dimension'] = life_quality['dimension'].astype('category')
    life_quality['creation_date'] = pd.to_datetime(life_quality['creation_date'])
    return life_quality

def get_adherence_dataset():
    adherence = pd.read_csv(ADHERENCE)
    adherence['survey_date'] = pd.to_datetime(adherence['survey_date'])
    adherence.loc[adherence['quantitative_result']=='<30%', 'quantitative_result'] = 0
    adherence.loc[adherence['quantitative_result']=='30-65%', 'quantitative_result'] = 1
    adherence.loc[adherence['quantitative_result']=='64-84%', 'quantitative_result'] = 2
    adherence.loc[adherence['quantitative_result']=='85-94%', 'quantitative_result'] = 3
    adherence.loc[adherence['quantitative_result']=='95-100%', 'quantitative_result'] = 4
    adherence.loc[adherence['smaq2']=='<30%', 'smaq2'] = 0
    adherence.loc[adherence['smaq2']=='30-65%', 'smaq2'] = 1
    adherence.loc[adherence['smaq2']=='64-84%', 'smaq2'] = 2
    adherence.loc[adherence['smaq2']=='85-94%', 'smaq2'] = 3
    adherence.loc[adherence['smaq2']=='95-100%', 'smaq2'] = 4
    adherence.loc[adherence['morisky_green']=='si', 'morisky_green'] = 1
    adherence.loc[adherence['morisky_green']=='no', 'morisky_green'] = 0
    adherence.loc[adherence['smaq1']=='si', 'smaq1'] = 1
    adherence.loc[adherence['smaq1']=='no', 'smaq1'] = 0
    adherence.loc[adherence['espa']=='si', 'espa'] = 1
    adherence.loc[adherence['espa']=='no', 'espa'] = 0
    adherence.loc[adherence['qualitative_result']=='si', 'qualitative_result'] = 1
    adherence.loc[adherence['qualitative_result']=='no', 'qualitative_result'] = 0
    adherence['smaq1'] = adherence['smaq1'].astype('float') 
    adherence['smaq2'] = adherence['smaq2'].astype('float') 
    adherence['morisky_green'] = adherence['morisky_green'].astype('float') 
    adherence['espa'] = adherence['espa'].astype('float') 
    adherence['nm_espa'] = adherence['nm_espa'].astype('float') 
    adherence['qualitative_result'] = adherence['qualitative_result'].astype('float') 
    adherence['quantitative_result'] = adherence['quantitative_result'].astype('float') 
    
    adherence_s= adherence[adherence.quantitative_result < 4]
    adherence_n= adherence[adherence.quantitative_result == 4]
    Todos=adherence['id_patient'].unique()                  #List of all of the ids.
    id_list_s_not=adherence_s['id_patient'].unique() #List of id's that are not 'siempre'
    ads = adherence[~adherence['id_patient'].isin(id_list_s_not)].copy()  #ads : Dataframe of id's that are always adherent.
    id_list_n_not=adherence_n['id_patient'].unique() #List of id's that are not 'nunca'
    adn = adherence[~adherence['id_patient'].isin(id_list_n_not)].copy()  #adn : Dataframe of id's that never were adherent.

    Siempre_ad=ads['id_patient'].unique()            #List of id's that are 'siempre'
    Nunca_ad=adn['id_patient'].unique()              #List of id's that are 'nunca'

    Intermitentes = [x for x in Todos if x not in Siempre_ad]
    Intermitentes = [x for x in Intermitentes if x not in Nunca_ad]
    Intermitentes = np.array(Intermitentes)  #Intermitentes: list of id's that are 'Intermitent'

    Todosmenosint=[x for x in Todos if x not in Intermitentes] 
    Todosmenosint = np.array(Todosmenosint)  #List of id's that are 'Intermitent'

    adi = adherence[~adherence['id_patient'].isin(Todosmenosint)].copy()  #adi: Dataframe of id's that has intermitent adherence.
    adi['quantitative_result'] = adi['quantitative_result'].astype('int64')
    middle_group_scores = adi.groupby('id_patient').quantitative_result.mean().reset_index()  #Sortearlo por el promedio.
    intermediate_adherence_thresholds = adi.groupby('id_patient').quantitative_result.mean().quantile([0.25, 0.75])
    scores_t75 = intermediate_adherence_thresholds[0.75]
    scores_t25 = intermediate_adherence_thresholds[0.25]
    middle_group_scores["category"] = np.where(middle_group_scores['quantitative_result'] > scores_t75, 'A-', 
    (np.where(middle_group_scores['quantitative_result'] < scores_t25, 'N+', 'M')))
    adi = adi.merge(middle_group_scores[['id_patient', 'category']], how='left')
    ads['category']='A'
    adn['category']='N'
    adherence = pd.concat([ads, adi, adn], ignore_index=True).sort_values(by=['id_patient', 'survey_date']).reset_index(drop=True)
   
    adherence['category'] = adherence['category'].astype('category')
    adherence['category'].cat.reorder_categories(['N', 'N+', 'M', 'A-', 'A'], ordered=True, inplace=True)
    
    adherence_change = pd.DataFrame()
    for paciente, df in adherence.groupby('id_patient'):
        temp_df = df.copy().reset_index(drop=True)
        temp_df['morisky_change'] = temp_df['morisky_green'].diff()
        temp_df['smaq1_change'] = temp_df['smaq1'].diff()
        temp_df['smaq2_change'] = temp_df['smaq2'].diff()
        temp_df['espa_change'] = temp_df['espa'].diff()
        temp_df['nm_espa_change'] = temp_df['nm_espa'].diff()
        temp_df['qualitative_result_change'] = temp_df['qualitative_result'].diff()
        temp_df['quantitative_result_change'] = temp_df['quantitative_result'].diff()
        temp_df['days_since_last_control'] = temp_df['survey_date'].diff() / np.timedelta64(1, 'D')
        temp_df['num_reports'] = temp_df.index + 1
        temp_df['ongoing_adherence_percentage'] = 100*(temp_df['qualitative_result'].cumsum()/(temp_df.index+1))
        adherence_change = adherence_change.append(temp_df, ignore_index=True)
       
    return (adherence, adherence_change)

def get_hospitalizations_dataset():
    hospitalizations = pd.read_csv(HOSPITALIZATIONS)
    hospitalizations['gender'] = hospitalizations['gender'].astype('category')
    hospitalizations['diagnosis_code'] = hospitalizations['diagnosis_code'].astype('category')
    return hospitalizations

def get_pathological_record_dataset():
    pathologics = pd.read_csv(PATHOLOGICAL_RECORD)
    pathologics['update_date'] = pd.to_datetime(pathologics['update_date'])
    pathologics['start_date'] = pd.to_datetime(pathologics['start_date'])
    pathologics['end_date']=pd.to_datetime(pathologics['end_date'])
    return pathologics

def get_act_dataset():
    act = pd.read_csv(ACT)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return act

def get_act_disag_dataset():
    act_disag = pd.read_csv(ACT_DISAG)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return act_disag

def get_bio_meds_dataset():
    bio_meds = pd.read_csv(BIO_MEDS, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return bio_meds

def get_dyspnea_dataset():
    dyspnea = pd.read_csv(DYSPNEA, sep=',') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return dyspnea

def get_emergencies_dataset():
    emergencies = pd.read_csv(EMERGENCIES, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return emergencies

def get_habits_dataset():
    habits = pd.read_csv(HABITS, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return habits

def get_height_weight_dataset():
    height_weight = pd.read_csv(HEIGHT_WEIGHT, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return height_weight

def get_medical_treatments_dataset():
    med_treat = pd.read_csv(MEDICAL_TREATMENTS, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return med_treat

def get_med_collec_issues_dataset():
    med_collec_issues = pd.read_csv(MEDS_COLLECTING_ISSUES, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return med_collec_issues

def get_paraclinical_dataset():
    paraclinical = pd.read_csv(PARACLINICAL, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return paraclinical

def get_pharma_vigilance_dataset():
    pharma_vigilance = pd.read_csv(PHARMA_VIGILANCE, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return pharma_vigilance

def get_vaccination_dataset():
    vaccination = pd.read_csv(VACCINATION, sep='|') # -> TO DO: set the right delimiter (sep)
    # Tidying up dataframe (define categories explicitely and datetime fields if required) ...
    return vaccination


