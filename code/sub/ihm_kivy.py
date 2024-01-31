from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import *
from kivymd.uix.list import MDList, OneLineListItem

class Interface(MDApp):
    def add_client(self, client):
        self.__client = client
    def build(self):
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
                # Page d'accueil
                MDTopAppBar(
                    id="menu_top_bar",
                    pos_hint={"top": 1},
                    elevation=4,
                    title="Robot_6",
                    left_action_items=[["menu", lambda x: self.nav_drawer("open")]],
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
                                text="Page 1",
                                text_color=(1,1,1,1),
                                icon="",
                                on_press=self.switch_screen
                            ),
                            MDNavigationDrawerItem(
                                text="Page 2",
                                text_color=(1,1,1,1),
                                icon="",
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
        MDSnackbar(
                MDLabel(
                    text=message,
                    theme_text_color="Custom",
                    text_color=(0,0,0,1)
                ),
                y=15,
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                md_bg_color= couleur,
            ).open()


    def switch_screen(self, instance_list_item: OneLineListItem):
            self.__screen_manager.current = ["Screen 1", "Screen 2"][instance_list_item.text]
            self.nav_drawer("close")

    def nav_drawer(self, action: str):
        self.__screen_manager.get_screen(self.__screen_manager.current).ids.navigation_layout.ids.nav_drawer.ids.nav_drawer_menu.ids.nav_drawer_header.text = f"Connecté en tant que {self.__client.get_login()}"
        self.__screen_manager.get_screen(self.__screen_manager.current).ids.navigation_layout.ids.nav_drawer.set_state(action)