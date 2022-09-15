from tksheet import Sheet
import tkinter as tk
from tkinter import filedialog as fdia
import pandas as pd

 
class Teilnehmer(tk.Tk):
    def __init__(self,parent=None):
        tk.Tk.__init__(self)
        self.parent=parent
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.sheet = Sheet(self.frame,
                           data = [[1,"Name 1"],[2,"Name 2"],
                                   [3,"Name 3"],[4,"Name 4"]],
                           show_row_index=False,
                           width=400,
                           show_x_scrollbar=False)
        self.sheet.headers(["Start-Nr","Name"])
        self.sheet.column_width(0, width=50,
                                   only_set_if_too_small = False, redraw = True)
        self.sheet.column_width(1, width=250,
                                   only_set_if_too_small = False, redraw = True)
        self.sheet.enable_bindings()
        self.frame.grid_columnconfigure(0, weight=1, uniform="fred")
        self.frame.grid_columnconfigure(1, weight=1, uniform="fred")
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, columnspan = 2, sticky = "nswe")

        self.button_left = tk.Button( self.frame, text="Load CSV",
                                      command=self.csv_load)
        self.button_left.grid(row=9, column=0, sticky = "nswe")

        self.button_right = tk.Button( self.frame, text="Save and Exit",
                                       command=self.save_csv)
        self.button_right.grid(row=9, column=1, sticky = "nswe")

    def csv_load( self) :
        fd = fdia.askopenfile( filetypes=(('CSV Dateien','*.csv')
                                          ,('All files', '*.*')))
        if fd :
            self.tn = pd.read_csv( fd, sep=";")
            self.sheet.set_sheet_data( data = self.tn.values.tolist())
                                      # [self.tn['Start-Nr'],self.tn['Name']])
        self.sheet.column_width(0, width=50,
                                   only_set_if_too_small = False, redraw = True)
        self.sheet.column_width(1, width=250,
                                   only_set_if_too_small = False, redraw = True)
        self.lift()

    def save_csv( self) :
        col = [self.sheet.get_column_data(c) for c in range(2)]
        # print(len(col))
        # print( col[0])
        # print( self.sheet.headers())
        di = dict(zip(self.sheet.headers(),col))
        print(di)
        df = pd.DataFrame(data=di)
        print(df)
        df.to_csv( "output.csv",sep=";",index=False)
        if self.parent :
            print("Master gefunden")
            self.parent.df = df
            self.parent.tn_sheet.set_column_data(1,
                                        values=tuple(self.parent.df['Name']),
                                        redraw=True)
            self.parent.tn_sheet.refresh()


        self.destroy()



if __name__ == "__main__" :

    app = Teilnehmer()
    app.mainloop()

