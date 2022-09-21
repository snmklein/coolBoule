
import pandas as pd

class Tabelle:
    """ Daten fuer rechten Fame der Hauptmaske """

    def __init__(self) :

        self.tab = pd.DataFrame({'Start_Nr' : [i for i in range(1,9)],
                                 'Siege' : 0,
                                 'Punkte' : 0})
        self.tab.set_index('Start_Nr', inplace=True)
        
    def ins_reslst( self, reslst) :
        """ Eintragen einer Liste von Ergebnissen <reslst> der Form
            ((Teiln.1, Teiln.2),(Punkte Teiln.1,Punkte Teiln.2)) """
        for ((t1,t2),(a,b)) in reslst:
            delta = a - b
            self.tab.loc[t1]['Punkte'] += delta
            self.tab.loc[t2]['Punkte'] -= delta
            if delta > 0 :
                self.tab.loc[t1]['Siege'] += 1
            else :
                self.tab.loc[t2]['Siege'] += 1
        self.tab = self.tab.sort_values( by=['Siege','Punkte'], ascending=False)
        return self.tab

    
if __name__ == "__main__" :

    app = Tabelle()
    app.ins_reslst( [((1,2),(13,8)),((3,4),(7,13)),
                     ((5,6),(13,9)),((7,8),(4,13))])
    print(app.tab)
