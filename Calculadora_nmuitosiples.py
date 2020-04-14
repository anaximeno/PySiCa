from pythonworks import Functions

print('*Opa bem vindo a calculadora simples, se precisar de ajuda escreva isso na tela!*')

# Variáveis
tentado = False

while True:
    ope = input('Escolha a Operação -> ').lower()
    try:
        if ope == 'adi':
            x = float(input('Primeiro número -> '))
            y = float(input('Segundo número -> '))
            print(f'O resultado é {Functions.adicao(x, y)}')
        elif ope == 'sub':
            x = float(input('Primeiro número -> '))
            y = float(input('Segundo número -> '))
            print(f'O resultado é {Functions.subtracao(x, y)}')
        elif ope == 'multi':
            x = float(input('Primeiro número -> '))
            y = float(input('Segundo número -> '))
            print(f'O resultado é {Functions.multiplicacao(x, y)}')
        elif ope == 'divi':
            try:
                x = float(input('Primeiro número -> '))
                y = float(input('Segundo número -> '))
                print(f'O resultado é {Functions.divisao(x, y)}')
            except ZeroDivisionError:
                print("Erro Matemático - você não pode dividir um número por zero")
        elif ope == 'pot':
            x = float(input('Base -> '))
            y = float(input('Potência -> '))
            print(f'O resultado é {Functions.potencia(x, y)}')
        elif ope == 'ajuda':
            print('''
            Escreva:
            - adi (para adição)
            - sub (para subtração)
            - multi (p/ multiplicação)
            - divi (p/ divisão)
            - pot (p/ calcular potência)
            - sair (p/ sair da calculadora)
            ''')
        elif ope == 'sair':
            break
        elif ope.isspace() is True or ope == '':
            print('Você deve escrever alguma coisa!')
        else:
            if tentado is False:
                tentado = True
                print('Tente de novo por favor')
            else:
                print('Procure por "ajuda" (ou escreva isso)!')
    except ValueError:
        print('#Evite usar vírgula para atribuir casas decimais, em vez disso use ponto.')
        print('#Não use letra ou qualquer outro símbolo no lugar dos números!')
