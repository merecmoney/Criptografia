import fileinput

S = [41, 46, 67, 201, 162, 216, 124, 1, 61, 54, 84, 161, 236, 240, 6,
  19, 98, 167, 5, 243, 192, 199, 115, 140, 152, 147, 43, 217, 188,
  76, 130, 202, 30, 155, 87, 60, 253, 212, 224, 22, 103, 66, 111, 24,
  138, 23, 229, 18, 190, 78, 196, 214, 218, 158, 222, 73, 160, 251,
  245, 142, 187, 47, 238, 122, 169, 104, 121, 145, 21, 178, 7, 63,
  148, 194, 16, 137, 11, 34, 95, 33, 128, 127, 93, 154, 90, 144, 50,
  39, 53, 62, 204, 231, 191, 247, 151, 3, 255, 25, 48, 179, 72, 165,
  181, 209, 215, 94, 146, 42, 172, 86, 170, 198, 79, 184, 56, 210,
  150, 164, 125, 182, 118, 252, 107, 226, 156, 116, 4, 241, 69, 157,
  112, 89, 100, 113, 135, 32, 134, 91, 207, 101, 230, 45, 168, 2, 27,
  96, 37, 173, 174, 176, 185, 246, 28, 70, 97, 105, 52, 64, 126, 15,
  85, 71, 163, 35, 221, 81, 175, 58, 195, 92, 249, 206, 186, 197,
  234, 38, 44, 83, 13, 110, 133, 40, 132, 9, 211, 223, 205, 244, 65,
  129, 77, 82, 106, 220, 55, 200, 108, 193, 171, 250, 36, 225, 123,
  8, 12, 189, 177, 74, 120, 136, 149, 139, 227, 99, 232, 109, 233,
  203, 213, 254, 59, 0, 29, 57, 242, 239, 183, 14, 102, 88, 208, 228,
  166, 119, 114, 248, 235, 117, 75, 10, 49, 68, 80, 180, 143, 237,
  31, 26, 219, 153, 141, 51, 159, 17, 131, 20]

def padding(messageArray):
    """
    Function to add padding to message until it is a multiple of 16 bytes
    Args:
        messageArray: list with message byte values
    Returns:
        message padded as a list object, every element is a byte in decimal base
    """
    lengthMessage = len(messageArray)
    byteToAddToMessage = 16 - (lengthMessage % 16)
    for byte in range(byteToAddToMessage):
        messageArray.append(byteToAddToMessage)
    return messageArray

def checksum(paddedMessage):
    """
    Function to add checksum(16 bytes) to padded message
    Args:
        paddedMessage: list with padded message byte values
    Returns:
        padded message with checksum as a list object, every element is a byte in decimal base
    """
    lengthPaddedMessage = len(paddedMessage)
    checksum = [0 for i in range(16)]
    L = 0
    for i in range(lengthPaddedMessage//16):
        for j in range(16):
            c = paddedMessage[16*i + j]
            checksum[j] = checksum[j] ^ S[c ^ L]
            L = checksum[j]

    return paddedMessage + checksum

def createHash(message):
    """
    Function to create a hash from message
    Args:
        message: list with message byte values
    Returns:
        a hash of 16 bytes as a list object, , every element is a byte in decimal base
    """
    X = [0 for i in range(48)]
    lengthMessage = len(message)
    for i in range(lengthMessage//16):
        for j in range(16):
            X[j+16] = message[16*i + j]
            X[j+32] = X[j+16] ^ X[j]
        t = 0
        for j in range(18):
            for k in range(48):
                t = X[k] ^ S[t]
                X[k] = t
            t = (t + j)%256
    return X[:16]

def getHash(message):
    """
    Function to get a hash string from message
    Args:
        message: list with message byte values
    Returns:
        a hash of 16 bytes as a hexadecimal string
    """
    hashString = []
    for byte in createHash(message):
        hashString.append("{:02x}".format(byte))
    return ''.join(hashString)

def MD2(message):
    """
    Function to get MD2(Message Digest 2) from a message
    Args:
        message: String
    Returns:
        hash string of the message
    """
    # array to convert messsage characters to decimal values, every element
    # is a byte in decimal base
    messageArray = [ord(character) for character in message]
    paddedMessage = padding(messageArray)
    paddedMessage = checksum(paddedMessage)
    return getHash(paddedMessage)

def main():
    lines = []

    for line in fileinput.input():
        lines.append(line.strip("\n"))

    for line in lines:
        if line == "\"\"":
            print(MD2(""))
            continue
        print(MD2(line))

main()
