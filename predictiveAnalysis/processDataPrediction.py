import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import argparse
import sys
sys.path.insert(1, '../')
from utils.get_locations import HEALTH_FACILITY_TOWNS, GetLocations

def processDataPrediction(data_path, save_path):

    data_dir, filename = os.path.split(data_path) 

    df = pd.read_csv(data_path)


    # Drop entries where too many features are not present
    df = df.drop(df.index[df['source'].isin(['abdominal', 'eau', 'chaud', 'sro', 'coartem'])]) # 5 entries
    df = df.drop(df.index[df['t_ab_recommended'].isna()]) # 8 entries
    df = df.drop(df.index[df['a_gender2'].isna()]) # 10 entries
    df = df.reset_index()



    diagnoses = [ 
        'hisdx_severe',
        'hisdx_urti',
        'hisdx_lrti',
        'hisdx_cough_persist',
        'hisdx_diarrhwatery',
        'hisdx_diarrhblood',
        'hisdx_otitis',
        'hisdx_malaria_simple',
        'hisdx_malaria_sev',
        'hisdx_malnut',
        'hisdx_measles',
        'hisdx_anemia',
        'hisdx_others',
        'hisdx_ot_skin',
        'hisdx_ot_uti',
        'hisdx_ot_eye',
        'hisdx_ot_mouth',
        'hisdx_ot_fever_viral'
    ]



    # Categorical features
    neuro_features = [
        'd_unconscious',
        'd_convuls_his',
        'd_convuls_now',
        'danger_sign_neck',
        'danger_sign_interaction',
        'danger_sign_tonus',
        's_limp'
    ]
    resp_features = [
        #'cough_ds',
        'cough_indrawing',
        'cough_malaise_his',
        'cough_prolonged',
        'cough_wheez_rhinitis',
        'cough_wheeze_rash',
        'cough_wheezing',
        #'cough_oxygen',
        #'cough_rr',
        'high_respiratory_rate',
        's_cough',
        'danger_sign_grunting',
    ]

    # Replace bad entries with None
    df.loc[df.index[df['hydration_thirst']=='574143ff-2257-438e-932f-291250d6c2cf'], 'hydration_thirst'] = np.nan
    df.loc[df.index[df['hydration_thirst']=='9f1e50be-ea44-45bf-baba-15e6079b2268'], 'hydration_thirst'] = np.nan
    df.loc[df.index[df['hydration_thirst']=='5ad025d5-b7fe-4fe6-ac2d-aa4c75914cb4'], 'hydration_thirst'] = np.nan
    df.loc[df.index[df['abdo_ds']=='[1fafe800-fd5b-11e3-a3ac-0800200c9a66]'], 'abdo_ds'] = np.nan

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
        #'abdo_ds',
        's_diarr',
        's_abdopain',
        's_vomit',
        'danger_sign_vomit_confirmed',
        'danger_sign_vomit_only',
        'danger_sign_vomiting'
    ]
    df.loc[df.index[df['ear_pus']=='earpus_none'], 'ear_pus'] = 0
    ear_features = [
        'ear_pain_new',
        'ear_pain_prolonged',
        'ear_tender_swelling',
        'ear_pus',
        's_earpain'   
    ]

    """
    group as muac_low
    --s_muac_orange
    --s_muac_red
    """
    muac_low = ((df['s_muac']=='orange') | (df['s_muac']=='red')).astype(int).rename('muac_low')

    """
    redo as hb_low if lab_hb is not <9
    --lab_hb
    """
    hb_low = (df['lab_hb']<9).astype(int).rename('hb_low')

    df.loc[df.index[df['eye_sympt']=='[1fafe800-fd5b-11e3-a3ac-0800200c9a66]'], 'eye_sympt'] = np.nan
    eye_features = ['eye_sympt', 's_eyepb']

    nonspecific_features = ['s_none', 'no_symptom_classifying_reported', 'no_symptom_ecare_reported']
    measles_features = ['ms_measles']
    skin_features = ['s_skin']
    urine_features = ['lab_urine_pos', 's_dysuria', 's_hematuria']

    categorical_features = [
        'a_gender2',
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


    categorical_features += neuro_features + measles_features + nonspecific_features  +  resp_features + abdo_features + ear_features + eye_features +  skin_features + urine_features

    # One-Hot encoding
    categorical_data = pd.get_dummies(
        df[categorical_features], columns=categorical_features, dummy_na=True
    ).rename(
        lambda col: col.replace('.0', ''), axis=1
    )
    categorical_data


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

    spatial_feats_for_pred = ['latitude', 'longitude']


    # Temporal features

    temporal_features = [
        'created'
    ]

    datetimes = pd.to_datetime(df['created'], format='%d%b%Y %H:%M:%S')
    temporal_data = pd.DataFrame()


    # Add $\Big(\sin\left(\frac{2\pi}{52}\textrm{week_number}\right),  \cos\left(\frac{2\pi}{52}\textrm{week_number}\right)\Big)$
    temporal_data['week_number_sine'] = [np.sin((2*np.pi/52)*date.week) for date in datetimes]
    temporal_data['week_number_cosine'] = [np.cos((2*np.pi/52)*date.week) for date in datetimes]

    # Add $\Big(\sin\left(\frac{2\pi}{12}\textrm{month}\right),  \cos\left(\frac{2\pi}{12}\textrm{month}\right)\Big)$
    temporal_data['month_sine'] = [np.sin((2*np.pi/12)*date.month) for date in datetimes]
    temporal_data['month_cosine'] = [np.cos((2*np.pi/12)*date.month) for date in datetimes]

    temporal_data['year'] = [date.year for date in datetimes]
    temporal_data['year'] = temporal_data['year'].astype(float)
    temporal_data['datetime'] = datetimes


    temporal_feats_for_pred = [
        'week_number_sine',
        'week_number_cosine',
        'month_sine',
        'month_cosine',
        'year'
    ]

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

    normalization_stats['spatial_data_mean'] = spatial_data[spatial_feats_for_pred].mean().to_dict()
    normalization_stats['spatial_data_std'] = spatial_data[spatial_feats_for_pred].std().to_dict()

    normalization_stats['temporal_data_mean'] = temporal_data[temporal_feats_for_pred].mean().to_dict()
    normalization_stats['temporal_data_std'] = temporal_data[temporal_feats_for_pred].std().to_dict()

    #Normalize
    numerical_data = (numerical_data-numerical_data.mean())/numerical_data.std()

    spatial_data[spatial_feats_for_pred] -= spatial_data[spatial_feats_for_pred].mean()
    spatial_data[spatial_feats_for_pred] /= spatial_data[spatial_feats_for_pred].std()

    temporal_data[temporal_feats_for_pred] -= temporal_data[temporal_feats_for_pred].mean()
    temporal_data[temporal_feats_for_pred] /= temporal_data[temporal_feats_for_pred].std()


    # Clean DataFrame
    patient_data = pd.concat(
        [
            spatial_data, 
            temporal_data, 
            numerical_data, 
            categorical_data.astype(np.float64),
            df[diagnoses]
        ], 
        axis=1
    )
    
    if save_path:
        save_dir, filename = os.path.split(save_path)
    else:
        save_dir, filename = data_dir, 'patient_pred_data.csv'
        save_path = os.path.join(save_dir, filename)
    patient_data.to_csv(save_path, index=False)


    # Save metadata about the processed dataset
    metadata = {
        'spatial_features': list(spatial_data.columns),
        'spatial_feats_for_pred' : spatial_feats_for_pred,
        'temporal_features': list(temporal_data.columns),
        'temporal_feats_for_pred' : temporal_feats_for_pred,
        'numerical_features': list(numerical_data.columns),
        'categorical_features': list(categorical_data.columns),
        'diagnoses' : diagnoses,
        'normalization_stats' : normalization_stats
        
    }

    filename = 'metadata_patient_pred.json'
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'w') as file:
        json.dump(metadata, file, indent=4)


if __name__ == "__main__":
    

    arg_parser = argparse.ArgumentParser(
        description='Process raw data to craft patient dataset for predictive analysis'
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

    processDataPrediction(args.data_path, args.save_path)
