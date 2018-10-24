"""
'Reception Desk' of Mission Control.
Handles Telnet clients issuing commands for device control.
Functions should encompass client -> server interactions.
This file should NOT handle server -> device interactions.
"""
import logging

from miniboa import TelnetServer

IDLE_TIMEOUT = 120
CLIENTS = []
RUN = True
WELCOME = "Mission Control Reception at your service.\n$reception> "

"""
Server internal operations
"""


def on_connect(client):
    logging.info("Opened connection to " + str(client.addrport()))
    CLIENTS.append(client)
    client.send(WELCOME)


def on_disconnect(client):
    logging.info("Closed connection to " + str(client.addrport()))
    CLIENTS.remove(client)


def kick_idle():
    for client in CLIENTS:
        if client.idle() > IDLE_TIMEOUT:
            logging.info("Kicked for idle: " + str(client.addrport()))
            close(client, None)


def tell_all(message):
    for client in CLIENTS:
        client.send(message + "\n")


def tell(client, message):
    client.send(message + "\n")


def process():
    for client in CLIENTS:
        if client.active and client.cmd_ready:
            interpret(client, client.get_command())
            client.send("$reception > ")


def interpret(client, command: str):
    logging.debug(str(client.addrport()) + "sent " + command)
    components = command.split()
    command = components[0]
    args = components[1:]

    call = COMMANDS.get(command)
    if call is None:
        tell(client, "Unrecognized command '" + command + "'.")
    else:
        call(client, args)


"""
Client addressable commands
"""


def hlp(client, args):
    if len(args) == 0:
        client.send("Available commands: ")
        for command in COMMANDS.keys():
            client.send(command + " ")
        tell(client, "\nFor details, use help <command>.")
    else:
        help_text = COMMANDS_HELP.get(args[0])
        if help_text is None:
            tell(client, "Unrecognized command '" + args[0] + "'.")
        else:
            tell(client, args[0] + ": " + help_text)


def close(client, args):
    client.active = False
    client.deactivate()


def vec(client, args):
    pass


"""
Definition of commands
"""
COMMANDS = {
    'help': hlp,
    'close': close,
    'exit': close,
    'vec': vec,
}

COMMANDS_HELP = {
    'help': "Why would you ask for help using the help command?",
    'close': "Terminates Telnet session.",
    'exit': "Terminates Telnet session.",
}

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    telnet_server = TelnetServer(
        port=9090,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout=0.5)

    logging.info("Listening on " + str(telnet_server.port))

    while RUN:
        telnet_server.poll()
        process()
        kick_idle()

    logging.info("Shutting down.")
