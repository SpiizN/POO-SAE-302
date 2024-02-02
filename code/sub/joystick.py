import pygame, math, json, socket, time

class Joystick:
    def __init__(self) -> None:
        """Constructeur de la classe Joystick
        """
        self.__boutons: dict
        self.__boutons_old: dict
        self.__connected: bool
        self.__joystick_name: str
        self.__liste_actions: list

        self.__boutons_old: int = 0
        self.__connected = False
        self.__liste_actions = [{"temps": 0.2, "coord": [-0.0,0.0]}]
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
            temps_debut = time.time()
            button_state = int(self.__joystick.get_button(0))
            print(self.envoyer_mvmt(x_axis, y_axis))
            temps_fin = time.time()
            temps_diff = temps_fin - temps_debut
            self.__liste_actions.append({"temps": temps_diff, "coord": [round(x_axis,2), round(y_axis,2)]})

    def control_ihm(self,x: float, y: float) -> None:
        """Méthode de la classe Joystick qui permet d'envoyer les controles de l'ihm au serveur.

        Args:
            x (float): Position x
            y (float): Position y
        """
        temps_debut = time.time()
        print(self.envoyer_mvmt(x, y))
        temps_fin = time.time()
        temps_diff = temps_fin - temps_debut
        self.__liste_actions.append({"temps": temps_diff, "coord": [round(x,2), round(y,2)]})

    def retour(self) -> None:
        """Méthode de la classe Joystick qui permet de faire revenir le robot à son emplacement d'origine
        """
        self.__liste_actions.reverse() # Inverser la liste des actions réalisées
        for dictionnaire in self.__liste_actions: # Pour tous les éléments de la liste on envoie au serveur chaque commande 
            self.envoyer_mvmt(-float(dictionnaire.get('coord')[0]),-float(dictionnaire.get('coord')[1]))
            time.sleep(dictionnaire.get("temps"))
        self.__liste_actions = [{"temps": 0.2, "coord": [-0.0, 0.0]}] # Envoie d'une commande d'arrêt à la fin

    def envoyer_mvmt(self, x: float, y: float) -> str:
        """Méthode de la classe Joystick qui permet d'envoyer les messages de mouvements au serveur.
        
        Args:
            x (float): Coord x du joystick
            y (float): Coord y du joystick

        Return:
            str: Message envoyé au serveur
        """
        msg: str = f"MVMT 1 {round(x,2)} {round(y,2)}" # Initalisation du message
        self.__client.envoyer(msg) # Envoie du message
        time.sleep(0.1) # Attente avant d'envoyer un nouveau message pour ne pas flood le serveur

        return msg

    def mainloop(self) -> None:
        """Méthode de la classe Joystick qui permet d'envoyer au serveur les actions effectuées avec la manette.

        Args:
            socket (socket): Socket en cours avec le serveur
        """
        while self.__boutons_old != 1: # Tant que le bouton 1 (B ou Rond) n'est appuyé alors on regard si des déplacements sont réalisés
            self.get_buttons() # Déplacement joystick
            self.__boutons_old = int(self.__joystick.get_button(1)) # Bouton 1 (B ou Rond)
            if int(self.__joystick.get_button(2)) == 1: # Bouton 2 (X ou Carré) pour le retour arrière
                self.retour()

