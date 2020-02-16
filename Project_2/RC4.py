def swap(array, index1, index2):
    tmp = array[index1]
    array[index1] = array[index2]
    array[index2] = tmp

def keyScheduling(key):
    sequence = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + sequence[i] + ord(key[i % len(key)])) % 256
        swap(sequence, i, j)
    return sequence

def pseudoRandomGenerationAlgorithm(sequence, textLenght):
    i = 0
    j = 0
    bits = []
    for k in range(textLenght):
        i = (i + 1) % 256
        j = (j + sequence[i]) % 256
        swap(sequence, i, j)
        K = sequence[(sequence[i] + sequence[j]) % 256]
        bits.append(K)
    return bits

def createEncryptedText(keystream, text):
    for index in range(len(text)):
        characterValue = ord(text[index])
        kValue = keystream[index]
        encryptedCharacter = characterValue ^ kValue
        print("{:02X}".format(encryptedCharacter), end = '')
    print()

def createDesencyptedText(keystream, text):
    for index in range(len(text)):
        characterValue = text[index]
        kValue = keystream[index]
        desencryptedCharacter = characterValue ^ kValue
        print("{}".format(chr(desencryptedCharacter)), end = '')
    print()


def encryptRC4(key, text):
    sequence = keyScheduling(key)
    keystream = pseudoRandomGenerationAlgorithm(sequence, len(text))
    createEncryptedText(keystream, text)

def desencryptRC4(key, text):
    hexCharacters = ['0x' + (text[index: index+2]) for index in range(0, len(text), 2)]
    decimalCharacters = [int(hexCharacter, 16) for hexCharacter in hexCharacters]
    sequence = keyScheduling(key)
    keystream = pseudoRandomGenerationAlgorithm(sequence, len(decimalCharacters))
    createDesencyptedText(keystream, decimalCharacters)

encryptRC4("Key", "Plaintext")
encryptRC4("Wiki", "pedia")
encryptRC4("Secret", "Attack at dawn")
desencryptRC4("Key", "BBF316E8D940AF0AD3")
desencryptRC4("Wiki", "1021BF0420")
desencryptRC4("Secret", "45A01F645FC35B383552544B9BF5")
