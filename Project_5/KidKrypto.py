import fileinput

publicKey = None
privateKey = None

def createKeys(a, b, A, B):
    """
    Function to create public and private Key.
    Args:
        a: random positive Integer
        b: random positive Integer
        A: random positive Integer
        B: random positive Integer
    """
    global publicKey, privateKey

    M = a*b - 1
    e = A*M + a
    d = B*M + b
    n = (e*d -1) // M

    publicKey = (n,e)
    privateKey = d

def encrypt(message):
    """
    Function to create ciphertext given a message using the public key.
    Args:
        message: message to encrypt
    Returns:
        If message is less than n, ciphertext is returned
        If not return -1
    """
    # Message Integer must be less than n
    if message < publicKey[0]:
        #ciphertext
        y = (message*publicKey[1]) % publicKey[0]
        print(y)
        return y
    return -1

def desencrypt(ciphertext):
    """
    Function to get plain text given a ciphertext using the private key.
    Args:
        ciphertext: ciphertext to desencrypt
    Returns:
        plaintext
    """
    plainText = (ciphertext*privateKey) % publicKey[0]
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
