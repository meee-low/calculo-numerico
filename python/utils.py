""" 
Contém funções mais genéricas que são usadas em outros módulos.
"""


import numpy as np 
from matplotlib import pyplot as plt 
import math

def plotar_funcao(f, x_min, x_max, numero_de_pontos=500):
    """Plota a função `f` de `x_min` a `x_max`.

    Args:
        f (function): A função a ser plotada. O ideal é usar operadores aritméticos básicos (+, -, *, /, **) e \
            funções vetorizadas do numpy (ex.: np.sin, np.cos, np.exp), para ser mais rápido. 
        x_min (float): O valor mínimo de x a ser plotado.
        x_max (float): O valor máximo de x a ser plotado.
        numero_de_pontos (int, optional): Quantidade de pontos a serem usados para plotar a função.
    """
    xx = np.linspace(x_min, x_max, num=numero_de_pontos, endpoint=True) # cria os valores de x a serem plotados
    yy = f(xx) # avalia o valor de y para cada x, de acordo com a função.
    
    plt.plot(xx, yy)
    
    plt.grid()
    plt.axhline(y=0, color='black') # desenha a linha horizontal em y=0
    
    plt.show()
    
def checa_tolerancia(x_i, x, digse=2):
    """Checa se o erro relativo está dentro da tolerância desejada.

    Args:
        x_i (float): O valor da iteração anterior. 
        x (float): O valor da iteração atual. 
        digse (int, optional): O número de digitos significativos que desejamos. Padrão é 2 (erro de 1%).

    Returns:
        bool: `True` se estiver dentro da tolerância, `False` se não estiver.
    """
    erro_relativo = abs((x - x_i)/x_i)
    return erro_relativo <= 10**-digse

def arredonda_com_digse(x, digse=2):
    """Arredonda o número `x` baseado nos digitos significativos. 

    Args:
        x (float): O número a ser arredondado. 
        digse (int, optional): Número de digitos significativos.

    Returns:
        float: O resultado arredondado.
    """
    ordem_de_grandeza = -int(math.ceil(math.log10(abs(x))))
    grandeza_significativa = ordem_de_grandeza + digse
    return round(x, grandeza_significativa)