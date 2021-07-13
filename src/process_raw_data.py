import gzip
import csv
import pandas as pd


class Sequences:
    # def __init__(self, pdb_code, chain, sequence, secondary_str):
    #     self.pdb_code = pdb_code
    #     self.chain = chain
    #     self.sequence = sequence
    #     self.secondary_str = secondary_str
    #
    def process_raw_sequences(self, raw_sequences_file: str):
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

    def combine_pdb_pisces(self, sequences_df: pd.DataFrame, pisces_file: str):
        pisces_df = pd.read_csv(pisces_file, sep='\t')

        return pisces_df

    def clean_sequences(self, sequences_df: pd.DataFrame):
        pass


# processing = Sequences()
# 
# seq_df = processing.process_raw_sequences(raw_sequences_file='../../data/2021-07-09-ss.txt.gz')
# print(seq_df.head())
# 
# pisces_df = processing.combine_pdb_pisces(seq_df, '../../data/cullpdb_pc30_res2.0_R0.25_d2021_07_02_chains10870.gz')
# print(pisces_df.head(1))

