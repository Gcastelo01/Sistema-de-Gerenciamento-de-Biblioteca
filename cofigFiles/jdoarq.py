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
        self.loginButton.set_css_name('logbutton')
        
        self.registerButton = Gtk.Button(label='Register')
        self.registerButton.set_css_name("regbutt")

        self.box.pack_start(self.loginButton, True, True, 1)
        self.box.pack_end(self.registerButton, True, True, 1)
        self.box.set_spacing(6)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_path("cofigFiles/.css/mainwindow.css")

win = LoginScreen()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()