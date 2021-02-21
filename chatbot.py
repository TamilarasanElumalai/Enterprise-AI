import nltk
import pickle
from nltk.stem import WordNetLemmatizer
import json
lem = WordNetLemmatizer()
import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
words =[]
documents= []
classes = []
ignore_words = ['!','?',':',';','.',',','-']
intents = open('intents.json').read()
images = open('images.json').read()
suggestions = open('suggestions.json').read()
intents = json.loads(intents)
images = json.loads(images)
suggestions = json.loads(suggestions)
import nltk
nltk.download('punkt')
for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w,intent['tag']))
        
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
import nltk
nltk.download('wordnet')
words = [lem.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))
training=[]

output_empty = [0]*len(classes)

for doc in documents:
    
    bag =[]
    
    pattern_words = doc[0] # list of tokenized words for each doc
    
    pattern_words = [lem.lemmatize(w.lower()) for w in pattern_words]
    
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] =1
    training.append([bag , output_row])

random.shuffle(training)
training  = np.array(training)
train_x = list(training[:,0])
train_y = list(training[:,1])
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu')) #input layer
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu')) #hidden layer with 64 neurons
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax')) #output layer number of neurons=intent

sgd = SGD(lr = 0.01, decay = 1e-6, momentum=0.9, nesterov=True) # learning rate = 0.01 
model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

#fitting and saving the model

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

model.save('chatbot_model.h5', hist)
from keras.models import load_model
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl','rb'))

classes = pickle.load(open('classes.pkl','rb'))
def cleanup_sent(sentence):
    sen_words =  nltk.word_tokenize(sentence)
    sen_words = [lem.lemmatize(word.lower()) for word in sen_words]
    return sen_words
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sen_words = cleanup_sent(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sen_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    PROB_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>PROB_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result
def getImage(ints, images_json):
    list_images = images_json['intents']
    tag = ints[0]['intent']
    for i in list_images:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            return result
    return ("-1")
def getSuggest(ints, sugg_json):
    tag = ints[0]['intent']
    list_sugg = sugg_json['intents']
    for i in list_sugg:
        if(i['tag']== tag):
            result = i['responses']
            return result
    return("-1")
def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    img = getImage(ints, images)
    sugg = getSuggest(ints,suggestions)
    answer=[]
    answer.append(res)
    if img!='-1':
        answer.append(img)
    else:
        answer.append("-1")
    if sugg!='-1':
        answer.append(sugg)
    else:
        answer.append("-1")
    return answer
import tkinter
from tkinter import *
from PIL import Image,ImageTk
def fb():
    window = Toplevel(base)
    window.title("Feedback")
    window.geometry("200x200")
    var='0'
    #var.set(0)
    r1 = Radiobutton(window, text='1 Star ', variable=var, value='1', background = "light blue",command=window.destroy,tristatevalue=0)
    r1.pack(side = TOP, ipady = 5) 
    r2 = Radiobutton(window, text='2 Stars', variable=var, value='2',background = "light blue", command=window.destroy,tristatevalue=0)
    r2.pack(side = TOP, ipady = 5) 
    r3 = Radiobutton(window, text='3 Stars', variable=var, value='3', background = "light blue",command=window.destroy,tristatevalue=0)
    r3.pack(side = TOP, ipady = 5) 
    r4 = Radiobutton(window, text='4 Stars', variable=var, value='4', background = "light blue",command=window.destroy,tristatevalue=0)
    r4.pack(side = TOP, ipady = 5) 
    r5= Radiobutton(window, text='5 Stars', variable=var, value='5', background = "light blue",command=window.destroy,tristatevalue=0)
    r5.pack(side = TOP, ipady = 5) 
    ChatLog.config(state = NORMAL)
        
    return var
def printfb(var):
    ChatLog.insert(END, "Jarvis:Thank you for your feedback!\n\n")
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)

global img

def send():
    
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        ChatLog.config(state = NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 14, 'bold' ))
        
        answer = chatbot_response(msg)
        res=answer[0]
        ChatLog.insert(END, "Jarvis: " + res + '\n\n')
        if answer[1]!='-1':
            ChatLog.insert(END, "Jarvis: ")
            result = answer[1]
            img=Image.open(result)
            img=img.resize((300,300),Image.ANTIALIAS)
            img=ImageTk.PhotoImage(img)
            ChatLog.image=img
            ChatLog.image_create(INSERT, image=img)
        if answer[2]!='-1':
            #for i in answer[2]:
            ChatLog.window_create(ChatLog.index("end"), window = Button(ChatLog, text=answer[2][0], width=50,height=2,bg='white',command=lambda:suggsend(answer[2][0])) ) 
            ChatLog.window_create(ChatLog.index("end"), window = Button(ChatLog, text=answer[2][1], width=50,height=2,bg='white',command=lambda:suggsend(answer[2][1])) )
            ChatLog.window_create(ChatLog.index("end"), window = Button(ChatLog, text=answer[2][2], width=50,height=2,bg='white',command=lambda:suggsend(answer[2][2])) )
            
        ChatLog.insert(END, "\n\n")
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
def suggsend(i):
    ChatLog.config(state = NORMAL)
    ChatLog.config(foreground="#442265", font=("Verdana", 16,'bold'))
    answer = chatbot_response(i)
    res=answer[0]
    ChatLog.insert(END, "Jarvis: " + res + '\n')
    
base = Tk()
base.title("Welcome to Customer Care")
base.geometry("700x500")
base.resizable(width=FALSE, height=FALSE)
    
ChatLog = Text(base, bd=0, bg="#FAF5A8", height="8", width="50", font=("Arial",16,'bold'))
        
ChatLog.config(state =  DISABLED)
    
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
    
SendButton = Button(base, font=("Comic Sans MS",14,'bold'), text="SEND", width="12", height=5,
                    bd=0, bg="#3cd548", activebackground="#3c9d9b",fg='#ffffff',
                    command=send )
 
    #Create the box to enter message

EntryBox = Text(base, bd=0, bg="#FAF5A8",width="29", height="5", font=("Arial",14))
  
scrollbar.place(x=600,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=599)
EntryBox.place(x=6, y=401, height=70, width=350)
SendButton.place(x=370, y=410, height=50,width=150)
fbButton = Button(base, font=("Verdana",12,'bold'), text="Feedback", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command=lambda:printfb(fb()))

fbButton.place(x=6, y=350, height=40) 
base.mainloop()
