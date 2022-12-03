"""
Define funções geradoras que dão os resultados de cada iteração, a partir dos métodos iterativos.

As funções geradoras são usadas pela função `usa_gerador` para chegar nas raízes e plotar o passos dados.

Exemplo de uso:
  f = lambda x: x**2 - 17*x + 4
  derivada = lambda x: 2*x - 17
  ger_newton = gerador_newton(f, derivada)
  usa_gerador(ger_newton, 17, digse=4)
  x_isolado = lambda x: (x**2 + 4)/17
  ger_aprsuc = gerador_aproximacoes_sucessivas(x_isolado)
  usa_gerador(ger_aprsuc, 1, plot=True, retorna_arredondado=True)
"""
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # importa da mesma pasta
import utils

def gerador_bissecao(f):
    """Retorna uma função geradora que usa o método da bisseção.

    Args:
        f (function): A função cujas raízes queremos encontrar.

    Returns:
        (function): A função geradora.
    """
    def gerador(x_esquerda, x_direita, max_iteracoes=500):
        """Gera iterações através do método da bisseção.

        Args:
            x_esquerda (float): O valor inicial do x à esquerda da raiz.
            x_direita (float): O valor inicial do x à direita da raiz.
            max_iteracoes (int, optional): O número máximo de iterações. 500 por padrão.

        Raises:
            ValueError: Quando os valores iniciais resultam em pontos do mesmo lado do eixo x \
                (sem raiz garantida entre eles).

        Yields:
            float: O resultado da próxima iteração.
        """
        if f(x_esquerda) * f(x_direita) > 0:
            raise ValueError(f"Os valores da função nos valores \
                iniciais devem ter sinais opostos. Valores dados: {x_esquerda}, {x_direita}")
        for _ in range(max_iteracoes):
            medio = (x_esquerda + x_direita) / 2 # próxima iteração
            yield medio
            if f(medio) * f(x_direita) < 0:
                # se o médio e o x da direita ainda tiverem sinais diferentes
                x_esquerda = medio # avança o x da esquerda até o médio
            else:
                # médio e o x da direita tem sinais iguais, então troca o x da direita
                x_direita = medio # recua o x da direita até o médio

    return gerador

def gerador_aproximacoes_sucessivas(funcao_de_iteracao):
    """Retorna uma função geradora que usa o método das aproximações sucessivas.

    Args:
        funcao_de_iteracao (function): A função que indica o próximo valor de x \
            em termos do x anterior. (Isolar x na função original)

    Returns:
        (function): A função geradora.
    """
    def gerador(x_inicial, max_iteracoes=500):
        """Gera iterações através do método das aproximações sucessivas.

        Args:
            x_inicial (float): A estimativa inicial.
            max_iteracoes (int, optional): O número máximo de iterações. 500 por padrão.

        Yields:
            float: O resultado da próxima iteração.
        """
        atual = x_inicial
        for _ in range(max_iteracoes): # repete até o máximo de iterações
            yield atual
            atual = funcao_de_iteracao(atual)

    return gerador

def gerador_newton(f, dfdx):
    """Retorna uma função geradora que usa o método de Newton.

    Args:
        f (function): A função cujas raízes queremos encontrar.
        dfdx (function): A derivada de `f`.

    Returns:
        (function): A função geradora.
    """
    def gerador(x_inicial, max_iteracoes=500):
        """Gera iterações através método de Newton.

        Args:
            x_inicial (float): A estimativa inicial.
            max_iteracoes (int, optional): O número máximo de iterações. 500 por padrão.

        Yields:
            float: O resultado da próxima iteração.
        """
        atual = x_inicial
        for _ in range(max_iteracoes): # repete até o máximo de iterações
            yield atual
            atual = atual - f(atual)/dfdx(atual) # ajusta o valor atual de acordo com o método de Newton

    return gerador

def usa_gerador(gerador, valores_iniciais, digse=2, plot=False, retorna_arredondado=False):
    """Toma valores do gerador até convergir em um valor que satisfaz o DIGSE desejado. \
    Além disso, pode plotar os resultados. Pode também já arrendondar o resultado de acordo com o DIGSE.

    Args:
        gerador (function): Uma função geradora responsável por calcular o valor da próxima iteração.
        valores_iniciais (float | list[float]):
        digse (int, optional): O número de digitos significativos que desejamos. 2 por padrão (erro de 1%).
        plot (bool, optional): Se os resultados devem ser plotados. `False` por padrão.
        retorna_arredondado (bool, optional): Se os resultados devem ser arredondados.

    Raises:
        ValueError: Se não convergir em um valor que satisfaz o DIGSE desejado.

    Returns:
        float: O resultado (geralmente uma raiz do problema).
    """
    resultado = None

    ger = gerador(valores_iniciais)

    estimativas = [next(ger)] # coloca o valor inicial dentro da lista
    for x in ger:
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

    if resultado is None: # Caso não encontre o resultado dentro da tolerância
        max_valores = min(len(estimativas), 5)
        raise ValueError(f"Não foi possível convergir para um resultado dentro \
            da tolerância desejada. Últimos valores: {estimativas[-max_valores:]}")

    log = f"Raiz em {resultado}"
    if retorna_arredondado:
        log += f" (DIGSE: {digse})"
    print(log)

    return resultado
