from confusable_homoglyphs import confusables

def is_valid_int(char):
    try:
        return isinstance(int(char), int)
    except:
        return False

def string_coerce(string):
    string_chars = []
    for char in string:
        aliases = confusables.is_confusable(char, greedy=False, preferred_aliases=[], allow_digit=False)
        string_chars += aliases

    coerced = []
    for char in string_chars:
        if char['alias'] == 'LATIN':
            coerced.append(char['character'])

        elif is_valid_int(char):
            coerced.append(char['character'])

        else:
            for homoglyph in char['homoglyphs']:
                if homoglyph['n'].startswith('LATIN') or homoglyph['n'].startswith('DIGIT'):
                    coerced.append(homoglyph['c'])
                    break

    return ''.join(coerced)

if __name__ == '__main__':
    test_strings = ('𐌚cha𝐧')

    for string in test_strings:
        result = string_coerce(string)
        test_original = bool(confusables.is_confusable(string, preferred_aliases=['latin', 'common']))

        print('Original is unsafe: {}'.format(str(test_original)))
        print('{} -> {}'.format(string, result))
        print(confusables.is_confusable(result, preferred_aliases=['latin', 'common']))
