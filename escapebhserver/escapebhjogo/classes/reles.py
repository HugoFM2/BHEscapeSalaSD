import time
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp

"""Modulo com os metodos e atributos para trabalhar
com os modulos reles.
"""

class Reles(object):

    @classmethod
    def desligarTodosReles(cls):
        # Reles como OUTPUT (O rele e desativado em nivel alto)
        #time.sleep(1)
        for i in range(0,8):
            mcp.setup(i, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
            mcp.setup(i, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
            mcp.output(i, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
            mcp.output(i, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    @classmethod
    def testarGPA(cls, gp):
        print('Iniciando teste da GPA: ' + str(gp) )
        mcp.output(gp, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.5)
        mcp.output(gp, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    @classmethod
    def testarGPB(cls, gp):
        print('Iniciando teste da GPB: ' + str(gp) )
        mcp.output(gp, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.5)
        mcp.output(gp, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)