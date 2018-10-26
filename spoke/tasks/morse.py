def do(client, text):
    build = ""
    for word in text:
        build = build + encode(word)
    # TODO: Blink an LED
    print(build)
    client.okay(client)


def discover():
    return 'text'


def encode(word):
    word = word.upper()
    build = ""
    for c in word:
        switcher = {
            'A': ".- ",
            'B': "-... ",
            'C': "-.-. ",
            'D': "-.. ",
            'E': ". ",
            'F': "..-. ",
            'G': "--. ",
            'H': ".... ",
            'I': ".. ",
            'J': ".--- ",
            'K': "-.- ",
            'L': ".-.. ",
            'M': "-- ",
            'N': "-. ",
            'O': "--- ",
            'P': ".--. ",
            'Q': "--.- ",
            'R': ".-. ",
            'S': "... ",
            'T': "- ",
            'U': "..- ",
            'V': "...- ",
            'W': ".-- ",
            'X': "-..- ",
            'Y': "-.-- ",
            'Z': "--.. ",
            '1': ".---- ",
            '2': "..--- ",
            '3': "...-- ",
            '4': "....- ",
            '5': "..... ",
            '6': "-.... ",
            '7': "--... ",
            '8': "---.. ",
            '9': "----. ",
            '0': "----- ",
            '.': ".-.-.-\n",
            '!': "-.-.--\n",
            '?': "..--..\n",
            ',': "--..-- ",
            ' ': "/ ",
        }
        char = switcher.get(c, "")
        if char is not None:
            build = build + char
    build = build + ".-.-"
    return build
