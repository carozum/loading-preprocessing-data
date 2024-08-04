import spacy

# Charger le modèle de langue anglais
nlp = spacy.load('en_core_web_sm')

# Exemple de texte
text = "This is an example sentence for NLP processing."

# Traiter le texte
doc = nlp(text)

# Afficher les entités nommées
for ent in doc.ents:
    print(ent.text, ent.label_)
