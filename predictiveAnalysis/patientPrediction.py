import os
import numpy as np
import pandas as pd
import json
import copy
import argparse

from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, roc_auc_score
from sklearn.feature_selection import RFE


def DiagnosisPrediction(args):

    data_path = args.data_path
    df = pd.read_csv(data_path)

    data_dir, _ = os.path.split(data_path)
    filename = 'metadata_patient_pred.json'
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'r') as file:
        metadata = json.load(file)


    features_for_pred = metadata['numerical_features'] + metadata['categorical_features']
    features_for_pred += metadata['spatial_feats_for_pred'] + metadata['temporal_feats_for_pred']
    prediction_data = df[features_for_pred].copy()


    labels = df[metadata['diagnoses']]


    ###### Training / Prediction ######

    # Train binary a classifier for each diagnosis.
    classifier_base = SGDClassifier(
        #loss='hinge', # -> Linear SVM
        loss='log',    # -> Logistic Regression
        penalty='l2', 
        alpha=0.0001, 
        l1_ratio=0.15,
        max_iter=1000, tol=0.001, 
        shuffle=True, 
        verbose=args.verbose, 
        epsilon=0.1, 
        n_jobs=None, 
        random_state=None, 
        learning_rate='optimal', 
        eta0=0.0, 
        power_t=0.5, 
        early_stopping=False, 
        validation_fraction=0.1, 
        n_iter_no_change=5, 
        average=False
    )

    for diag in metadata['diagnoses']:
        y = labels[diag] # Labels the current diagnosis
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(prediction_data, y, test_size=0.2, random_state=None)
        
        # Classifier instance
        classifier = copy.deepcopy(classifier_base) # Copy classifier instance
        
        classifier.fit(X_train, y_train) # Train
        y_pred = classifier.predict(X_test) # Test
        
        # Quantify scores
        score = classifier.decision_function(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        rocauc = roc_auc_score(y_test, score)
        
        #Printing
        print(f'Acc:{acc:.3f},  F1:{f1:.3f},  ROC_AUC:{rocauc:.3f}, Diagnosis:{diag}')


    ####### Recursive Feature Elimination #######
    # Recursively remove weights of the linear classifier by selecting the most important features.

    for diag in metadata['diagnoses']:
        y = labels[diag] # Labels the current diagnosis
        X_train, X_test, y_train, y_test = train_test_split(prediction_data, y, test_size=0.2, random_state=None)
        
        # Train a classifier with full features
        classifier = copy.deepcopy(classifier_base) # Copy classifier instance
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        score = classifier.decision_function(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1_full = f1_score(y_test, y_pred)
        rocauc = roc_auc_score(y_test, score)
        
        # Recursively eliminate weights to reach a desired subset of features
        classifier = copy.deepcopy(classifier_base)
        rfe = RFE(classifier, n_features_to_select=int(args.n_features), step=int(args.step), verbose=int(args.verbose))
        
        rfe.fit(X_train, y_train) # Train 
        y_pred = rfe.predict(X_test) # Test
        
        # Quantify scores
        score = rfe.decision_function(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1_topK = f1_score(y_test, y_pred)
        rocauc = roc_auc_score(y_test, score)
        
        # Print results
        #print(f'Acc:{acc:.3f},  F1:{f1:.3f},  ROC_AUC:{rocauc:.3f}, Diagnosis:{diag}')
        print(f'Full features F1:{f1_full:.3f} | Top {args.n_features} features F1:{f1_topK:.3f} Diagnosis:{diag}')
        print(f'Top {args.n_features} features: {rfe.get_feature_names_out()}')
        print('')


if __name__ == "__main__":
    

    arg_parser = argparse.ArgumentParser(
        description="Train binary classifier for each diagnosis and perform recursive feature elimination."
    )

    arg_parser.add_argument(
        '-i', '--data_path', 
        dest='data_path',
        required=True,
        help='Path to dataset file (should be .csv)'
    )

    arg_parser.add_argument(
        '--n_features', 
        dest='n_features',
        required=False,
        default=4,
        help='The number of features to select.'
    )

    arg_parser.add_argument(
        '--step', 
        dest='step',
        required=False,
        default=100,
        help='Number of features to eliminate at every iteration.'
    )

    arg_parser.add_argument(
        '--verbose', 
        dest='verbose',
        required=False,
        default=0,
        help='Verbosity level.'
    )

    args = arg_parser.parse_args()


    DiagnosisPrediction(args)