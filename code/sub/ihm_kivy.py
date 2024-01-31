from kivymd.uix.button import MDRoundFlatButton, MDFloatingActionButton
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import *
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from collections import deque
from kivy.clock import Clock
from kivy.clock import Clock
import time

class Interface(MDApp):
    def add_client(self, client, joystick):
        self.__client = client
        self.__joystick = joystick
    def build(self):
        self.__liste_notifications: list = []
        Clock.schedule_interval(self.notification_queue, 1.5)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.__screen_manager = ScreenManager(transition=SlideTransition())
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
                    on_text_validate=self.valider,
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
                    on_text_validate=self.valider
                ),
                MDRoundFlatButton(
                    id="connexion_serveur_bouton",
                    text="Connexion",
                    font_size=18,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_press=self.__client.connexion
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
                        on_text_validate=self.valider
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
                        on_text_validate=self.valider
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
            MDScreen(
                MDBoxLayout(
                MDLabel(id="joystick_label",text='Joystick value: 0, 0', color=(0, 0, 0, 1)),
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
                id="joystick_conainer",
                orientation='vertical',
            ),
                # Page d'accueil
                MDTopAppBar(
                    id="menu_top_bar",
                    pos_hint={"top": 1},
                    elevation=4,
                    title="Robot_6",
                    left_action_items=[["menu", lambda x: self.nav_drawer("open")]],
                    right_action_items=[["controller_state", lambda x: self.controller_state()]]
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
        self.__screen_manager.current = "Connexion"
        return self.__screen_manager

    def quitter(self):
        self.on_stop()
        self.stop()

    def valider(self,tmp):
        screen = self.__screen_manager.get_screen(self.__screen_manager.current).ids
        if "connexion_serveur_card" in screen.keys():
            if screen.connexion_serveur_card.ids.connexion_ip.focus == True:
                screen.connexion_serveur_card.ids.connexion_port.focus = True
            elif screen.connexion_serveur_card.ids.connexion_port.focus == True:
                self.__client.connexion("tmp")
        elif "connexion_card" in screen.keys():
            if screen.connexion_card.ids.connexion_login.focus == True:
                screen.connexion_card.ids.connexion_password.focus = True
            elif screen.connexion_card.ids.connexion_password.focus == True:
                self.__client.authentification("tmp")

    def notification_info(self, message: str, couleur: str) -> None:
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
            ))

    def controller_state(self):
        if self.__client.get_joystick_state():
            self.theme_cls.primary_palette = "Green"
            self.notification_info(f"Your controller {self.__client.get_joystick_name()} is detected.", "#82F069")
            ################# Désactiver le joystick graphique
        else:
            self.theme_cls.primary_palette = "Red"
            self.notification_info(f"No controller as been detected.", "#F9C649")
            ################# Désactiver le activer le joystick graphique
    
    def notification_queue(self, dt) -> None:
        if self.__liste_notifications != []:
            self.__liste_notifications[0].open()
            del self.__liste_notifications[0]
        
    def controller_state_reset(self):
        self.theme_cls.primary_palette = "BlueGray"

    def switch_screen(self, instance_list_item: OneLineListItem):
            self.__screen_manager.current = instance_list_item.text
            self.nav_drawer("close")

    def nav_drawer(self, action: str):
        self.__screen_manager.get_screen(self.__screen_manager.current).ids.navigation_layout.ids.nav_drawer.ids.nav_drawer_menu.ids.nav_drawer_header.text = f"Connecté en tant que {self.__client.get_login()}"
        self.__screen_manager.get_screen(self.__screen_manager.current).ids.navigation_layout.ids.nav_drawer.set_state(action)

    def on_joystick_move(self, instance, touch):
        container = self.__screen_manager.get_screen("Accueil").ids.joystick_conainer.ids
        joystick_box = container.joystick_box
        joystick_button = joystick_box.ids.joystick_button
        joystick_label = container.joystick_label
        if joystick_button.collide_point(*touch.pos):
            # Calcul des déplacements relatifs par rapport au centre du joystick
            dx = touch.pos[0] - joystick_box.center_x
            dy = touch.pos[1] - joystick_box.center_y

            # Normalisation des valeurs dans la plage de -1 à 1
            x = max(-1, min(1, dx / (joystick_box.width / 2)))
            y = max(-1, min(1, dy / (joystick_box.height / 2)))

            # Mise à jour de la position du bouton
            joystick_button.center_x = joystick_box.center_x + x * (joystick_box.width / 2)
            joystick_button.center_y = joystick_box.center_y + y * (joystick_box.height / 2)

            x = (joystick_button.center_x - joystick_box.x - joystick_box.width / 2) / (joystick_box.width / 2)
            y = (joystick_button.center_y - joystick_box.y - joystick_box.height / 2) / (joystick_box.height / 2)
            joystick_label.text = f'Joystick value: {-x:.2f}, {y:.2f}'
            self.__joystick.envoyer_mvmt(x, y)

    def on_joystick_release(self, instance, button):
        container = self.__screen_manager.get_screen("Accueil").ids.joystick_conainer.ids
        joystick_box = container.joystick_box
        joystick_button = joystick_box.ids.joystick_button
        joystick_label = container.joystick_label
        joystick_button.x = joystick_box.center_x - 25
        joystick_button.y = joystick_box.center_y - 25
        joystick_label.text = 'Joystick value: 0, 0'
        self.__joystick.envoyer_mvmt(0, 0)