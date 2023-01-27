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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

# Backtracking reasons
(KEY_ROTATION_COLLISION, DUPLICATE_KEY_VALUE, BACKTRACK_TO_INDEX) = range(3)

# K1
#cipher_words = ['89411894', '4254', '7171031', '4502', '971559793', '53177', '636187', '20', '4504', '376', '361', '57643', '85053600', '29', '7004062', '4468', '923921735', '946320122', '930424404', '88527391', '692473', '84524991', '87445918', '638440', '23', '52381']
#cipher_text = "8505360071710319463201224502636187376700406263844057643636187717103197155979336129523819304244044504450237692392173589411894450245029304244048505360071710317171031700406270040624468450244687004062923921735531774468845249912097155979345043769304244044468850536006361878744591845028852739171710314468850536004502361450445048941189423450488527391923921735294468894118948852739144686384404502692473845249917171031425444686384409715597934502425470040625764363844020874459185764336145028852739163618792392173557643299715597936924733762336171710318505360020850536007171031930424404238505360063844063618787445918450288527391717103144688505360045023619715597938505360084524991523815764353177376894118944502425463844037670040626924736924732369247394632012294632012245044502523816384404468930424404576436361876384409715597937171031425457643376971559793700406288527391946320122"
# K2
cipher_words = ['55709', '605858', '4045', '341', '945432286', '641971', '7699855', '7954481', '7080686', '7906967', '391', '7614435', '7811539', '7073281', '4530', '338', '59207', '920376451', '21', '20', '52123', '652655', '50461', '308', '89447709', '7756659']
cipher_text = "65265521707328176144355570955709795448179544815570989447709404555709652655504616419715570959207894477097811539769985552123308894477093087699855652655391404578115399454322867756659605858790696760585852123781153992037645177566596526552033879544816419717080686790696721769985533876144352179069676419714045775665934150461215920721453078115395920740457699855504613917073281769985570806867756659920376451341338391920376451920376451775665979544815570952123338781153976998557614435781153950461605858453045306419718944770930821708068639164197120769985578115397756659920376451920376451391769985540456419718944770939192037645120708068634192037645194543228620391557093086058583085920721404550461652655945432286795448179069677906967341652655641971592072065265564197194543228665265534176144357614435761443570732813083915570955709212045305920789447709391557094530920376451708068639189447709708068689447709769985545302059207338308795448165265533845306058586419717073281894477097811539945432286453060585845302021894477096419718944770952123775665934165265534120453055709795448120761443576998557906967453021308592077073281338775665934121707328145305920760585878115394530652655338945432286592077614435707328130870732816058585570960585892037645140457614435945432286945432286557095570921761443530865265545307756659945432286391214045404533833876144355046121557093389454322862089447709761443552123557097080686308215046192037645121769985579544814530214530521235046177566597073281945432286920376451920376451391769985540455920792037645189447709795448133892037645179544817073281605858641971641971708068650461781153989447709203384045790696740453412055709894477094530557097614435391214530920376451945432286391504615920734134164197155709404540452059207652655521233082079544817756659605858308781153952123775665960585876144353917954481"
# K3
#cipher_words = ['243255912', '222146337', '946294413', '37638005', '80920926', '63388773', '6103003', '5954191', '2167948', '0273351', '8621836', '871646', '317077', '156978', '444396', '143261', '96972', '79833', '14246', '09525', '0648', '860', '781', '418', '30', '93']
#cipher_text = "86096972781418871646243255912860798333763800541880920926222146337946294413243255912610300306489462944138092092630317077243255912064863388773156978969721569783044439661030039314326179833142468092092644439631707731707759541912167948376380053763800514246376380054443962221463377983324325591202733511569788621836860142466103003860095258716468621836610300322214633741893781610300361030030648933015697815697887164686061030037812221463374184443966103003798336103003095256338877378194629441331707793418860809209260952531707724325591278114246243255912871646418633887739697231707761030035954191064894629441314246860142469309525376380050273351595419122214633724325591215697814326186024325591202733519697279833871646860095255954191064830027335144439615697815697886218360273351871646969723170779697294629441314246610300331707722214633763388773798333063388773871646862183693781376380052167948317077095256103003860142462432559123030610300314326102733518716462432559124443968092092644439694629441363388773095252221463372432559127983341896972243255912809209260648142461569789341894629441396972156978064879833633887734443964180648317077946294413222146337633887739697214246932432559120273351798337983341806488621836303763800506487983387164693932167948143261969728621836860939359541913763800580920926095257816338877359541919363388773781376380057818092092659541918621836871646095253170779386218368621836142461424686094629441306487983302733519697287164602733519697214246064821679481432611424614326159541911432613170771432610952596972243255912216794880920926027335131707722214633715697896972418946294413809209260952586044439696972222146337095254182432559122221463374443969697280920926860027335159541911432611432616103003142469462944138092092661030033763800561030032167948798334443968716461432611432616338877309525305954191064886014246798338092092641894629441396972798338092092614246862183615697886024325591294629441302733512432559124443968092092680920926222146337143261222146337143261156978222146337317077064831707759541916103003376380058716460648222146337444396860418798339314326106488608716468601424641863388773610300359541916338877386218361569788606338877378137638005216794878180920926027335193610300337638005306338877341886086218360273351444396633887738600273351939359541917812221463378716469321679486338877378186218360273351934188621836860633887739697279833809209266338877386094629441386087164609525156978142461424630862183686086218362432559129697293376380053015697824325591280920926222146337156978969721432618716461569783170774189462944138092092661030039321679484443963763800521679489697221679480952515697830317077317077143261871646317077243255912142468092092678187164614246222146337809209261432612432559122432559128716462432559128600273351243255912064879833798338600273351317077143261095251424663388773860309341893595419180920926860095252167948809209261424679833871646142468606338877302733518092092693633887733031707787164622214633737638005860860216794879833610300306488716464443968621836064837638005095258092092686078124325591278122214633778141859541917812167948027335121679482167948027335115697814326194629441380920926418222146337862183641841821679484443960952579833143261143261798339462944135954191809209268607983363388773216794837638005969722167948304187813170772167948969723170777983396972946294413222146337064886218364183170778716468092092615697815697830243255912222146337222146337444396"
cipher_list = []

assert(len(cipher_words) == 26)

#
# Break the cipher out into a list of words
#
i = 0
while i < len(cipher_text) - 1:
    for j in range(min(len(cipher_text), i+9), i+1, -1):
        word = cipher_text[i:j]
        if word in cipher_words:
            cipher_list.append(word)
            break
    i = j

print("cipher_list:", cipher_list)
print("Cipher length =", len(cipher_list))

#
# Make sure we have a match
#
assert(cipher_text == ''.join(cipher_list))

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

#
# Figure out what offsets we can, based on the plaintext we're trying to fit
#
#def find_known_rotation_offsets(cipher):
#    offsets = {}
#
#    #
#    # TBD: compute offsets for words that lie between two words with known offsets
#    # E.g. if we know offset for 5555, and sequence is 5555 4444 5555, we should
#    # be able to compute 4444
#    #
#    for i in range(len(cipher) - 1):
#        if cipher[i][0] == cipher[i + 1][0]:
#            rot = (ord(cipher[i+1][1]) - ord(cipher[i][1])) % 26
#            offsets[cipher[i][0]] = rot
#
#    print("Calculated the following rotation offsets:", offsets)
#    return offsets

def doit(cipher, known_rotation_offsets):
    state = []
    key = {}
    guessed_keys = []           # list of guessed cipher words in order of first appearance
    current_rotation = 0            # alphabet offset at the current point in the cipher
    start_rotation = current_rotation # first offset we tried before moving on to others
    #known_rotation_offsets = find_known_rotation_offsets(cipher)
    last_key_collision = [None] * len(cipher)

    i = 0
    backtrack_loop_count = 0
    backtrack_status = None

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

        #
        # State 3: cipher word not present in key and no duplicate key mappings
        #
        else:

            #
            # If we were able to pre-calculate the rotation offset, use that; otherwise,
            # start things off with an initial value of 0
            #
            rot_val = 0
            if cipher_word in known_rotation_offsets:
                rot_val = known_rotation_offsets[cipher_word]
                current_rotation = (current_rotation + rot_val) % 26
            else:
                guessed_keys.append(cipher_word)
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


def fit_plaintext(text, offset):
    # TBD: build_rotation_matrix() needs to handle the offset
    known_rotations = build_rotation_matrix(text)
    return None

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

def build_rotation_matrix(text):
    def find_pivot(mat, start_row_index):
        # Iterate through the columns (except for the RHS, which we don't want to
        # ever use as a pivot)
        for col_num in range(len(mat[0]) - 1):
            for row_num in range(start_row_index, len(mat)):
                if mat[row_num][col_num] != 0:
                    print("Found pivot (%d,%d)" % (row_num, col_num))
                    return (row_num, col_num)
        print("No pivot found")
        return (None, None)

    def gauss_jordan_reduce(mat):
        for row_index in range(len(mat)):
            (pivot_row_index, pivot_col_index) = find_pivot(mat, row_index)
            if pivot_row_index == None:
                break
            assert(pivot_row_index >= row_index)
            if pivot_row_index > row_index:
                print("swap rows %d and %d" % (row_index, pivot_row_index))
                temp = mat[row_index]
                mat[row_index] = mat[pivot_row_index]
                mat[pivot_row_index] = temp
                print("matrix now", mat)

            pivot_val = mat[row_index][pivot_col_index]

            #
            # Transform row to make pivot equal 1
            # This also converts everything to floating point
            #
            mat[row_index] = [i / pivot_val for i in mat[row_index]]

            #
            # Transform other rows so that everything else in the pivot column is zero
            #
            pivot_row = mat[row_index]
            pivot_row[-1] %= 26
            print("Pivot row: %s; first nonzero index: %d" % (pivot_row, pivot_col_index))
            for secondary_row_index in range(0, len(mat)):
                if secondary_row_index == row_index:
                    continue
                secondary_row = mat[secondary_row_index]

                #
                # Most of the numbers in the matrix represent code word frequencies, not
                # rotation values, so should not be taken modulo 26. The exception is the
                # final row in the matrix, which is the RHS of that row's equation.
                #
                if secondary_row[pivot_col_index] != 0:
                    row_mult = [x * secondary_row[pivot_col_index] for x in pivot_row]
                    new_row = [x-y for (x,y) in zip(secondary_row, row_mult)]
                    new_row[-1] %= 26
                    print("new_row %s" % new_row)
                    mat[secondary_row_index] = new_row

            print("Subsequent rows: %s" % mat[row_index+1:])
            print("After %d iteration(s), matrix now:" % (row_index+1))
            print_matrix(mat)

    def get_computed_codeword_rotations(matrix, words):
        rotations = {}
        for row in matrix:
            l = [(mult, word) for (mult, word) in zip(row, words) if mult != 0]
            print("non-zero multipliers:", l, "=>", row[-1])
            # TBD: handle rows with multiple entries in the backtracking algo somehow
            if len(l) == 1:
                (mult, word) = l[0]
                # multiplier should always be 1 for a matrix in reduced row echelon form.
                # anything else means we have a bug
                assert(mult == 1.0)
                assert(row[-1].is_integer())   # Can't have a fractional rotation value
                rotations[word] = int(row[-1])
        return(rotations)

    def print_matrix(mat):
        for i in mat:
            print(' '.join(['{:-4.1f}'.format(x) for x in i]))

    assert(len(text) <= len(cipher_list))
    cipher = cipher_list[:len(text)]
    last_occurrence_of = {}
    unique_words = list(set(cipher))
    unique_words.sort()
    print("cipher slice:", cipher)
    print("cipher slice has %d total words (%d unique)" % (len(text), len(unique_words)))
    print("unique words:", unique_words)
    matrix = []
    for i in range(len(text)):
        word = cipher[i]
        if word not in last_occurrence_of:
            last_occurrence_of[word] = i
            continue
        l = last_occurrence_of[word]
        required_rot = (ord(text[i]) - ord(text[l])) % 26
        print("Required total rotation between %d and %d = %d" % (l, i, required_rot))
        sl = cipher[l:i]
        print("Slice", sl)

        counts = {}
        for j in sl:
            if j in counts:
                counts[j] += 1
                continue
            counts[j] = 1
        matrix_row = []
        for j in unique_words:
            if j in counts:
                matrix_row.append(counts[j])
                continue
            matrix_row.append(0)
        matrix_row.append(required_rot)
        matrix.append(matrix_row)
        last_occurrence_of[word] = i
        
    print("unique words:", unique_words)
    print("Initial matrix:")
    print_matrix(matrix)
    gauss_jordan_reduce(matrix)
    known_rotations = get_computed_codeword_rotations(matrix, unique_words)
    print("Computed rotations", known_rotations)
    return(known_rotations)

#text = 'congratulationsyouareacryptogr'
#text = 'congratulationsyouareacryptographerext'
text = 'congratulationsyouareacryptographerextraordi'

#build_rotation_matrix('norththirtyninedegreestenpoint')
print(fit_plaintext(text, 0))

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

