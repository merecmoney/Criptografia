import fileinput

publicKey = None
privateKey = None

def createKeys(a, b, A, B):
    global publicKey, privateKey

    M = a*b - 1
    e = A*M + a
    d = B*M + b
    n = (e*d -1) // M

    publicKey = (n,e)
    privateKey = d

def encrypt(message):
    if message < publicKey[0]:
        #ciphertext
        y = (message*publicKey[1]) % publicKey[0]
        print(y)
    return y

def desencrypt(cipherText):
    plainText = (cipherText*privateKey) % publicKey[0]
    print(plainText)
    return plainText

createKeys(3, 4, 5, 6)
desencrypt(encrypt(200))

createKeys(47, 22, 11, 5)
desencrypt(encrypt(4356))
