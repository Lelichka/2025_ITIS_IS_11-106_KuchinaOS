from itertools import chain

class BooleanSearch:
    def __init__(self, index):
        self.index = index
        self.all_docs = set()
        for doc_ids in index.values():
            self.all_docs.update(doc_ids)

    def parse_expression(self, expression):
        expression = expression.replace('И', '&').replace('ИЛИ', '|').replace('НЕ', '!')
        return list(chain.from_iterable([['!',token[1:]] if token.startswith('!') else [token] for token in expression.split(' ')]))

    def evaluate_expression(self, tokens):
        output = []
        operators = []

        precedence = {'&': 2, '|': 1, '!': 3}

        def apply_operator(op):
            if op == '&':
                b = output.pop()
                a = output.pop()
                output.append(a.intersection(b))
            elif op == '|':
                b = output.pop()
                a = output.pop()
                output.append(a.union(b))
            elif op == '!':
                a = output.pop()
                output.append(self.all_docs.difference(a))

        for token in tokens:
            if token in self.index:
                output.append(set(self.index[token]))
            elif token in precedence:
                while (operators and
                       precedence[operators[-1]] >= precedence[token]):
                    apply_operator(operators.pop())
                operators.append(token)
            else:
                output.append(set())

        while operators:
            apply_operator(operators.pop())

        return output[0] if output else set()

    def search(self, expression):
        tokens = self.parse_expression(expression)
        return self.evaluate_expression(tokens)
