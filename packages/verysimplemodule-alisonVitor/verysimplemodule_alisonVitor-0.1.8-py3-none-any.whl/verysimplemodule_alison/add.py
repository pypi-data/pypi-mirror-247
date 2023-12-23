import abc

class Add(abc.ABC):
    def add(self, num1, num2):
        return num1 + num2
