class AFN:
    def __init__(self):
        self.estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
        self.alfabeto = {'a', 'b'}
        self.transiciones = {
            'q0': {
                'ε': ['q1', 'q2', 'q5']
            },
            'q1': {
                'a': ['q3']
            },
            'q2': {
                'b': ['q4']
            },
            'q3': {
                'ε': ['q5']
            },
            'q4': {
                'ε': ['q5']
            },
            'q5': {
                'ε': ['q0'] 
            }
        }
        self.estado_inicial = 'q0'
        self.estados_finales = {'q5'}
    
    def epsilon_cierre(self, estados):
        stack = list(estados)
        closure = set(estados)
        
        while stack:
            estado = stack.pop()
            for siguiente in self.transiciones.get(estado, {}).get('ε', []):
                if siguiente not in closure:
                    closure.add(siguiente)
                    stack.append(siguiente)
        return closure
    
    def mover(self, estados, simbolo):
        nuevos_estados = set()
        for estado in estados:
            if simbolo in self.transiciones.get(estado, {}):
                nuevos_estados.update(self.transiciones[estado][simbolo])
        return nuevos_estados

    def acepta(self, cadena):
        estados_actuales = self.epsilon_cierre({self.estado_inicial})
        
        for simbolo in cadena:
            estados_actuales = self.mover(estados_actuales, simbolo)
            estados_actuales = self.epsilon_cierre(estados_actuales)
        
        return any(estado in self.estados_finales for estado in estados_actuales)


afn = AFN()

test_strings = ["a", "b", "ab", "bas", "aab", "abb", "bba", "abab", "abba", "aaa", "bbb", ""]

for string in test_strings:
    resultado = afn.acepta(string)
    print(f"Cadena '{string}': {'Aceptada' if resultado else 'Rechazada'}")
