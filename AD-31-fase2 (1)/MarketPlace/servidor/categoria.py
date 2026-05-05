class Categoria:
    _contador_global = 1

    def __init__(self, nome):
        self.id_categoria = Categoria._contador_global
        self.nome = nome
        Categoria._contador_global += 1

    def obter_id(self): 
        return self.id_categoria
