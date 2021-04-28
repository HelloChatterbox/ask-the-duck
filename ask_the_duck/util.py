from google_trans_new import google_translator
from RAKEkeywords import Rake
from quebra_frases import sentence_tokenize
import simplematch


class Translator:
    translator = google_translator()
    tx_cache = {}  # avoid translating twice

    @classmethod
    def translate(cls, text, lang_tgt, lang_src="en"):
        # if langs are the same do nothing
        if not lang_tgt.startswith(lang_src):
            if lang_tgt not in cls.tx_cache:
                cls.tx_cache[lang_tgt] = {}
            # if translated before, dont translate again
            if text in cls.tx_cache[lang_tgt]:
                # get previous translated value
                translated_text = cls.tx_cache[lang_tgt][text]
            else:
                # translate this utterance
                translated_text = cls.translator.translate(text,
                                                           lang_tgt=lang_tgt,
                                                           lang_src=lang_src)
                if isinstance(translated_text, list):
                    # usually male/female forms of the word
                    return translated_text[0]

                # save the translation if we need it again
                cls.tx_cache[lang_tgt][text] = translated_text
        else:
            translated_text = text.strip()
        return translated_text

    @classmethod
    def translate_dict(cls, data, lang_tgt, lang_src="en"):
        for k, v in data.items():
            if isinstance(v, dict):
                data[k] = cls.translate_dict(v, lang_tgt, lang_src)
            elif isinstance(v, str):
                data[k] = cls.translate(v, lang_tgt, lang_src)
            elif isinstance(v, list):
                data[k] = cls.translate_list(v, lang_tgt, lang_src)
        return data

    @classmethod
    def translate_list(cls, data, lang_tgt, lang_src="en"):
        for idx, v in enumerate(data):
            if isinstance(v, dict):
                data[idx] = cls.translate_dict(v, lang_tgt, lang_src)
            elif isinstance(v, str):
                data[idx] = cls.translate(v, lang_tgt, lang_src)
            elif isinstance(v, list):
                data[idx] = cls.translate_list(v, lang_tgt, lang_src)
        return data


def rake_keywords(text, lang="en"):
    return Rake(lang=lang).extract_keywords(text)


def sentence_split(text, max_sentences=3):
    return sentence_tokenize(text)[:max_sentences]


def extract_keyword(query):
    # regex from narrow to broader matches
    query = query.lower()

    match = simplematch.match("who is {query}", query) or \
            simplematch.match("what is {query}", query) or \
            simplematch.match("when is {query}", query) or \
            simplematch.match("tell me about {query}", query)
    if match:
        match = match["query"]
    else:
        # let's try to extract the best keyword and use it as query
        kwords = rake_keywords(query)
        match = kwords[0][0]
    return match


def match_infobox_field(query):
    query = query.lower()

    # known for
    match = simplematch.match("what is {query} known for", query) or \
            simplematch.match("what is {query} famous for", query)
    if match:
        return match["query"], "known for"

    # resting place
    match = simplematch.match("where is {query} resting place*", query) or \
            simplematch.match("where is {query} resting buried*", query)
    if match:
        return match["query"], "resting place"

    # birthday
    match = simplematch.match("when was {query} born*", query) or \
            simplematch.match("when is {query} birth*", query)
    if match:
        return match["query"], "born"

    # death
    match = simplematch.match("when was {query} death*", query) or \
            simplematch.match("when did {query} die*", query) or \
            simplematch.match("what was {query} *death", query) or \
            simplematch.match("what is {query} *death", query)

    if match:
        return match["query"], "died"

    # children
    match = simplematch.match("how many children did {query} have*",
                              query) or \
            simplematch.match("how many children does {query} have*",
                              query)
    if match:
        return match["query"], "children"

    # alma mater
    match = simplematch.match("what is {query} alma mater", query) or \
            simplematch.match("where did {query} study*", query)
    if match:
        return match["query"], "alma mater"

    return None, None
