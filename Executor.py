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
            var_name = stmt[1]
            if self.current_input_index < len(self.inputs):
                var_value = self.inputs[self.current_input_index]
                self.current_input_index += 1
            else:
                var_value = input()
            self.symbol_table[var_name] = int(var_value) if var_value.isdigit() else var_value

        elif stmt[0] == 'OUTPUT':
            if isinstance(stmt[1], tuple):
                for v in stmt[1]:
                    self.execute_output(v)
            else:
                self.execute_output(stmt[1])

        elif stmt[0] == '=':
            var_name = stmt[1]
            value = stmt[2]
            value = self.evaluate_expr(value)
            self.symbol_table[var_name] = value

        # Caso seja uma declaração de canal
        elif stmt[0] == 'C_CHANNEL':
            self.channels[stmt[1]] = (stmt[2], stmt[3])

        # Envio e recepção de dados pelo canal
        elif not isinstance(stmt[0], tuple) and stmt[0] in self.channels:
            if stmt[1] == 'SEND':
                channel_name = stmt[0]
                channel = self.channels.get(channel_name)
                if channel:
                    # Implementação específica para envio de dados
                    pass  # Você pode implementar conforme necessário

            elif stmt[1] == 'RECEIVE':
                channel_name = stmt[0]
                channel = self.channels.get(channel_name)
                if channel:
                    # Implementação específica para recepção de dados
                    pass  # Você pode implementar conforme necessário

        elif isinstance(stmt, tuple):
            for s in stmt:
                self.execute_stmt(s)

    def execute_output(self, v):
        var_value = self.symbol_table.get(v, v)
        formatted_output = str(var_value).replace("\\n", "\n")
        self.outputs.append(formatted_output)

    def execute_bool(self, expr):
        if isinstance(expr, tuple):
            op, left, right = expr

            left_value = self.evaluate_expr(left)
            right_value = self.evaluate_expr(right)

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
        if isinstance(expr, int):
            return expr
        elif isinstance(expr, str):
            if expr.isdigit():
                return int(expr)
            else:
                return self.symbol_table.get(expr, expr)
        elif isinstance(expr, tuple):
            if len(expr) == 3:
                op, left, right = expr
                left_value = self.evaluate_expr(left)
                right_value = self.evaluate_expr(right)
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
