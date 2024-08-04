Stanford NLP is another natural language processing tool that can be run locally.

## installation
pip install stanfordnlp
stanfordnlp.download('en')

## example of use
import stanfordnlp

## model download
stanfordnlp.download('en')

## pipeline configuration
nlp = stanfordnlp.Pipeline()

## example of text
text = "This is an example sentence for NLP processing."

## text processing
doc = nlp(text)

# Afficher les tokens
for sentence in doc.sentences:
    for word in sentence.words:
        print(word.text, word.lemma, word.pos)
