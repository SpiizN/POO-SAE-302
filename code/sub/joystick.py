import pygame, math, json, socket, time

class Joystick:
    def __init__(self) -> None:
        """Constructeur de la classe Joystick
        """
        self.__boutons: dict
        self.__boutons_old: dict
        self.__connected: bool
        self.__joystick_name: str
        

        self.__boutons_old: int = 0
        self.__connected = False

        pygame.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            self.__connected = False
        else:
            self.__joystick = pygame.joystick.Joystick(0)
            self.__joystick.init()
            self.__joystick_name = self.__joystick.get_name()
            self.__connected = True

    def retry(self) -> None:
        """Méthode qui retente de connecter une manette / tester si la manette a été déconnectée
        """
        pygame.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            self.__connected = False
        else:
            self.__joystick = pygame.joystick.Joystick(0)
            self.__joystick.init()
            self.__joystick_name = self.__joystick.get_name()
            self.__connected = True

    def is_connected(self) -> bool:
        """Méthode de la classe Joystick qui permet de savoir si une manette est connectée.

        Returns:
            bool: Booléen, True si une manette est connectée
        """
        self.retry()
        return self.__connected

    def get_name(self) -> str:
        """Méthode de la classe Joystick qui permet de savoir le nom de la manette.

        Returns:
            str: Nom de la manette
        """
        return self.__joystick_name

    def get_update(self, client) -> None:
        """Méthode de la classe joystick qui permet d'avoir le client.

        Args:
            client (client): Client
        """
        self.__client = client

    def get_buttons(self) -> None:
        """Méthode de la classe Joystick qui permet de récuper les actions faites et les envoyer au serveur.
        """
        pygame.event.pump()
        button_state = int(self.__joystick.get_button(0)) # Bouton X(A)
        while button_state == 1: # Tant que le bouton X(A) de la manette est appuyé on envoie les informations du joystick au serveur
            pygame.event.pump() # Mise à jour des valeurs des boutons
            x_axis = -self.__joystick.get_axis(0) # Axe vertical
            y_axis = -self.__joystick.get_axis(1) # Axe horizontal
            print(self.envoyer_mvmt(x_axis, y_axis))
    
    def envoyer_mvmt(self, x: float, y: float) -> str:
        """Méthode de la classe Joystick qui permet d'envoyer les messages de mouvements au serveur.
        
        Args:
            x (float): Coord x du joystick
            y (float): Coord y du joystick

        Return:
            str: Message envoyé au serveur
        """
        msg = f"MVMT 1 {round(x,2)} {round(y,2)}"
        self.__client.envoyer(msg)
        time.sleep(0.1)
        return msg



    def quit(self) -> None:
        """Méthode de la classe Joystick pour arréter l'échange.
        """
        self.__joystick.quit()
        pygame.quit()

    def mainloop(self, socket: socket) -> None:
        """Méthode de la classe Joystick qui permet d'envoyer au serveur les actions effectuées avec la manette.

        Args:
            socket (socket): Socket en cours avec le serveur
        """
        self.__socket = socket
        while self.__boutons_old != 1:
            self.get_buttons() 
            self.__boutons_old = int(self.__joystick.get_button(1))
            
        self.envoyer("QUIT")
