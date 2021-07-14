import gzip
import csv
import pandas as pd
import numpy as np

class Sequences:
    @staticmethod
    def process_raw_sequences(raw_sequences_file: str) -> pd.DataFrame:
        output_csv = raw_sequences_file.replace('txt.gz', 'csv')
        with gzip.open(filename=raw_sequences_file, mode='rt') as input_file:
            with open(output_csv, 'wt') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(['pdb_id', 'chain', 'sequence', 'secondary_struct'])
                i = 0
                next_line = input_file.readline()
                while next_line:
                    line = next_line
                    if line.startswith('>') and line.rstrip().split(':')[-1] == 'sequence':
                        line = line.replace('>', '')
                        pdb_id, chain = line.split(':')[0], line.split(':')[1]

                        sequence = ''
                        next_line = input_file.readline()
                        while True:
                            if next_line.startswith('>'):
                                break
                            else:
                                sequence = sequence + next_line.replace('\n', '')
                                next_line = input_file.readline()

                        if next_line.rstrip().split(':')[-1] == 'secstr':
                            next_line = input_file.readline()
                            secondary_str = ''
                            while next_line:
                                if next_line.startswith('>'):
                                    i += 1
                                    break
                                else:
                                    secondary_str = secondary_str + next_line.replace('\n', '').replace(' ', 'C')
                                    next_line = input_file.readline()

                    if len(sequence) == len(secondary_str):
                        csv_writer.writerow([pdb_id, chain, sequence, secondary_str])

                    else:
                        raise ValueError('The lengths of sequence and secondary structure does not match!')

        print(f'processed {i} sequences')
        sequences_df = pd.read_csv(output_csv)  # converting to DataFrame here due to lower efficiency to writerow()
        return sequences_df

    @staticmethod
    def clean_pisces(sequences_df: pd.DataFrame, pisces_file: str) -> pd.DataFrame:
        pisces_df = pd.read_csv(pisces_file, sep=r'[\t ]+', engine='python')
        pisces_df.rename(columns={'Exptl.': 'source', 'R-factor': 'R_value', 'FreeRvalue': 'R_free'}, inplace=True)
        pisces_df['pdb_id'] = pd.Series(x[0:4] for x in pisces_df['IDs'] if len(x) == 5)
        pisces_df['chain'] = pd.Series(x[4] for x in pisces_df['IDs'] if len(x) == 5)
        pisces_df.drop(columns=['IDs'], inplace=True)
        return pisces_df

    def clean_sequences(self, sequences_df: pd.DataFrame):
        pass


processing = Sequences()

# # seq_df = processing.process_raw_sequences(raw_sequences_file='../../data/2021-07-09-ss.txt.gz')
# seq_df = pd.read_csv('../../data/2021-07-09-ss.csv')
# # print(seq_df.head())
#
#
# psc_df = processing.clean_pisces(seq_df, '../../data/cullpdb_pc30_res2.0_R0.25_d2021_07_02_chains10870.gz')
# print(psc_df.head())


