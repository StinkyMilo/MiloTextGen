# First argument should be the filename of a grammar to use. 
# Example: py .\generate_10_items.py example_grammars/command_test.tsv
# The program will produce 10 random items using that grammar.
from milotextgen import Generator
import sys
gen = Generator(sys.argv[1])
for i in gen.generate_multi(10):
    print(i)