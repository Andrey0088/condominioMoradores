class Condominio():

    def __init__(self, nome, endereco, lista_moradores):
        self._nome = nome
        self._endereco = endereco
        self._lista_moradores = lista_moradores

    def adicionaMorador(self, cpf, morador):
        self._lista_moradores[cpf] = morador

    def obterMorador(self, CPF):
        if len(self._lista_moradores) != 0 and CPF in self._lista_moradores.keys():
            return self._lista_moradores[CPF]
        else:
            return "Erro"

    def excluiMorador(self, CPF):
        if CPF in self._lista_moradores.keys():
            del self._lista_moradores[CPF]
            return True
        else:
            return False

    def getLista_Moradores(self):
        return self._lista_moradores


class Morador():

    def __init__(self, nome, cpf, apartamento_bloco, pai, mae):
        self._nome = nome
        self._cpf = cpf
        self._apartamento_bloco = apartamento_bloco
        self._pai = pai
        self._mae = mae

    def getNome(self):
        return self._nome

    def getCPF(self):
        return self._cpf

    def getApartamentoBloco(self):
        return self._apartamento_bloco

    def getPai(self):
        return self._pai

    def getMae(self):
        return self._mae
