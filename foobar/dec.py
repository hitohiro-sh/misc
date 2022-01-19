import base64
encrypted=""
my_eyes=str.encode("")
decoded=base64.b64decode(encrypted)
decrypted=""
for i in range(0,len(decoded)):
    decrypted+=chr((my_eyes[i%len(my_eyes)] ^ decoded[i]))
print(decrypted)