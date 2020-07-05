import pandas as pd
import numpy as np

DATASET_PATH = './data/cleansed'
ACT = f'{DATASET_PATH}/...'
ACT_DISAG = f'{DATASET_PATH}/...'
ADHERENCE = f'{DATASET_PATH}/Adher.csv' # -> TO DO: In the notebook use standard file name format and place file into the 'cleansed' directory
BASIC_DATA = f'{DATASET_PATH}/datos_basicos.csv'
BIO_MEDS = f'{DATASET_PATH}/...'
DYSPNEA = f'{DATASET_PATH}/...'
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
    basic_info['genero'] = basic_info['genero'].astype('category')
    basic_info['escolaridad'] = basic_info['escolaridad'].astype('category')
    basic_info['escolaridad'].cat.reorder_categories(['ANALFABETA', 'EDAD PREESCOLAR', 'PRIMARIA', \
                                                    'SECUNDARIA', 'TECNICO', 'TECNOLOGO', 'UNIVERSITARIO', \
                                                    'POSGRADO'], ordered=True, inplace=True)
    basic_info['estado_civil'] = basic_info['estado_civil'].astype('category')
    basic_info['zona'] = basic_info['zona'].astype('category')
    basic_info['nivel_socioeconomico'] = basic_info['nivel_socioeconomico'].astype('category')
    basic_info['nivel_socioeconomico'].cat.reorder_categories(['NIVEL 0 DEL SISBEN', 'NIVEL 1 DEL SISBEN', \
                                                            'NIVEL 2 DEL SISBEN', 'A', 'B', 'C'], \
                                                            ordered=True, inplace=True)
    basic_info['ocupacion'] = basic_info['ocupacion'].astype('category')
    basic_info['regimen'] = basic_info['regimen'].astype('category')
    basic_info['tipo_afiliacion'] = basic_info['tipo_afiliacion'].astype('category')
    basic_info['relacion_laboral'] = basic_info['relacion_laboral'].astype('category')
    basic_info['fecha_nacimiento'] = pd.to_datetime(basic_info['fecha_nacimiento'])
    return basic_info

def get_family_records_dataset():
    familiar_records = pd.read_csv(FAMILY_RECORD, sep='|')
    # set datatype and explicit category sorting for categorical data
    familiar_records['eps'] = familiar_records['eps'].astype('category')
    familiar_records['diagnostico'] = familiar_records['diagnostico'].astype('category')
    familiar_records['cod_diagnostico'] = familiar_records['cod_diagnostico'].astype('category')
    familiar_records['parentesco'] = familiar_records['parentesco'].astype('category')
    return familiar_records

def get_wellbeing_index_dataset():
    life_quality = pd.read_csv(WELLBEING_INDEX, sep='|')
    # set datatype and explicit category sorting for categorical data
    life_quality['dimensiones'] = life_quality['dimensiones'].astype('category')
    return life_quality

def get_adherence_dataset():
    adherence = pd.read_csv(ADHERENCE)
    adherence['fe_entrevista'] = pd.to_datetime(adherence['fe_entrevista'])
    adherence.loc[adherence['cuantitativo_ponderado']=='<30%', 'cuantitativo_ponderado'] = 0
    adherence.loc[adherence['cuantitativo_ponderado']=='30-65%', 'cuantitativo_ponderado'] = 1
    adherence.loc[adherence['cuantitativo_ponderado']=='64-84%', 'cuantitativo_ponderado'] = 2
    adherence.loc[adherence['cuantitativo_ponderado']=='85-94%', 'cuantitativo_ponderado'] = 3
    adherence.loc[adherence['cuantitativo_ponderado']=='95-100%', 'cuantitativo_ponderado'] = 4
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
    adherence.loc[adherence['cualitativo_ponderado']=='si', 'cualitativo_ponderado'] = 1
    adherence.loc[adherence['cualitativo_ponderado']=='no', 'cualitativo_ponderado'] = 0
    
    adherence_s= adherence[adherence.cuantitativo_ponderado < 4]
    adherence_n= adherence[adherence.cuantitativo_ponderado == 4]
    Todos=adherence['id'].unique()                  #List of all of the ids.
    id_list_s_not=adherence_s['id'].unique() #List of id's that are not 'siempre'
    ads = adherence[~adherence['id'].isin(id_list_s_not)].copy()  #ads : Dataframe of id's that are always adherent.
    id_list_n_not=adherence_n['id'].unique() #List of id's that are not 'nunca'
    adn = adherence[~adherence['id'].isin(id_list_n_not)].copy()  #adn : Dataframe of id's that never were adherent.

    Siempre_ad=ads['id'].unique()            #List of id's that are 'siempre'
    Nunca_ad=adn['id'].unique()              #List of id's that are 'nunca'

    Intermitentes = [x for x in Todos if x not in Siempre_ad]
    Intermitentes = [x for x in Intermitentes if x not in Nunca_ad]
    Intermitentes = np.array(Intermitentes)  #Intermitentes: list of id's that are 'Intermitent'

    Todosmenosint=[x for x in Todos if x not in Intermitentes] 
    Todosmenosint = np.array(Todosmenosint)  #List of id's that are 'Intermitent'

    adi = adherence[~adherence['id'].isin(Todosmenosint)].copy()  #adi: Dataframe of id's that has intermitent adherence.
    adi['cuantitativo_ponderado'] = adi['cuantitativo_ponderado'].astype('int64')
    middle_group_scores = adi.groupby('id').cuantitativo_ponderado.mean().reset_index()  #Sortearlo por el promedio.
    intermediate_adherence_thresholds = adi.groupby('id').cuantitativo_ponderado.mean().quantile([0.25, 0.75])
    scores_t75 = intermediate_adherence_thresholds[0.75]
    scores_t25 = intermediate_adherence_thresholds[0.25]
    middle_group_scores["categoria"] = np.where(middle_group_scores['cuantitativo_ponderado'] > scores_t75, 'A-', 
    (np.where(middle_group_scores['cuantitativo_ponderado'] < scores_t25, 'N+', 'M')))
    adi = adi.merge(middle_group_scores[['id', 'categoria']], how='left')
    ads['categoria']='A'
    adn['categoria']='N'
    adherence = pd.concat([ads, adi, adn], ignore_index=True).sort_values(by=['id', 'fe_entrevista']).reset_index(drop=True)
   
    adherence['categoria'] = adherence['categoria'].astype('category')
    adherence['categoria'].cat.reorder_categories(['N', 'N+', 'M', 'A-', 'A'], ordered=True, inplace=True)
    
    adherence_change = pd.DataFrame()
    for paciente, df in adherence.groupby('id'):
        temp_df = df.copy()
        temp_df['morisky_change'] = temp_df['morisky_green'].diff()
        temp_df['smaq1_change'] = temp_df['smaq1'].diff()
        temp_df['smaq2_change'] = temp_df['smaq2'].diff()
        temp_df['espa_change'] = temp_df['espa'].diff()
        temp_df['nm_espa_change'] = temp_df['nm_espa'].diff()
        temp_df['cualitativo_ponderado_change'] = temp_df['cualitativo_ponderado'].diff()
        temp_df['cuantitativo_ponderado_change'] = temp_df['cuantitativo_ponderado'].diff()
        adherence_change = adherence_change.append(temp_df, ignore_index=True)
       
    return (adherence, adherence_change)

def get_hospitalizations_dataset():
    hospitalizations = pd.read_csv(HOSPITALIZATIONS)
    hospitalizations['sexo'] = hospitalizations['sexo'].astype('category')
    hospitalizations['cod_diagnostico'] = hospitalizations['cod_diagnostico'].astype('category')
    return hospitalizations

def get_pathological_record_dataset():
    pathologics = pd.read_csv(PATHOLOGICAL_RECORD)
    pathologics['fe_actualizada'] = pd.to_datetime(pathologics['fe_actualizada'])
    pathologics['fe_inicio'] = pd.to_datetime(pathologics['fe_inicio'])
    pathologics['fe_fin']=pd.to_datetime(pathologics['fe_fin'])
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
    dyspnea = pd.read_csv(DYSPNEA, sep='|') # -> TO DO: set the right delimiter (sep)
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


