from kivymd.app import MDApp
from kivy.lang import Builder

from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBody, TwoLineAvatarIconListItem
from kivymd.uix.button import MDIconButton
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu

Window.size = (360, 640)

KV = '''
<TextField@MDTextField>:
    size_hint: None, None
    size: 80, 50
    font_size: 14

<MainWindow>:
    orientation: 'vertical'

    MDToolbar:
        anchor_title: 'center'
        title: "ZernoApp"
        left_action_items: [["tune", lambda x: app.callback()]]
        right_action_items: [["history", lambda x: app.callback()]]

    MDLabel:
        font_size: 22
        text: 'Добавить заказ'

    MDBoxLayout:
        orientation: 'horizontal'
        spacing: "20dp"
        padding: "20dp"

        TextField:
            hint_text: "Сколько тонн?"

        TextField:
            hint_text: "Что кидаете?"

        TextField:
            hint_text: "Сколько вас?"

    MDBottomNavigation:

        MDBottomNavigationItem:
            icon: 'plus'
            name: "screen 1"
            text: 'Главная'
            

        MDBottomNavigationItem:
            icon: 'clock-outline'
            name: "screen 2"
            text: 'Открытые'

        MDBottomNavigationItem:
            icon: 'check-bold'
            name: "screen 3"
            text: 'Закрытые'
'''

class MainWindow(MDBoxLayout):
    pass

class ZernoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    ZernoApp().run()