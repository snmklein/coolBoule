
"""

Boule-Turnier-Software-Implementierung mit Klassen

Eigenschaften:

- Versuch, globale Variable zu vermeiden
- Ohne Datenbank-Anbindung, um meinen kleinen Laeppe nicht zu ueberlasten


"""

from tksheet import Sheet
from tkinter import *
from tkinter import messagebox
import pandas as pd
from random import randint
from teilnehmer import Teilnehmer
from paarungen import Paarungen
from tabelle import Tabelle

def random_result( res) :
    """ Ermittle ein Boule-Zufallsergebnis, wenn noch keines eingetragen ist """
    if res == (0,0) :
        idx = randint(0,1)
        val = randint(1,12)
        erg = [13,13]
        erg[idx] = val
        res = tuple(erg)
    return res


class BouleApp:
    def __init__(self, parent):

        self.df = None
        self.count = 100
        self.idx_runde = 0
        self.paarungen = Paarungen(8)
        self.tab = Tabelle()

        self.mainFrame = Frame(parent)
        self.master = parent
        # self.mainFrame.pack()
        self.mainFrame.grid(row=0,column=0, sticky="nswe")
        # parent.geometry('1400x300')
        parent.title("Boule Turnier Software")

        self.menu = Menu(self.mainFrame)
        self.insert_submenus( )

        self.lframe = Frame( parent,bg="yellow")
        self.insert_lframe()

        self.rframe = Frame( parent,bg="orange")
        self.insert_rframe()

        parent.config(menu=self.menu)


    def insert_lframe(self) :
        # self.lframe.pack( side=LEFT)
        self.lframe.grid(row=0,column=0, sticky="nswe")
        ltitle=Label(self.lframe,text="Tabelle")
        ltitle.pack()
        # ltitle.grid(row = 0, column = 0, sticky = "nswe")
        self.tn_sheet = Sheet( self.lframe, # data = [[1,2],[3,4],[5,6]])
                               data =
                                    [[1,"a",0,0],[2,"b",0,0],[3,"c",0,0],
                                    [4,"d",0,0],[5,"e",0,0],[6,"f",0,0],
                                    [7,"g",0,0],[8,"h",0,0]],
                               height=300,width=400,  # sonst gelber Balken
                               show_row_index=False,
                               show_x_scrollbar=False,
                               show_y_scrollbar=False)
        self.tn_sheet.pack( )
        # self.tn_sheet.grid(row = 1, column = 0, sticky = "nswe")
        self.tn_sheet.headers(["Start-Nr","Name","Siege","Punkte"])
        self.tn_sheet.set_all_column_widths(width=None,
                                         only_set_if_too_small=False,
                                         redraw=True,
                                         recreate_selection_boxes=True)
        self.tn_sheet.column_width(column=1, width=230,
                                   only_set_if_too_small = False, redraw = True)


    def insert_rframe(self) :
        # self.lframe.pack( side=LEFT)
        self.rframe.grid(row=0,column=1, sticky="nswe")
        self.rtitle=Label(self.rframe,
                     text="Ergenisse Runde {}".format(self.idx_runde+1))
        self.rtitle.pack()
        # ltitle.grid(row = 0, column = 0, sticky = "nswe")
        self.erg_sheet = Sheet( self.rframe, # data = [[1,2],[3,4],[5,6]])
                               data =
                                    [[1,"a",0,0,"b"],[2,"c",0,0,"d"],
                                    [3,"e",0,0,"f"], [4,"g",0,0,"h"]],
                                width=600,
                               show_row_index=False,
                               show_x_scrollbar=False,
                               show_y_scrollbar=False)
        self.erg_sheet.pack( )
        # self.tn_sheet.grid(row = 1, column = 0, sticky = "nswe")
        self.erg_sheet.headers(["Bahn","Team A","   ","   ","Team B"])
        self.erg_sheet.set_all_column_widths(width=None,
                                         only_set_if_too_small=False,
                                         redraw=True,
                                         recreate_selection_boxes=True)
        self.erg_sheet.column_width(column=1, width=230,
                                   only_set_if_too_small = False, redraw = True)
        self.erg_sheet.column_width(column=2, width=30,
                                   only_set_if_too_small = False, redraw = True)
        self.erg_sheet.column_width(column=3, width=30,
                                   only_set_if_too_small = False, redraw = True)
        self.erg_sheet.column_width(column=4, width=230,
                                   only_set_if_too_small = False, redraw = True)


    def insert_submenus( self) :
        
        ei = Menu( self.menu,tearoff=0)
        self.menu.add_cascade(label="Einstellungen", menu=ei,command=self.submit)
        ei.add_command(label="Grundeinstellungen (Anzahl der Plätze usw.)",
                       command=self.submit)
        ei.add_command(label="Formation (Tete a tete, Doublette, Triplette)",
                       command=self.submit)
        ei.add_command(label="Neue Teilnehmerliste erstellen",
                       command=self.submit)
        ei.add_command(label="Zeitlimit",command=self.submit)

        tn = Menu(self.menu)
        self.menu.add_cascade(label="Teilnehmer", menu=tn)
        tn.add_command(label="Teilnehmer einpflegen",command=self.tn_edit)
        # tn.add_command(label="Teilnehmerliste erstellen",command=self.submit)
        tn.add_command(label="Teilnehmer Status ändern A/P",
                       command=self.insert_df)

        erg = Menu(self.menu)
        self.menu.add_cascade(label="Ergebnisse", menu=erg)
        erg.add_command( label="Eingeben", command=self.erg_edit)
        erg.add_command( label="Speichern", command=self.erg_save)
        erg.add_command( label="In Tabelle eintragen",
                         command=self.insert_last_erg)
        erg.add_command( label="Ergebnisse löschen",
                         command=self.erg_clear)
        erg.add_command( label="Nächste Runde",command=self.erg_nxtround)

    def submit(self) :
        self.count += 1
        messagebox.showinfo( "Information",
                             "Aktueller Zählerstand: {} ".format( self.count))

    def erg_insert_paarungen(self) :
        pairlst = self.paarungen.get_round(self.idx_runde)
        t1 = [self.df['Name'][x-1] for x in pairlst[0]]
        t2 = [self.df['Name'][x-1] for x in pairlst[1]]
        self.erg_sheet.set_column_data(1,values=tuple(t1),redraw=True)
        self.erg_sheet.set_column_data(4,values=tuple(t2),redraw=True)


    def insert_df( self) :
        if not self.df.empty :
            messagebox.showinfo("Teilnehmer",
                                "Name: {}".format(list(self.df['Name'])[2]))
            self.tn_sheet.set_column_data(1, values=tuple(self.df['Name']),
                                          redraw=True)
            self.tn_sheet.refresh()
            self.erg_insert_paarungen()

        self.count += 20
        
    def tn_edit(self) :
        app = Teilnehmer(self)

    def erg_edit(self) :
        self.erg_sheet.readonly_columns([0,1,4],readonly=True,redraw=True)
        self.erg_sheet.enable_bindings()

    def erg_save(self) :
        self.erg_sheet.disable_bindings()
        e1=map(int,self.erg_sheet.get_column_data(2))
        e2=map(int,self.erg_sheet.get_column_data(3))
        eges= [ random_result(el) for el in list(zip(e1,e2))]
        print(eges)
        eges_lst = list(zip(*eges))
        print(eges_lst)
        self.erg_sheet.set_column_data( 2, values=eges_lst[0],redraw=True)
        self.erg_sheet.set_column_data( 3, values=eges_lst[1],redraw=True)
        pairlst = self.paarungen.get_round(self.idx_runde)
        pges = list(zip(pairlst[0],pairlst[1]))
        print(pges)
        ergebnis=list(zip(pges,eges))
        print(ergebnis)
        self.last_erg = ergebnis

    def erg_clear(self):
        """ Loeschen der Ergebnisspalte """
        self.erg_sheet.set_column_data(2, values=4 * [0], redraw=True)
        self.erg_sheet.set_column_data(3, values=4*[0], redraw=True)

    def erg_nxtround(self):
        self.idx_runde +=1
        self.rtitle.config(text="Ergenisse Runde {}".format(self.idx_runde+1))
        self.erg_insert_paarungen()
        self.erg_clear()
        
    def insert_last_erg( self) :
        self.tab.ins_reslst( self.last_erg)
        self.tn_sheet.set_column_data(0, values=tuple(self.tab.tab.index),
                                          redraw=True)
        self.tn_sheet.set_column_data(1,
                                      values=[self.df['Name'][x-1] for x in self.tab.tab.index],
                                      redraw=True)
        self.tn_sheet.set_column_data(2, values=tuple(self.tab.tab['Siege']),
                                      redraw=True)
        self.tn_sheet.set_column_data(3, values=tuple(self.tab.tab['Punkte']),
                                      redraw=True)

root = Tk()
boule = BouleApp(root)
root.mainloop()
