""" 
Define funções geradoras que dão os resultados de cada iteração, a partir dos métodos iterativos.

As funções geradoras são usadas pela função `usa_gerador` para chegar nas raízes e plotar o passos dados.

Exemplo de uso:

  f = lambda x: x ** 2 - 17*x  + 4
  derivada = lambda x: 2*x - 17
  ger_newton = gerador_newton(f, derivada, x_inicial=17)
  usa_gerador(ger_newton, digse=4)
  x_isolado = lambda x: (x**2 + 4)/17
  ger_aprsuc = gerador_aproximacoes_sucessivas(x_isolado, x_inicial=1)
  usa_gerador(ger_aprsuc, plot=True, retorna_arredondado=True)
"""
import numpy as np 
from matplotlib import pyplot as plt
import utils

def gerador_aproximacoes_sucessivas(funcao_de_iteracao, x_inicial, max_iteracoes=500):
    atual = x_inicial
    for _ in range(max_iteracoes): # repete até o máximo de iterações
        yield atual
        atual = funcao_de_iteracao(atual)

def gerador_newton(f, dfdx, x_inicial, max_iteracoes=500):
    """Gera iterações através método de Newton.

    Args:
        f (function): A função cujas raízes queremos encontrar. 
        dfdx (function): A derivada de `f`. 
        x_inicial (float): A estimativa inicial. 
        max_iteracoes (int, optional): O número máximo de iterações. 500 por padrão.

    Yields:
        float: O resultado da próxima iteração. 
    """
    atual = x_inicial
    for _ in range(max_iteracoes): # repete até o máximo de iterações
        yield atual
        atual = atual - f(atual)/dfdx(atual) # ajusta o valor atual de acordo com o método de Newton
    
    
def usa_gerador(gerador, digse=2, plot=False, retorna_arredondado=False):
    """Toma valores do gerador até convergir em um valor que satisfaz o DIGSE desejado. \ 
    Além disso, pode plotar os resultados. Pode também já arrendondar o resultado de acordo com o DIGSE. 

    Args:
        gerador (function): Uma função geradora responsável por calcular o valor da próxima iteração.
        digse (int, optional): O número de digitos significativos que desejamos. 2 por padrão (erro de 1%).
        plot (bool, optional): Se os resultados devem ser plotados. `False` por padrão.
        retorna_arredondado (bool, optional): _description_. Defaults to False.

    Raises:
        ValueError: Se não convergir em um valor que satisfaz o DIGSE desejado.

    Returns:
        float: O resultado (geralmente uma raiz do problema).
    """
    resultado = None
    
    estimativas = [next(gerador)] # coloca o valor inicial dentro da lista
    for x in gerador:
        estimativas.append(x)
        if utils.checa_tolerancia(estimativas[-2], estimativas[-1], digse): # Compara as duas últimas iterações.
            # Se atingimos a tolerância desejada, para de iterar e salva o resultado.
            if retorna_arredondado:
                resultado = utils.arredonda_com_digse(x, digse)
            else:
                resultado = x
            break
    
    if plot: # Caso queira visualizar os resultados.
        xx = np.arange(len(estimativas))
        
        plt.plot(xx, estimativas, 'o')
        
        plt.grid()
        plt.axhline(y=resultado, linestyle='--', color='black') # Marca a linha do resultado.
        plt.yticks(list(plt.yticks()[0]) + [resultado]) # Marca o resultado no eixo vertical.
        
        plt.show()
        
    if resultado is None:
        # Caso não encontre o resultado dentro da tolerância:
        raise ValueError(f"Não foi possível convergir para um resultado dentro da tolerância desejada. Últimos valores: {estimativas[-5:]}")    
    
    print(f"Raiz em {resultado} (DIGSE: {digse}).")

    return resultado