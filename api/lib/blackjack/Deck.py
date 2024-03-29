
class Deck: 
    '''
    @title Deck
    
    @desc A 52-card deck of integer values that represent cards. Aces are 11 by 
    default. All face cards are 10. 
    '''
    def __init__(self): 
        self.cards = []
        
        #4 of each 
        for i in range(2, 10): 
            for n in range(4): 
                self.cards.append(i)
                
        #16 10s
        for i in range(16): 
            self.cards.append(10)
            
        #4 aces 
        for i in range(4): 
            self.cards.append(11)
        
        