import os
import base64
import hashlib
import tkinter as tk
os.chdir(os.path.dirname(os.path.abspath(__file__)))
root = tk.Tk()
root.geometry("480x640")
root.title("Enter the Produck key")
def hash_bytes(byte_data):
    sha256_hash = hashlib.sha256(byte_data).digest()
    encoded = base64.b64encode(sha256_hash)[:12].decode('utf-8')
    return encoded
c = 0
def check():
    with open("Licence", "rb") as file:
        encrypted_product_key = file.read()
        original_string = encrypted_product_key
        encrypted_string = hash_bytes(original_string)

    input_key = entry_1.get().strip()  
    if input_key == encrypted_string:
        with open("public_key.pem", "w") as file:
                 file.write(encrypted_string)
        message_label.config(text="Key validated!", fg="green")
        root.after(1000, out)
    else:
        message_label.config(text="Invalid Key!", fg="red")
        global c
        c += 1
        if c > 3:
            message_label.config(text="Executing the Anti-piracy Algorithm", fg="red")
            root.after(500, anti)
            root.after(1000, out)

def out():
    root.destroy()

def anti():
    try:
        os.remove("gui1 copy.py")
        os.remove("gui2 copy.py")
        os.remove("gui3 copy.py")
        # root.after(500,out)
    except Exception as ex:
        print("Execution of anti-piracy algorithm failed:", ex)

label_1 = tk.Label(root, text="Enter Key: ", font=('Arial', 14))
label_1.pack(padx=5)

message_label2 = tk.Label(root, text="", font=("Arial", 14))
message_label2.pack()

entry_1 = tk.Entry(root, font=("Arial", 12))
entry_1.pack(pady=5)

button_print = tk.Button(root, text="Validate", command=check, font=("Arial", 14))
button_print.pack(pady=10)

message_label = tk.Label(root, text="", font=("Arial", 14))
message_label.pack()
with open("public_key.pem", "r") as file:
        data=(file.read())
        with open("Licence", "rb") as file:
            encrypted_product_key = hash_bytes(file.read())
            if data==encrypted_product_key:
                out()
            else:
                print("Key not matched or changed by the user .")
root.mainloop()
