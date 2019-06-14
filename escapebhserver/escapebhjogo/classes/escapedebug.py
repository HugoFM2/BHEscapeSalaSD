
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp

# Classe criada para testes de desenvolvimento

class debug(object):

    # METODO ESTATICO mcp23017debug
    @staticmethod
    def mcp23017debug():
        print('Debug Escape BH - MCP23017')
        mcp.confRegistradoresComZero()


