def split_cipher(cipher_words, cipher_text):
    assert(len(cipher_words) == 26)
    cipher_list = []

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

    #        
    # Make sure we have a match
    #
    assert(cipher_text == ''.join(cipher_list))
    return(cipher_list)

def read_cipher(fname):
    raw_cipher = ''

    #
    # Number of times a sequence must appear in the cipher for it to be considered a potential code word
    # TBD: automatically adjust this based on the length of the cipher?
    #
    FREQ_THRESHOLD = 10

    #
    # Try to find 26 unique digit sequences in the cipher
    # Probably not the most efficient code around, but gets the job done :)
    #
    def find_words(word_length):
        nonlocal raw_cipher
        word_counts = {}

        #
        # Find every possible word of the specified length in the cipher and build
        # a dictionary to count the number of occurrences of each word
        #
        for i in range(len(raw_cipher) - word_length):
            word = raw_cipher[i:i+word_length]

            # Skip any sequence containing a space, which indicates we're across a separator boundary
            if ' ' in word:
                continue
            try:
                word_counts[word] += 1
            except KeyError:
                word_counts[word] = 1

        # Build a list of words which occur at least FREQ_THRESHOLD times in the cipher
        word_candidates = [foo for foo in word_counts.keys() if word_counts[foo] >= FREQ_THRESHOLD]
        if len(word_candidates) > 0:
            print("Found %d potential words of length %d:" % (len(word_candidates), word_length), word_candidates)

        #
        # Replace each occurrence of the candidate word with a separator, so that we can identify
        # shorter sequences without getting "false positives" from adjacent numbers
        #
        for word in word_candidates:
            raw_cipher = raw_cipher.replace(word, " ")
        return word_candidates

    with open(fname, 'r') as file:
        cipher_words = []
        raw_cipher = file.read().rstrip()

        # Search for words in order of longest (9) to shortest (2)
        for l in range(9, 1, -1):
            cipher_words.extend(find_words(l))

        # A successful run should report 26 cipher words with no leftovers
        print("Found %d cipher words: " % len(cipher_words), cipher_words)
        if len(raw_cipher.replace(' ', '')) > 0:
            print("leftovers:", raw_cipher)
