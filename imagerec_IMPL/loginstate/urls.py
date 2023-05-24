from django.urls import path
from . import views
# [ ] Modificare il chatbot per farlo funzionare nel modo richiesto
# [ ] (Optional) Riaddestrare il modello e caricarlo sulla webapp 
# [x] Trovare cibi che vengono riconosciuti bene
# [x] Preparare struttura capitoli per tesi di laurea da presentare alla prof
# [x] Modificare colore health labels in base a caratteristiche utente
# [x] Sistemare il checked in registrazione
# [x] Sistemare i nomi delle card (ora invisibili, vorrei fare un display flex che li metta agli opposti in verticale)
# [x] Abbellire l'upload dell'immagine in home
# [x] Aggiustare le measure unit in recipeDetails
# [x] Implementare il chatbot
# [x] Aggiungere la pagina per visualizzare gli alimenti cliccando sulle card (sostituire a quel getrecipeinfo)
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('registration/', views.registrationPage, name="registration"),
    path('logout/', views.logoutUser, name="logout"),
    #path('chatbot/', views.chatbot, name='chatbot'),
    path('recipeDetails/', views.recipeDetails, name='recipeDetails')
]