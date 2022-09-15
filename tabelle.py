
import pandas as pd

class Tabelle:
    """ Daten fuer rechten Fame der Hauptmaske """

    def __init__(self) :

        self.tab = pd.DataFrame({'Start_Nr' : [for i in range(1,9)],
                                 'Siege' : 0,
                                 'Punkte' : 0})
        
    
