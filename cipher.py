class Cipher:
    class KnownPlaintextSlice:
        def __init__(self, cipher, plaintext, cipher_index):
            self.plaintext = plaintext
            self.cipher_slice = cipher.word_list[cipher_index:cipher_index+len(plaintext)]
            self.cipher_index = cipher_index

        def __getitem__(self, i):
            return (self.cipher_slice[i], self.plaintext[i])

        def __iter__(self):
            return zip(self.cipher_slice, self.plaintext)

        def __lt__(self, other):
            return self.cipher_index < other.cipher_index

        def __repr__(self):
            return f"{self.cipher_index}:'{self.plaintext}'"

    def known_plaintext_slice(self, plaintext, cipher_index):
        return self.KnownPlaintextSlice(self, plaintext, cipher_index)

    def __init__(self, fname):
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
            # Tries to find 26 unique digit sequences in the cipher when the word lengths are not known ahead of time.
            # Probably not the most efficient code around, but gets the job done :)
            #
            def find_words(word_length):
                nonlocal raw_cipher
                word_counts = {}

                #
                # Number of times a sequence must appear in the cipher for it to be considered a potential code word
                # TBD: automatically adjust this based on the length of the cipher?
                #
                FREQ_THRESHOLD = 10

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

            #
            # Figure out the set of codewords when we have the luxury of knowing the lengths ahead
            # of time (e.g. ciphers #1 and #2)
            #
            def read_known_length_words(raw_cipher):
                cipher_dict = {}
                pos = 0
                code = ''
                while pos < len(raw_cipher):
                    code_length = int(raw_cipher[pos])
                    assert(code_length > 0)
                    for i in range(0, code_length):
                        code += raw_cipher[pos]
                        pos += 1

                    # Keep track of frequencies "because we can"
                    # not using them at the moment
                    if code in cipher_dict:
                        cipher_dict[code] += 1
                    else:
                        cipher_dict[code] = 1
                    code = ''

                return(list(cipher_dict.keys()))

            cipher_words = []
            with open(fname, 'r') as file:
                assume_codeword_lengths = file.readline().rstrip().lower()
                if assume_codeword_lengths in ('true', 'yes', 't', 'y'):
                    assume_codeword_lengths = True
                else:
                    assume_codeword_lengths = False
                raw_cipher = file.read().rstrip()
                r = raw_cipher

                if assume_codeword_lengths == True:
                    cipher_words = read_known_length_words(raw_cipher)
                else:
                    # Search for words in order of longest (9) to shortest (2)
                    for l in range(9, 1, -1):
                        cipher_words.extend(find_words(l))
                    assert len(raw_cipher.replace(' ', '')) == 0, f"leftovers: {raw_cipher}"

                # A successful run should report 26 cipher words with no leftovers
                print(f"Found {len(cipher_words)} cipher words: {cipher_words}")
                assert(len(cipher_words) == 26)

            return(cipher_words, split_cipher(cipher_words, r))

        (self.unique_words, self.word_list) = read_cipher(fname)
        self.unique_words.sort()

    def __len__(self):
        return len(self.word_list)

    def __getitem__(self, i):
        return self.word_list[i]
