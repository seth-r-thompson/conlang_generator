import numpy.random as rng
import numpy as np

_max_phrase_types = 5
_max_sentence_types = 5
_par_length = 50
_sen_length = 5
_phrase_length = 3
_word_count = 50

def model():
    Noun = ["N", "n", 1] # basic noun phrase
    Verb = ["V", "v", 1] # basic verb phrase
    phrases = [Noun, Verb]

    for i in range(0, rng.randint(0, _max_phrase_types)):
        phrase = str(chr(65 + i)) # phrase name
        template = phrase.lower() # basic phrase template
        freq = rng.rand() # phrase freq

        phrases.append([phrase, template, freq])

    for phrase in phrases:
        length = rng.randint(0, _phrase_length)
        for i in range(0, length):
            constituent = rng.choice([phrase[0] for phrase in phrases])
            if rng.rand() < 0.75 or phrase[0] == constituent:
                constituent = constituent.lower()
            phrase[1] = rng.choice([phrase[1] + constituent, constituent + phrase[1]])

    return phrases

def arrange(phrases):
    intransitive = rng.choice(["NV", "VN"], p=[0.85, 0.15]) # basic order of instransitive sentences
    transitive = rng.choice(["NVN", "NNV", "VNN"], p=[0.4, 0.5, 0.1]) # basic order of transitive sentences
    sentences = [intransitive, transitive]
    paragraph = ""
    phrase_types = [phrase[0] for phrase in phrases]

    # generate permutations of sentences
    for i in range(0, _max_sentence_types):
        sentence = rng.choice([intransitive, transitive])
        length = rng.randint(0, _sen_length)
        
        for j in range(0, length):
            location = rng.randint(0,len(sentence))
            adjunct = rng.choice(phrase_types)
            sentence = sentence[location:] + adjunct + sentence[:location]
        
        sentences.append(sentence)

    # form random paragraph of sentences
    for k in range(0, _par_length):
        sentence = rng.choice(sentences)
        # omit based on frequency
        for c in sentence:
            if c in phrase_types and rng.rand() < 1 - phrases[phrase_types.index(c)][2]:
                continue
        paragraph += sentence + "."

    # recursively replace phrases with their templates
    while True:
        new_paragraph = ""
        for c in paragraph:
            if c in phrase_types:
                new_paragraph += phrases[phrase_types.index(c)][1]
            else:
                new_paragraph += c

        if paragraph == new_paragraph: # no change occured
            break
        else:
            paragraph = new_paragraph

    return paragraph

def populate(paragraph):
    words = []
    text = ""

    for i in range(0, _word_count):
        words.append(new_word())

    pos = [item for item in list(set(paragraph)) if item != "." and item != ","] # unique parts of speech

    words = np.array_split(np.array(words), len(pos) + 1) # split words into groups based on pos

    # replace paragraph template with words
    is_capitalized = True
    for c in paragraph:
        if c in pos:
            word = rng.choice(words[pos.index(c)])
            if is_capitalized:
                word = word.capitalize()
                is_capitalized = False
            text += " " + word
        else:
            text += c
        if c == ".":
            is_capitalized = True

    return text

_plosives = ["p", "t", "k", "b", "d", "g"]
_plosives_weight = [.05, .25, .20, .15, .20, .15]
_fricatives = ["s", "z", "f", "v", "h"]
_fricatives_weight = [.50, .20, .05, .05, .20]
_sonorants = ["m", "n", "l", "r", "w", "y"]
_sonorants_weight = [.15, .30, .10, .15, .10, .20]
_vowels = ["a", "e", "i", "o", "u"]
_vowels_weight = [.30, .25, .20, .15, .10]
_onsets = ["P", "F", "S", "PS"]
_onsets_weight = [0.40, 0.25, 0.25, 0.1]
_codas = ["P", "F", "S", "FP", "SP", "SF"]
_codas_weight = [0.30, 0.20, 0.20, 0.05, 0.15, 0.1]

def new_word():
    word = ""

    onset = rng.choice(_onsets, p=_onsets_weight)
    nucleus = rng.choice(_vowels, p=_vowels_weight)
    if rng.rand() < 0.25:
        nucleus += rng.choice(_vowels, p=_vowels_weight)
    coda = rng.choice(_codas, p=_codas_weight)

    word_template = onset + nucleus + coda

    for char in word_template:
        if char == "P":
            word += rng.choice(_plosives, p=_plosives_weight)
        elif char == "F":
            word += rng.choice(_fricatives, p=_fricatives_weight)
        elif char == "S":
            word += rng.choice(_sonorants, p=_sonorants_weight)
        else:
            word += char

    if rng.rand() < .25:
        return word + new_word() # multisyllable word

    return word

# main
for index in range(0, 1):
    phrases = model()
    paragraph = arrange(phrases)
    text = populate(paragraph)

print(text)