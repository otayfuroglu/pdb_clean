#
import pandas as pd
import os
import numpy as np
import argparse
from parameters import names, colspecs



def read_pdb(pdb_path):
    # Read PDB file into a DataFrame
    return pd.read_fwf(pdb_path, names=names, colspecs=colspecs)



parser = argparse.ArgumentParser(description="Give something ...")
parser.add_argument("-pdb_path", type=str, required=True, help="")
args=parser.parse_args()



#  if __main__ == "__name__":
pdb_path = args.pdb_path
pdb = read_pdb(pdb_path)



# Extract lines starting with "ATOM" from the DataFrame
pdb_atom_df = pdb[pdb['ATOM'] == 'ATOM']

# Write the filtered DataFrame to a new CSV file
pdb_atom_df.to_csv("pdb_atom.csv", sep=' ', index=False, na_rep='NaN')

# Print the DataFrame containing lines starting with "ATOM"
print(pdb_atom_df)


#checking if there are multiple chains in the sequence
chains = pdb_atom_df.chainid.unique()
if len(chains) ==2:
    chain_1=chains[0]
    chain_2=chains[1]
#remove alternate locations
alt_loc = pdb_atom_df.altloc.unique()
if len(alt_loc) > 1:
    # Filter rows where Alt_Loc is not NaN
    pdb_atom_df = pdb_atom_df[pdb_atom_df['altloc'].isna()]

seq_num = pdb_atom_df.resseq.values.astype(int)
print(seq_num)
seq_diff = np.abs(np.diff(seq_num))
print(seq_diff)
if np.any(seq_diff > 1):
    gap_id = np.where(seq_diff > 1)[0]
    print(gap_id)
else:
    print("no")

