from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import numpy as np
import pandas as pd


#  function inspired from https://www.kaggle.com/helmehelmuto/secondary-structure-prediction-with-keras
def convert_to_ngrams(sequences: pd.Series, n: int) -> np.array:
    seq_list = []
    for item in sequences.values:
        seq_list.append([item[i:i+n] for i in np.arange(len(item))])
    return np.array(seq_list, dtype=object)


def tokenize_inputs(input_sequences: np.array, maxlen: int) -> np.array:
    input_tokenizer = Tokenizer()
    input_tokenizer.fit_on_texts(input_sequences)
    x_seq = input_tokenizer.texts_to_sequences(input_sequences)
    x_seq = pad_sequences(x_seq, maxlen=maxlen, padding='post')
    return x_seq


def tokenize_target(target_sst: pd.Series, maxlen: int) -> np.array:
    target_tokenizer = Tokenizer(char_level=True, lower=False)
    target_tokenizer.fit_on_texts(target_sst)
    y_sst = target_tokenizer.texts_to_sequences(target_sst)
    y_sst = pad_sequences(y_sst, maxlen=maxlen, padding='post')
    y_sst = to_categorical(y_sst)
    return y_sst
