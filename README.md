# Banking FAQ Chatbot

Paprastas banko FAQ chatbot prototipas, naudojantis Word2Vec/FastText embeddings semantiniam panašumui nustatyti.

## Aprašymas

Šis chatbot gali suprasti vartotojo klausimus ir pateikti tinkamus atsakymus iš dažniausiai užduodamų klausimų (FAQ) duomenų bazės. Chatbot naudoja Word2Vec arba FastText embeddings modelius, kad rastų semantiškai panašiausius klausimus ir pateiktų atitinkamus atsakymus.

## Funkcionalumas

- ✅ Supranta vartotojo įvestį lietuvių kalba
- ✅ Susieja klausimus su FAQ duomenų baze naudojant semantinį panašumą
- ✅ Pateikia tinkamus atsakymus
- ✅ Web sąsaja su Streamlit
- ✅ Konsolinė versija testavimui

## Reikalavimai

- Python 3.8 arba naujesnė versija
- pip (Python paketų valdymo įrankis)

## Instaliacija

1. **Klonuokite repozitoriją arba atsisiųskite failus**

2. **Sukurkite virtualią aplinką (rekomenduojama):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# arba
venv\Scripts\activate  # Windows
```

3. **Įdiekite priklausomybes:**
```bash
pip install -r requirements.txt
```

## Naudojimas

### Web sąsaja (Streamlit)

Paleiskite Streamlit aplikaciją:

```bash
streamlit run app.py
```

Aplikacija bus prieinama naršyklėje adresu `http://localhost:8501`

### Konsolinė versija

Paleiskite chatbot tiesiogiai:

```bash
python chatbot.py
```

Tai paleis testinį scenarijų su keliais pavyzdiniais klausimais.

### Programiškai naudojant Python

```python
from chatbot import BankingChatbot

# Sukurkite chatbot instanciją
chatbot = BankingChatbot(use_fasttext=False)  # False = Word2Vec, True = FastText

# Užduokite klausimą
response = chatbot.get_response("Kaip atidaryti sąskaitą?")
print(response)
```

## FAQ duomenų bazė

Chatbot naudoja `faq_data.json` failą, kuriame yra klausimų ir atsakymų poros. Šiuo metu yra 12 skirtingų klausimų apie:

- Sąskaitų atidarymą
- Mokesčius
- Internetinio banko prieigą
- Pavedimus
- PIN kodų keitimą
- Kredito korteles
- Debeto korteles
- Indėlius
- Kortelių blokavimą
- Banko išrašus
- Bankomato mokesčius

Galite pridėti daugiau klausimų redaguodami `faq_data.json` failą.

## Technologijos

- **Word2Vec/FastText**: Semantiniam panašumui nustatyti (gensim biblioteka)
- **NLTK**: Teksto apdorojimui (tokenizacija, stopwords)
- **scikit-learn**: Kosinusiniam panašumui skaičiuoti
- **Streamlit**: Web sąsajai
- **NumPy**: Vektorių operacijoms

## Kaip veikia

1. **Teksto apdorojimas**: Vartotojo klausimas ir FAQ klausimai yra apdorojami (mažosios raidės, tokenizacija, stopwords pašalinimas)

2. **Embeddings generavimas**: 
   - Word2Vec arba FastText modelis treniruojamas ant visų FAQ klausimų
   - Kiekvienas klausimas konvertuojamas į vektorių (vidurkis visų žodžių embeddings)

3. **Panašumo skaičiavimas**: 
   - Vartotojo klausimo embedding skaičiuojamas
   - Kosinusinis panašumas skaičiuojamas su visais FAQ klausimais
   - Randamas labiausiai panašus klausimas

4. **Atsakymo pateikimas**: 
   - Jei panašumas viršija slenkstį (0.3), pateikiamas atitinkamas atsakymas
   - Kitu atveju pateikiamas bendras atsakymas

## Pavyzdiniai klausimai

Chatbot gali atsakyti į šiuos ir panašius klausimus:

1. "Kaip atidaryti sąskaitą?"
2. "Kokie yra sąskaitos valdymo mokesčiai?"
3. "Kaip gauti internetinio banko prieigą?"
4. "Kiek kainuoja pavedimas į kitą banką?"
5. "Kaip pakeisti PIN kodą?"
6. "Kokios yra kredito kortelės palūkanos?"
7. "Kaip užsisakyti debeto kortelę?"
8. "Kokie yra indėlių palūkanų normos?"
9. "Ką daryti, jei praradau kortelę?"
10. "Kaip gauti banko išrašą?"

## Struktūra projekto

```
banking_chatbot/
├── app.py                 # Streamlit web sąsaja
├── chatbot.py             # Pagrindinė chatbot logika
├── faq_data.json          # FAQ klausimų ir atsakymų duomenys
├── requirements.txt       # Python priklausomybės
├── README.md             # Šis failas
└── LICENSE               # Licencijos failas
```

## Pastabos

- Chatbot treniruojamas kiekvieną kartą paleidžiant programą (nėra išsaugotų modelių)
- FastText gali geriau dirbti su retais žodžiais, nes gali apdoroti out-of-vocabulary žodžius
- Panašumo slenkstis (threshold) gali būti pritaikytas `chatbot.py` faile

## Autorius

Projektas sukurtas kaip akademinio projekto dalis.

## Licencija

GNU General Public License v3.0

