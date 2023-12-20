"""
Duniya kee sochu ki saade baare
ae gal billo chhad de, chhad de, chhad de
Apne tu mummy-daddy da vi darr
dil ton hun kad de, kad de ...
 
Tu meri heer, maine dil se maana tujhe
Har veervar Peer baba se bhi manga tujhe

Kar deni hal main saari mushkil
Rakh yaqeen, just chill
Jehda aaya saade vich, I gonna kill

Main 
====================================================
Made by Tanishq JM for ACS college of engineering .
Result analizer.
====================================================
Copyright @2023 
"""

import tkinter as tk
import subprocess
import os,glob,gui4,sys
import Extraction as myex
from PIL import Image, ImageTk
import pandas as pd
import key_test as kt

kt.test_key()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def file_location():
    file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(file_path)
    print()
    subprocess.Popen(f'explorer {folder_path}')

def animate_label():
        if status_label.cget("text") == "Processing":
            status_label.config(text="Processing.")
        elif status_label.cget("text") == "Processing.":
            status_label.config(text="Processing..")
        elif status_label.cget("text") == "Processing..":
            status_label.config(text="Processing...")
        else:
            status_label.config(text="Processing")
        status_label.after(50, animate_label)

def open_gui1():
    kt.test_key()
    def destroy_test_section():
        label_2.destroy()
        entry_2.destroy()
        label_5.destroy()
        entry_5.destroy()
        button_clear.destroy()
        button_print.destroy()
        message_label.destroy()
        status_label.destroy()
        button_open_location.destroy()

    def Synthesize():
        animate_label()
        Sub_Code = entry_2.get()
        Sub_Code=Sub_Code.strip().split(",")
        input_5 = entry_5.get()
        df=pd.read_excel(r"Subject data\Data_Set.xlsx")
        cradit=[]
        Teacher_name=[]
        Sub_name=[]
        for i in range(len(df['Subject'])):
            if df['Subject'][i] in Sub_Code:
                Teacher_name.append(df['Teacher'][i])
                cradit.append(df['cradit'][i])
                Sub_name.append(df['Sub_name'][i])

        myex.Gen(Sub_name,Sub_Code,cradit,Teacher_name,input_5)
        message_label.config(text="Task compleated !", fg="green")
        root.after(10000, destroy_test_section)

    root.title("Sec_C Result analyser")
    root.geometry("1280x720")  
    global status_label
    status_label = tk.Label(root, text="Processing", font=("Arial", 14))
    status_label.pack()
    label_2 = tk.Label(root, text="Sub_Code :", font=("Arial", 14))
    label_2.pack(pady=5)
    entry_2 = tk.Entry(root, font=("Arial", 12))
    entry_2.pack(pady=5)
    label_5 = tk.Label(root, text="PDF Title :", font=("Arial", 14))
    label_5.pack(pady=5)
    entry_5 = tk.Entry(root, font=("Arial", 12))
    entry_5.pack(pady=5)


    button_print = tk.Button(root, text="Synthesize", command=Synthesize, font=("Arial", 14))
    button_print.pack(pady=10)
    button_clear = tk.Button(root, text="Clear Screen", command=destroy_test_section)
    button_clear.pack()
    button_open_location = tk.Button(root, text='Open File Location', command=file_location, font=('Arial', 14))
    button_open_location.pack(padx=10, pady=10)

    message_label = tk.Label(root, text="", font=("Arial", 14))
    message_label.pack()

def open_gui2():

    from tkinter import filedialog
    import shutil
    kt.test_key()
    def destroy_test_section():
        button_clear.destroy()
        status_label.destroy()
        label_2.destroy()
        entry_2.destroy()
        label_5.destroy()
        entry_5.destroy()
        button_copy_pdfs.destroy()
        button_open_location.destroy()
        button_print.destroy()
        message_label.destroy()
        status_label.destroy()

    def Get_Data():
        animate_label()
        Sub_Code = entry_2.get()
        Sub_Code=Sub_Code.strip().split(",")
        input_5 = entry_5.get()
        df=pd.read_excel(r"Subject data\Data_Set.xlsx")
        cradit=[]
        Teacher_name=[]
        Sub_name=[]
        for i in range(len(df['Subject'])):
            if df['Subject'][i] in Sub_Code:
                Teacher_name.append(df['Teacher'][i])
                cradit.append(df['cradit'][i])
                Sub_name.append(df['Sub_name'][i])
        import pdf_extract
        myex.Gen(Sub_name,Sub_Code,cradit,Teacher_name,input_5)
        message_label.config(text="Task compleated !", fg="green")
        root.after(10000, destroy_test_section)

    def copy_pdfs():
        source_folder = filedialog.askdirectory(title="Select Source Folder")
        destination_folder = os.path.join(os.getcwd(), "PDF")  # Destination folder

        try:
            if source_folder:  # Check if a source folder is selected
                for file_name in os.listdir(source_folder):
                    if file_name.endswith(".pdf"):
                        source_file_path = os.path.join(source_folder, file_name)
                        shutil.copy(source_file_path, destination_folder)
                message_label.config(text="PDFs copied successfully!", fg="green")
            else:
                message_label.config(text="No source folder selected!", fg="red")
        except Exception as e:
            message_label.config(text=f"Error: {str(e)}", fg="red")

    global status_label
    status_label = tk.Label(root, text="Processing", font=("Arial", 14))
    status_label.pack()

    root.title("Read_From_PDF_File")
    label_2 = tk.Label(root, text="Sub_Code :", font=("Arial", 14))
    label_2.pack(pady=5)
    entry_2 = tk.Entry(root, font=("Arial", 12))
    entry_2.pack(pady=5)
    label_5 = tk.Label(root, text="PDF Title :", font=("Arial", 14))
    label_5.pack(pady=5)
    entry_5 = tk.Entry(root, font=("Arial", 12))
    entry_5.pack(pady=5)
    button_print = tk.Button(root, text="Synthesize", command=Get_Data, font=("Arial", 14))
    button_print.pack(pady=10)
    message_label = tk.Label(root, text="", font=("Arial", 14))
    message_label.pack()
    # Create a button to copy PDFs
    button_copy_pdfs = tk.Button(root, text="Copy PDFs", command=copy_pdfs, font=("Arial", 14))
    button_copy_pdfs.pack(pady=10)

    button_clear = tk.Button(root, text="Clear Screen", command=destroy_test_section)
    button_clear.pack()

    button_open_location = tk.Button(root, text='Open File Location', command=file_location, font=('Arial', 14))
    button_open_location.pack(padx=10, pady=10)

    message_label = tk.Label(root, text="", font=("Arial", 14))
    message_label.pack()

def open_gui3():
    import numpy as np
    kt.test_key()

    def destroy_test_section():
        button_clear.destroy()
        entry_1.destroy()
        button_print.destroy()
        message_label.destroy()
        message_label2.destroy()
        message_label3.destroy()
        message_label4.destroy()
        lable_1.destroy()

    DIR=os.getcwd()
    def Get_Data():
        try:
            input_1 = (entry_1.get())
            print(input_1)
            File_path=DIR+f"\sheets\{input_1}.xlsx"# loacation of the files is : D:\python\database\sheets\1AH22CS149.xlsx
            df=pd.read_excel(File_path)
            df2=pd.read_excel(r"output\output_data_output.xlsx")
            temp=['TOTAL','percentage','SGPA','Grade']
            df3=df2['usn']
            data=[]
            for i in range(len(df3)):
                if input_1==df3[i]:
                    for k in range(4):
                        data.append(df2[temp[k]][i])

            message_label.config(text="PDFs copied successfully!", fg="green")
        except Exception as ex:
            print(ex)
            df=ex
        message_label2.config(text=df, fg="green")
        message_label3.config(text=data, fg="green")

    lable_1=tk.Label(root,text="Enter the USN : ",font = ('Arual,14'))
    lable_1.pack(padx=5)

    message_label2 = tk.Label(root, text="", font=("Arial", 14))
    message_label2.pack(pady=1)

    message_label4 = tk.Label(root, text="T|%|Sgpa|Grade", font=("Arial", 14))
    message_label4.pack(pady=5)

    message_label3 = tk.Label(root, text="", font=("Arial", 14))
    message_label3.pack(pady=10)

    entry_1 = tk.Entry(root, font=("Arial", 12))
    entry_1.pack(pady=5)

    button_print = tk.Button(root, text="Print Inputs", command=Get_Data, font=("Arial", 14))
    button_print.pack(pady=10)

    button_clear = tk.Button(root, text="Clear Screen", command=destroy_test_section)
    button_clear.pack()

    message_label = tk.Label(root, text="", font=("Arial", 14))
    message_label.pack()

def open_gui4():
    kt.test_key()
    import zipfile
    from datetime import datetime

    def destroy_test_section():
        button_clear.destroy()
        button_create_zip.destroy()
        message_label.destroy()
        button_create_zip.destroy()
        button_directory_clear.destroy()
        button_open_location.destroy()
    
    def file_location():
        file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(file_path)
        subprocess.Popen(f'explorer {folder_path}')

    def create_zip():#D:\python\database\output
        folders_to_zip = ["output", "PDF", "sheets"]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"backup_{timestamp}.zip"

        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for folder in folders_to_zip:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.join(folder, '..'))
                        zipf.write(file_path, arcname=arcname)

        message_label.config(text=f"ZIP file '{zip_filename}' created successfully!", fg="green")

    root.title("Create Backup")

    def clear_files():
        create_zip()
        folders_to_clear = ["output", "PDF", "sheets"]
        file_extensions = ["pdf", "xlsx","jpg"]

        for folder in folders_to_clear:
            for ext in file_extensions:
                file_list = glob.glob(f"{folder}/*.{ext}")
                for file in file_list:
                    os.remove(file)

        message_label.config(text="PDF and XLSX files cleared successfully!", fg="green")

    button_create_zip = tk.Button(root, text="Create Backup", command=create_zip)
    button_create_zip.pack(pady=10)

    button_open_location = tk.Button(root, text='Open File Location', command=file_location)
    button_open_location.pack(pady=10)
    button_clear = tk.Button(root, text="Clear Screen", command=destroy_test_section)
    button_clear.pack(pady=5)

    button_directory_clear = tk.Button(root, text="Clear data ", command=clear_files)
    button_directory_clear.pack(pady=5)

    message_label = tk.Label(root, text="", font=("Arial", 12))
    message_label.pack()

root = tk.Tk()
root.geometry("1280x1080")
root.title("Sec_C Result analyser")

logo_image = Image.open("acs.png")
logo_image = logo_image.resize((100, 100))
logo_image = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_image)
logo_label.pack()
# button1 = tk.Button(root, text="Read Excel", command=open_gui1)
# button1.pack(row=0, column=0, padx=10 ,pady=10)
# button2 = tk.Button(root, text=" Read PDF ", command=open_gui2)
# button2.pack(row=0, column=1, padx=10,pady=10)
# button3 = tk.Button(root, text="Data extraction ", command=open_gui3)
# button3.pack(row=0, column=1, padx=10,pady=10)
# button4 = tk.Button(root, text="Open GUI 4", command=open_gui4)
# button4.pack(row=0, column=3, padx=10,pady=10)
button1 = tk.Button(root, text="Read Excel", command=open_gui1)
button1.pack(side=tk.RIGHT, padx=40, pady=10)#side=tk.LEFT, padx=50, pady=10

button2 = tk.Button(root, text="Read PDF", command=open_gui2)
button2.pack(side=tk.RIGHT, padx=40, pady=10)#side=tk.LEFT, padx=50, pady=10

button3 = tk.Button(root, text="Data Extraction", command=open_gui3)
button3.pack(side=tk.RIGHT, padx=40, pady=10)#side=tk.RIGHT, padx=50, pady=10

button4 = tk.Button(root, text="Backup", command=open_gui4)
button4.pack(side=tk.RIGHT, padx=40, pady=10)#side=tk.RIGHT, padx=50, pady=10

# Developer name label
developer_label = tk.Label(root, text="BY : TanishqJM", font=("Arial", 10))
developer_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()