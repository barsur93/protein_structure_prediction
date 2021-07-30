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

# tokenizer_encoder = Tokenizer()
# tokenizer_encoder.fit_on_texts(input_grams)
# input_data = tokenizer_encoder.texts_to_sequences(input_grams)
# input_data = sequence.pad_sequences(input_data, maxlen=maxlen_seq, padding='post')
#
# tokenizer_decoder = Tokenizer(char_level=True)
# tokenizer_decoder.fit_on_texts(target_seqs)
# target_data = tokenizer_decoder.texts_to_sequences(target_seqs)
# target_data = sequence.pad_sequences(target_data, maxlen=maxlen_seq, padding='post')
# target_data = to_categorical(target_data)
# input_data.shape, target_data.shape
