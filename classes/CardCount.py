from classes.Card import Card

class CardCount: 
    '''
    @title CardCount 
    @desc Keeps a perfect count of cards that have been dealt from a shoe, and given the 
    number of cards in the shoe, can calculate probabilities of certain events happening 
    (i.e. regarding what cards will be dealt)
    '''
    def __init__(self, num_decks: int = 1): 
        self.cards_dealt = {}
        self.num_decks = num_decks
        
        for i in range(1, 11): 
            self.cards_dealt[i] = 0
            
    def probability_of_getting(self, card_value: int) -> float: 
        card_counts  = {}
        num_cards_dealt = 0
        for i in range (1, 11): 
            card_counts[i] = (4 * self.num_decks)
            num_cards_dealt += self.cards_dealt[i]
        card_counts[10] = (16 * self.num_decks)
            
        for i in range(1, 11): 
            card_counts[i] -= self.cards_dealt[i]
            
        probabilities = {}
        total_cards_remaining = (self.num_decks*52) - num_cards_dealt
        for i in range (1, 11): 
            probabilities[i] = card_counts[i] / total_cards_remaining
            
        return probabilities[card_value]
    
    def probability_of_n_or_over(self, card_value: int) -> float: 
        prob = 0.0
        for i in range(card_value, 11): 
            p = self.probability_of_getting(i)
            #print(f'prob of {i}: {p}')
            prob += p
        return prob
    
    #TODO: test this 
    #TODO: this is not taking into account the possibility of 11
    def probability_of_n_or_under(self, card_value: int) -> float: 
        return 1 - self.probability_of_n_or_over(card_value +1) 
    
    def append(self, card: Card): 
        self.cards_dealt[card.numeric_value] += 1
        
    def add_decks(self, count): 
        self.num_decks += count 
        
    #TODO: test this 
    #TODO: (HIGH) this is not taking into account the new decks added in 
    def add_counts(self, counts): 
        for i in range(1, 11): 
            self.cards_dealt[i] += counts.cards_dealt[i]