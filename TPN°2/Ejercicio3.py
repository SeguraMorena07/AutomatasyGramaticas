class AFN:
    def __init__(self):
        self.estados = {'e0', 'e1',}
        self.alfabeto = {'a', 'b'}
        self.transiciones = {
            'e0': {
                'a': ['e0'],
                'b': ['e0'],
                'ε': ['e1']
            },
            'e1' : {}
        }
        self.estado_inicial = 'e0'
        self.estados_finales = {'e1'}
    
    def mover(self, estado, simbolo):
        nuevos_estados = set()
        if simbolo in self.transiciones.get(estado, {}):
            nuevos_estados.update(self.transiciones[estado][simbolo])
        return nuevos_estados

afn = AFN()
test_strings = ["ε", "a", "b", "ab", "ba", "aab", "abb", "bba", "abab", "abba", "aaa", "bbb"]

for string in test_strings:
    estado_actual = afn.estado_inicial
    print(f"Procesando cadena: {string}")
    for simbolo in string:
        siguientes_estados = afn.mover(estado_actual, simbolo)
        print(f"Desde {estado_actual} con '{simbolo}' -> {siguientes_estados}")
        if siguientes_estados:
            estado_actual = list(siguientes_estados)[0]
        else:
            break
    print()