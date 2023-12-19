
"""
The pdf Extration tool ...

"""
import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# import pdf_extract 
class Gen:
    def __init__(self,Sub_name,sub_code,cradite,Teacher_name,text) -> None:
        self.subject_marks = []
        # Name =[]
        self.sub=sub_code
        self.Usn=[]
        self.Sub_name=Sub_name 
        self.main()
        temp10=len(self.subject_marks)
        data=[] #this is the place where all the data will be used for the calculation 
        for i in range(temp10):
            temp12=[self.Usn[i].rstrip('.xlsx'),self.Usn[i].rstrip('.xlsx')]
            for k in range(len(self.subject_marks[i])):
                temp12.append(self.subject_marks[i][k])
            data.append(temp12)
        self.sub=self.sub[::-1]
        self.sub.append("name")
        self.sub.append("usn")
        self.sub=self.sub[::-1]
        columns = self.sub
        df = pd.DataFrame(data, columns=columns)
        # Specify the output file path
        output_file = r'output\\output_data.xlsx'
        df.to_excel(output_file, index=False)
        print(f"Data has been successfully written to '{output_file}'.")
        # sub=['BCEDK203', 'BCHES202', 'BESCK204A','BICOK207','BIDTK258','BMATS201','BPLCK205B','BPWSK206']
        df = pd.read_excel(output_file)
        column_names = df.columns.tolist()
        self.sub=[i for i in column_names]

        import AH22CS174
        k=AH22CS174.Result_cal(output_file,self.Sub_name,self.sub[2:],Teacher_name,cradite,text)     

    # Extract info in which all the information will be extracted and then i will be saved in to a file .
    def Extract_info(self,file_path):
        
        # Read the Excel file
        df = pd.read_excel(file_path)

        subjects = df['Subject'].tolist()
        totals = df['Total'].tolist()

        marks=[]

        for i in range(len(subjects)):
            if subjects[i] in (self.sub):
                m=subjects.index(subjects[i])
                marks.append(totals[m])
            else:pass
        self.subject_marks.append(marks)
        pass

    def main(self):
        file_path = r"sheets"
        for i in os.listdir(file_path):
            if i.endswith('.xlsx'):
                self.Usn.append(i)
                u=os.path.join(file_path,i)
                self.Extract_info(u)