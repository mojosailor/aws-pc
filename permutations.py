# WARNING: The scripts f2py and numpy-config are installed in '/home/mojosailor/.local/bin' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

# Program to count the number of permutations in a table of vm guests based on vCPU, Memory, Target Engine, license model, deployment type

import pandas as pd
from itertools import permutations

# Function to generate permutations from a list of values
def generate_permutations(input_list):
    return list(permutations(input_list))


# Read the input Excel file
input_file = r'C:\Users/RLovell\"OneDrive - Smartronix, LLC"/\clients\"Comm of MA"\EOANF\DOR\MPA\python\dbase-inputs.csv'  # Replace with your input file name
output_file = r'C:\Users/RLovell\"OneDrive - Smartronix, LLC"/\clients\"Comm of MA"\EOANF\DOR\MPA\python/dbase-output.csv'  # Replace with your desired output file name
#sheet_name = 'Databases'  # Sheet name containing input data
#output_sheet_name = 'Permutations'  # Sheet name for output

# Read input data (assuming values are in a single row or column)
df = pd.read_csv(input_file, header=None)
input_values = df.values.flatten().tolist()

# Generate permutations
perms = generate_permutations(input_values)

# Create a DataFrame from permutations and write to Excel
perms_df = pd.DataFrame(perms, columns=[f'Value_{i+1}' for i in range(len(input_values))])
perms_df.to_csv(output_file, index=False)

print(f"Permutations generated and saved to {output_file}'.")
