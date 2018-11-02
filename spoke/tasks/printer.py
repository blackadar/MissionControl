def do(client, text):
    print(client.addrport() + ": " + ' '.join(map(str, text)))
    client.okay(client)


def discover():
    return 'text'


def status():
    return 'READY'
