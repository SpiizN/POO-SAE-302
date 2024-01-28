from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition


class Interface(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.__screen_manager = ScreenManager()
        self.__screen_manager.add_widget(MDScreen(
            MDCard(
                MDLabel(
                    text="Connexion au serveur",
                    halign="center",
                    size_hint_y=None,
                    font_style="H5",
                    padding_y=15
                ),
                MDTextField(
                    id="connexion_ip",
                    mode="round",
                    hint_text="Adresse IP",
                    icon_right="ip-network",
                    text="10.3.141.1",
                    size_hint_x=None,
                    width=300,
                    font_size=18,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_text_validate=self.valider
                ),
                MDTextField(
                    id="connexion_port",
                    mode="round",
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
                    on_press=self.connexion
                ),
                MDRoundFlatButton(
                    id="quitter_bouton",
                    text="Quitter",
                    font_size=18,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_press=self.quitter
                ),
                id="connexion_serveur_card",
                size_hint=(None, None),
                size=(400, 300),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                elevation=10,
                padding=25,
                spacing=25,
                orientation='vertical'
            ),
            id="connexion_screen",
            name="Connexion"
        ))
        self.__screen_manager.add_widget(MDScreen(
                # Ajouter logo
                MDCard(
                    MDLabel(
                        text="Authentification",
                        halign="center",
                        size_hint_y=None,
                        font_style="H5",
                        padding_y=15
                    ),
                    MDTextField(
                        id="connexion_login",
                        mode="round",
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
                        mode="round",
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
                        text="Connexion",
                        font_size=18,
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        on_press=self.authentification
                    ),
                    MDRoundFlatButton(
                        id="quitter_bouton",
                        text="Quitter",
                        font_size=18,
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        on_press=self.quitter
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
        
        self.__screen_manager.current = "Connexion"
        return self.__screen_manager

    def quitter(self, tmp):
        self.stop()

    def valider(self,tmp):
        screen = self.__screen_manager.get_screen(self.__screen_manager.current).ids
        print(screen)
        if "connexion_serveur_card" in screen.keys():
            if screen.connexion_serveur_card.ids.connexion_ip.focus == True:
                screen.connexion_serveur_card.ids.connexion_port.focus = True
            elif screen.connexion_serveur_card.ids.connexion_port.focus == True:
                self.connexion("tmp")
        elif "connexion_card" in screen.keys():
            if screen.connexion_card.ids.connexion_login.focus == True:
                screen.connexion_card.ids.connexion_password.focus = True
            elif screen.connexion_card.ids.connexion_password.focus == True:
                self.authentification("tmp")

    def connexion(self, tmp):
        if True:
            self.__screen_manager.current = "Authentification"
            self.notification_info("Connexion Réussite", "#82F069")
        else:
            # Adresse mac refusé
            self.notification_info("Connexion Impossible", "#FA7D7D")

    def authentification(self, tmp) -> None:
        
        card = self.__screen_manager.get_screen(self.__screen_manager.current).ids.connexion_card.ids
        login = card.connexion_login
        password = card.connexion_password

        login_text = login.text
        password_text = password.text
        print("Login :", login_text)
        print("Password :", password_text)
        if login_text == "plop": # Ajouter condition identifiant faux
            login.error = True
            password.error = True
            self.notification_info("Identifiant incorrect", "#FA7D7D")
        else:
            self.notification_info("Authentification Réussite", "#82F069")
                   
    
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

if __name__ == "__main__":
    Interface().run()