import pandas as pd

# Read the CSV file into a DataFrame
csv_file_path = r'C:\users\rlovell\python\aws-pc\input-test.csv'  # Replace with your actual CSV file path
df = pd.read_csv(csv_file_path)

#/ Print each row to stdout
for index, row in df.iterrows():
   print(','.join(map(str, row.values)))
   
# Count the number of occurrences of each unique row
row_counts = df.value_counts().reset_index(name='Count')

# Print each unique row with its count appended
for index, row in row_counts.iterrows():
    print(','.join(map(str, row.values)))
