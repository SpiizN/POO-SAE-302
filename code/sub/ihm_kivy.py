from kivymd.uix.button import MDRoundFlatButton, MDFloatingActionButton
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import *
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.clock import Clock
import time

class Interface(MDApp):
    def build(self):
        """Méthode constructeur de la classe Interface/MDAPP

        Returns:
            Les pages de l'interface pour le builder KivyMD 
        """
        self.__liste_notifications: list = []
        Clock.schedule_interval(self.notification_queue, 2.2) # Initialisation du système de gestion des notifiactions
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.__screen_manager = ScreenManager(transition=SlideTransition()) # Initialisation du système de gestion des pages
        self.__screen_manager.add_widget(MDScreen(
            MDCard( # Page de connexion
                MDLabel(
                    text="Connexion au serveur",
                    halign="center",
                    size_hint_y=None,
                    font_style="H5",
                ),
                MDTextField(
                    id="connexion_ip",
                    mode="fill",
                    hint_text="Adresse IP",
                    icon_right="ip-network",
                    text="10.3.141.1",
                    size_hint_x=None,
                    width=300,
                    font_size=18,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_text_validate=lambda x:self.valider(),
                ),
                MDTextField(
                    id="connexion_port",
                    mode="fill",
                    hint_text="Port",
                    icon_right="ethernet",
                    text="5001",
                    size_hint_x=None,
                    width=300,
                    font_size=18,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_text_validate=lambda x:self.valider()
                ),
                MDRoundFlatButton(
                    id="connexion_serveur_bouton",
                    text="Connexion",
                    font_size=18,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_press=lambda x:self.__client.connexion()
                ),
                MDRoundFlatButton(
                    id="quitter_bouton",
                    text="Quitter",
                    font_size=18,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_press=lambda x:self.__client.quitter(),
                ),
                id="connexion_serveur_card",
                size_hint=(None, None),
                size=(400, 500),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                
                padding=25,
                spacing=25,
                orientation='vertical'
            ),
            id="connexion_screen",
            name="Connexion"
        ))
        self.__screen_manager.add_widget(MDScreen(
                # Ajouter logo
                MDCard( # Page d'authentification
                    MDLabel(
                        text="Authentification",
                        halign="center",
                        size_hint_y=None,
                        font_style="H5",
                        padding_y=15
                    ),
                    MDTextField(
                        id="connexion_login",
                        mode="fill",
                        hint_text="Identifiant",
                        icon_right="account",
                        size_hint_x=None,
                        width=300,
                        font_size=18,
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        on_text_validate=lambda x:self.valider()
                    ),
                    MDTextField(
                        id="connexion_password",
                        mode="fill",
                        hint_text="Mot de passe",
                        icon_right="eye-off",
                        size_hint_x=None,
                        width=300,
                        font_size=18,
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        password=True,
                        on_text_validate=lambda x:self.valider()
                    ),
                    MDRoundFlatButton(
                        id="connexion_bouton",
                        text="Authentification",
                        font_size=18,
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        on_press=self.__client.authentification
                    ),
                    MDRoundFlatButton(
                        id="quitter_bouton",
                        text="Quitter",
                        font_size=18,
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        on_press=lambda x:self.__client.quitter(),
                    ),
                    id="connexion_card",
                    size_hint=(None, None),
                    size=(400, 500),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    elevation=10,
                    padding=25,
                    spacing=25,
                    orientation='vertical'
                ),
                id="connexion_screen",
                name="Authentification"
            ))
        self.__screen_manager.add_widget(
            # Page d'acceuil
            MDScreen(
                MDBoxLayout(
                MDRoundFlatButton(id="joystick_retour", text="Retour au départ",on_press=lambda x:self.__client.control_retour(),pos_hint={'center_x': 0.9, 'center_y': 0.5},),
                MDBoxLayout(
                    MDFloatingActionButton(
                        id="joystick_button",
                        icon="camera-control",
                        size_hint=(None, None),
                        size=('50dp', '50dp'),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                        on_touch_move=self.on_joystick_move,
                        on_touch_up=self.on_joystick_release
                    ),
                    id="joystick_box",
                    orientation='vertical',
                    size_hint=(None, None),
                    size=('150dp', '150dp'),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    padding=10
                ),
                id="joystick_container",
                orientation='vertical',
                ),
                MDTopAppBar(
                    id="menu_top_bar",
                    pos_hint={"top": 1},
                    elevation=4,
                    title="Robot_6",
                    left_action_items=[["menu", lambda x: self.nav_drawer("open")]],
                    right_action_items=[["controller", lambda x: self.controller_state()]]
                ),
                MDNavigationLayout(
                    MDNavigationDrawer(
                        MDNavigationDrawerMenu(
                            MDNavigationDrawerHeader(
                                id="nav_drawer_header",
                                title="Menu",
                                text=" ",
                                spacing="4dp",
                                padding=("12dp", 0, 0, "36dp"),
                            ),
                            MDNavigationDrawerItem(
                                text="Accueil",
                                text="Accueil",
                                text_color=(1,1,1,1),
                                icon="camera-control",
                                on_press=self.switch_screen
                            ),
                            MDNavigationDrawerItem(
                                text="Log",
                                text_color=(1,1,1,1),
                                icon="math-log",
                                on_press=self.switch_screen
                            ),
                            MDNavigationDrawerDivider(),
                            MDNavigationDrawerItem(
                                text="Se Déconnecter",
                                selected_color=(1,0,0,1),
                                selected=True,
                                icon="",
                                on_press=lambda x:self.__client.deconnecter(),
                            ),
                            MDNavigationDrawerItem(
                                text="Quitter",
                                selected_color=(1,0,0,1),
                                selected=True,
                                icon="",
                                on_press=lambda x:self.__client.quitter(),
                            ),
                            id="nav_drawer_menu",
                        ),
                        id="nav_drawer",
                        radius=(0, 16, 16, 0),
                    ),
                    id="navigation_layout",
                ),
                id="accueil_screen",
                name="Accueil"    
            )
        )
        self.__screen_manager.current = "Connexion" # Initialisation de l'interface sur la page de connexion
        return self.__screen_manager

    def quitter(self):
        """Méthode de la classe Interface qui permet de fermer l'interface
        """
        self.stop()
    
    def add_client(self, client, joystick):
        """Méthode de la classe Interface pour récupérer les informations liées au client et à la manette

        Args:
            client (Client): Objet Client
            joystick (Joystick): Objet Joystick
        """
        self.__client = client
        self.__joystick = joystick

    def valider(self):
        """Méthode de la classe Interface qui permet de déplacer l'utilisateur lorsqu'il écrit dans les zones de connexions.
        """
        screen = self.__screen_manager.get_screen(self.__screen_manager.current).ids
        if "connexion_serveur_card" in screen.keys(): # Si l'utilisateur est sur la page de connexion alors il est déplacé dans les zones suivantes lorsqu'il appuie sur entré
            if screen.connexion_serveur_card.ids.connexion_ip.focus == True:
                screen.connexion_serveur_card.ids.connexion_port.focus = True
            elif screen.connexion_serveur_card.ids.connexion_port.focus == True:
                self.__client.connexion()
        elif "connexion_card" in screen.keys(): # Si l'utilisateur est sur la page de connexion alors il est déplacé dans les zones suivantes lorsqu'il appuie sur entré
            if screen.connexion_card.ids.connexion_login.focus == True:
                screen.connexion_card.ids.connexion_password.focus = True
            elif screen.connexion_card.ids.connexion_password.focus == True:
                self.__client.authentification('tmp')

    def notification_info(self, message: str, couleur: str, duration: float=1.5) -> None:
        """Méthode de la classe Interface qui permet d'afficher des notifications sur l'interface.

        Args:
            message (str): Message à afficher
            couleur (str): Couleur de la notification
            duration (float, optional): Durée de la notification. Defaut à 1.5.
        """
        self.__liste_notifications.append(MDSnackbar(
                MDLabel(
                    text=message,
                    theme_text_color="Custom",
                    text_color=(0,0,0,1)
                ),
                y=15,
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                md_bg_color= couleur,
                duration=duration,
            ))

    def controller_state(self):
        """Méthode de la classe Interface qui permet détecter la présence d'une manette et de désactiver le bouton de joystick.
        """
        if self.__client.get_joystick_state(): # Si une manette est présente alors on change de couleur le thème 
            self.theme_cls.primary_palette = "Green" # Une notification de la prise en compte est affiché
            self.notification_info(f"Votre manette {self.__client.get_joystick_name()} est détectée.", "#82F069")
            self.__screen_manager.get_screen("Accueil").ids.joystick_container.ids.joystick_box.ids.joystick_button.disabled = True
            # self.notification_info(f"Pour quitter le mode manette vous devez appuyer sur le bouton 2 (B ou O).", "#0DC5FF", duration=10)
            self.__client.control_manette()
            self.notification_info(f"Vous quitter le mode manette.", "#0DC5FF")
        else: # Si aucune manette n'est présente alors on change la couleur du thème
            self.theme_cls.primary_palette = "Red"
            self.notification_info(f"Aucune manette n'est détectée.", "#F9C649")
            self.__screen_manager.get_screen("Accueil").ids.joystick_container.ids.joystick_box.ids.joystick_button.disabled = False
    
    def notification_queue(self, dt) -> None:
        """Méthode de la classe Interface qui permet de gérer l'affichage de notification.
        """
        if self.__liste_notifications != []: # Si il y a des notifications en attentes
            self.__liste_notifications[0].open() # Afficher la notifiaction
            del self.__liste_notifications[0] # La supprimer de la liste d'attente
        
    def controller_state_reset(self):
        """Méthode de la classe Interface qui permet de réinitialiser le thème de l'application.
        """
        self.theme_cls.primary_palette = "BlueGray"

    def switch_screen(self, instance_list_item: OneLineListItem):
        """Méthode de la classe Interface qui permet de changer de page sur l'interface en fonction du nom de la page.

        Args:
            instance_list_item (OneLineListItem): Nom de la page sur laquelle se rendre
        """
        self.__screen_manager.current = instance_list_item.text # Changement de page
        self.nav_drawer("close") # Fermeture du menu déroulant

    def nav_drawer(self, action: str):
        """Méthode de la classe Interface qui permet d'ouvrir le menu déroulant.

        Args:
            action (str): 'open' ou 'close'
        """
        self.__screen_manager.get_screen(self.__screen_manager.current).ids.navigation_layout.ids.nav_drawer.ids.nav_drawer_menu.ids.nav_drawer_header.text = f"Connecté en tant que {self.__client.get_login()}"
        self.__screen_manager.get_screen(self.__screen_manager.current).ids.navigation_layout.ids.nav_drawer.set_state(action)

    def on_joystick_move(self, instance, touch):
        """Méthode de la classe Interface qui permet de déplacer le joystick de la page d'accueil.
        """
        # Initialisation des variables de joystick
        container = self.__screen_manager.get_screen("Accueil").ids.joystick_container.ids
        joystick_box = container.joystick_box
        joystick_button = joystick_box.ids.joystick_button

        if joystick_button.collide_point(*touch.pos): #Si le bouton n'est pas au position actuel
            # Calcul des déplacements par rapport au centre du joystick
            dx = touch.pos[0] - joystick_box.center_x
            dy = touch.pos[1] - joystick_box.center_y
            # Normalisation des valeurs entre 1 et -1
            x = max(-1, min(1, dx / (joystick_box.width / 2)))
            y = max(-1, min(1, dy / (joystick_box.height / 2)))
            # Mise à jour de la position du bouton
            joystick_button.center_x = joystick_box.center_x + x * (joystick_box.width / 2)
            joystick_button.center_y = joystick_box.center_y + y * (joystick_box.height / 2)
            x = (joystick_button.center_x - joystick_box.x - joystick_box.width / 2) / (joystick_box.width / 2)
            y = (joystick_button.center_y - joystick_box.y - joystick_box.height / 2) / (joystick_box.height / 2)
            self.__joystick.control_ihm(x, y) # Envoie des valeurs au serveur

    def on_joystick_release(self, instance, button):
        """Méthode de la classe Interface qui permet de remettre le joystick au centre lorsqu'on le relache.
        """
        # Initialisation des variables de joystick
        container = self.__screen_manager.get_screen("Accueil").ids.joystick_container.ids
        joystick_box = container.joystick_box
        joystick_button = joystick_box.ids.joystick_button
        # Mise à jour de la position du joystick
        joystick_button.x = joystick_box.center_x - 25
        joystick_button.y = joystick_box.center_y - 25
        self.__joystick.envoyer_mvmt(0, 0) # Envoie de la valeur au serveur pour arreter le robot