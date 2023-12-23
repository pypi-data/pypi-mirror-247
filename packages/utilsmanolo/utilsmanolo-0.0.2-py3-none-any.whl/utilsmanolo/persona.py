"""
Creacion de personas
"""


class Persona:
    """
    clase para la creacion de usuarios
    """

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre
