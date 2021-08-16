import gzip
import csv
import pandas as pd


class Sequences:
    @staticmethod
    def process_raw_sequences(raw_sequences_file: str) -> pd.DataFrame:
        """
        Processing of raw sequences from the PDB database into pandas DataFrame
        :param raw_sequences_file: raw sequences from PDB database
        :return: DataFrame with sequences
        """
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
                        pdb_id, chain = line.split(':')[0], line.split(':')[1].upper()

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
        # print('coś')
        sequences_df = pd.read_csv(output_csv)  # converting to DataFrame due to lower efficiency compared to writerow()
        return sequences_df

    @staticmethod
    def clean_pisces(pisces_file: str) -> pd.DataFrame:
        """
        Processing of raw data from the PISCES database
        :param pisces_file: PISCES data
        :return: DataFrame with cleaned PISCES data
        """
        pisces_df = pd.read_csv(pisces_file, sep=r'[\t ]+', engine='python')
        pisces_df.rename(columns={'Exptl.': 'source', 'R-factor': 'R_value', 'FreeRvalue': 'R_free'}, inplace=True)
        pisces_df['pdb_id'] = pd.Series(x[0:4] for x in pisces_df['IDs'] if len(x) >= 5)
        pisces_df['chain'] = pd.Series(x[4].upper() for x in pisces_df['IDs'] if len(x) >= 5)
        pisces_df.drop(columns=['IDs'], inplace=True)
        return pisces_df

    @staticmethod
    def combine_pdb_pisces(sequences_df: pd.DataFrame, pisces_df: pd.DataFrame) -> pd.DataFrame:
        """
        Combines PDB database sequences with PISCES data
        :param sequences_df: processed PDB sequences
        :param pisces_df: cleaned PISCES data
        :return: DataFrame after PDB sequences and PISCES data intersection
        """
        combined_df = sequences_df.merge(pisces_df, on=['pdb_id', 'chain'])
        return combined_df

    @staticmethod
    def generate_seq_q8_q3_representation(combined_df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts Q8 secondary structure representation into Q3 secondary structure representation
        :param combined_df: DataFrame containing sequences after intersection of PDB data and PISCES data
        :return: DataFrame with additional column containing Q3 secondary structure representation
        """
        q8_to_q3 = {
            ord('G'): 'H', ord('I'): 'H', ord('B'): 'E', ord('T'): 'C', ord('S'): 'C',
        }
        combined_df.rename(columns={'secondary_struct': 'sst_q8', 'sequence': 'seq'}, inplace=True)
        combined_df['sst_q3'] = [seq.translate(q8_to_q3) for seq in combined_df.sst_q8]
        df_for_modeling = combined_df[['pdb_id', 'seq', 'sst_q8', 'sst_q3']]
        return df_for_modeling
