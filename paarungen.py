
# coding: utf-8

# # Paarungen

# Prinzip: Jeder gegen jeden
# 
# aus Wikipedia


def lshift( lst) :
    return [lst[-1]] + lst[:-1] 


class Paarungen :
    
    def __init__( self, anz_teams) :
        """ <anz_teams> muss in dieser Einfach-Version gerade sein! """
        self.lng = anz_teams
        self.anz_runden = int(self.lng/2)
        self.pairs = self.create_pairs()
        
    def create_pairs( self ) :
        # Ursprungsliste mit Team-Nummern 
        lst = [n+1 for n in range(self.lng)]
        
        # Aus dieser Liste die Paarungen bilden
        pairs= []
        for r in range(self.lng-1 ) :
            
            # Paarungen einer Runde
            rnd = [(lst[x],lst[-1-x]) for x in range(self.anz_runden)]
            pairs.append(rnd)
        
            # Vorbereiten der Liste fuer die naechste Runde
            lst = lshift(lst)
            x = lst[1]
            lst[1] = lst[0]
            lst[0] = x
            
        return pairs
    
    def get_round( self, idx) :
        rnd = self.pairs[idx]
        return ([el[0] for el in rnd],[el[1] for el in rnd])
    


if __name__ == "__main__" :

    p = Paarungen(8)
    for i in p.pairs :
        print( i)
    print( p.get_round(1))

