import hashlib
import base64
import sys
import gui4
# from . import gui4

class test_key:
    def __init__(self):
        with open("public_key.pem", "r") as file:
            data=(file.read())
            with open("Licence", "rb") as file:
                encrypted_product_key = self.hash_bytes(file.read())
                if data==encrypted_product_key:
                    # print("matched")
                    pass
                else:
                    gui4.anti()
                    print("Key not matched !")
                    print("Exicuting safty algorithum ... ")
                    sys.exit()
    def hash_bytes(self,byte_data):
        sha256_hash = hashlib.sha256(byte_data).digest()
        encoded = base64.b64encode(sha256_hash)[:12].decode('utf-8')
        return encoded

