"""
Spoke 'Junction' of Mission Control.
Handles Telnet clients issuing commands for direct service control.
Functions should encompass server -> device interactions.
Direct user interface is expected to be less frequent.
"""
import logging
import pickle

from miniboa import TelnetServer

from spoke.tasks import morse, printer

IDLE_TIMEOUT = 30
CLIENTS = []
SERVICES = {}
ALL_SERVICES = {
    'morse': morse,
    'print': printer,
}
RUN = True
WELCOME = "Mission Control Junction at your service.\n$junction > "

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


def read_services():
    try:
        with open('save/services.pkl', 'rb') as file:
            global SERVICES
            SERVICES = pickle.load(file)
    except FileNotFoundError:
        logging.info("No saved services found.")


def save_services():
    logging.info("Saving services to file.")
    with open('save/vectors.pkl', 'wb') as output:
        pickle.dump(SERVICES, output)


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


def error(client):
    tell(client, "ERROR")


def okay(client):
    tell(client, "OKAY")


def stop(client, args):
    logging.info("Client " + str(client.addrport()) + " requested stop service.")
    save_services()
    global RUN
    RUN = False


def process():
    for client in CLIENTS:
        if client.active and client.cmd_ready:
            interpret(client, client.get_command())
            client.send("$junction > ")


def interpret(client, command: str):
    logging.debug(str(client.addrport()) + " sent " + command)
    components = command.split()
    if len(components) > 0:
        command = components[0].lower()
        args = components[1:]

        call = COMMANDS.get(command)
        if call is None:
            error(client)
            tell(client, "Command '" + command + "' not found.")
        else:
            call(client, args)
    else:
        client.send("")


"""
Client addressable commands
"""


def hlp(client, args):
    if len(args) == 0:
        tell(client, "Available commands: " + ', '.join(map(str, COMMANDS.keys())))
        tell(client, "For details, use help <command>.")
    else:
        help_text = COMMANDS_HELP.get(args[0])
        if help_text is None:
            error(client)
            tell(client, "Command '" + args[0] + "' not found.")
        else:
            tell(client, args[0] + ": " + help_text)


def close(client, args):
    client.active = False
    client.deactivate()


def service(client, args):
    if len(args) < 1:
        tell(client, COMMANDS_HELP.get('service'))
        return
    target = str(args[0])
    if target not in SERVICES.keys():
        error(client)
        tell(client, "Service '" + target + "' not available.")
    else:
        call = SERVICES.get(target).do
        if len(args) > 1:
            call(client, args[1:])
        else:
            call(client)


def discover(client, args):
    build = {}
    for svc in SERVICES.keys():
        build[svc] = SERVICES.get(svc).discover()
    tell(client, str(build))


def enable(client, args):
    if len(args) < 1:
        tell(client, COMMANDS_HELP.get('enable'))
        return
    target = str(args[0])
    if target not in ALL_SERVICES.keys():
        error(client)
        tell(client, "Service '" + target + "' not available to enable.")
    else:
        SERVICES[target] = ALL_SERVICES.get(target)
        okay(client)


"""
Definition of commands
"""
COMMANDS = {
    'help': hlp,
    'end': close,
    'exit': close,
    'stop': stop,
    'service': service,
    'discover': discover,
    'enable': enable,
}

COMMANDS_HELP = {
    'help': "... you've got this one.",
    'end': "Terminates Telnet session.",
    'exit': "Terminates Telnet session.",
    'stop': "Stops the junction service, closing all connections.",
    'service': "Perform a service command.\nservice <name> <*action> <*args>",
    'discover': "Return a formatted list of services and actions.",
    'enable': "Enable a service on the device.\nenable <name> <*args>"
}

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    telnet_server = TelnetServer(
        port=9092,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout=0.5)

    logging.info("Listening on " + str(telnet_server.port))

    read_services()

    while RUN:
        telnet_server.poll()
        process()
        kick_idle()

    logging.info("Shutting down.")
