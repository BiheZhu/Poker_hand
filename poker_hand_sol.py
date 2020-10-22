import sys
from collections import namedtuple

class Card(namedtuple('Card', 'face, suit')):
    def __repr__(self):
        return ''.join(self)

suit = ['H', 'D', 'S', 'C']
faces = '2 3 4 5 6 7 8 9 T J Q K A'
face = faces.split()

#############################
# identify rank of the hand #
#############################

# 1 highest value card
def high_card(hand):
    all_faces = [f for f,s in hand]
    return 'high_card', sorted(all_faces, key=lambda f: face.index(f), reverse=True)

# 2 Two cards of same value
def one_pair(hand):
    all_faces = [f for f,s in hand]
    face_types = set(all_faces)
    pairs = [f for f in face_types if all_faces.count(f) == 2]
    if len(pairs) != 1:
        return False
    face_types.remove(pairs[0])
    return 'one_pair', pairs + sorted(face_types, key=lambda f: face.index(f), reverse=True)

# 3 Two different pairs
def two_pairs(hand):
    all_faces = [f for f,s in hand]
    face_types = set(all_faces)
    pairs = [f for f in face_types if all_faces.count(f) == 2]
    if len(pairs) != 2:
        return False
    p0, p1 = pairs
    other = [(face_types - set(pairs)).pop()]
    return 'two_pairs', pairs + other if face.index(p0) > face.index(p1) else pairs[::-1] + other
 
# 4 Three of a kind: Three cards of the same value
def three_of_a_kind(hand):
    all_faces = [f for f,s in hand]
    face_types = set(all_faces)
    if len(face_types) <= 2:
        return False
    for f in face_types:
        if all_faces.count(f) == 3:
            face_types.remove(f)
            return ('three_of_a_kind', [f] + sorted(face_types, key=lambda f: face.index(f), reverse=True))
    else:
        return False

# 5 Straight: All five cards in consecutive value order
def straight(hand):
    ordered = sorted(hand, key=lambda card: face.index(card.face))
    if ' '.join(card.face for card in ordered) in faces:
        return 'straight', [ordered[-1].face]
    return False

# 6 Flush: All five cards having the same suit
def flush(hand):
    all_suit_types = {s for f, s in hand}
    if len(all_suit_types) == 1:
        all_faces = [f for f,s in hand]
        face_types = set(all_faces)
        return 'flush', sorted(face_types, key=lambda f: face.index(f), reverse=True)
    return False

# 7 Full house: Three of a kind and a Pair
def full_house(hand):
    all_faces = [f for f,s in hand]
    face_types = set(all_faces)
    if len(face_types) != 2:
        return False
    for f in face_types:
        if all_faces.count(f) == 3:
            face_types.remove(f)
            return 'full_house', [f, face_types.pop()]
    else:
        return False

# 8 Four of a kind: Four cards of the same value
def four_of_a_kind(hand):
    all_faces = [f for f,s in hand]
    face_types = set(all_faces)
    if len(face_types) != 2:
        return False
    for f in face_types:
        if all_faces.count(f) == 4:
            face_types.remove(f)
            return 'four_of_a_kind', [f, face_types.pop()]
    else:
        return False

# 9 Straight flush: All five cards in consecutive value order, with the same suit
def straight_flush(hand):
    all_suit_types = {s for f, s in hand}
    if len(all_suit_types) == 1:
        ordered = sorted(hand, key=lambda card: (face.index(card.face), card.suit))
        if ' '.join(card.face for card in ordered) in faces:
            return 'straight_flush', [ordered[-1].face]
    return False

# 10 Royal Flush: Ten, Jack, Queen, King and Ace in the same suit
def royal_flush(hand):
    all_suit_types = {s for f, s in hand}
    if len(all_suit_types) == 1:
        all_faces = {f for f,s in hand}
        if all_faces == { 'T', 'J', 'Q', 'K', 'A'}:
            ordered = sorted(hand, key=lambda card: (face.index(card.face)))
            return 'royal_flush', ordered
    return False
 
#############################
#  #
#############################

hand_rank_function_ordered =  [royal_flush, straight_flush, four_of_a_kind, full_house, flush, 
                    straight, three_of_a_kind, two_pairs, one_pair, high_card]

rank_order = {'royal_flush': 10, 'straight_flush': 9, 'four_of_a_kind': 8, 
                'full_house': 7, 'flush': 6, 'straight': 5, 'three_of_a_kind': 4, 
                'two_pairs': 3, 'one_pair': 2, 'high_card': 1}
 
def rank(cards):
    hand = []
    for card in cards.split():
        f, s = card[0], card[1]
        hand.append(Card(f, s))
    for rank_function in hand_rank_function_ordered:
        rank = rank_function(hand)
        if rank:
            break
    return rank

if __name__ == '__main__':
    No_of_player_1_won = 0
    No_of_player_2_won = 0

    for line in sys.stdin:
        try:
            hand_1 = line[0:len(line)//2].rstrip(' ')
            hand_2 = line[len(line)//2 if len(line)%2 ==0 else ((len(line)//2)+1):].strip('\n')
            
            rank_1 = rank(hand_1)
            rank_2 = rank(hand_2)
            
            if rank_order[rank_1[0]] > rank_order[rank_2[0]]:
                # print('Player 1 won!')
                No_of_player_1_won += 1
            elif rank_order[rank_1[0]] < rank_order[rank_2[0]]:
                # print('Player 2 won!')
                No_of_player_2_won += 1
            else:
                if rank_1[0] == 'royal_flush':
                    pass
                    # print('tie!')
                else:
                    # print('tie, check the next highest card!')
                    tie = True
                    for i in range(len(rank_1[1])):
                        a = face.index(rank_1[1][i])
                        b = face.index(rank_2[1][i])
                        if a > b:
                            # print('Player 1 won!')
                            No_of_player_1_won += 1
                            tie = False
                            break
                        elif a < b:
                            # print('Player 2 won!')
                            No_of_player_2_won += 1
                            tie = False
                            break
                    if tie:
                        pass
                        # print('tie!')
            # print()
        except Exception:
            # print("EOF")
            break
    print('Player 1: ', No_of_player_1_won)
    print('Player 2: ', No_of_player_2_won)
    

    


    