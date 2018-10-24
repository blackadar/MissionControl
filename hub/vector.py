"""
Server representation of controllable device
"""


class Vector:

    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.services = []


class Service:
    pass
