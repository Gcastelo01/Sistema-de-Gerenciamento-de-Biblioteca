#TODO   Criar classe MenuScreen para tela de menu

import gi
# from . import libfunctions

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class LoginScreen(Gtk.Window):
    def __init__(self):
        self.__user = 0

        Gtk.Window.__init__(self, title='Tela de Login')
        Gtk.Window.set_default_size(self, 420, 680)

        self.box = Gtk.Box(spacing=10)
        self.add(self.box)

        self.loginButton = Gtk.Button(label="login")
        self.loginButton.set_name('logbutton')

        self.box.pack_start(self.loginButton, False, False, 6)
        self.box.set_spacing(30)
    
    def style(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(".cofigfiles.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gtk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

win = LoginScreen()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()