from kivy.lang import Builder
from kivymd.app import MDApp
from sub.joystick import Joystick

KV = '''
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "MDTopAppBar"
        right_action_items: [["dots-vertical", lambda x: app.quit()], ["clock", lambda x: app.quit()]

    MDLabel:
        text: "Content"
        halign: "center"
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def joystick_detection(self) -> None:
        self.__joystick: Joystick = Joystick()
        return self.__joystick.get_name()


Test().run()