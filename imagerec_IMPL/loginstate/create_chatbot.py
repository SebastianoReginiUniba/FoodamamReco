from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'FoodBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Mi dispiace, non capisco. Sto ancora imparando.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///food_chatbot_database.sqlite3'
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.italian")