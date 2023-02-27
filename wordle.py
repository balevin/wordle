import time
import math
import pickle
import random
class Board():
    def __init__(self, answer) -> None:
        self.tiles = [['_', '_', '_', '_', '_'],['_', '_', '_', '_', '_'],['_', '_', '_', '_', '_'],['_', '_', '_', '_', '_'],['_', '_', '_', '_', '_'],['_', '_', '_', '_', '_']]
        self.tile_colors = ['w','w','w','w','w'],['w','w','w','w','w'],['w','w','w','w','w'],['w','w','w','w','w'],['w','w','w','w','w'],['w','w','w','w','w']
        self.guesses_used = 0
        self.the_answer = answer

    def try_word(self, word):
        assert len(word)==5
        if self.check_won(word):
            return 'won'
        if self.guesses_used==6:
            return 'lost'
        return 'playing'

    def update(self, word):
        pattern = self.update_colors(word)
        self.update_board(word)
        self.guesses_used+=1
        return pattern

    def check_won(self, word):
        if word==self.the_answer:
            self.tile_printer()
            self.color_printer()
            print('you win')
            print('---------------------------------------------------------------------------------')
            print('It took ' + str(self.guesses_used) + " guesses")
            print('---------------------------------------------------------------------------------')
            return True
        return False
    
    def get_tiles(self):
        return self.tiles

    def tile_printer(self):
        str_builder = ''
        for row in self.tiles:
            for letter in row:
                str_builder+=letter + '  '
            str_builder += '\n'
        print(str_builder)
        
    def color_printer(self):
        str_builder = ''
        for row in self.tile_colors:
            for letter in row:
                str_builder+=letter + '  '
            str_builder += '\n'
        print(str_builder)
    
    def update_board(self, word):
        self.tiles[self.guesses_used] = word


    def update_colors(self, word):
        for i in range(len(word)):
            if word[i]==self.the_answer[i]:
                self.tile_colors[self.guesses_used][i] = 'green'
            elif word[i] in self.the_answer:
                self.tile_colors[self.guesses_used][i] = 'yellow'
            else:
                self.tile_colors[self.guesses_used][i] = 'grey'
        return self.tile_colors[self.guesses_used]
            

class Game():
    def __init__(self) -> None:
        self.board = Board() 
        self.guesser = Guesser()
        self.answer = None
        self.game_state = 'start'


    def __init__(self, answer):
        self.board = Board(answer)
        self.game_state = 'start' 
        self.answer = answer
        self.guesser_map = {}
        self.guesser = Guesser()
        self.play_game()

    def get_board(self):
        return self.board

    def get_answer(self):
        return self.answer

    def __print__(self):
        return self.board
    
    def play_game(self):
        while self.game_state in ('playing', 'start'):
            print(self.game_state)
            self.board.tile_printer()
            self.board.color_printer()
            if self.game_state == 'start':
                guess = 'saner'
            else:
                guess = self.guesser.create_guess(self.board.guesses_used)
                if len(guess)==6:
                    self.guesser_map[guess[:-1]] = self.answer
                    pickle.dump(self.guesser_map, open('guesser_map.pickle', 'wb'))
                    guess = guess[:-1]
            self.game_state = 'playing'
            self.guesser.remove_word(guess)
            print(guess)
            pattern = self.board.update(guess)
            self.game_state = self.board.try_word(guess)
            self.guesser.exclude_answers(guess, pattern)
            self.guesser.exclude_words(guess, pattern)
    
class Guesser():
    def __init__(self):
        self.allowed_words = []
        self.percent_guess_map = {}
        for line in open('allowed_words.txt'):
            if len(line)==6:
                self.allowed_words.append(line[:-1])
        for line in open('freq_map.json'):
            dict_str = line
        split = dict_str.split(':')
        self.word_probabilities = {}
        for i in range(len(split)):
            if i==0:
                key = split[i][2:-1]
            else:
                try:
                    value, next_key = split[i].split(',')
                    next_key = next_key[2:-1]
                    self.word_probabilities[key] = float(value)
                    key = next_key
                except:
                    value = split[i][:-1]
                    self.word_probabilities[key] = float(value)
        self.possible_words = []
        for line in open('possible_words.txt'):
            if len(line)==6:
                self.possible_words.append(line[:-1])
        
        print('starting length possible: ', len(self.possible_words))
        print('starting length allowable: ', len(self.allowed_words))
        # POSSIBLE IS THE ANSWERS
        try:
            t1 = time.time()
            self.patterns = pickle.load(open('patterns.pickle', 'rb'))
            print('time: ', time.time()-t1)
        except:
            t1 = time.time()
            self.patterns = [] 
            self.colors =['green', 'yellow', 'grey']
            for c1 in self.colors:
                for c2 in self.colors:
                    for c3 in self.colors:
                        for c4 in self.colors:
                            for c5 in self.colors:
                                self.patterns.append([c1,c2,c3, c4,c5])
            print('time1: ', time.time()-t1)
            input()
            pickle.dump(self.patterns, open('patterns.pickle', 'wb'))
                    
                    


    def remove_word(self, word):
        self.allowed_words.remove(word)

    def remove_answer(self, answer):
        self.possible_words.remove(answer)

    def create_guess(self, guesses_used = None):

        max_word = ''
        max_ent = 0
        print('new length: ', len(self.allowed_words))
        if len(self.possible_words) == 1:
            return self.possible_words[0]
        if guesses_used==5:
            max_prob = 0
            max_word = ''
            for word in self.possible_words:
                prob = self.word_probabilities[word]
                if prob>max_prob:
                    max_prob = prob
                    max_word = word
            return max_word
        # test
        # prob_sum = 0
        # max_prob = 0
        # max_word = ''
        # for word in self.possible_words:
        #     prob = self.word_probabilities[word]
        #     prob_sum+=prob
        #     if prob>max_prob:
        #         max_prob = prob
        #         max_word = word
        # if (self.word_probabilities[max_word]/prob_sum)>0.5:
        #     print('making 50 percent guess')
        #     # print(self.possible_words)
        #     # print(max_word)
        #     # print(self.word_probabilities[max_word])
        #     # print([self.word_probabilities[x] for x in self.possible_words])
        #     self.percent_guess_map[max_word] = [self.possible_words, [self.word_probabilities[x] for x in self.possible_words]]
        #     pickle.dump(self.percent_guess_map, open('percent_guess_map.pickle', 'wb'))
        #     return max_word+'_'
            
        for word in self.allowed_words:
            ent = self.calculate_entropy(word)
            if ent>max_ent:
                max_word = word
                max_ent = ent
        print(max_ent)
        return max_word


    def exclude_answers(self, guess, pattern):
        to_remove = []
        print('num answers: ', len(self.possible_words))
        for word in self.possible_words:
            if not self.possible_match(guess, pattern, word):
                to_remove.append(word)
            
        for word in to_remove:
            self.remove_answer(word)
        print('num answers: ', len(self.possible_words))
        if len(self.possible_words)==2:
            print(self.possible_words)
            print([self.word_probabilities[x] for x in self.possible_words])
       
    
    def exclude_words(self, guess, pattern):
        to_remove = []
        for word in self.allowed_words:
            if not self.possible_match(guess, pattern, word):
                to_remove.append(word)
        for word in to_remove:
            self.remove_word(word)

    def possible_match(self, guess, pattern, word):
        verbose = False
        if word == 'aalii':
            verbose = True
        for i in range(5):
            if pattern[i]=='green':
                if guess[i]!=word[i]:
                    return False
            elif pattern[i] == 'yellow':
                if guess[i] not in word or guess[i]==word[i]:
                    return False
            else:
                if guess[i] in word:
                    return False
        return True
    def calculate_entropy(self, word):

        # Take a word:
        # 	go through each possible pattern it could give you
        # 		probability of this pattern*-log(pattern)

        # These probabilities are found empirically from the data:
        # 	probability of a pattern!


        # you have to remove all the letters from the possible
        # figure out what their result was after the guess
        # can get that from the Board object
        pattern_map = {}
        for pattern in self.patterns:
            countah = 0
            for answer in self.possible_words:
                result = self.pattern_match(pattern, word, answer)
                countah += result
            pattern_map[tuple(pattern)] = countah/len(self.allowed_words)
        ent = 0
        for patt in pattern_map:
            if pattern_map[patt]>0:
                ent += pattern_map[patt]*-math.log2(pattern_map[patt])

        # return ent*self.word_probabilities[word]
        return ent

            
    def pattern_match(self, pattern, guess, answer):
        real_pattern = []
        for i in range(len(guess)):
            if guess[i]==answer[i]:
                real_pattern.append('green')
            elif guess[i] in answer:
                real_pattern.append('yellow')

            else:
                real_pattern.append('grey')
        return real_pattern==pattern




class ManualGuesser(Guesser):
    def __init__():
        super.__init__()
    
    def create_guess(self):
        guess = input('What word do you want to guess?: ')
        return guess


possible_words = []

for line in open('possible_words.txt'):
    if len(line)==6:
        possible_words.append(line[:-1])
# ans_dict = {}
# print(len(possible_words))
# # # TEST ALL POSSIBLE ANSWERS
# count = 0
# for ans in possible_words:
#     if count%(len(possible_words)//10)==0:
#         print('-----------------------------------------------------------------')
#         print(str(count/len(possible_words))+ ' percent done')
#         print('-----------------------------------------------------------------')
#         pickle.dump(ans_dict, open('results_big3.pickle', 'wb'))
#     # ans = possible_words[random.randint(0,len(possible_words)-1)]
#     print(ans)
#     game = Game(ans)
#     if game.game_state == 'lost':
#         print('---------------------------------------------------------------')
#         print('you lost')
#         print('---------------------------------------------------------------')
#         ans_dict[ans] = 0
#     else:
#         ans_dict[ans] = game.board.guesses_used
#     count += 1

# lost_count = 0
# for ans in ['foyer', 'homer', 'patch', 'punch', 'rover', 'rower', 'tower', 'vaunt', 'waste', 'watch', 'water', 'wound']:
#     print(ans)
#     game = Game(ans)
#     if game.game_state == 'lost':
#         lost_count += 1
#         print('---------------------------------------------------------------')
#         print('you lost')
#         print('---------------------------------------------------------------')
#         input()
# print('we lost: ' + str(lost_count))

# PLAY RANDOM GAME
# answer = possible_words[random.randint(0,len(possible_words))]
answer = 'usage'
print(answer)
game = Game(answer)
print('guesses: ', game.board.guesses_used)
# saner
# look at patch, wtf is going on