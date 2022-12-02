from geradores import *
from utils import *



# Exemplo: raízes de f(x) = x^2 - 17x + 4

f = lambda x: x ** 2 - 17*x  + 4

plotar_funcao(f, -2, 20)  # plota de -2 a 20

# Raízes próximas de 0 e de 17. 

# Método de Newton:

# f(x) = x^2 - 17x + 4
# f'(x) = 2x - 17

derivada = lambda x: 2*x - 17

ger_newton = gerador_newton(f, derivada, x_inicial=17) # cria um gerador usando o metodo de newton 
usa_gerador(ger_newton, plot=True, digse=4) # encontra uma das raízes

# f(x) = x^2 - 17x + 4 = 0
# <=> x^2 + 4 = 17x
# <=> (x^2 + 4)/17 = x

x_isolado = lambda x: (x**2 + 4)/17

ger_aprsuc = gerador_aproximacoes_sucessivas(x_isolado, x_inicial=1)
usa_gerador(ger_aprsuc, plot=True) # encontra a outra raiz, com digse 5