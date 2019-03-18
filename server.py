from cmdFile import *


cc = cmdFile('ttg')
while True:
    s = input(">>")
    cc.putCommand(s)
    p = cc.getLastOutput()
    while len(p) == 0:
        p = cc.getLastOutput()
    print("\n")
    print(str(p.decode("utf-8")))