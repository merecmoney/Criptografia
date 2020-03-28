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

def main():
    lines = []

    for line in fileinput.input():
        lines.append(line.strip("\n"))

    createKeys(int(lines[1]), int(lines[2]), int(lines[3]), int(lines[4]))
    #if first line is "E" encrypt, if not desencrypt
    if lines[0] == "E":
        encrypt(int(lines[5]))
    else:
        desencrypt(int(lines[5]))

main()
