"""
Server representation of controllable device
"""
import ast
import logging
import socket
import telnetlib


class Vector:

    def __init__(self, ip: str, port: str, name: str):
        super().__init__()
        self.ip = ip
        self.port = port
        self.name = name
        self.tn = None
        self.services = {}
        self.send("", None)
        self.discover()

    def __getstate__(self):
        state = {
            'ip': self.ip,
            'port': self.port,
            'name': self.name,
            'services': self.services,
        }
        return state

    def __setstate__(self, state):
        self.ip = state.get('ip')
        self.port = state.get('port')
        self.name = state.get('name')
        self.services = state.get('services')
        self.tn = None

    def discover(self, in_open=False):
        if not in_open:
            self.open_telnet()
        try:
            services = self.send("discover", None)
        except ConnectionError:
            logging.error("Unable to discover " + self.name)
            return

        if services == '':
            logging.error("Empty string on discovery from " + self.ip + " '" + str(services) + "'")
            return
        """
        Expecting services in the format of a str(dict)
        {'service': ('opt', 'opt'), 'service2': ('opt', 'opt', 'opt')}
        """
        try:
            self.services = ast.literal_eval(services.strip())
        except (ValueError, AttributeError, SyntaxError):
            logging.error("Malformed string on discovery from " + self.ip + " '" + str(services) + "'")

    def validate(self, service, options):
        valid = True
        if service not in self.services.keys() and service is not "discover":
            valid = False
        service_options = self.services.get(service)
        if service_options is not None and type(service_options) is "tuple":
            if service_options is not None and (options is None or len(options) == 0):
                valid = False
            elif service_options is not None and options[0] not in service_options:
                valid = False
        return valid

    def tell(self, service, options):
        return self.send("service " + service, options)

    def send(self, service, options):
        self.open_telnet()
        if self.tn is not None:
            try:
                self.tn.read_until("".encode('utf-8'))  # Clear the buffer
                if options is not None:
                    if type(options) is "str":
                        options = (options,)
                    self.tn.write((service + " " + ' '.join(map(str, options)) + "\r\n").encode('utf-8'))
                else:
                    if type(options) is "str":
                        options = (options,)
                    self.tn.write((service + "\r\n").encode('utf-8'))
                ret = str(self.tn.read_until("> ".encode('utf-8'), timeout=5).decode('utf-8'))
                if ret is None or ret == "":
                    raise ConnectionError
                ret = ret.replace('\r\n$junction >', '')
                ret = ret.replace('$junction >', '')
                ret = ret.replace('\r\n$reception >', '')
                ret = ret.replace('$reception >', '')
                ret = ret.strip()
                logging.debug("Junction " + self.ip + ": " + ret)
                return ret
            except (ConnectionAbortedError, ConnectionRefusedError, ConnectionAbortedError, ConnectionError,
                    ConnectionResetError, socket.timeout):
                logging.info(self.ip + " closed, retrying...")
                self.tn = None
                self.open_telnet()
                ret = self.send(service, options)
                return ret
            except EOFError:
                logging.debug("Junction sent EOF")
                self.tn.read_all()
                self.tn.close()
                self.tn = None
                self.open_telnet()
                ret = self.send(service, options)
                return ret
        else:
            raise ConnectionError("Vector '" + self.name + "' unavailable.")

    def open_telnet(self):
        if self.tn is None:
            try:
                self.tn = telnetlib.Telnet(self.ip, self.port, timeout=5)
                self.tn.read_until("> ".encode('utf-8'), timeout=5)  # Ignore welcome message
                # self.discover(in_open=True)
            except (ConnectionAbortedError, ConnectionRefusedError, ConnectionAbortedError, ConnectionError,
                    ConnectionResetError, TimeoutError, socket.timeout):
                logging.error("Unable to reach " + self.ip)


class Group:
    def __init__(self, vectors: list, name: str):
        super().__init__()
        self.vectors = vectors
        self.services = []
        self.name = name

    def discover(self):
        self.services = []
        for vector in self.vectors:
            vector.discover()
            for service, options in vector.services.items():
                string = (service + ": " + str(options))
                if string not in self.services:
                    self.services.append(string)
