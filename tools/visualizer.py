import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def visualize_occurrence(feature_series: pd.Series, xlabel: str) -> plt:
    """
    Generate barplot for selected feature series
    :param feature_series: pandas Series of the feature which will be visualized
    :param xlabel: the label of the x-axis
    :return: matplotlib.pyplot object
    """
    occurrences = Counter(''.join(feature_series.values))
    sorted_occurrences = {k: v for k, v in sorted(occurrences.items(),
                                                  key=lambda item: item[1],
                                                  reverse=True)}
    plt.bar(x=np.arange(1, len(sorted_occurrences) + 1),
            height=[x*100 / sum(sorted_occurrences.values()) for x in sorted_occurrences.values()],
            tick_label=list(sorted_occurrences.keys()))
    plt.ylim(0, 50)
    plt.xlabel(xlabel)
    plt.ylabel('Occurrence [%]')
    return plt
