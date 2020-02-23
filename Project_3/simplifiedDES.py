numberZero = [0, 0]
numberOne = [0, 1]
numberTwo = [1, 0]
numberThree = [1, 1]

Sbox0 = [
    [numberOne, numberZero, numberThree, numberTwo],
    [numberThree, numberTwo, numberOne, numberZero],
    [numberZero, numberTwo, numberOne, numberThree],
    [numberThree, numberOne, numberThree, numberTwo]
]

Sbox1 = [
    [numberZero, numberOne, numberTwo, numberThree],
    [numberTwo, numberZero, numberOne, numberThree],
    [numberThree, numberZero, numberOne, numberZero],
    [numberTwo, numberOne, numberZero, numberThree]
]


def initialPermutation(plainText):
    permutation = [1, 5, 2, 0, 3, 7, 4, 6]
    permutedPlainText = []
    for index in range(8):
        bit = int(plainText[permutation[index]])
        permutedPlainText.append(bit)

    return permutedPlainText

def inversePermutation(bits):
    permutation = [3, 0, 2, 4, 6, 1, 7, 5]
    inverseBits = []
    for index in range(8):
        bit = int(bits[permutation[index]])
        inverseBits.append(bit)

    return inverseBits

def createKeys(key):
    keys = [[], []]
    permutationForKey1 = [0, 6, 8, 3, 7, 2, 9, 5]
    permutationForKey2 = [7, 2, 5, 4, 9, 1, 8, 0]
    for index in range(8):
        # create key 1
        bitKey1 = int(key[permutationForKey1[index]])
        keys[0].append(bitKey1)
        # create key 2
        bitKey2 = int(key[permutationForKey2[index]])
        keys[1].append(bitKey2)

    return keys


def getHalves(array):
    halfIndex = len(array) // 2
    halves = []
    # create left half
    halves.append(array[:halfIndex])
    # create right half
    halves.append(array[halfIndex:])

    return halves

def expand4bitsTo8(bits):
    transformation = [3, 0, 1, 2, 1, 2, 3, 0]
    expansion = []
    for index in range(8):
        expansion.append(bits[transformation[index]])

    return expansion

def applySboxes(halves):
    leftHalf = halves[0]
    rightHalf = halves[1]
    rowSbox0 = int(str(leftHalf[0]) + str(leftHalf[3]), 2)
    columnSbox0 = int(str(leftHalf[1]) + str(leftHalf[2]), 2)
    rowSbox1 = int(str(rightHalf[0]) + str(rightHalf[3]), 2)
    columnSbox1 = int(str(rightHalf[1]) + str(rightHalf[2]), 2)

    return Sbox0[rowSbox0][columnSbox0] + Sbox1[rowSbox1][columnSbox1]

def mixingFunction(rightHalf, subKey):
    mixedBits = []
    expansion = expand4bitsTo8(rightHalf)
    # XOR between Expansion and Subkey
    for index in range(8):
        # XOR bit by bit
        mixedBits.append(expansion[index] ^ subKey[index])
    # apply SBoxes
    appliedSboxes = applySboxes(getHalves(mixedBits))
    # apply final permutation
    permutation = [1, 3, 2, 0]
    bits = []
    for index in range(4):
        bits.append(appliedSboxes[permutation[index]])

    return bits

def feistelOperation(text, subKey):
    # left half at index 0, right one at index 1
    halves = getHalves(text)
    leftHalf = halves[0]
    newLeftHalf = []
    rightHalf = halves[1]
    newRightHalf = mixingFunction(halves[1], subKey)
    # XOR between left Half and right half after applying the function
    for index in range(4):
        # XOR bit by bit
        newLeftHalf.append(leftHalf[index] ^ newRightHalf[index])
    return newLeftHalf + rightHalf

def simplifiedDES(plainText, key1, key2):
    # create initial permutation for Text
    initialText = initialPermutation(plainText)
    feistelStep = feistelOperation(initialText, key1)
    halves = getHalves(feistelStep)
    swapedHalves = halves[1] + halves[0]
    feistelStep = feistelOperation(swapedHalves, key2)
    return inversePermutation(feistelStep)

def encryptSimplifiedDES(plainText, key):
    # get Keys(Key 1 and Key 2)
    keys = createKeys(key)
    return simplifiedDES(plainText, keys[0], keys[1])

def desencryptSimplifiedDES(plainText, key):
    # get Keys(Key 1 and Key 2)
    keys = createKeys(key)
    # keys in reverse order
    return simplifiedDES(plainText, keys[1], keys[0])

print(encryptSimplifiedDES("01010101", "0000011111"))
print(encryptSimplifiedDES("10100101", "0010010111"))
print(encryptSimplifiedDES("00000000", "0000000000"))
print(encryptSimplifiedDES("11111111", "1111111111"))

print(desencryptSimplifiedDES("11000100", "0000011111"))
print(desencryptSimplifiedDES("00110110", "0010010111"))
print(desencryptSimplifiedDES("11110000", "0000000000"))
print(desencryptSimplifiedDES("00001111", "1111111111"))
