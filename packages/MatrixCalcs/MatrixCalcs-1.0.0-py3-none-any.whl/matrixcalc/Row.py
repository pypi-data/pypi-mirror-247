class Row:

    def __init__(self, content: list[int]):
        self.content = content

    def to_string(self):
        final = f'[{self.content[0]}'
        for i in range(1, len(self.content)):
            final += f', {self.content[i]}'
        return final + "]"

    def length(self) -> int:
        return len(self.content)


if __name__ == "__main__":
    c = [1, 2, 3, 4]
    r = Row(c)
    print(r.to_string())


