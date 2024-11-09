
#importing the required libraries
import sys #for command line arguments
import pandas as pd #for data manipulation
import os #for file operations

# Function to read a subset of columns from a CSV file based on column headers
def process_csv_subset(inv_file_path, columns_headers_string, output_file_path):
    # If columns_headers_string is not provided, read the first row of the input file to get column headers
    if not columns_headers_string:
        columns_headers_list = pd.read_csv(inv_file_path, nrows=0).columns.tolist()
        columns_headers_string = ','.join(columns_headers_list)
    else:
    # Convert the comma-delimited string of column headers to a list
        columns_headers_list = [x.strip() for x in columns_headers_string.split(',')]
    
    # Read the CSV file and use only the specified columns
    df_inv = pd.read_csv(inv_file_path, usecols=columns_headers_list, dtype=str)
    
    # Normalize the data by trimming spaces and ensuring consistent formatting
    df_inv = df_inv.map(lambda x: str(x).strip())
    
    # Ensure all data, including numbers, is output as text
    df_inv = df_inv.map(str)

    # Exclude the first column for the duplicate analysis (assuming the first column is unique ID)
    unique_id_col = df_inv.iloc[:, 0]  # The first column
    data_without_unique_id = df_inv.iloc[:, 1:]  # All columns except the first
    
    # Group rows by all columns except the unique ID and count occurrences
    row_counts = data_without_unique_id.value_counts().reset_index(name='Count')
        
    # Add back the unique ID column by taking one representative from each group
    row_counts['Unique_ID'] = df_inv.groupby(list(df_inv.columns[1:]))[df_inv.columns[0]].first().values
    
    # Rearrange columns to put the unique ID first
    row_counts = row_counts[['Unique_ID'] + list(df_inv.columns[1:]) + ['Count']]
    
    # Read the matching price CSV file
    df_price = pd.read_csv(price_csv_path, dtype=str)
    df_price = df_price.map(lambda x: str(x).strip())  # Normalize data

    # Merge based on matching columns and select the return field
    matching_columns = df_price.columns[1:]  # All columns except Unique_ID for matching
    df_merged = pd.merge(row_counts, df_price, on=matching_columns.tolist(), how='left')

    # Append the return field to the row_counts DataFrame
    if instance_type in df_merged.columns:
        row_counts['Instance Type'] = df_merged[instance_type]
    else:
        raise ValueError(f"'{instance_type}' not found in the matching CSV file.")
    
    # Prepare output as a list of strings
    output = row_counts.apply(lambda row: ','.join(map(str, row.values)), axis=1).tolist()
    
    # Print summary rows to STDOUT
    print("\n-----------Run Summary:--------------\n")
    print(columns_headers_string)
    for line in output:
        print(line)
        count_summary = row_counts['Count'].sum()
    print(f'\nRow Count Total: {count_summary}')
   
    # Write the current run's rows to the output file
    with open(output_file_path, 'w') as file:
        for line in output:
            file.write(line + '\n')  # Write each row count as a new line
     
    print(f'\nRun summary has been written to {output_file_path}')

    
# Get the input file path from command-line arguments or use default
# default_inv_file_path = 'your_csv_file.csv'  # Replace with your default CSV file path
inv_file_path = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else default_inv_file_path

# Main script execution
if __name__ == "__main__":
    # Get the input file path and column headers string from command-line arguments or use defaults
    default_inv_file_path = 'dbase-input.csv'  # Replace with your actual CSV file path
    default_columns_headers_string = 'vCPU,Memory-Trim,Database Engine,Database Edition,Deployment Option'  # Replace with your actual column headers
    inv_file_path = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else default_inv_file_path
    columns_headers_string = sys.argv[2] if len(sys.argv) > 2 else default_columns_headers_string  # Second argument for column headers string
    output_file_path = 'output-test.txt'
    price_csv_path = 'aws rds pricing file.csv'  # Replace with the path to the matching CSV file
    instance_type = 'Instance Type'  # Replace with the name of the field to append


process_csv_subset(inv_file_path, columns_headers_string, output_file_path)



