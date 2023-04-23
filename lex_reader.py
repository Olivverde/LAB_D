# Abrir archivo
import json
from NFA_lab import *
from labB import *
import copy
class Lexer(object):

    def __init__(self) -> None:
        self.pre_exist_patterns = self.pre_fab()

    def pre_load(self, path):
        
        with open(path) as file:
            pos_status = False
            for line in file:
                
                if 'let' in line:
                    pos_status = True
                if 'tokens' in line and pos_status == False:
                    print('---------------------------------------')
                    print("ERROR: NO SE ENCONTRÓ EXPRESIONES REGULARES PREVIAS A LOS TOKENS!!!")
                    print('---------------------------------------')
                    raise SystemExit
                if 'rule' in line:
                    if not 'rule tokens =' in line:
                        print('---------------------------------------')
                        print("ERROR: EXPRESIÓN DE TOKEN NO RECONOCIDA!!!")
                        print('---------------------------------------')
                        raise SystemExit
                if 'ids' in line:
                    print('---------------------------------------')
                    print("ERROR: TOKEN NO RECONOCIDO!!!")
                    print('---------------------------------------')
                    raise SystemExit
                    
                balance_score_paren = 0
                balance_score_mark = 0
                for c in [char for char in line]:
                    if not "'('" in line and not "')'" in line:
                        if c == '(' or c == ')':
                            balance_score_paren += 1
                    if c == "'":
                        balance_score_mark += 1
                if balance_score_mark%2 != 0 or balance_score_paren%2 != 0:
                    print(line)
                    print(balance_score_mark, balance_score_paren)
                    print('---------------------------------------')
                    print("ERROR: EXPRESIÓN DESBALANCEADA!!!")
                    print('---------------------------------------')
                    raise SystemExit
        
    def pre_fab(self):
        patterns_ax = { "'A'-'Z'": [chr(i) for i in range(ord('A'), ord('Z')+1)],
                              "'a'-'z'": [chr(i) for i in range(ord('a'), ord('z')+1)],
                              "'0'-'9'": [chr(i) for i in range(ord('0'), ord('9')+1)]}
        for i in patterns_ax:
            patterns_ax[i] = [letra + "|" for letra in patterns_ax[i]]
            patterns_ax[i][-1] = patterns_ax[i][-1][0]
        return patterns_ax
        
    def pattern_xtension(self, raw_pattern, previus_pattern):
        
        section = raw_pattern
        if previus_pattern + "+" in raw_pattern:
            section = "(" + previus_pattern + ")" + "(" + previus_pattern + "*)"
        
        if "?" in raw_pattern:
            raw_deconst = [char for char in raw_pattern]
            aux_constr = []
            for e in raw_deconst:
                # Si identifica un ?
                if e == '?':
                    internal = ""
                    prev = aux_constr.pop()
                    # Identifica si es un ) o un ]
                    if prev == ")":
                        par_finder = ""
                        # Buscara todo lo que haya dentro del paréntesis
                        while par_finder != "(":
                            par_finder = aux_constr.pop()
                            if par_finder != "(":
                                internal = par_finder + internal
                        # Modificará el contenido extraído
                        internal = "(" + "(" + internal + ")" + "|" + "ε)"
                        aux_constr.append(internal)
                        
                    elif prev == "]":
                        
                        par_finder = ""
                        # Buscara todo lo que haya dentro del corchete
                        while par_finder != "[":
                            par_finder = aux_constr.pop()
                            if par_finder != "[":
                                internal = par_finder + internal
                        # Modificará el contenido extraído
                        internal = internal.split("'")
                        internal = ''.join(internal)
                        aux = ""
                        for k in internal:
                            aux += k + "|"
                        internal = aux
                        internal = "(" + internal + "ε)"
                        aux_constr.append(internal)
                       
                else:
                    aux_constr.append(e)
                
                section = ''.join(aux_constr)
        
        
        return section
          
    def pattern_translation(self, raw_pattern, patterns):
        pep = self.pre_exist_patterns
        aux_pattern = []
        section = ''
        # Si comienza con [ ] se los retira
        # if "'" in raw_pattern:
        #     raw_pattern = raw_pattern.replace("'","")
        if raw_pattern.startswith("[") and raw_pattern.endswith("]"):  
            raw_pattern = raw_pattern[1:-1]
            if raw_pattern.startswith('"') and raw_pattern.endswith('"'):
                raw_pattern = raw_pattern[1:-1]
                
                if '\\' in raw_pattern:
                    ax = ''
                    raw_pattern = [x for x in raw_pattern.split('\\') if x]
                    for e in range(len(raw_pattern)):
                        ax = ax + '\\' + raw_pattern[e]
                        if e != len(raw_pattern) - 1:   
                            ax = ax + '|'
                    raw_pattern = ax
                else:
                    ax = ''
                    for e in range(len(raw_pattern)):
                        ax = ax + raw_pattern[e]
                        if e != len(raw_pattern) - 1:   
                            ax = ax + '|'
                    raw_pattern = ax
            
            

            # Si identifica un patron pre-existente lo traduce
            for i in pep.keys():
                if i in raw_pattern:
                    raw_pattern = raw_pattern.replace(i,'')
                    if len(aux_pattern) != 0:
                        aux_pattern.append('|')
                        aux_pattern = aux_pattern + pep[i]
                    elif len(aux_pattern) == 0:
                        aux_pattern = aux_pattern + pep[i]
        # Si identifica una patrón participe dentro de otro patrón
        for j in patterns.keys():
            if j in raw_pattern:
                section = self.pattern_xtension(raw_pattern, j)
                return section
        
        if "'" in raw_pattern:
            raw_pattern = (raw_pattern.split("'"))
            aux = []
            for i in raw_pattern:
                if i != '':
                    aux.append(i)
                    aux.append('|')
            aux.pop()
            section = ''.join(aux)
            return "("+section+")"
        
        
        section = list(filter(None,raw_pattern.split("'")))
        section = section + aux_pattern
        
        section = ''.join(section)
        
        return "("+section+")"
    
    def reader(self, path):
        

        with open(path) as file:
            
            patterns = {}
            # Inicializar lista vacía
            let_vars = []
            # Leer archivo línea por línea
            for line in file:
                # Buscar "let" en la línea
                if 'let' in line:
                    # Obtener la variable después de "let" eliminando los espacios en blanco y el salto de línea
                    var = line.split("let ")[1].strip()
                    pattern_name = var.split("=")[0].strip()
                    pattern = var.split("=")[1].strip()
                    
                    pattern = self.pattern_translation(pattern, patterns)
                    
                    available_patterns = []
                    for l in patterns.keys():
                        if l in pattern:
                            available_patterns.append(l)
                    
                    for m in range(len(available_patterns)-1, -1, -1):
                        ava_aux = available_patterns[m]
                        pattern = pattern.replace(ava_aux, patterns[ava_aux])
                    
                    if "'" in pattern:
                        pattern = pattern.replace("'", '')
                    patterns[pattern_name] = pattern
            return patterns

    def afn_union(self, patterns):
        G = nx.DiGraph()
        afds = []
        afns = []
        for i in patterns:
            score = 0
            N = NFA()
            F = FDA()
            lib = Libs(patterns[i])
            postfix = lib.get_postfix()
            # print(postfix)
            N.thompson(postfix)
           
            a,b = F.subConstruct(N.AFN_transitions, N.get_acceptance_state()+1)
            
            afds.append(b)
            
        return afds, patterns
            
    def int_to_str(self,key):
        if isinstance(key, int):
            return str(key)
        return key

    def file_generator(self, afds, patterns):
        json_afds = json.dumps(afds, indent=4,ensure_ascii=False,default=self.int_to_str)
        json_patterns = json.dumps(patterns, indent=4)
 
        with open("test.py", "w", encoding='utf-8') as archivo:
            archivo.write(f"from labB import *\n")
            archivo.write(f"afds = {json_afds}\n")
            archivo.write(f"patterns = {json_patterns}\n\n")
            archivo.write('class Test:\n')
            archivo.write('    def identifyer(self, w, afds, patterns):\n')
            archivo.write('        a = FDA()\n')
            archivo.write('        flag = 0\n')
            archivo.write('        for i in patterns:\n')
            archivo.write('            patterns[i] = afds[flag]\n')
            archivo.write('            flag += 1\n')
            archivo.write('        aux_w = \'\'\n')
            archivo.write('        result = \'\'\n')
            archivo.write('        for c in range(len(w)):\n')
            archivo.write('            aux_w += w[c]\n')
            archivo.write('            for pat in patterns:\n')
            archivo.write('                b = patterns[pat]\n')
            archivo.write('                result = a.afd_simulation(aux_w, b)\n')
            archivo.write('                if result == \'PASS\':\n')
            archivo.write('                    print(\'<\', aux_w, \' →\', pat, \'>\')\n')
            archivo.write('t = Test()\n')
            archivo.write('w = \'abc\'\n')
            archivo.write('t.identifyer(w, afds, patterns)\n')

            

    def identifyer(self,w, afds, patterns):
        a = FDA()
        flag = 0
        for i in patterns:
            patterns[i] = afds[flag]
            flag += 1
        
        print(patterns)
        aux_w = ''
        result = ''
        for c in range(len(w)):
            aux_w += w[c]
            for pat in patterns:
                b = patterns[pat]
                b = patterns['digit']
                print(b)
                result = a.afd_simulation('1', b)
                if result == 'PASS':
                    print('<',aux_w,' →',pat,'>')
                
            


path = 'inputs/slr-1.yal'
L = Lexer()
patterns  = L.reader(path)
L.pre_load(path)
afds, patterns = L.afn_union(patterns)
L.file_generator(afds,patterns)
# L.identifyer('abc',afds, patterns)
# print(acceptance)
# a,b = FDA().subConstruct(afn_master, acceptance+1)
# print('Subconstruction DFA Set →',b)
# # print('-----------------------------------------------------------')
# FDA().graph(b)

# w = 'AA2'
# print('W =',w,' → Subconstruction DFA Set Simulation Status:',FDA().afd_simulation(w,b))
