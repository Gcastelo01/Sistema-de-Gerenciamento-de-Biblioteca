#TODO   Criar classe MenuScreen para tela de menu

import gi
from .libfunctions.libFunctions import User, Livro


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class LoginScreen(Gtk.Window, User):
    def __init__(self):

        Gtk.Window.__init__(self, title='Tela de Login', default_width=480, default_heigth=690)
        
        self.box = Gtk.Box(fill=True)
        self.add