from enum import Enum, auto

class Estado(Enum):
    LISTO = auto()
    EJECUCION = auto()
    BLOQUEADO = auto()
    FINALIZADO = auto()