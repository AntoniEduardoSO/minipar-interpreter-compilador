# Executor.py
import threading

class Executor:
    def __init__(self, inputs=None):
        self.has_error = False
        self.symbol_table = {}
        self.channels = {}
        self.inputs = inputs or []
        self.outputs = []
        self.current_input_index = 0

    def to_number(self, value):
        if isinstance(value, (int, float)):
            return value
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value  # Retorna a string original se não for número

    # Funções de execução para cada tipo de instrução
    def execute_stmt(self, stmt):
        if stmt[0] == 'SEQ':
            # Para cada instrução no bloco SEQ, execute
            for s in stmt[1]:
                self.execute_stmt(s)

        elif stmt[0] == 'PAR':
            threads = []
            # Para cada instrução no bloco PAR, coloque em uma thread e execute
            for s in stmt[1]:
                thread = threading.Thread(target=self.execute_stmt, args=(s,))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

        elif stmt[0] == 'IF':
            if self.execute_bool(stmt[1]):
                for s in stmt[2]:
                    self.execute_stmt(s)

        elif stmt[0] == 'WHILE':
            while self.execute_bool(stmt[1]):
                for s in stmt[2]:
                    self.execute_stmt(s)

        elif stmt[0] == 'INPUT':
            # Esta parte pode ser deixada em branco, pois o Input será tratado na atribuição
            pass

        elif stmt[0] == 'OUTPUT':
            if isinstance(stmt[1], tuple):
                for v in stmt[1]:
                    self.execute_output(v)
            else:
                self.execute_output(stmt[1])

        elif stmt[0] == '=':
            var_name = stmt[1]
            value = stmt[2]
            if isinstance(value, tuple) and value[0] == 'INPUT':
                # Tratar atribuição com Input()
                if self.current_input_index < len(self.inputs):
                    var_value = self.inputs[self.current_input_index]
                    self.current_input_index += 1
                else:
                    var_value = input()
                self.symbol_table[var_name] = self.to_number(var_value)
            else:
                value = self.evaluate_expr(value)
                self.symbol_table[var_name] = value

        # Outras instruções...
        elif isinstance(stmt, tuple):
            for s in stmt:
                self.execute_stmt(s)

    def execute_output(self, v):
        value = self.evaluate_expr(v)
        formatted_output = str(value).replace("\\n", "\n")
        self.outputs.append(formatted_output)

    def execute_bool(self, expr):
        if isinstance(expr, tuple):
            op, left, right = expr

            left_value = self.evaluate_expr(left)
            right_value = self.evaluate_expr(right)

            left_value = self.to_number(left_value)
            right_value = self.to_number(right_value)

            if op == '<':
                return left_value < right_value
            elif op == '>':
                return left_value > right_value
            elif op == '<=':
                return left_value <= right_value
            elif op == '>=':
                return left_value >= right_value
            elif op == '==':
                return left_value == right_value
            elif op == '!=':
                return left_value != right_value
        else:
            return bool(self.evaluate_expr(expr))

    def evaluate_expr(self, expr):
        if isinstance(expr, (int, float)):
            return expr
        elif isinstance(expr, str):
            value = self.symbol_table.get(expr, expr)
            return self.to_number(value)
        elif isinstance(expr, tuple):
            if len(expr) == 3:
                op, left, right = expr
                left_value = self.evaluate_expr(left)
                right_value = self.evaluate_expr(right)

                left_value = self.to_number(left_value)
                right_value = self.to_number(right_value)

                if op == '+':
                    return left_value + right_value
                elif op == '-':
                    return left_value - right_value
                elif op == '*':
                    return left_value * right_value
                elif op == '/':
                    return left_value / right_value
                elif op in ['<', '>', '<=', '>=', '==', '!=']:
                    return self.execute_bool(expr)
        return 0
