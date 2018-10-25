"""
Server representation of controllable device
"""
import ast
import logging
import telnetlib


class Vector:

    def __init__(self, ip: str, port: str, name: str):
        super().__init__()
        self.ip = ip
        self.port = port
        self.name = name
        self.tn = telnetlib.Telnet(ip, port)
        self.tn.read_eager()  # Ignore welcome message
        self.services = {
            'debug': ('test', 'test2'),
        }

    def discover(self):
        self.tn.write("DISCOVER")
        services = self.tn.read_eager()
        """
        Expecting services in the format of a str(dict)
        {'service': ('opt', 'opt'), 'service2': ('opt', 'opt', 'opt')}
        """
        try:
            self.services = ast.literal_eval(services.strip())
        except ValueError:
            logging.error("Malformed string on discovery from " + self.ip + "'" + services + "'")

    def validate(self, service, options):
        valid = True
        if service not in self.services:
            valid = False
        service_options = self.services.get(service)
        if service_options is not None and (options is None or len(options) == 0):
            valid = False
        elif service_options is not None and options[0] not in service_options:
            valid = False
        return valid

    def tell(self, service, options):
        print("SEND ", self.name, service, options)
        self.tn.write(service + " " + ' '.join(map(str, options)))
        return self.tn.read_eager()


class Group:

    def __init__(self, vectors: list, name: str):
        super().__init__()
        self.vectors = vectors
        self.services = []
        self.name = name

    def discover(self):
        self.services = []
        for vector in self.vectors:
            for service, options in vector.services.items():
                string = (service + ": " + str(options))
                if string not in self.services:
                    self.services.append(string)
