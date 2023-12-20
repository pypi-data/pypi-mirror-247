import os
import pandas as pd
import tabula
# import Extraction as myex

# Function to process PDF and generate Excel file
def process_pdf(pdf_file):
    # Extracting data from the first table on the first page of the PDF
    df = tabula.read_pdf(pdf_file, pages=1, multiple_tables=False)

    # Get the first table from the DataFrame list
    if isinstance(df, list):
        full_df = df[0]
    else:
        full_df = df

    # Filtering relevant columns
    relevant_columns = ['Subject', 'Result','Total']
    full_df = full_df[relevant_columns].copy()  # Make a copy to avoid SettingWithCopyWarning

    # Apply modifications to Total based on the 'Result' column
    for index, row in full_df.iterrows():
        if row['Result'] == 'F':
            full_df.loc[index, 'Total'] = -1
        elif row['Result'] == 'P':
            full_df.loc[index, 'Total'] = full_df.loc[index, 'Total']
        else:
            full_df.loc[index, 'Total'] = -2

    # Remove rows with 'Subject' as 'Code'
    full_df = full_df[full_df['Subject'] != 'Code']

    # Grouping data by Subject Code and aggregating Total Marks
    grouped_data = full_df.groupby('Subject')['Total'].agg(lambda x: ', '.join(map(str, x))).reset_index()[0:-1:1]

    # Generate output file name based on the PDF file name
    output_file=os.path.splitext(pdf_file)[0].split("\\")

    Pdf_name =r"\\"+ output_file[-1]
    # output_file[-2]="sheets"

    output_file="\\".join(output_file)
    output_file = r"sheets"+ Pdf_name+'.xlsx'
    # output_file = os.path.splitext(pdf_file)[0] + '_subject_wise_totals.xlsx'
    # Writing the grouped data to an Excel file
    grouped_data.to_excel(output_file, index=False)
    print(f"Data from '{pdf_file}' has been successfully written to '{output_file}'.")

def main():
    # Directory containing PDF files
    pdf_directory = r"PDF"

    # Process each PDF file in the directory
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_directory, filename)
            process_pdf(file_path)

# Exicute it ...
os.chdir(os.path.dirname(os.path.abspath(__file__)))
main()

# myex.Gen(input_1,input_2,input_3,input_4,input_5)
