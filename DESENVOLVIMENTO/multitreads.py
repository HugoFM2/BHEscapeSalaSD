#!/usr/bin/python
 
import threading
import time
 
def minhafuncao(message):
    while True:
        print (message)
        time.sleep(1)
 
 
t1 = threading.Thread(target=minhafuncao,args=("\t -Thread 1 sendo executada",))
t2 = threading.Thread(target=minhafuncao,args=("\t -Thread 2 sendo executada",))
t1.start()
t2.start()

while t1.isAlive() and t2.isAlive():
    print ("Aguardando threads serem finalizadas")
    time.sleep(0.5)
 
print ("Threads finalizadas")
print ("Finalizando programa. \n")