SEQ
Output("CALCULADORA\n\n")
Output("Operadores: + - * /\n\n")

Output("Digite o primeiro numero:\n")
valor1 = Input()
Output("valor1: ", valor1)
Output("\n")

Output("Digite o segundo numero:\n")
valor2 = Input()
Output("valor2: ", valor2)
Output("\n")

Output("Digite a operacao entre os números:\n")
operation = Input()
Output("operation: ", operation)
Output("\n")

result = 0

if (operation == '-'){
    result = valor1 - valor2
}
if (operation == '+'){
    result = valor1 + valor2
}
if (operation == '*'){
    result = valor1 * valor2
}
if (operation == '/') {
    result = valor1 / valor2
}

Output("resultado: ", result)
Output("\n")
