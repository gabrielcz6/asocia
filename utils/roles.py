from enum import Enum

class Roles(Enum):
    DECANO = "decano"
    PROFESOR = "profesor"
    SECRETARIA = "secretaria"

if __name__ == "__main__":
    # Uso
    print(Roles.DECANO.value)      # Color.ROJO
    print(Roles.PROFESOR) # 1