# -*- coding : utf8 -*-
import socket, json, sys, hashlib, time
from sub.joystick import Joystick
from sub.ihm_kivy import Interface

class Client:
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
        """Méthode constructeur de la classe Client.
        
        Args:
            ip_serveur: str -> L'IP du serveur.
            port_serveur: int -> Le port d'écoute du serveur.
        """
        # Déclaration
        self.__ip_serveur: str
        self.__port_serveur: int
        self.__socket: socket
        self.__connexion_ok: bool
        self.__authentification_ok: bool
        self.__joystick: Joystick
        self.__interface: Interface
        self.__nb_tentatives: int
        self.__login: str
        # Initialisation
        self.__login = ""
        self.__ip_serveur = ip_serveur
        self.__port_serveur = port_serveur
        self.__connexion_ok = False
        self.__authentification_ok = False
        self.__nb_tentatives = 1
        self.__joystick = Joystick()
        self.__interface = Interface()
        self.__interface.add_client(self, self.__joystick)
        self.__interface.run()

    def get_connexion_ok(self) -> bool:
        """Méthode de la classe Client qui permet de savoir si la connexion à été initialisée.

        Returns:
            bool: True si la connexion est réussite
        """
        return self.__connexion_ok

    def get_authentification_ok(self) -> bool:
        """Méthode de la classe Client qui permet de savoir si l'utilisateur est connecté.

        Returns:
            bool: True si l'utilisateur est connecté
        """
        return self.__authentification_ok

    def get_joystick(self) -> Joystick:
        """Méthode de la classe Client qui permet de savoir si une manette est connecté.

        Returns:
            Joystick: True si une manette est présente
        """
        return self.__joystick
    
    def get_login(self) -> str:
        """Méthode de la classe Client qui permet de savoir le nom d'utilisateur.

        Returns:
            str: Identifiant de l'utilisateur
        """
        return self.__login

    def connexion(self) -> None:
        """Méthode de la classe Client qui initialise le socket
        """
        card = self.__interface._Interface__screen_manager.get_screen(self.__interface._Interface__screen_manager.current).ids.connexion_serveur_card.ids
        self.__ip_serveur = card.connexion_ip.text
        self.__port_serveur = int(card.connexion_port.text)
        
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création de la socket
            self.__socket.connect((self.__ip_serveur, self.__port_serveur)) # Connection au service distant
            self.__joystick.get_update(self)
            # Filtrage MAC
            msg_serveur = self.recevoir()
            if msg_serveur.split()[1].lower() == "accepted": # Mac
                self.__connexion_ok = True
                self.__interface._Interface__screen_manager.current = "Authentification"
                self.__interface.notification_info("Connexion Réussite", "#82F069")
            else:
                self.__interface.notification_info("Connexion impossible", "#F9C649")
        except Exception as ex:
            self.__interface.notification_info("Serveur non joignable", "#F9C649")

    def authentification(self,tmp) -> str:
        """Méthode de la classe Client qui permet à l'utilisateur de s'authentifier.
        """
        card = self.__interface._Interface__screen_manager.get_screen(self.__interface._Interface__screen_manager.current).ids.connexion_card.ids
        msg_serveur = self.recevoir()
        if self.__connexion_ok:
            if not self.__authentification_ok and self.__nb_tentatives < 3:
                msg_serveur = "a a"
                self.__login = card.connexion_login.text
                passwd = hashlib.sha256((card.connexion_password.text).encode('utf-8')).hexdigest()
                self.envoyer(f"CONN LOGIN {self.__login} {passwd}")
                msg_serveur = self.recevoir()
                self.__nb_tentatives += 1
                if msg_serveur.split()[1] == "ACCEPTED":
                    self.__authentification_ok = True
                    self.__interface.notification_info("Authentification Réussite", "#82F069")
                    self.__interface._Interface__screen_manager.current = "Accueil"
                elif msg_serveur.split()[1] == "REFUSED":
                    print(msg_serveur)
                    msg_serveur = self.recevoir()
                    print("3",msg_serveur)
                    self.__interface.notification_info("Identifiants invalides", "#F9C649")
                    card.connexion_login.error = True
                    card.connexion_password.error = True
            elif (not self.__authentification_ok) and (self.__nb_tentatives == 3):
                    self.__interface.notification_info("Trop de tentatives", "#F9C649") # Ne veut pas s'afficher
                    card.connexion_login.error = True
                    card.connexion_password.error = True
                    time.sleep(2)
                    self.quitter()

    def quitter(self) -> None:
        """Méthode de la classe Client qui permet de fermer le client.
        """
        if self.__connexion_ok:
            self.envoyer("QUIT")
            self.__socket.close()
        self.__interface.quitter()

    def deconnecter(self) -> None:
        """Méthode de la classe Client qui permet à l'utilisateur de se déconnecter.
        """
        self.__interface.notification_info("Déconnexion", "#F9C649")
        self.envoyer("QUIT")
        self.__socket.close()
        self.__interface._Interface__screen_manager.current = "Connexion"
        self.__connexion_ok = False
        self.__authentification_ok = False
        self.__interface.controller_state_reset()
        self.__nb_tentatives = 1

    def get_joystick_name(self) -> str:
        """Méthode de la classe Client qui permet de savoir le nom de la manette connectée.

        Returns:
            str: Nom de la manette
        """
        return self.__joystick.get_name()

    def get_joystick_state(self) -> bool:
        """Méthode de la classe Client qui permet de savoir si une manette est connectée.

        Returns:
            bool: True si une manette est reconnu False sinon
        """
        return self.__joystick.is_connected()

    def control_manette(self) -> None:
        """Méthode de la classe Client qui permet de lancer l'authentification et l'envoie des contrôles.
        """
        if self.get_joystick_state(): # Si une manette est connectée alors on lance la recherche de boutons
            self.__joystick.mainloop()
            
    def control_retour(self) -> None:
        """Méthode de la classe Client qui permet de lancer la fonction retour
        """
        self.__joystick.retour()

    def envoyer(self, msg: str) -> None:
        """Méthode de la classe Client qui permet d'envoyer un message au serveur.

        Args:
            msg (str): Message à envoyer au serveur
        """
        self.__socket.send(json.dumps({"q": f"{msg}"}).encode("utf-8"))

    def recevoir(self) -> str:
        """Méthode de la classe Client qui permet de recevoir le message envoyé par le serveur.

        Returns:
            str: Message reçu
        """
        try:
            msg = self.__socket.recv(1024).decode("utf-8")
            print(msg)
        except:
            msg = "a a"
        return json.loads(msg)["q"]

if __name__=="__main__":
    try:
        ip_serveur = str(sys.argv[1].split(":")[0])
        port_serveur = int(sys.argv[1].split(":")[1])
    except IndexError as e:
        ip_serveur = "10.3.141.1"
        port_serveur = 5001

    client: Client
    client = Client(ip_serveur=ip_serveur, port_serveur=port_serveur)