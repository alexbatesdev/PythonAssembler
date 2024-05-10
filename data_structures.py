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
            current_binary = current.toBinary()
            inverted_binary = []
            for i in current_binary[::-1]:
                inverted_binary.append(i)
            binary.extend(inverted_binary)
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
            current = current.next


class Command:
    def __init__(self, args, label=None):
        self.args: list[str] = args
        self.label: str = label
        self.next: Command = None
        self.previous: Command = None
        self.condition = resolve_condition(
            self.args[0].replace(self.__class__.__name__, "")
        )

    def toBinary(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def setNext(self, next):
        self.next = next
        next.previous = self

    def setPrevious(self, previous):
        self.previous = previous
        previous.next = self

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.condition} {' '.join(self.args[1:])} {self.label != None and ':3 '+self.label or ''}"
