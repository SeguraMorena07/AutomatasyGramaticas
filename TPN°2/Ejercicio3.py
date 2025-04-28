class AFN:
    def __init__(self):
        self.estados = {'q0', 'qf'}
        self.alfabeto = {'a', 'b'}
        self.transiciones = {
            'q0': {
                'a': {'q0', 'qf'},
                'b': {'q0', 'qf'},
                'ε': {'qf'}
            }
        }
        self.estado_inicial = 'q0'
        self.estados_finales = {'qf'}
    
    def mover(self, estado, simbolo):
        return self.transiciones.get(estado, {}).get(simbolo, set())

afn = AFN()
