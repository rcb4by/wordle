import re
import random

def get_guess(guess, target):
    res = list('W' * len(target))
    seen = {}
    for i, (g, t) in enumerate(zip(guess, target)):
        if g not in seen:
            seen[g] = 0
        if g == t:
            res[i] = 'R'
            seen[g] += 1

    for i, (g, t) in enumerate(zip(guess, target)):
        if seen[g] < target.count(g) and res[i] == 'W':
            res[i] = 'L'
        if res[i] != 'R':
            seen[g] += 1

    return res

def validate_word(word, good, bad, correct):
    freq = {}

    for k, v in correct.items():
        if word[k] != v:
            return False
        elif v not in freq:
            freq[v] = -1
        else:
            freq[v] -= 1

    for c in word:
        if c not in freq:
            freq[c] = 1
        else:
            freq[c] += 1

    for g, idx in good.items():
        if freq.get(g, 0) <= 0:
            return False
        else:
            for i in idx:
                if word[i] == g:
                    return False
        freq[g] -= 1

    for b in bad:
        if freq.get(b, 0) > 0:
            return False

    return True
    
def match_guesses(words, pattern, target):
    res = []

    for word in words:
        if get_guess(word, target) == pattern:
            res.append(word)

    return res


def generate_matrix(words, guess, target, good={}, bad=set(), correct={}):
    pattern = get_guess(guess, target)
    print(f'Trying new guess "{guess}" with pattern {str(pattern)}')

    if pattern == ['R', 'R', 'R', 'R', 'R']:
        return [pattern], [target]

    for i, (g, p) in enumerate(zip(guess, pattern)):
        if p == 'R':
            correct[i] = g
            if g in good:
                del good[g]
        elif p == 'L':
            if g in good:
                good[g].append(i)
            else:
                good[g] = [i]
        else:
            bad.add(g)
    
    new_words = [word for word in words if validate_word(word, good, bad, correct)]

    print(f'good letters: {good}')
    print(f'bad letters: {bad}')
    print(f'correct letters: {correct}')
    print(f'{len(new_words)} possible words remaining;')
    print(new_words)
    if target not in new_words:
        print('TARGET IS GONEEE!!!!!')
        return [pattern], [guess]
    if not new_words:
        print('No Choices left!!!')
        return [pattern], [guess]

    new_guess = random.choice(new_words)
    mat, rix = generate_matrix(new_words, new_guess, target, good, bad, correct)

    return [pattern] + mat, [guess] + rix


def find_matrices(words, guess, target, matrix, good, bad, correct):
    if not matrix:
        print('MADE IT TO THE BOTTOM!!')
        return [[]]

    pattern = get_guess(guess, target)
    if pattern != matrix[0]:
        return False

    for i, (g, p) in enumerate(zip(guess, pattern)):
        if p == 'R':
            correct[i] = g
            if g in good:
                del good[g]
        elif p == 'L':
            if g in good:
                good[g].append(i)
            else:
                good[g] = [i]
        else:
            bad.add(g)
    
    new_words = [word for word in words if validate_word(word, good, bad, correct)]

    if target not in new_words:
        return False
    if not new_words:
        return False

    results = []
    for word in new_words:
        new_guess = word
        answer = find_matrices(new_words, new_guess, target, matrix[1:], dict(good), set(bad), dict(correct))
        if answer:
            for a in answer:
                results.append([guess] + a)
    return results



def get5(filename):
    with open(filename, 'r') as f:
        thing = f.read()

    thing = thing.splitlines()

    for word in thing:
        if len(word) == 5:
            print(word)

def check_matrices(target, matrix):
    matrix = [list(pattern) for pattern in matrix]
    print(f'Parsed matrix {matrix}')

    with open('5letters.txt', 'r') as f:
        words = f.read().split('\n')[:-1]

    answers = []
    for word in words:
        answer = find_matrices(words, word, target, matrix, {}, set(), {})
        if answer:
            answers += answer

    print(f'{len(answers)} answers found:')
    for mat in answers:
        print('\n'.join([str(word) for word in mat]))
        print()


def play_game(target, guess):

    with open('5letters.txt', 'r') as f:
        words = f.read().split('\n')[:-1]

    mat, rix = generate_matrix(words, guess, target)

    print('Result:')
    print('\n'.join([str(word) for word in rix]))

    print('Words:')
    print('\n'.join([str(word) for word in mat]))
    return mat

target = input('Target: ')
guess = input('Guess: ')

matrix = play_game(target, guess)
check_matrices(target, matrix)
# get5('20k.txt')
