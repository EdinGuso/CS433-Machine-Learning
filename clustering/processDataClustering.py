
import os
import argparse
import numpy as np
import pandas as pd
import json
import sys
sys.path.insert(1, '../')
from utils.get_locations import HEALTH_FACILITY_TOWNS, GetLocations


def processDataClustering(data_path, save_path):
    
    data_dir, filename = os.path.split(data_path) 

    df = pd.read_csv(data_path)

    # Drop entries where too many features are not present
    df = df.drop(df.index[df['source'].isin(['abdominal', 'eau', 'chaud', 'sro', 'coartem'])]) # 5 entries
    df = df.drop(df.index[df['t_ab_recommended'].isna()]) # 8 entries
    df = df.drop(df.index[df['a_gender2'].isna()]) # 10 entries
    df = df.reset_index()


    # Categorical features
    """
    group neuro_any
    --d_unconscious
    --d_convuls_his
    --d_convuls_now
    --danger_sign_neck
    --danger_sign_interaction
    --danger_sign_tonus
    --s_limp
    """

    neuro_features = [
        'd_unconscious',
        'd_convuls_his',
        'd_convuls_now',
        'danger_sign_neck',
        'danger_sign_interaction',
        'danger_sign_tonus',
        's_limp'
    ]

    neuro_any = df[neuro_features].any(axis='columns', skipna=True).astype(int).rename('neuro_any')

    """
    group as muac_low
    --s_muac_orange
    --s_muac_red
    """

    muac_low = ((df['s_muac']=='orange') | (df['s_muac']=='red')).astype(int).rename('muac_low')

    """
    s_measles group ms_measles with measles_danger_signs
    """

    df.loc[df.index[df['measles_danger_signs']=='[1fafe800-fd5b-11e3-a3ac-0800200c9a66]'], 'measles_danger_signs'] = None
    df.loc[df.index[df['measles_danger_signs']=='["1fafe800-fd5b-11e3-a3ac-0800200c9a66"]'], 'measles_danger_signs'] = None

    measles_features = ['ms_measles', 'measles_danger_signs']
    s_measles = df[measles_features].any(axis='columns', skipna=True).astype(int).rename('s_measles')

    """
    group as nonspecific
    --s_none
    --no_symptom_classifying_reported
    --no_symptom_ecare_reported
    """

    nonspecific_features = ['s_none', 'no_symptom_classifying_reported', 'no_symptom_ecare_reported']
    nonspecific = df[nonspecific_features].any(axis='columns', skipna=True).astype(int).rename('nonspecific')

    """
    group as resp_any
    --cough_ds
    --cough_indrawing
    --cough_malaise_his
    --cough_prolonged
    --cough_wheez_rhinitis
    --cough_wheeze_rash
    --cough_wheezing
    --cough_oxygen
    --cough_rr
    --high_respiratory_rate
    --s_cough
    --danger_sign_grunting
    """

    # Replace bad entries with None
    df.loc[df.index[df['cough_ds']=='[1fafe800-fd5b-11e3-a3ac-0800200c9a66]'], 'cough_ds'] = None
    df.loc[df.index[df['cough_ds']=='["1fafe800-fd5b-11e3-a3ac-0800200c9a66"]'], 'cough_ds'] = None

    resp_features = [
        'cough_ds',
        'cough_indrawing',
        'cough_malaise_his',
        'cough_prolonged',
        'cough_wheez_rhinitis',
        'cough_wheeze_rash',
        'cough_wheezing',
        'cough_oxygen',
        'cough_rr',
        'high_respiratory_rate',
        's_cough',
        'danger_sign_grunting',
    ]

    resp_any = df[resp_features].any(axis='columns', skipna=True).astype(int).rename('resp_any')

    """
    group below into abdo_any
    --hydration_assessed
    --hydration_eye
    --hydration_neuro
    --hydration_skin
    --hydration_thirst
    --diarrhoea_prolonged
    --bloody_stool
    --abdo_ds
    --s_diarr
    --s_abdopain
    --s_vomit
    --danger_sign_vomit_confirmed
    --danger_sign_vomit_only
    --danger_sign_vomiting
    """

    # Replace bad entries with None
    df.loc[df.index[df['hydration_thirst']=='574143ff-2257-438e-932f-291250d6c2cf'], 'hydration_thirst'] = None
    df.loc[df.index[df['hydration_thirst']=='9f1e50be-ea44-45bf-baba-15e6079b2268'], 'hydration_thirst'] = None
    df.loc[df.index[df['hydration_thirst']=='5ad025d5-b7fe-4fe6-ac2d-aa4c75914cb4'], 'hydration_thirst'] = None
    df.loc[df.index[df['abdo_ds']=='[1fafe800-fd5b-11e3-a3ac-0800200c9a66]'], 'abdo_ds'] = None

    df.loc[df.index[df['hydration_neuro']=='normal'], 'hydration_neuro'] = 0
    df.loc[df.index[df['hydration_skin']=='normal'], 'hydration_skin'] = 0
    df.loc[df.index[df['hydration_thirst']=='normal'], 'hydration_thirst'] = 0

    abdo_features = [
        'hydration_assessed',
        'hydration_eye',
        'hydration_neuro',
        'hydration_skin',
        'hydration_thirst',
        'diarrhoea_prolonged',
        'bloody_stool',
        'abdo_ds',
        's_diarr',
        's_abdopain',
        's_vomit',
        'danger_sign_vomit_confirmed',
        'danger_sign_vomit_only',
        'danger_sign_vomiting'
    ]

    abdo_any = df[abdo_features].any(axis='columns', skipna=True).astype(int).rename('abdo_any')

    """
    group below into ear_any
    --ear_pain_new
    --ear_pain_prolonged
    --ear_tender_swelling
    --ear_pus
    --s_earpain
    """

    df.loc[df.index[df['ear_pus']=='earpus_none'], 'ear_pus'] = 0

    ear_features = [
        'ear_pain_new',
        'ear_pain_prolonged',
        'ear_tender_swelling',
        'ear_pus',
        's_earpain'   
    ]
    ear_any = df[ear_features].any(axis='columns', skipna=True).astype(int).rename('ear_any')

    """
    eye_sympt (group with s_eyepb)
    """

    df.loc[df.index[df['eye_sympt']=='[1fafe800-fd5b-11e3-a3ac-0800200c9a66]'], 'eye_sympt'] = None

    eye_features = ['eye_sympt', 's_eyepb']
    eye_sympt = df[eye_features].any(axis='columns', skipna=True).astype(int).rename('eye_sympt')


    """
    group as skin_any
    --s_skin
    --skin_symptoms
    """

    df.loc[df.index[df['skin_symptoms']=='[1fafe800-fd5b-11e3-a3ac-0800200c9a66]'], 'skin_symptoms'] = None

    skin_features = ['s_skin', 'skin_symptoms']
    skin_any = df[skin_features].any(axis='columns', skipna=True).astype(int).rename('skin_any')

    """
    group urine_signs
    --lab_urine_pos
    --s_dysuria
    --s_hematuria
    """

    urine_features = ['lab_urine_pos', 's_dysuria', 's_hematuria']
    urine_signs = df[urine_features].any(axis='columns', skipna=True).astype(int).rename('urine_signs')


    """
    redo as hb_low if lab_hb is not <9
    --lab_hb
    """
    hb_low = (df['lab_hb']<9).astype(int).rename('hb_low')

    df.loc[df.index[df['a_gender2']=='male'], 'a_gender2'] = 0
    df.loc[df.index[df['a_gender2']=='female'], 'a_gender2'] = 1

    df.loc[df.index[df['s_pallor']=='none'], 's_pallor'] = 0
    df.loc[df.index[df['s_pallor']=='moderate'], 's_pallor'] = 1
    df.loc[df.index[df['s_pallor']=='severe'], 's_pallor'] = 1


    categorical_features = [
        #'a_gender2',
        'anaphyl_confirmed',
        'danger_sign_jaundice',
        'fever_prolonged',
        'lab_malaria_pos',
        'mouth_trush',
        's_oedema',
        's_pallor',
        's_drepano',
        # 's_fever_any' - Not present in dataset,
        's_throat',
        's_mouthpb',
        's_joint',
        'sam_u6add_ocp',
        'wfa_less_than_neg3sd'
    ]

    grouped_features = [
        'neuro_any', 
        'muac_low', 
        's_measles', 
        'nonspecific', 
        'resp_any', 
        'abdo_any', 
        'ear_any', 
        'eye_sympt', 
        'skin_any', 
        'urine_signs', 
        'hb_low'
    ]

    categorical_data = [
        neuro_any,
        muac_low,
        s_measles,
        nonspecific,
        resp_any,
        abdo_any,
        ear_any,
        eye_sympt,
        skin_any,
        urine_signs,
        hb_low,
        df[categorical_features].copy().fillna(0)
    ]

    categorical_data = pd.concat(categorical_data, axis='columns')
    categorical_features.extend(grouped_features)


    # Spatial features
    spatial_features = [
        'source',
        'project',
        'hf'
    ]

    filename = 'gps_coordinates.json'
    file_path = os.path.join(data_dir, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            gps_coordinates = json.load(file)
    else:
        GetLocations(data_dir)
        with open(file_path, 'r') as file:
            gps_coordinates = json.load(file)

    df['hf'] = df['hf'].astype(int)

    spatial_data = pd.DataFrame.from_dict(
        {
            'country': [project.split('-')[0] for project in df['project']],
            'hf_town': [HEALTH_FACILITY_TOWNS[hf] for hf in df['hf']],
            'latitude': [gps_coordinates[HEALTH_FACILITY_TOWNS[hf]][0] for hf in df['hf']],
            'longitude': [gps_coordinates[HEALTH_FACILITY_TOWNS[hf]][1] for hf in df['hf']]
        }
    )

    # Temporal features
    temporal_features = [
        'created'
    ]

    datetimes = pd.to_datetime(df['created'], format='%d%b%Y %H:%M:%S')

    temporal_data = pd.DataFrame()

    temporal_data['week'] = [date.week for date in datetimes]
    temporal_data['month'] = [date.month for date in datetimes]
    temporal_data['year'] = [date.year for date in datetimes]
    temporal_data['datetime'] = datetimes

    # 53rd week does not exist
    temporal_data.loc[temporal_data.index[(temporal_data['week']==53) &  (temporal_data['year']==2020)], 'week'] = 52
    temporal_data.loc[temporal_data.index[(temporal_data['week']==53) &  (temporal_data['year']==2021)], 'week'] = 1


    # Numerical features
    numerical_features = [
        'a_age',
        #'a_weight'
    ]


    # Median Imputation
    # Instead of mean use median imputation to fill missing data since median is robust to outliers
    df[numerical_features] = df[numerical_features].astype(float)
    numerical_data = df[numerical_features].fillna(df[numerical_features].median())


    # Save statistics of features before normalization
    normalization_stats = {}
    normalization_stats['numerical_data_mean'] = numerical_data.mean().to_dict()
    normalization_stats['numerical_data_std'] = numerical_data.std().to_dict()

    # Normalization
    numerical_data = (numerical_data-numerical_data.mean())/numerical_data.std()


    # Clean DataFrame
    patient_data = pd.concat(
        [
            spatial_data, 
            temporal_data, 
            numerical_data, 
            categorical_data.astype(np.float64),
        ], 
        axis=1
    )
    
    if save_path:
        save_dir, filename = os.path.split(save_path)
    else:
        save_dir, filename = data_dir, 'patient_data.csv'
        save_path = os.path.join(save_dir, filename)

    patient_data.to_csv(save_path, index=False)



    # Save metadata about the processed dataset
    metadata = {
        'spatial_features': list(spatial_data.columns),
        'temporal_features': list(temporal_data.columns),
        'numerical_features': list(numerical_data.columns),
        'categorical_features': list(categorical_data.columns),
        'normalization_stats' : normalization_stats
    }

    filename = 'metadata_patient.json'
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'w') as file:
        json.dump(metadata, file, indent=4)



if __name__ == "__main__":
    

    arg_parser = argparse.ArgumentParser(
        description='Process raw data to craft patient dataset for clustering'
    )

    arg_parser.add_argument(
        '-i', '--data_path', 
        dest='data_path',
        required=True,
        help='Path to dataset file (should be .csv)'
    )

    arg_parser.add_argument(
        '-o', '--save_path', 
        dest='save_path',
        required=False,
        help='Path for storing processed dataset. If no path is provided, file will be dumb the directory of the input dataset.'
    )

    args = arg_parser.parse_args()


    processDataClustering(args.data_path, args.save_path)
