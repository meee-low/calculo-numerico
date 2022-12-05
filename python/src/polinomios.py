class Polinomio:
    def __init__(self, *args):
        if len(args) < 2:
            raise ValueError("O polinômio precisa de pelo menos dois coeficientes (ex.: ax + b).")
        self.coeficientes = args

    def __call__(self, x):
        """Avalia o polinômio no valor `x`.

        Args:
            x (float): O valor de x.

        Returns:
            float: O resultado do polinômio no valor `x`.
        """
        soma = 0
        for potencia, coef in enumerate(self.coeficientes[::-1]):
            soma += coef * x**potencia
        return soma

    def cotas(self):
        """Calcula as cotas pelas cotas de Kojima. Para polinômios lineares, usa cotas de Fujiwara.

        As cotas indicam que as raízes do polinômio se encontram dentro do raio dado no resultado:
        |r| <= cota

        Returns:
            float: A cota de Kojima (ou Fujiwara).
        """
        k = [abs(a_i / self.coeficientes[0]) ** (1/(i+1))
             for i, a_i in enumerate(self.coeficientes[1:])]

        sorted_k = sorted(k)
        q1 = sorted_k[-1]
        # Caso não tenha termos suficientes, usa o termo anterior (cota de Fujiwara):
        q2 = sorted_k[-2] if len(sorted_k) >= 2 else q1
        return q1 + q2

    def conta_raizes(self):
        """Conta as raízes positivas e negativas pela regra de Descartes."""
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
