import json
import csv
def load_vocab_from_json(file_path):
    '''Load vocab data from a json file'''
    with open(file_path, 'r') as f:
        data = json.load(f)

    result = {}
    for word, definition in data.items():
        result[word] = VocabCard(word, definition) 
    return result 

def write_list_to_csv(words_list, output_file):
    '''Writes a list of words to a csv file with each word wrapped in double quotes'''
    with open(output_file, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for word in words_list:
            writer.writerow([word])

class VocabCard:
    '''Represents a single vocab card'''
    def __init__(self, word, defintion, repetitions=0, interval=1, ease_factor=2.5, review_counter=0, is_new=True):
        '''This method defines the arguments or properties expected when we create an instance of this class i.e a vocab card'''
        self.word = word
        self.definition = defintion
        self.repetitions = repetitions
        self.interval = interval
        self.ease_factor = ease_factor
        self.review_counter = review_counter 
        self.is_new = is_new
    
    def update_card(self):
        '''This method is responsible for handling an encounter with the word and updating when we should encounter it next and a few other things'''
        if self.repetitions == 0:
            self.interval = 2
        elif self.repetitions == 1:
            self.interval = 4
        else: 
            self.interval = round(self.interval * self.ease_factor)

    
        self.repetitions += 1
        self.is_new = False

        self.ease_factor = max(1.3, self.ease_factor + 0.1) 

        self.review_counter = self.interval

    def is_learned(self, max_repetitions=5):
        '''telling is if this word is learned completely (which is based off a max_repetitions parameter that we will define later)'''
        return self.repetitions >= max_repetitions



def show_word_status(vocab_cards):
    '''Displays the current status of the words, and also returns the due words (which is a list)'''
    due_words = []
    for card in vocab_cards.values():
       
        if card.review_counter <= 0 and not card.is_new:
            due_words.append(card)

    return due_words

def review_session(vocab_cards, max_repetitions=5):
    '''Reviews words until all are ordered / mastered'''
    history = []
    total_words_reviewed = 0

    while True:
        # Reduce the review counter for all words
        for card in vocab_cards.values():
            if card.review_counter > 0:
                card.review_counter -= 1

        # Get words due for review
        due_words = show_word_status(vocab_cards)

        # If no due words, introduce a new word as a filler
        if not due_words:
            filler_word = None
            for card in vocab_cards.values():
                if card.is_new:
                    filler_word = card
                    break
            if filler_word:
                filler_word.is_new = False # mark as no longer new
                print(f'Introducing a new word: {filler_word.word}')
                history.append(filler_word.word)
                total_words_reviewed += 1
                continue
            else: 
                all_learned = True
                for card in vocab_cards.values():
                    if not card.is_learned(max_repetitions):
                        all_learned = False
                        break
                if all_learned:
                    print('Congrats! All words are learned :)')
                    break

        # Review the due words
        for card in due_words:
            print(f'Reviewing: {card.word}')
            history.append(card.word) # track the word in history
            card.update_card()
            total_words_reviewed += 1

    # 1.5 save this long list of all our words to a csv file, that can later be read by our game
    # write out our history list to a csv file 
    output_file = 'words_history.csv'
    write_list_to_csv(history, output_file)
    print(len(history))


if __name__ == '__main__':
    vocab_cards = load_vocab_from_json('definitions.json')
    print('Starting vocab learning session...')
    review_session(vocab_cards)
