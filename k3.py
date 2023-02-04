#!/usr/bin/env python3 -u
#
# North Thirty Nine Degrees Ten Point and West Seventy Six Degrees Fifty One Point
# norththirtyninedegreestenpoint
# westseventysixdegreesfiftyonepoint
#
# TODO:
# - Find all workable solutions??
# - Decryption routine - run after successful completion to check result for correctness
# - Return success or failure (key or None)
# - Manage output somehow - verbosity toggle, periodic checkpoint output, ctrl-c to show current state, etc
#
# Data structures, programming languages, algorithm design and analysis, cryptography, automata theory
# Program to find exactly 26 code words and split cipher into a list
# Modified/extended version of part 2 algorithm would take thousands of years to complete
# Backtracking - devil in the details
# Tried recursion
# Getting iteration correct without infinite loops
# Python debugger

import hashlib
import logging
import random
import sys

from rotation_matrix import build_rotation_matrix
from split_cipher import read_cipher, split_cipher

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

# Backtracking reasons
(KEY_ROTATION_COLLISION, DUPLICATE_KEY_VALUE, BACKTRACK_TO_INDEX) = range(3)

#
# This is just ugly af, but seems to work...
#
def decryptit(cipher_list, key):
    def rotate(l, n):
        return l[-n:] + l[:-n]

    #
    # Build a list of keys indexed by alphabet letter
    # So we can do proper rotation
    #
    def build_key_list(key):
        key_list = [None] * 26
        for i in key.keys():
            key_list[ord(key[i]['root_char']) - ord('a')] = i
        return key_list

    def reassign_key_letters(key, key_list):
        for a in range(len(key_list)):
            foo = key_list[a]
            if foo != None:
                key[foo]['root_char'] = chr(a + ord('a'))

    k = key.copy()
    key_list = build_key_list(k)
    plaintext = ""
    for word in cipher_list:
        if word in k:
            rot = k[word]['rotation']
            plaintext += k[word]['root_char']
            if rot > 0:
                key_list = rotate(key_list, rot)
                reassign_key_letters(k, key_list)
        else:
            print("word", word, "not in key - finishing")
            break
    return plaintext

#non-zero multipliers: [(1.0, '143261'), (1.0, '871646')] => 19.0
#non-zero multipliers: [(1.0, '222146337'), (1.0, '80920926')] => 3.0
#non-zero multipliers: [(1.0, '418'), (1.0, '946294413')] => 0.0
#non-zero multipliers: [(1.0, '6103003'), (1.0, '80920926')] => 9.0
#'key': {'860': {'root_char': 'w', 'rotation': 0, 'first_occurrence': 0}}
def get_valid_rotation(key, word):
    if word == '143261':
        if '871646' in key:
            return (19 - key['871646']['rotation']) % 26
        return None
    elif word == '871646':
        if '143261' in key:
            return (19 - key['143261']['rotation']) % 26
        return None
    elif word == '222146337':
        if '80920926' in key:
            return (3 - key['80920926']['rotation']) % 26
        return None
    elif word == '80920926':
        # Note- this one occurs twice
        rotval = None
        if '222146337' in key:
            rotval = (3 - key['222146337']['rotation']) % 26
        if '6103003' in key:
            rotval2 = (9 - key['6103003']['rotation']) % 26
            if (rotval != None) and (rotval != rotval2):
                return -1
            rotval = rotval2
        return rotval
    elif word == '418':
        if '946294413' in key:
            return (0 - key['946294413']['rotation']) % 26
        return None
    elif word == '946294413':
        if '418' in key:
            return (0 - key['418']['rotation']) % 26
        return None
    elif word == '6103003':
        if '80920926' in key:
            return (9 - key['80920926']['rotation']) % 26
        return None
    else:
        # Should theoretically never get here
        return None

#
# Gets initial initial rotation for a codeword by looking at the rotation matrix
# Returns:
#    A rotation value if we could calculate one
#    None if we couldn't (indicating we should guess a rotation, starting at zero)
#    -1 if we calculated two or more conflicting values (indicating we need to backtrack)
#
def get_initial_rotation(key, word, known_rotations, oldrots):
    if word in oldrots:
        return oldrots[word]
    if word in ['143261','871646','222146337','80920926','418','946294413','6103003']:
        result = get_valid_rotation(key, word)
        if result == None:
            logging.debug(f"get_valid_rotation: not enough variables known to calculate word {word} (start with 0)")
            return None
        elif result == -1:
            logging.debug(f"get_valid_rotation: conflicting rotation values for word {word} (backtrack)")
            exit(0)   # TBD- need to backtrack
        else:
            logging.debug(f"get_valid_rotation: computed rotation value for word {word} == {result}")
            return result

    # Free/independent variable not in matrix (start at 0)
    return None

def doit(cipher, known_rotations):
    state = []
    key = {}
    guessed_keys = []           # list of guessed cipher words in order of first appearance
    current_rotation = 0            # alphabet offset at the current point in the cipher
    start_rotation = current_rotation # first offset we tried before moving on to others
    last_key_collision = [None] * len(cipher)

    i = 0
    backtrack_loop_count = 0
    backtrack_status = None

    # Put the rotations into a form that the current code understands
    oldrots = dict([(word,mat[0][1]) for (word,mat) in known_rotations.items() if len(mat[0][0]) == 1])

    #
    # Variables to save with state (anything not explicitly set/assigned at start of while loop):
    # current_rotation, start_rotation, key
    #
    while i < len(cipher):
        (cipher_word, plaintext_char) = cipher[i]
        key_char = chr((ord(plaintext_char) - ord('a') - current_rotation) % 26 + ord('a'))
        try_new_rotation_offset = False

        logging.debug("index %d word %s plaintext_char %c key_char %c current_rotation %d key %s" % (i, cipher_word, plaintext_char, key_char, current_rotation, key))

        #
        # State 1: cipher word is present in key
        #
        if cipher_word in key:
            k = key[cipher_word]
            ch = k['root_char']
            of = k['rotation']

            #
            # If we got here after backtracking, check what happened and figure out what to do
            #
            if backtrack_status:
                if backtrack_status['reason'] == BACKTRACK_TO_INDEX:
                    backtrack_index = backtrack_status['index']
                    if i == backtrack_index:
                        of += 1
                        try_new_rotation_offset = True
                    else:
                        pass  # Just keep going until we get to the target index

                elif backtrack_status['reason'] == KEY_ROTATION_COLLISION or backtrack_status['reason'] == DUPLICATE_KEY_VALUE:
                    if len(guessed_keys) < 1:
                        # This can happen if the only remaining keys were pre-calculated
                        logging.debug("No more guessed keys remain")
                        break
                    most_recent_guessed_word = guessed_keys[-1]
                    backtrack_index = key[most_recent_guessed_word]['first_occurrence']
                    if i == backtrack_index:
                        # We are already at the first occurrence of the most recent guessed word
                        if 'expected_value' in backtrack_status:
                            of = backtrack_status['expected_value']
                            logging.debug("Set rotation for %s to calculated value %d" % (cipher_word, of))

                            #
                            # Need to remove the current key from list of guessed keys for this and future frames
                            # so we don't later try to increment a calculated rotation offset.. however, not sure
                            # if the last element on the list will always be the current word... hence the assert()
                            #
                            assert(guessed_keys.pop() == cipher_word)
                        else:
                            # No expected_value - likely a DUPLICATE_KEY_VALUE - just try incrementing the rotation
                            of += 1
                        try_new_rotation_offset = True
                    else:
                        logging.debug("Backtrack to index %d (first occurrence of word %s); current index %d" % (backtrack_index, most_recent_guessed_word, i))
                        backtrack_status = { 'reason': BACKTRACK_TO_INDEX, 'index': backtrack_index }
                else:
                    logging.error("Unhandled backtrack status %d" % backtrack_status)
                    break

            #
            # Not backtracking: check for key collision (key[n] already set to something other than
            # what we are trying to assign)
            #
            elif ch != key_char:
                ev = (ord(key_char) - ord(ch)) % 26

                #
                # expected_value is what the rotation would need to be set to to make the current
                # code word map to the current plaintext character. However, it is kinda meaningless
                # except for (I think) the first occurrence of the cipher word..
                #
                backtrack_status = {'reason': KEY_ROTATION_COLLISION, 'expected_value': ev}
                logging.debug("key collision for '%s' at index %d: %s != %s; rotation difference = %d" % (cipher_word, i, key_char, ch, ev))
                l = last_key_collision[i]
                if l and l['root_char'] == ch and l['key_char'] == key_char:
                    l['count'] += 1
                    logging.debug("**duplicate collision at index %d (count=%d)**" % (i, l['count']))
                else:
                    # Either no prior collision at this index, or a new one
                    l = { 'root_char': ch, 'key_char': key_char, 'count': 1 }
                    last_key_collision[i] = l
                backtrack_status['collision_count'] = l['count']

            if try_new_rotation_offset:
                if of == 26:
                    # We've run through all possible rotation values, so need to backtrack again
                    logging.debug("Exhausted all possible rotation values for %s at index %d" % (cipher_word, i))
                    logging.debug("Current guessed_keys: %s" % guessed_keys)
                    if len(guessed_keys) < 2:
                        print("No more keys to guess")
                        break
                    # Go back and start iterating over the second-most-recently added key
                    next_word = guessed_keys[-2]
                    next_index = key[next_word]['first_occurrence']
                    logging.debug("backtrack to index %d word %s (current index %d)" % (next_index, next_word, i))
                    backtrack_status = { 'reason': BACKTRACK_TO_INDEX, 'index': next_index }
                else:
                    logging.debug("Try new rotation value %d for word %s" % (of, cipher_word))
                    k['rotation'] = of
                    backtrack_status = None

            if backtrack_status == None:
                current_rotation = (current_rotation + of) % 26

        #
        # State 2: duplicate key_val (key[a] and key[b] both map to the same letter)
        #          Pretty sure this just means we need to backtrack, but we'll see
        #
        elif key_char in [a['root_char'] for a in key.values()]:
            logging.debug("duplicate key_val %c at index %d (orig %c offset %d)" % (key_char, i, plaintext_char, current_rotation))
            backtrack_status = { 'reason': DUPLICATE_KEY_VALUE }

        else:

            #
            # Calculate an initial rotation value (if possible) and add the word to the key
            #
            rot_val = get_initial_rotation(key, cipher_word, known_rotations, oldrots)
            if rot_val == None:
                rot_val = 0
                guessed_keys.append(cipher_word)
            elif rot_val > 0:
                current_rotation = (current_rotation + rot_val) % 26

            key[cipher_word] = { 'root_char': key_char, 'rotation': rot_val, 'first_occurrence': i }
            logging.debug("Add key %s with char %s, rotation %d" % (cipher_word, key_char, rot_val))

        #
        # Backtrack if needed; otherwise, save state and keep going
        #
        if backtrack_status == None:
            state_vars = {
                'start_rotation': start_rotation,
                'key': key.copy(),
                'guessed_keys': guessed_keys.copy()
            }
            logging.debug("state_vars: %s" % state_vars)
            state.append(state_vars)
            start_rotation = current_rotation
            i += 1

        else:
            logging.debug("Backtracking- status: %s" % backtrack_status)
            i -= 1
            if i < 0:
                print("Could not find a fit... giving up")
                break

            # restore the previous state
            d = state.pop()
            start_rotation = d['start_rotation']
            guessed_keys = d['guessed_keys']
            current_rotation = start_rotation
            key = d['key']

            backtrack_loop_count += 1
            #if backtrack_loop_count >= 10000:
            #    print("Breaking loop")
            #    break

    print("Final value of i=%d" % i)
    print("Key:", key)
    #print("Final state:", state)
    print("Backtrack Loop Count:", backtrack_loop_count)
    if i > 0:
        return key
    else:
        return None


def fit_plaintext(cipher_list, text, offset):
    known_rotations = build_rotation_matrix(cipher_list, text, offset)
#    return None

    cipher = list(zip(cipher_list[offset:], text))
    key = doit(cipher, known_rotations)
    if key != None:
        p = decryptit(cipher_list[offset:], key)

        #
        # Check to make sure the decrypted plaintext matches the input plaintext.
        # If it's a complete mismatch, that could indicate a bug. Most likely scenario
        # here is that doit() exited before it could fit all of the plaintext, resulting
        # in a partial (but otherwise correct) decryption, which is also treated as
        # a failure.
        #
        # In the case of a matching but incorrect key (e.g. fits the input text but not
        # the entire plaintext) it's not uncommon to have some garbage characters at the
        # end of the decrypted result. So, need to truncate decryptit() output to the
        # same length as the input text. This is still considered a successful result,
        # although the key is not correct - it just means we need to try to fit a longer
        # string.
        #
        if len(p) < len(text):
            logging.debug("Partial decryption result: %s" % p)
            return None
        if p[:len(text)] != text:
            logging.debug("Decryption mismatch: %s != %s" % (p, text))
            return None
        return p
    return None

(cipher_words, cipher_list) = read_cipher("k3.txt", False)

print("cipher_list:", cipher_list)
print("Cipher length =", len(cipher_list))

#text = 'congratulationsyouareacryptogr'
#text = 'congratulationsyouareacryptographere'
#text = 'congratulationsyouareacryptographerextraordinaire'
#text = 'norththirtyninedegreestenpoint'
text = 'westseventysixdegreesfiftyonepoint'
#text = 'cryptographerextraordinaire'
#text = 'confusingididntwantanynum'
#text = 'degreestenpoint'

print(fit_plaintext(cipher_list, text, 414))

#for i in range(len(cipher_list) - len(text)):
#    print(f"Fitting {text} at position {i}")
#    print(fit_plaintext(cipher_list, text, i))

#matched_positions = []
#eliminated_positions = [0, 245, 246, 327, 328, 329, 523, 524, 20, 37, 73, 100, 130, 161, 225, 244, 251, 253, 255, 292, 311, 332, 348, 401, 410, 436, 457, 475, 513, 515, 521, 522, 3, 15, 57, 83, 115, 153, 211, 219, 233, 243, 254, 291, 310, 325, 336, 345, 374, 383, 386, 389, 398, 416, 448, 459, 462, 464]
#for i in range(len(cipher_list) - len(text)):
#    if i in eliminated_positions:
#        continue
#    r = fit_plaintext(text, i)
#    if r == None:
#        print("No fit at position %d" % i)
#        eliminated_positions.append(i)
#    else:
#        print("Got fit at position %d: %s" % (i, r))
#        matched_positions.append(i)
#print("Matched positions: ", matched_positions)
#print("Eliminated positions: ", eliminated_positions)

