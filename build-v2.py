# import pandas as pd
import pandas as pd

# File variables
input_file = r'C:\users\rlovell\python\aws-pc\input-test.csv'  # Replace with your actual CSV file path
output_file = r'C:\users\rlovell\python\aws-pc\output-file.csv'

# Read input data (assuming values are in a single row or column)
df = pd.read_csv(input_file)

# Exclude the first column from the duplicates analysis
unique_id_col = df.iloc[:, 0]  # The first column
data_without_unique_id = df.iloc[:, 1:]  # All columns except the first

# Normalize the data by trimming spaces
data_without_unique_id = data_without_unique_id.map(lambda x: str(x).strip())

# Group by all columns except the first and count occurrences
row_counts = data_without_unique_id.value_counts().reset_index(name='Count')

# Add the unique identifier back to the output
row_counts.insert(0, 'Unique_ID', unique_id_col)

# Print each unique row with its count appended
output = row_counts.apply(lambda row: ','.join(map(str, row.values)), axis=1).tolist()

# write the output to a file
with open(output_file, 'w') as file:
    for line in output:
        file.write(line + '\n')

# Print each row to stdout
for index, row in row_counts.iterrows():
    print(','.join(map(str, row.values)))