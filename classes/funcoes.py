from typing import List


class Funcoes:

    def __init__(self):
        pass

    @staticmethod
    def retorna_chamados_diferentes(lista1, lista2) -> List:
        """
        Retorna a diferença entra as listas de dicionários
        :param lista1:
        :param lista2:
        :return: diferença entre as listas
        """
        diferenca: List = []
        for dicionario1 in lista1:
            existe = False

            for dicionario2 in lista2:
                if dicionario1['CHAVE'] == dicionario2['CHAVE']:
                    existe = True
                    break

            if not existe:
                diferenca.append(dicionario1)

        return diferenca

    @staticmethod
    def verifica_status_chamado(lista1, lista2) -> List:
        """
        Retorna uma lista atualizada com alterações de status de chamado (No Prazo e Fora do Prazo).
        :param lista1: Chamados do Share_Point
        :param lista2: Chamados do Jira
        :return: lista atualizada dos chamados
        """

        for dicionario1 in lista1:
            for dicionario2 in lista2:
                if dicionario1['CHAVE'] == dicionario2['CHAVE']:
                    for campo in dicionario2.keys():
                        if dicionario1[campo] != dicionario2[campo]:
                            dicionario1[campo] = dicionario2[campo]
                break

        return lista1
