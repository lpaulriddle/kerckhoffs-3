#!/usr/bin/env python3
#sed "s/Good reduction for/{ 'position':/" outout2 | sed "s/ - 25 computed rotations/, 'rotations'/" | sed 's/$/}/'

from ast import literal_eval
with open("outout") as file:
    lines = [literal_eval(line.rstrip()) for line in file]
for gads in lines:
    thing = sum([len(bar[0][0]) for (foo, bar) in gads['rotations'].items()])
    print(thing)
    print(gads)
    
