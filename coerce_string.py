from confusable_homoglyphs import confusables

def is_valid_int(char):
    try:
        return isinstance(int(char), int)
    except:
        return False

def string_coerce(string):
    #do initial test for safety
    test = bool(confusables.is_confusable(string, preferred_aliases=['latin', 'common']))

    if not test:
        return string

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
    test_strings = (
        '𐌚chan', #unsafe
        '8chan', #safe
        'уolo', #unsafe
        'Κiller Quеen', #unsafe
        'This is a safe sentence.', #safe
        "It'ѕ lit yo" #unsafe
        )

    for string in test_strings:
        #handle sentences by checking each word individually
        words = string.split(' ')
        result = ""

        for word in words:
            result += ' {}'.format(string_coerce(word))

        result = result.strip()

        test_original = bool(confusables.is_confusable(string, preferred_aliases=['latin', 'common']))

        print('Original is unsafe: {}'.format(str(test_original)))
        print('{} -> {}'.format(string, result))
        test_new = bool(confusables.is_confusable(result, preferred_aliases=['latin', 'common']))
        print('Coersion is unsafe: {}\n'.format(str(test_new)))
