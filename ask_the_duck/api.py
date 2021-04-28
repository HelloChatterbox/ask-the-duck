from ask_the_duck.util import Translator, extract_keyword, sentence_split, match_infobox_field
from ask_the_duck.session import SESSION


class DDG:
    def __init__(self, lang="en"):
        self.lang = lang.split("-")[0].lower()

    # ddg api
    def search(self, query, raw=True):
        if self.lang != "en":
            # translate input to English
            query = Translator.translate(query, "en", self.lang)
        data = SESSION.get("https://api.duckduckgo.com",
                           params={"format": "json",
                                   "q": query}).json()
        if self.lang != "en" and not raw:
            # translate output to self.lang
            return Translator.translate_dict(data, self.lang, "en")
        return data

    def get_infobox(self, query, raw=False):
        data = self.search(query)
        # info
        related_topics = [t.get("Text") for t in data.get("RelatedTopics", [])]
        infobox = {}
        infodict = data.get("Infobox") or {}
        for entry in infodict.get("content", []):
            k = entry["label"].lower().strip()
            infobox[k] = entry["value"]
        if self.lang != "en" and not raw:
            # translate output to self.lang
            infobox = Translator.translate_dict(infobox, self.lang, "en")
            related_topics = Translator.translate_list(related_topics,
                                                       self.lang, "en")
        return infobox, related_topics

    # spoken answers api
    def spoken_answer(self, query, max_sentences=3):
        return self.ask_the_duck(query, max_sentences)

    def ask_the_duck(self, query, max_sentences=3):
        if self.lang != "en":
            # translate input to English
            query = Translator.translate(query, "en", self.lang)

        # match an infobox field with some basic regexes
        # (primitive intent parsing)
        selected, key = match_infobox_field(query)
        if key:
            selected = extract_keyword(selected)
            infobox = self.get_infobox(selected, raw=True) or {}
            answer = infobox.get(key)
            if answer:
                return answer

        # extract the best keyword with some regexes or fallback to RAKE
        query = extract_keyword(query)
        data = self.search(query)

        # summary
        summary = data.get("AbstractText")
        if not summary:
            return None

        # translate output to self.lang
        summary = Translator.translate(summary, self.lang, "en")
        sentences = sentence_split(summary, max_sentences)
        return " ".join(sentences)
