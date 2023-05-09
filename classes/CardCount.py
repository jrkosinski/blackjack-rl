from classes.Card import Card

class CardCount: 
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
            num_cards_dealt += cards_dealt[i]
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
            p = probability_of_getting(self.cards_dealt, i)
            print(f'prob of {i}: {p}')
            prob += p
        return prob
        
    def probability_of_ace(self): 
        return probability_of_getting(self.cards_dealt, 1)
        
    def append(self, card: Card): 
        self.cards_dealt[card.number_value] += 1
        
    def add_counts(self, counts): 
        for i in range(1, 11): 
            self.cards_dealt[i] += counts.cards_dealt[i]