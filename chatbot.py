import numpy as np
import json
import pickle
import random
import nltk
from nltk.stem import WordNetLemmatizer
from keras.api.models import Sequential
from keras.api.layers import Dense, Dropout
from keras.api.optimizers import SGD

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load and prepare intents
intents = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": [
                "Hi", "Hey", "Hello", "Good day", "Greetings",
                "What's up", "How are you", "Hi there"
            ],
            "responses": [
                "Hello! How can I help you today?",
                "Hi there! What would you like to know?",
                "Greetings! How may I assist you?"
            ]
        },
        {
            "tag": "about",
            "patterns": [
                "Who are you?", "What do you do?", "Tell me about yourself",
                "What's your background?", "Your experience?", "Your skills?"
            ],
            "responses": [
                "I'm Siga Saint, a software engineer specializing in Python, ML & AI",
                "I'm a 20-year-old self-taught developer with 4 years of experience",
                "I specialize in predictive algorithms, image processing, and website development"
            ]
        },
        {
            "tag": "projects",
            "patterns": [
                "What projects have you done?", "Show me your work",
                "Portfolio examples?", "What have you built?",
                "Your recent projects?"
            ],
            "responses": [
                "I've built several projects including this portfolio website, an e-commerce platform, and a blog site",
                "My key projects include web development, AI applications, and data analysis tools",
                "Check out my portfolio section for detailed project examples!"
            ]
        },
        {
            "tag": "contact",
            "patterns": [
                "How can I contact you?", "Contact information?",
                "How to reach you?", "Your email?", "Social media?"
            ],
            "responses": [
                "You can reach me through the contact form on this website",
                "Follow me on Twitter @saintispapi or Medium @pythonpathfinders",
                "Connect with me on GitHub @sigasaint"
            ]
        }
    ]
}

words = []
classes = []
documents = []
ignore_chars = ['?', '!', '.', ',']

# Create our training data
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and lower each word
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Save words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Create and train model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list):
    if not intents_list:
        return "I'm not sure how to respond to that"
    tag = intents_list[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def chat(message):
    ints = predict_class(message)
    res = get_response(ints)
    return res

if __name__ == "__main__":
    print("Chatbot is ready to talk! (type 'quit' to exit)")
    while True:
        message = input("You: ")
        if message.lower() == 'quit':
            break
        response = chat(message)
        print(f"Bot: {response}")