#!/usr/bin/env python3
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
import random

# Key entry types
(GUESSED, CALCULATED) = range(2)
(KEY_ROTATION_COLLISION, DUPLICATE_KEY_VALUE) = range(2)

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

print("cipher_list", cipher_list)

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

    key_list = build_key_list(key)
    plaintext = ""
    for word in cipher_list:
        if word in key:
            rot = key[word]['rotation']
            plaintext += key[word]['root_char']
            if rot > 0:
                key_list = rotate(key_list, rot)
                reassign_key_letters(key, key_list)
        else:
            print("word", word, "not in key - finishing")
            break
    return plaintext

#
# Figure out what offsets we can, based on the plaintext we're trying to fit
#
def find_known_rotation_offsets(cipher):
    offsets = {}

    #
    # TBD: compute offsets for words that lie between two words with known offsets
    # E.g. if we know offset for 5555, and sequence is 5555 4444 5555, we should
    # be able to compute 4444
    #
    for i in range(len(cipher) - 1):
        if cipher[i][0] == cipher[i + 1][0]:
            rot = (ord(cipher[i+1][1]) - ord(cipher[i][1])) % 26
            offsets[cipher[i][0]] = rot

    print("Calculated the following rotation offsets:", offsets)
    return offsets

def doit(cipher):
    state = []
#    key = {'652655': 'c', '21': 'j', '7073281': 'h', '7614435': 'z', '55709': 'f', '7954481': 'p', '89447709': 'l', '4045': 'v', '50461': 'w', '641971': 'a', '59207': 'm', '7811539': 'i', '7699855': 'q', '52123': 'y', '308': 'r', '391': 'b', '945432286': 'k', '7756659': 'n', '605858': 't', '7906967': 'd', '920376451': 's', '20': 'g', '338': 'u', '7080686': 'e', '341': 'o', '4530': 'x'}
#    for thing in key.keys():
#        ones = int(thing) % 10
#        key[thing] = { 'root_char': key[thing], 'rotation': ones }
    key = {}
    current_rotation = 0            # alphabet offset at the current point in the cipher
    start_rotation = current_rotation # first offset we tried before moving on to others
    known_rotation_offsets = find_known_rotation_offsets(cipher)

    i = 0
    loop_count = 0   # temp so we can break out of infinite loops
    backtrack_status = None

    #
    # Variables to save with state (anything not explicitly set/assigned at start of while loop):
    # current_rotation, start_rotation, key
    #
    while i < len(cipher):
        (cipher_word, plaintext_char) = cipher[i]
        key_char = chr((ord(plaintext_char) - ord('a') - current_rotation) % 26 + ord('a'))

        print("word %s plaintext_char %c key_char %c current_rotation %d key" % (cipher_word, plaintext_char, key_char, current_rotation), key)

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
                if backtrack_status['reason'] == KEY_ROTATION_COLLISION or backtrack_status['reason'] == DUPLICATE_KEY_VALUE:
                   # Redo this :)
                   if k['source'] == GUESSED:
                        of += 1
                        if of == 26:
                            # We've run through all possible rotation values, so need to backtrack again
                            print("Placeholder - tried all possible rotation values for %s" % cipher_word)
                            break
                        print("Trying new rotation value %d for word %s" % (of, cipher_word))
                        k['rotation'] = of
                        backtrack_status = None
                   else:
                        # Not a guessed rotation offset- fall through and keep backtracking
                        pass

                else:
                    print("Unhandled backtrack status", backtrack_status)
                    break

            #
            # Not backtracking: check for key collision (key[n] already set to something other than
            # what we are trying to assign
            #
            elif ch != key_char:
                ev = (ord(key_char) - ord(ch)) % 26

                #
                # expected_value is what the rotation would need to be set to to make the current
                # code word map to the current plaintext character. However, it is kinda meaningless
                # except for (I think) the first occurrence of the cipher word..
                #
                backtrack_status = {'reason': KEY_ROTATION_COLLISION, 'expected_value': ev}
                print("key collision for '%s': %s != %s; rotation difference = %d" % (cipher_word, key_char, ch, ev))

            if backtrack_status == None:
                current_rotation = (current_rotation + of) % 26

        #
        # State 2: duplicate key_val (key[a] and key[b] both map to the same letter)
        #          Pretty sure this just means we need to backtrack, but we'll see
        #
        elif key_char in [a['root_char'] for a in key.values()]:
            print("duplicate key_val %c (orig %c offset %d)" % (key_char, plaintext_char, current_rotation))
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
            rot_source = GUESSED
            if cipher_word in known_rotation_offsets:
                rot_val = known_rotation_offsets[cipher_word]
                rot_source = CALCULATED
                current_rotation = (current_rotation + rot_val) % 26
            key[cipher_word] = { 'root_char': key_char, 'rotation': rot_val, 'source': rot_source }

        #
        # Backtrack if needed; otherwise, save state and keep going
        #
        if backtrack_status == None:
            state.append({'start_rotation': start_rotation, 'key': key.copy()})
            print("current state:", state)
            start_rotation = current_rotation
            i += 1

        else:
            print("Backtracking")
            i -= 1
            if i < 0:
                print("Could not find a fit... giving up")
                break

            # restore the previous state
            d = state.pop()
            start_rotation = d['start_rotation']
            current_rotation = start_rotation
            key = d['key']

            loop_count += 1
            if loop_count >= 10000:
                print("Breaking loop")
                break

    print("Final value of i=%d" % i)
    print("Key:", key)
    #print("Final state:", state)
    return key

# Initialize position offsets to zero and create a list of tuples
#cipher = list(zip(cipher_list, 'congratulationsyou'))
cipher = list(zip(cipher_list, 'congratulatio'))
#cipher = list(zip(cipher_list, 'thecache'))
key = doit(cipher)
print(decryptit(cipher_list, key))
