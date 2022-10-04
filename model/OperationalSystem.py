import sys

class OperationalSystem:
    @staticmethod
    def get():
        return sys.platform.lower() 