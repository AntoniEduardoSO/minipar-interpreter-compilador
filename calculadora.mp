SEQ

valor1 = Input()

valor2 = Input()

operation = Input()


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
