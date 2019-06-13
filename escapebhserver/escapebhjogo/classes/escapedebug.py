
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp

# Classe criada para testes de desenvolvimento

class debug(object):

    @staticmethod
    def mcp23017debug():
        print('Debug Escape BH - MCP23017')
        #MCP23017.msg()
        mcp.setup(0, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(1, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(2, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(3, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(4, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(5, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(6, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(7, mcp.GPB, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(0, mcp.GPA, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(1, mcp.GPA, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(2, mcp.GPA, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(3, mcp.GPA, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(4, mcp.GPA, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(5, mcp.GPA, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(6, mcp.GPA, mcp.OUT, mcp.ADDRESS1)
        mcp.setup(7, mcp.GPA, mcp.OUT, mcp.ADDRESS1)


