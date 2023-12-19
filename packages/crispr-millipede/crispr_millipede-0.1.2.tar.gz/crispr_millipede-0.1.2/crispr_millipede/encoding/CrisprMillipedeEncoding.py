import pandas as pd

def read_allele_table(filename): 
    return pd.read_csv(filename, compression='zip', header=0, sep='\t', quotechar='"')
