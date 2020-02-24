import fileinput

def initialPermutation(text):
    """
    Function to make initial permutation given a text.
    Permute bits of text with the following order:
        b1 b5 b2 b0 b3 b7 b4 b6

    Args:
        text: 8 bit String

    Returns:
        List with permuted Bits
    """
    permutation = [1, 5, 2, 0, 3, 7, 4, 6]
    permutedText = []
    for index in range(8):
        bit = int(text[permutation[index]])
        permutedText.append(bit)

    return permutedText

def inversePermutation(bits):
    """
    Function to make inverse permutation given 8 bits.
    Permute bits with the following order:
        b3 b0 b2 b4 b6 b1 b7 b5

    Args:
        bits: List with 8 bits

    Returns:
        List with permuted Bits
    """
    permutation = [3, 0, 2, 4, 6, 1, 7, 5]
    inverseBits = []
    for index in range(8):
        bit = int(bits[permutation[index]])
        inverseBits.append(bit)

    return inverseBits

def createKeys(key):
    """
    Function to create subkeys given a key.
    Given a key, create two subkeys.

    Args:
        key: 10 bit String

    Returns:
        List with subkey 1 at index 0 and subkey 2 at index 1
    """
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
    """
    Function to get halves of an array.
    Given an array, return left and right half.

    Args:
        array: list with bits

    Returns:
        List with left half at index 0 and right half at index 1
    """
    halfIndex = len(array) // 2
    halves = []
    # create left half
    halves.append(array[:halfIndex])
    # create right half
    halves.append(array[halfIndex:])

    return halves

def expand4bitsTo8(bits):
    """
    Function to expand given 4 bits to 8 bits.
    Expand bits with the following order:
        b3 b0 b1 b2 b1 b2 b3 b0

    Args:
        bits: list with 4 bits

    Returns:
        List with eight bits
    """
    transformation = [3, 0, 1, 2, 1, 2, 3, 0]
    expansion = []
    for index in range(8):
        expansion.append(bits[transformation[index]])

    return expansion

def applySboxes(halves):
    """
    Function to apply SBoxes to 8 bits and return 4 bits.
    This applies to left half SBox 0 and to right one SBox 1.

    Args:
        halves: List with two list of bits, left Half is at index 0
        and right Half is at index 1

    Returns:
        List with 4 bits
    """

    # define numbers to used inside sbox
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

    leftHalf = halves[0]
    rightHalf = halves[1]
    # row and column for SBox 0
    rowSbox0 = int(str(leftHalf[0]) + str(leftHalf[3]), 2)
    columnSbox0 = int(str(leftHalf[1]) + str(leftHalf[2]), 2)
    # row and column for SBox 1
    rowSbox1 = int(str(rightHalf[0]) + str(rightHalf[3]), 2)
    columnSbox1 = int(str(rightHalf[1]) + str(rightHalf[2]), 2)
    # concatenate two lists with 2 bits and returns list with 4 bits
    return Sbox0[rowSbox0][columnSbox0] + Sbox1[rowSbox1][columnSbox1]

def mixingFunction(rightHalf, subKey):
    """
    Function to apply procedure of mixing Function.
    Mixing Function basically consists of 5 steps:
        - expansion of 4 bits(right Half) to 8 bits
        - apply XOR of 8 bits of last step with 8 bits of subkey
        - apply Sboxes to bits of last step
        - apply final permutation to 4 bits of last step
        - return 4 bits of last step

    Args:
        rightHalf: list with 4 bits
        subkey: List with 8 bits

    Returns:
        List with 4 bits
    """
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
    """
    Function to apply Feistel Operation and return 8 bits.
    Feistel Operation basically consists of 4 steps:
        - get Halves of given text
        - apply mixing function to right Half using given subkey
        - XOR 4 bits of last step with 4 bits of left Half
        - return 8 bits
    Args:
        text: list with 8 bits
        subkey: list with 8 bits to be used in mixing Function

    Returns:
        List with 8 bits
    """
    # left half at index 0, right one at index 1
    halves = getHalves(text)
    leftHalf = halves[0]
    newLeftHalf = []
    rightHalf = halves[1]
    newRightHalf = mixingFunction(rightHalf, subKey)
    # XOR between left Half and right half after applying the function
    for index in range(4):
        # XOR bit by bit
        newLeftHalf.append(leftHalf[index] ^ newRightHalf[index])
    return newLeftHalf + rightHalf

def simplifiedDES(plainText, subkey1, subkey2):
    """
    Function to apply simplified DES to a plain text given 2 subkeys
    simplifies DES basically consists of 5 Steps:
        - Initial permutation
        - Feistel operation using subkey K1
        - Switch left and right halves
        - Feistel operation using subkey K2
        - Inverse permutation

    Args:
        plainText: 8 bit String
        subkey1 : list with 4 bits
        subkey2 : list with 4 bits

    Returns:
        List with 8 bits
    """
    # create initial permutation for Text
    initialText = initialPermutation(plainText)
    feistelStep = feistelOperation(initialText, subkey1)
    halves = getHalves(feistelStep)
    swapedHalves = halves[1] + halves[0]
    feistelStep = feistelOperation(swapedHalves, subkey2)
    return inversePermutation(feistelStep)

def encryptSimplifiedDES(plainText, key):
    """
    Function to encrypt a plain Text with a given Key

    Args:
        plainText: 8 bit String
        key : 10 bit String

    Returns:
        8 bit String that represents encrypted text
    """
    # get Keys(Key 1 and Key 2)
    keys = createKeys(key)
    return simplifiedDES(plainText, keys[0], keys[1])

def desencryptSimplifiedDES(plainText, key):
    """
    Function to encrypt a plain Text with a given Key

    Args:
        plainText: 8 bit String
        key : 10 bit String

    Returns:
        8 bit String that represents desencrypted text
    """
    # get Keys(Key 1 and Key 2)
    keys = createKeys(key)
    # keys in reverse order
    return simplifiedDES(plainText, keys[1], keys[0])

def main():
    lines = []

    for line in fileinput.input():
        lines.append(line)

    for index in range(0, len(lines), 3):
        encryptOrDecrypt = (lines[index]).replace("\n", "")
        key = (lines[index + 1]).replace("\n", "")
        text = (lines[index + 2]).replace("\n", "")
        if encryptOrDecrypt == "E":
            output = encryptSimplifiedDES(text, key)
        else:
            output = desencryptSimplifiedDES(text, key)
        for bit in output:
            print(bit, end = "")
        print()

main()
