import fileinput

def createLettersDictionary(tableau):
    """Esta función es usada para dado un tableau poder crear un diccionario
    que nos permita obtener la posición de una letra dentro del tableau.

    El diccionario tiene la siguiente estructura:
    - la key es una letra del tableau
    - el valor es una tupla (fila, columna)
    Por ejemplo:

        key: a, value: (0,0)

    Args: el tableau del cuál se creará el diccionario.
    Returns: Un diccionario que tiene como claves las letras del tableau
    y valores las posiciones fila-columna de cada letra.
    """

    lettersDictionary = {}
    numberRows = len(tableau)
    numberColumns = len(tableau[0])
    #iteración del tableau para crear el diccionario
    for row in range(numberRows):
        for column in range(numberColumns):
            lettersDictionary[tableau[row][column]] = (row, column)
    return lettersDictionary

#tableau para la llave ENCRYPT
tableau = [["E", "N", "C", "R", "Y"],
["P", "T", "A", "B", "D"],
["F", "G", "H", "I", "K"],
["L", "M", "O", "Q", "S"],
["U", "V", "W", "X", "Z"]]

#diccionario que contiene las letras del tableau y como valores
#las posiciones fila-colunma de cada letra
lettersDictionary = createLettersDictionary(tableau)

def getCoordinateByLetter(letter):
    """Función que nos permite obtener la posición de la letra dentro
    del tableau

    Args: Letra de la cuál se desea obtener su posición
    Returns: Tupla (fila, columna)
    """
    return lettersDictionary[letter]

def getLetterByCoordinate(row, column):
    """Función que nos permite obtener una letra dada la fila
    y columna

    Args: Fila y columna en donde se encuentra la letra dentro del tableau
    Returns: Letra correspondiente a la posición dada
    """
    return tableau[row][column]

def createEncodedMessageEncrypt(text):
    """Función que crea el mensaje codificado dado el texto a encriptar.
    Por ejemplo la codificación del "MEETMEONFRIDAY" sería:
    3 0 0 1 3 0 3 0 2 0 2 1 1 0 1 0 0 1 1 0 2 1 0 3 3 4 2 4

    Args: texto a codificar
    Returns: secuencia de números que representa el mensaje codificado
    """

    rowString = []
    columnString = []

    for letter in text:
        #fila y columna de una letra dentro del tableau
        letterRowColumn = getCoordinateByLetter(letter)
        rowString.append(letterRowColumn[0])
        columnString.append(letterRowColumn[1])
    return rowString + columnString

def createEncryptedMessage(encodedMessage):
    """Función que crea el mensaje encriptado dado el texto a encriptar
    codificado

    Por ejemplo para el texto codicado:
    3 0 0 1 3 0 3 0 2 0 2 1 1 0 1 0 0 1 1 0 2 1 0 3 3 4 2 4
    El mensaje encriptado sería:
    LNLLFGPPNPGRSK

    Args: texto codificado
    Returns: Cadena que representa el mensaje encriptado
    """

    encryptedMessage = ""
    #iteracioń que toma de dos en dos sobre el texto codificado para
    #obtener el texto encriptado
    for index in range(0, len(encodedMessage), 2):
        rowIndex = encodedMessage[index]
        columnIndex = encodedMessage[index + 1]
        encryptedMessage += getLetterByCoordinate(rowIndex, columnIndex)
    return encryptedMessage

def getEncryptedMessage(text):
    """Función que recibe un texto y regresa regresa el mensaje encriptado

    Args: Texto a encriptar
    Returns: Mensaje encriptado
    """
    #Mensaje codificado
    encodedMessage = createEncodedMessageEncrypt(text)
    return createEncryptedMessage(encodedMessage)

def createEncodedMessageDesencrypt(text):
    """Función que crea el mensaje codificado dado el texto a desencriptar.
    Por ejemplo la codificación del "LNLLFGPPNPGRSK" sería:
    3 0 0 1 3 0 3 0 2 0 2 1 1 0 1 0 0 1 1 0 2 1 0 3 3 4 2 4

    Args: texto a codificar
    Returns: secuencia de números que representa el mensaje codificado
    """
    encodedMessage = []

    for letter in text:
        #fila y columna de una letra dentro del tableau
        letterRowColumn = getCoordinateByLetter(letter)
        encodedMessage.append(letterRowColumn[0])
        encodedMessage.append(letterRowColumn[1])
    return encodedMessage

def createDesencryptedMessage(encodedMessage):
    """Función que crea el mensaje desencriptado dado el texto a desencriptar
    codificado

    Por ejemplo para el texto codificado:
    3 0 0 1 3 0 3 0 2 0 2 1 1 0 1 0 0 1 1 0 2 1 0 3 3 4 2 4
    El mensaje desencriptado sería:
    MEETMEONFRIDAY

    Args: texto codificado
    Returns: Cadena que representa el mensaje desencriptado
    """

    #variable que tiene el índice medio que nos dice
    #desde dónde inicia la mitad del texto codificado
    middleIndex = len(encodedMessage)//2
    desencryptedMessage = ""
    for index in range(middleIndex):
        row = encodedMessage[index]
        column = encodedMessage[middleIndex + index]
        desencryptedMessage += getLetterByCoordinate(row, column)
    return desencryptedMessage

def getDesencryptedMessage(text):
    """Función que recibe un texto y regresa regresa el mensaje desencriptado

    Args: Texto a desencriptar
    Returns: Mensaje desencriptado
    """

    #Mensaje codificado
    encodedMessage = createEncodedMessageDesencrypt(text)
    return createDesencryptedMessage(encodedMessage)

lines = []

for line in fileinput.input():
    lines.append(line)

for index in range(0, len(lines), 2):
    text = (lines[index + 1]).replace("\n", "")
    if lines[index] == "ENCRYPT\n":
        #quitamos espacios a la cadena a encriptar
        text = (text).replace(" ", "")
        print(getEncryptedMessage(text))
    else:
        print(getDesencryptedMessage(text))
