import decodes as dc
from decodes.core import *
from decodes.extensions.lsystem import *

leng = LEngine("X")
leng.add_rule("X -> F-[[X]^XB]+F[&FXA]-X")
leng.add_rule("F -> F&FC")
leng.add_rule("A -> FX")
leng.add_rule("B -> CA")
leng.add_rule("C -> X")

for n in range(2): leng.step()
print leng.cur_gen

turt = LTurtle(leng.cur_gen)
geom = turt.go()

raw_input("press enter...")