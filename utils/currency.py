

class Currency:

    @classmethod
    def formatted(cls, amount):
        replaceRule = lambda char: {",": ".", ".": ","}.get(char) or char
        converter = lambda amount: "".join(replaceRule(char) for char in '{:0.2f}'.format(float(amount)/100))
        res = converter(amount).replace(",", ".")
        return str(res)
