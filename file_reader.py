from test import *
from lex_reader import *

input_paths = [
    'inputs/slr-1.yal',
    'inputs/slr-2.yal',
    'inputs/slr-3.yal',
    'inputs/slr-4.yal'
]

testing_paths = [
    ['Testing/slr-1.1.yal.run','Testing/slr-1.2.yal.run'],
    ['Testing/slr-2.1.yal.run','Testing/slr-2.2.yal.run'],
    ['Testing/slr-3.1.yal.run','Testing/slr-3.2.yal.run'],
    ['Testing/slr-4.1.yal.run','Testing/slr-4.2.yal.run']
]
i = 3
k_testing = 0

input_path = input_paths[i]
test_path = testing_paths[i][k_testing]


t = Test()
L = Lexer()
patterns, tokens  = L.reader(input_path)
L.pre_load(input_path)
afds, patterns = L.afn_union(patterns)
L.file_generator(afds, patterns, tokens)


with open(test_path, 'r') as f:
    for line in f:
        print('------------W------------')
        print(line)
        print('-------------------------')
        aux_list = t.identifyer2(line)
        print(aux_list[0])
        for i in aux_list[1]:
            print(i)    
        
        input('NEXT LINE... [enter]')



# t = Test()
# w = 'varOne+var2two'
# print(t.identifyer2(w))