#TODO   Criar classe MenuScreen para tela de menu

import gi
# from . import libfunctions

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class LoginScreen(Gtk.Window):
    def __init__(self):
        self.__user = 0

        #Inicializando a janela
        Gtk.Window.__init__(self, title='Tela de Login')
        Gtk.Window.set_default_size(self, 420, 680)

        #Criando uma listbox
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(self.listbox)

        #Criando as fileiras da janela:
        row_1 = Gtk.ListBoxRow()
        box_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row_1.add(box_1)
        
        #Criando a label e a entrada de texto
        label = Gtk.Label("Usuário: ")
        self.userName = Gtk.Entry()
        self.userName.set_text("Nome de usuário")
        box_1.pack_start(label, True, False, 30)
        box_1.pack_start(self.userName, True, True, 30)
        self.listbox.add(row_1)
        
        #Criando segunda Listbox
        row_2 = Gtk.ListBoxRow()
        box_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row_2.add(box_2)

        #Criando a label e a entrada de texto
        label = Gtk.Label("Senha: ")
        self.userName = Gtk.Entry()
        self.userName.set_text("Password")
        box_2.pack_start(label, True, False, 30)
        box_2.pack_start(self.userName, True, True, 30)
        self.listbox.add(row_2)

        #Criando 3ª listbox para posicionar os botões
        row_3 = Gtk.ListBoxRow()
        box_3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row_3.add(box_3)

        #Criando botão de Logar:
        self.logButt = Gtk.Button()
        self.logButt.set_label("Login")
        box_3.pack_start(self.logButt, True, False, 15)

        #Criando botão de Cadastro
        self.cadButt = Gtk.Button()
        self.cadButt.set_label("Cadastre-se")
        box_3.pack_end(self.cadButt, True, False, 15)

        self.listbox.add(row_3)
    
win = LoginScreen()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()