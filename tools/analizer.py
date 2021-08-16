import numpy as np
import pandas as pd
from typing import Tuple


def detect_nonstandard_aa(sequences: pd.Series) -> Tuple[list, list]:
    """
    Detects non-standard amino acids for each sequence in the Series
    :param sequences: pandas Series of sequences for investigation
    :return: List of counts of non-standard amino acids in each sequence and list of their types
    """
    nonstandard_aa = 'BJOUZX'
    contains_nonstandard_aa = []
    nonstandard_types = []
    for sequence in sequences:
        i = 0
        ns_types = ''
        for letter in sequence:
            if letter in nonstandard_aa:
                i += 1
                ns_types += letter
        contains_nonstandard_aa.append(i)
        nonstandard_types.append(ns_types)
    return contains_nonstandard_aa, nonstandard_types


def compare_original_predicted(predicted_sst: pd.Series, original_sst: pd.Series) -> Tuple[list, list]:
    """
    Compares original and predicted secondary structure types
    :param predicted_sst: Series of predicted secondary structures
    :param original_sst: Series of original secondary structures
    :return: List of percentage of correctly assigned positions and list of committed mistakes
    """
    success_rate = []
    mistakes = []
    if len(predicted_sst) == len(original_sst):
        for j in np.arange(len(predicted_sst)):
            i = 0
            mistakes_temp = []
            for x, y in zip(predicted_sst[j], original_sst[j]):
                if x == y:
                    i += 1
                else:
                    mistakes_temp.append(f'{x}-{y}')
            success_rate.append(i / len(predicted_sst[j]))
            mistakes.append(mistakes_temp)
    return success_rate, mistakes
