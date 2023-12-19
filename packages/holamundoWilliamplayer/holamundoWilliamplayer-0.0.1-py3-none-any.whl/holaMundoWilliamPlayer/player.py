"""
    Este es el modul que incluye la clase
     de reproductor de musica :)
"""


class Player:
    """
        Esta clase crea un reproductor 
        de musica
    """

    def play(self, song):
        """
        REproduce la cancion que recibio como parametro

        Parameters:
        song (str): este es un string con  el path de la cancion
        
        Returns:
        int: devuelve 1 reproduce con exito, en caso de fracaso devuelve 0
        """
        print("reproduciendo cancion")
    
    def stop(self):
        print("stopping")