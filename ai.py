import string
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout

def chew_chat(path, max_id):
    challenge = []
    response  = []
    last_who = None

    with open(path,'r') as f:
       while True:
           line = f.readline()
           if not line:
               break

           line = line[line.find('-') + 2:] #Remove time marker
           line = line.split(':', 1)        #Split after the ID
           if len(line) != 2:
               continue

           who  = line[0]
           text = line[1]

           if last_who:
               if who == max_id and last_who != max_id:
                   response.append(text.lower())
                   challenge.append(last_text.lower())

           last_who  = who
           last_text = text

    return challenge, response

def get_words_model(text):
    tokens = []
    for t in text:
        tokens += nltk.word_tokenize(t)

    words = []
    for w in tokens:
        if w in string.punctuation:
            continue
        w = lemmatizer.lemmatize(w)
        if w not in words:
            words.append(w)

    return words

def bag_of_words(text, words):
    bag = []

    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    for w in words:
        bag += [1] if w in tokens else [0]
        if w == tokens: print(w)
    return bag

def run(message):
    challenge = bag_of_words(message.lower(), words)
    result = model.predict(np.array([challenge]))[0]
    print(f'Found {challenge.count(1)} matching token, score: {np.max(result):5.4f}')
    result /= np.max(result)
    while True:
        idx = int(np.random.uniform() * len(result))
        if result[idx] > np.random.uniform():
            return response[idx]

#Init nltk
nltk.download('wordnet')
nltk.download('punkt')
lemmatizer = WordNetLemmatizer()

chat_logs = (('michele.txt', 'Massimiliano Stenghel'), ('specie.txt', 'Massimiliano Stenghel'))
challenge = []
response  = []
for (log, max_id) in chat_logs:
    c, r = chew_chat('data/' + log, max_id)
    challenge += c
    response += r
    print(f'Chat {log}: found {len(c)} challenges')

words = get_words_model(challenge + response)
bag = bag_of_words('siurana, cenando', words)

#Rearrange challenges and respons in a format comprehensible to the network
challenge = [bag_of_words(c, words) for c in challenge]
challenge = np.array(challenge)

response_idx = np.zeros([len(response), len(response)])
for idx, r in enumerate(response):
    response_idx[idx, idx] = 1.

#Init the network and train
model = Sequential()
model.add(Dense(128, input_shape=(len(words), ), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(len(challenge), activation='softmax'))
model.compile(optimizer='adam', loss='binary_crossentropy')
model.fit(challenge, response_idx, epochs=100)

'''
#Test
while True:
    message = input("")
    challenge = bag_of_words(message.lower(), words)
    result = model.predict(np.array([challenge]))[0]
    print(f'Found {challenge.count(1)} matching token, score: {np.max(result):5.4f}')
    result /= np.max(result)
    while True:
        idx = int(np.random.uniform() * len(result))
        if result[idx] > np.random.uniform():
            print(response[idx])
            break
'''
