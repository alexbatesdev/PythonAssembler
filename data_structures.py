from helper import resolve_condition


class CommandList:
    def __init__(self):
        self.head: Command = None
        self.tail: Command = None

    def append(self, command):
        if self.head is None:
            self.head = command
            self.tail = command
        else:
            self.tail.setNext(command)
            self.tail = command

    def toBinary(self):
        binary = []
        current = self.head
        while current is not None:
            binary.extend(current.toBinary())
            current = current.next
        return binary

    def getAtIndex(self, index):
        current = self.head
        for i in range(index):
            current = current.next
        return current

    def print(self):
        current = self.head
        while current is not None:
            print(current)
            current = current.next


class Command:
    def __init__(self, args, condition="AL", label=None):
        self.condition: str = resolve_condition(condition)
        self.args: list[str] = args
        self.label: str = label
        self.next: Command = None
        self.previous: Command = None

    def toBinary(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def setNext(self, next):
        self.next = next
        next.previous = self

    def setPrevious(self, previous):
        self.previous = previous
        previous.next = self

    def __str__(self) -> str:
        return f"{self.previous.__class__.__name__} <- {self.__class__.__name__} {' '.join(self.args)} {self.label != None and ':3 '+self.label or ''} -> {self.next.__class__.__name__}"
