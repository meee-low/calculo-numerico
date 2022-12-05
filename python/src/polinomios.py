class Polinomio:
    def __init__(self, *args):
        self.coeficientes = args

    def __call__(self, x):
        soma = 0
        for potencia, coef in enumerate(self.coeficientes[::-1]):
            soma += coef * x**potencia
        return soma

    def cotas(self):
        k = [abs(a_i / self.coeficientes[0]) ** (1/(i+1))
             for i, a_i in enumerate(self.coeficientes[1:])]

        # Cota de Kojima:
        sorted_k = sorted(k)
        q1, q2 = sorted_k[-1], sorted_k[-2]
        return q1 + q2

    def conta_raizes(self):
        # Regra de Descartes
        if len(self.coeficientes) <= 1:
            raise ValueError("Não tem termos suficientes.")
        trocas_de_sinais = [a1*a2 < 0 for a1, a2 in zip(self.coeficientes, self.coeficientes[1:])]

        trocas_pos = sum(trocas_de_sinais)
        trocas_neg = sum([not s for s in trocas_de_sinais])

        print(f"Trocas de sinal positivas: {trocas_pos}")
        print(f"Trocas de sinal negativas: {trocas_neg}")

        raizes_positivas_garantidas = trocas_pos % 2
        raizes_negativas_garantidas = trocas_neg % 2

        # print(f"Raízes positivas garantidas: {raizes_positivas_garantidas}")
        # print(f"Raízes negativas garantidas: {raizes_negativas_garantidas}")

    def __repr__(self):
        return f"Polinomio({self.coeficientes})"

    def __str__(self):
        termos = [f"{coef} * x**{potencia}"
                  for potencia, coef in enumerate(self.coeficientes[::-1])]
        termos = termos[::-1]
        return " + ".join(termos)
