"""
'Reception Desk' of Mission Control.
Handles Telnet clients issuing commands for device control.
Functions should encompass client -> server interactions.
This file should NOT handle server -> device interactions.
"""
import logging
import os
import pickle
import threading

from miniboa import TelnetServer

from hub.vector import Vector, Group

IDLE_TIMEOUT = 120
CLIENTS = []
VECTORS = {}
GROUPS = {}
RUN = True
WELCOME = "Mission Control Reception at your service.\n$reception > "

"""
Server state i/o operations
"""


def read_vectors():
    try:
        with open('save/vectors.pkl', 'rb') as file:
            global VECTORS
            VECTORS = pickle.load(file)
    except FileNotFoundError:
        logging.info("No saved vectors found.")


def verify_path():
    if not os.path.exists('save'):
        os.makedirs('save')


def read_groups():
    try:
        with open('save/groups.pkl', 'rb') as file:
            global GROUPS
            GROUPS = pickle.load(file)
    except FileNotFoundError:
        logging.info("No saved groups found.")


def save_vectors():
    logging.info("Saving vectors to file.")
    verify_path()
    with open('save/vectors.pkl', 'wb') as output:
        pickle.dump(VECTORS, output)


def save_groups():
    logging.info("Saving groups to file.")
    verify_path()
    with open('save/groups.pkl', 'wb') as output:
        pickle.dump(GROUPS, output)


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
            logging.info("Kicked " + str(client.addrport()))
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
    save_vectors()
    save_groups()
    global RUN
    RUN = False


def process():
    for client in CLIENTS:
        if client.active and client.cmd_ready:
            thread = threading.Thread(target=interpret, args=(client, client.get_command()))
            thread.start()


def interpret(client, command: str):
    logging.debug(str(client.addrport()) + " issued " + command)
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
    client.send("$reception > ")


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


def gvlist(client, args):
    if args is None or len(args) == 0:
        tell(client, str((len(VECTORS) + len(GROUPS))) + " addressable entities.")
        tell(client, str(len(VECTORS)) + " vector(s), " + str(len(GROUPS)) + " group(s).")
        client.send("VECTORS: ")
        for vector in VECTORS.values():
            client.send("{" + vector.name + "}")
        client.send("\n")
        client.send("GROUPS: ")
        for group in GROUPS.values():
            client.send("{" + group.name + "}")
        client.send("\n")
    else:
        target = args[0]
        if GROUPS.get(target) is not None:
            services = GROUPS.get(target).services
            if services is not None:
                tell(client, "SERVICES: " + str(services))
            else:
                tell(client, "SERVICES: NONE")
            client.send("VECTORS: ")
            for vector in GROUPS.get(target).vectors:
                client.send("{" + vector.name + "}")
            client.send("\n")
        elif VECTORS.get(target) is not None:
            services = VECTORS.get(target).services
            if services is not None:
                tell(client, "SERVICES: " + str(services))
            else:
                tell(client, "SERVICES: NONE")
        else:
            error(client)
            tell(client, "Entity '" + str(target) + "' does not exist.")


def add(client, args):
    if len(args) < 2:
        tell(client, COMMANDS_HELP.get('add'))
        return
    if str(args[0]).lower() == 'vector':
        if len(args) != 4:
            tell(client, COMMANDS_HELP.get('add'))
            return
        else:
            try:
                VECTORS[args[1]] = Vector(str(args[2]), str(args[3]), str(args[1]))
                logging.info("Created vector '" + args[1] + "'.")
                okay(client)
            except ConnectionError:
                error(client)
                tell(client, "Unable to connect to " + str(args[2]) + ".")

    elif str(args[0]).lower() == 'group':
        err = False
        construct = Group(list(), args[1])
        if len(args) > 2:
            for vector_name in args[2:]:
                vector = VECTORS.get(vector_name)
                if vector is not None:
                    construct.vectors.append(vector)
                else:
                    err = True
                    tell(client, "'" + vector_name + "' not found. Skipping...")
        construct.discover()
        GROUPS[args[1]] = construct
        logging.info("Created group '" + args[1] + "'.")
        if err:
            error(client)
        else:
            okay(client)
    else:
        error(client)
        tell(client, "Unrecognized type '" + args[0] + "'.")


def remove(client, args):
    if len(args) < 1:
        tell(client, COMMANDS_HELP.get('remove'))
        return
    target = str(args[0])
    if GROUPS.get(target) is not None:
        GROUPS.pop(target, None)
        logging.info("Removed group '" + args[0] + "'.")
        okay(client)
    elif VECTORS.get(target) is not None:
        for group in GROUPS.values():
            for vector in group.vectors:
                if VECTORS.get(target).name == vector.name:
                    group.vectors.remove(vector)
            group.discover()
        logging.info("Removed vector '" + args[0] + "'.")
        VECTORS.pop(target, None)
        okay(client)
    else:
        error(client)
        tell(client, "Entity '" + target + "' does not exist.")


def assign(client, args):
    if len(args) < 2:
        tell(client, COMMANDS_HELP.get('assign'))
        return
    vector = str(args[0])
    group = str(args[1])

    if GROUPS.get(group) is None or VECTORS.get(vector) is None:
        error(client)
        tell(client, "Entity does not exist.")
        return
    logging.info("Assigned '" + vector + "' to '" + group + "'.")
    GROUPS.get(group).vectors.append(VECTORS.get(vector))
    GROUPS.get(group).discover()
    okay(client)


def update(client, args):
    for vector in VECTORS.values():
        vector.discover()
    for group in GROUPS.values():
        group.discover()
    okay(client)


def save(client, args):
    save_vectors()
    save_groups()
    okay(client)


def discover(client, args):
    tell(client, "{}")


def status(client, args):
    if len(args) < 2:
        tell(client, COMMANDS_HELP.get('status'))
        return
    target = str(args[0])
    service = str(args[1])
    value = {}
    err = False

    if GROUPS.get(target) is not None:
        for vector in GROUPS.get(target).vectors:
            try:
                value[vector.name] = vector.send("status", (service,))
            except ConnectionError as exc:
                err = True
                tell(client, str(exc))
    elif VECTORS.get(target) is not None:
        try:
            value[VECTORS.get(target).name] = VECTORS.get(target).send("status", (service,))
        except ConnectionError as exc:
            err = True
            tell(client, str(exc))
    else:
        error(client)
        tell(client, "Entity '" + str(target) + "' does not exist.")
        return

    invalid = []
    for vector, result in value.items():
        if result is None or "ERROR" in result:
            err = True
            invalid.append(vector)
            tell(client, vector + " could not provide status '" + service + "'.")
    for vector in invalid:
        value.pop(vector)
    if err:
        error(client)
    tell(client, str(value))


def sys(client, args):
    logging.debug(client.addrport() + " sent system command " + ' '.join(map(str, args)))
    return vec(client, args, raw=True)


def vec(client, args, raw=False):
    if len(args) < 2:
        tell(client, COMMANDS_HELP.get('tell'))
        return
    target = args[0]
    service = args[1]
    if len(args) > 2:
        target_args = args[2:]
    else:
        target_args = None

    workers = []

    def work():
        if raw or vector.validate(service, target_args):
            name = vector.name
            try:
                if raw:
                    ret = vector.send(service, target_args)
                else:
                    ret = vector.tell(service, target_args)

                if ret is not None:
                    tell(client, name + ": " + ret.replace("\r\n", " "))
                else:
                    tell(client, name + ": No response...")
            except ConnectionError as exc:
                tell(client, str(exc))
        else:
            tell(client, str(vector.name) + " does not support " + str(service) + " " +
                 str(target_args if target_args is not None else "<>") + ".")

    if GROUPS.get(target) is not None:
        for vector in GROUPS.get(target).vectors:
            thread = threading.Thread(target=work)
            workers.append(thread)
            thread.start()
    elif VECTORS.get(target) is not None:
        vector = VECTORS.get(target)
        thread = threading.Thread(target=work)
        workers.append(thread)
        thread.start()
    else:
        error(client)
        tell(client, "Entity '" + str(target) + "' does not exist.")

    for worker in workers:
        worker.join()

"""
Definition of commands
"""
COMMANDS = {
    'help': hlp,
    'end': close,
    'exit': close,
    'tell': vec,
    'sys': sys,
    'list': gvlist,
    'add': add,
    'remove': remove,
    'assign': assign,
    'update': update,
    'status': status,
    'discover': discover,
    'save': save,
    'stop': stop,
}

COMMANDS_HELP = {
    'help': "... you've got this one.",
    'tell': "Issue a command to a vector or group.\ntell <name/group> <arguments>",
    'sys': "Issue a raw Junction system command.\nsys <name/group> <arguments>",
    'list': "Without arguments, lists all entities. With arguments, lists services.\nlist <*name/group>",
    'add': "Add a new vector or group.\nadd <'vector'/'group'> <name> <*IP Address> <*Port> <*Vector Names>",
    'remove': "Remove a vector or group.\nremove <name>",
    'assign': "Add a vector to a group.\nassign <vector> <group>",
    'update': "Update services available for all vectors and groups.",
    'status': "Return a formatted list of the status of a service on vector or group of vectors.\nstatus "
              "<'vector'/'group'> <service>",
    'save': "Save vectors and groups to local server files for recovery after restart.",
    'discover': "Formatted list of commands.",
    'end': "Terminates Telnet session.",
    'exit': "Terminates Telnet session.",
    'stop': "Stops the reception service, closing all connections.",
}

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    telnet_server = TelnetServer(
        port=9090,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout=0.5)

    logging.info("Listening on " + str(telnet_server.address) + ":" + str(telnet_server.port))

    read_vectors()
    read_groups()

    while RUN:
        telnet_server.poll()
        process()
        kick_idle()

    logging.info("Shutting down.")
