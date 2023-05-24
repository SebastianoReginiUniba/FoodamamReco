# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetRecipe(Action):
    def name(self) -> Text:
        return "action_get_recipe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Recupera l'ID della ricetta dai dati personalizzati
        recipe_id = tracker.get_slot("recipe_id")

        # Esegui il codice per recuperare le informazioni sulla ricetta utilizzando l'ID
        # e salva le informazioni in una variabile (ad esempio nella variabile recipe_info)

        # Invia le informazioni sulla ricetta al chatbot
        dispatcher.utter_message(
            response="utter_recipe_information",
            recipe_information=recipe_info
        )

        return []

