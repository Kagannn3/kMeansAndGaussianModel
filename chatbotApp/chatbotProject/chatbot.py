from chatterbot import ChatBot #import ChatBot class from the chatterbor package(dictionary)(framework)
from chatterbot.trainers import ChatterBotCorpusTrainer #import ChatterBotCorpusTrainer class from the trainers package(dictionary)(framework) of the chatterbor package(dictionary)(framework)


chatbot=ChatBot('ResearchBot') #creating an object of the ChatBot class 
trainer=ChatterBotCorpusTrainer(chatbot) # ChatterBotCorpusTrainer is to facilitate the training of a 
#chatbot using pre-defined datasets known as 'corpus-data' such as conversational datasets, 
# typical dialogues and so on.

trainer.train('chatterbot.corpus.english')
#train the chatbot (you can use different datasets or create your own)

while True:
    user_input=input('You: ')
    response=chatbot.get_response(user_input)
    print('Bot:', response)
