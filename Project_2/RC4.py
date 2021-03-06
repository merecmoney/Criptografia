import fileinput

def swap(array, index1, index2):
    """
    Función para realizar el intercambio de valores dentro de un arreglo.
    Tomamos los índices donde se encuentran los valores que deseamos
    intercambiar, y el arreglo correspondiente, y realizamos el intercambio.

    Args:
        array: Arreglo del que se desea intercambiar los valores.
        index1: índice donde su encuentra el primer valor que deseamos intercambiar
        index2: índice donde su encuentra el segundo valor que deseamos intercambiar
    """
    tmp = array[index1]
    array[index1] = array[index2]
    array[index2] = tmp

def keyScheduling(key):
    """
    Es la implementación del Key Scheduling algorithm para iniciar la permutación
    de la secuencia S. Básicamente es crear la secuencia S para ser utilizada
    más adelante por el Pseudo-random generation algorithm.

    Args:
        key: llave de cifrado
    Returns:
        Secuencia S
    """
    sequence = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + sequence[i] + ord(key[i % len(key)])) % 256
        swap(sequence, i, j)
    return sequence

def pseudoRandomGenerationAlgorithm(sequence, numberOfBytes):
    """
    Función que obtiene los bytes del "Keystream" para posteriormente
    ser utilizado para el cifrado o descifrado.

    Args:
        sequence: Secuencia S generada por el key-scheduling algorithm.
        numberOfBytes: número de bytes del texto a cifrar o descifrar.
    Returns:
        Arreglo con los bytes del "Keystream", cada elemento del arreglo
        está en base decimal y equivale a un byte del keystream.
    """
    i = 0
    j = 0
    keystream = []
    for k in range(numberOfBytes):
        i = (i + 1) % 256
        j = (j + sequence[i]) % 256
        swap(sequence, i, j)
        K = sequence[(sequence[i] + sequence[j]) % 256]
        keystream.append(K)
    return keystream

def createEncryptedText(keystream, text):
    """
    Función para imprimir el mensaje encriptado en hexadecimal haciendo uso del Keystream.
    Aquí simplemente aplicamos a un byte del keystream junto a un byte
    del texto en claro la función XOR,este proceso se hace hasta no tener mas bytes y
    obtenemos los bytes del mensaje cifrado.

    Args:
        keystream: Arreglo con los bytes del keystream
        text: el texto en claro
    """

    for index in range(len(text)):
        #obtener el valor del texto en decimal
        characterValue = ord(text[index])
        #obtener 1 byte del keystream
        kValue = keystream[index]
        #realizar la operación XOR
        encryptedCharacter = characterValue ^ kValue
        #imprimir el valor hexadecimal siempre con dos digítos(lo que equivale a un byte)
        #:02X sirve para imprimir el valor en hexadecimal y con
        #dos digítos, por ejemplo si el valor del resultado de la XOR
        #fue "A"  se pone un cero adelante es decir que imprima "0A"
        #para que forme los dos digítos hexadecimales
        print("{:02X}".format(encryptedCharacter), end = '')
    print()

def createDesencyptedText(keystream, encryptedText):
    """
    Función para imprimir el mensaje descifrado en ASCII
    haciendo uso del Keystream. Aquí simplemente aplicamos a un byte del
    keystream junto a un byte del texto cifrado la función XOR,
    este proceso se hace hasta no tener mas bytes y obtenemos los bytes
    del mensaje descifrado.

    Args:
        keystream: Arreglo con los bytes del keystream
        encryptedText: el mensaje cifrado
    """
    for index in range(len(encryptedText)):
        characterValue = encryptedText[index]
        #obtener 1 byte del keystream
        kValue = keystream[index]
        #realizar la operación XOR
        desencryptedCharacter = characterValue ^ kValue
        print("{}".format(chr(desencryptedCharacter)), end = '')
    print()


def encryptRC4(key, text):
    """
    Función para realizar el encriptado de un texto en claro con el algoritmo RC4.
    Esta función basicamente es la unión de las funciones keyScheduling,
    pseudoRandomGenerationAlgorithm y createEncryptedText.

    Args:
        key: llave de cifrado
        text: texto en claro
    """
    sequence = keyScheduling(key)
    keystream = pseudoRandomGenerationAlgorithm(sequence, len(text))
    createEncryptedText(keystream, text)

def desencryptRC4(key, text):
    """
    Función para realizar el desencriptado de un texto cifrado con el algoritmo RC4.
    Esta función basicamente es la unión de las funciones keyScheduling,
    pseudoRandomGenerationAlgorithm y createDesencyptedText.

    Args:
        key: llave de cifrado
        text: mensaje cifrado
    """
    #obtener los bytes del mensaje cifrado en hexadecimal
    #cada elemento del arreglo es un byte
    hexCharacters = ['0x' + (text[index: index+2]) for index in range(0, len(text), 2)]
    #obtener los bytes del mensaje cifrado en decimal
    # cada elemento del arreglo es un byte
    decimalCharacters = [int(hexCharacter, 16) for hexCharacter in hexCharacters]
    sequence = keyScheduling(key)
    keystream = pseudoRandomGenerationAlgorithm(sequence, len(decimalCharacters))
    createDesencyptedText(keystream, decimalCharacters)

def main():
    lines = []

    for line in fileinput.input():
        lines.append(line)

    for index in range(0, len(lines), 2):
        key = (lines[index]).replace("\n", "")
        text = (lines[index + 1]).replace("\n", "")
        encryptRC4(key, text)

main()
