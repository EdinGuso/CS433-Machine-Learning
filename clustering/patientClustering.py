import os
import argparse
import numpy as np
import pandas as pd
import json
import pickle
from kmodes.kprototypes import KPrototypes
from sklearn.mixture import GaussianMixture

def PatientClustering(args):

    data_path = args.data_path
    df = pd.read_csv(data_path)

    data_dir, _ = os.path.split(data_path)
    filename = 'metadata_patient.json'
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'r') as file:
        metadata = json.load(file)
        
    features_for_clustering = metadata['numerical_features'] + metadata['categorical_features']
    clustering_data = df[features_for_clustering].copy()
    categorical_feature_indices = [clustering_data.columns.get_loc(c) for c in metadata['categorical_features']]

    method = args.method
    n_clusters = int(args.n_clusters)
    n_init = int(args.n_init)
    max_iter = int(args.max_iter)

    if method == '1':
        # KPrototypes initialization
        model = KPrototypes(n_clusters=n_clusters, init='Huang', n_init=n_init, max_iter=max_iter, verbose=1)
        assignments = model.fit_predict(clustering_data, categorical=categorical_feature_indices)
        cluster_points = model.cluster_centroids_
    else:
        # Gaussian Mixture Model initialization
        model = GaussianMixture(n_components=n_clusters, covariance_type='full', n_init=n_init, max_iter=max_iter, random_state=0)
        assignments = model.fit_predict(clustering_data)
        cluster_points = model.means_

    # Spatiotemporal clustering features
    st_clustering_features = [
        'datetime',
        'country', 
        'hf_town', 
        'latitude', 
        'longitude'
    ]

    # Spatiotemporal clustering

    spatiotemporal_clustering = df[st_clustering_features].copy()
    spatiotemporal_clustering['assigned_cluster'] = assignments

    save_path = args.save_path
    if save_path:
        save_dir, filename = os.path.split(save_path)
    else:
        save_dir, filename = data_dir, 'clustered_data.csv'
        save_path = os.path.join(save_dir, filename)


    spatiotemporal_clustering.to_csv(save_path, index=False)

    # Put cluster points into a DataFrame
    cluster_points = pd.DataFrame(cluster_points, columns=features_for_clustering)


    #Unnormalize numerical features
    numerical_data_mean = pd.Series(metadata['normalization_stats']['numerical_data_mean'])
    numerical_data_std = pd.Series(metadata['normalization_stats']['numerical_data_std'])

    cluster_points[metadata['numerical_features']] = cluster_points[metadata['numerical_features']]*numerical_data_std
    cluster_points[metadata['numerical_features']] += numerical_data_mean

    threshold = 0.1
    if method == '0': # Binarize categorical features
        categorical_features = metadata['categorical_features']
        cluster_points[categorical_features] = (cluster_points[categorical_features]>threshold).astype(int)

    # Drop features consisting only of 0's
    cluster_points = cluster_points.drop(cluster_points.columns[cluster_points.sum(axis='rows')==0], axis='columns')

    # Save cluster centroids
    cluster_points.to_csv(os.path.join(data_dir, 'cluster_points.csv'), index=False)


    # Save model
    model_save_path = os.path.join(save_dir, 'clustering_model.pkl')
    with open(model_save_path, 'wb') as file:
        pickle.dump(model, file)

    print('Clustering is successfully completed.')


if __name__ == "__main__":
    

    arg_parser = argparse.ArgumentParser(
        description="Cluster patient's data using KPrototypes of GaussianMixture"
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
        help='Path for storing resuls. If no path is provided, file will be dumped the directory of the input dataset.'
    )

    arg_parser.add_argument(
        '--method', 
        dest='method',
        required=False,
        default='0',
        choices=['0', '1'],
        help='Clustering method. Either 0 for a Gaussian Mixture Model (default, fast) '
        +'or 1 for KPrototypes (slow, better cluster interpretability).'
    )


    arg_parser.add_argument(
        '--n_clusters', 
        dest='n_clusters',
        required=False,
        default=4,
        help='Number of clusters.'
    )

    arg_parser.add_argument(
        '--n_init', 
        dest='n_init',
        required=False,
        default=1,
        help='Number of initializations of the clustering algorith. The best results are kept.'
    )

    arg_parser.add_argument(
        '--max_iter', 
        dest='max_iter',
        required=False,
        default=100,
        help='Maximum number of iterations.'
    )

    args = arg_parser.parse_args()


    PatientClustering(args)