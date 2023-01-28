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
