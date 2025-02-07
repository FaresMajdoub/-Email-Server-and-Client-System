# Email Server and Client System

## 📌 Description
Ce projet implémente un système de courriels interne en utilisant des sockets et un protocole de communication personnalisé.  
Le système est composé d'un **client** pour l'envoi et la réception de courriels et d'un **serveur SMTP** pour la gestion des communications internes (@glo2000.ca).  
Le projet exploite des concepts avancés comme la gestion des connexions simultanées, le hachage sécurisé des mots de passe et le stockage structuré des messages.

## 🚀 Fonctionnalités
### Serveur
- **Création de comptes sécurisés** :
  - Vérification de la complexité des mots de passe (≥ 10 caractères, majuscules, minuscules, chiffres).
  - Stockage des mots de passe hachés avec SHA3-512.
- **Envoi de courriels internes** :
  - Gestion des boîtes de réception des utilisateurs.
  - Sauvegarde des courriels non délivrés dans un dossier dédié.
- **Consultation des courriels** :
  - Liste des messages avec sujet, envoyeur et date.
  - Lecture des courriels avec un affichage formaté.
- **Statistiques des utilisateurs** :
  - Nombre total de messages et taille du dossier.
- **Gestion des connexions simultanées** avec le module `glosocket`.

### Client
- **Connexion et création de comptes** :
  - Authentification sécurisée.
- **Envoi de courriels** :
  - Entrée du destinataire, du sujet et du contenu.
- **Consultation des courriels** :
  - Liste des messages disponibles.
  - Lecture d'un courriel spécifique.
- **Statistiques** :
  - Affichage du nombre de messages et de la taille de la boîte.
- **Déconnexion sécurisée**.

## 🏗️ Structure du projet
```
📂 **src/** - Code source  
  ├── `TP4_server.py` : Implémentation du serveur SMTP  
  ├── `TP4_client.py` : Implémentation du client de messagerie  
  ├── `glosocket` : Module pour les communications socket  
  ├── `gloutils` : Constantes et outils pour le projet  
  ├── `SERVER_DATA_DIR` : Dossier de stockage des données utilisateur  
  └── `SERVER_LOST_DIR` : Dossier des courriels non délivrés  
```

## 🔧 Installation & Exécution
### Pré-requis
- Python ≥ 3.8
- Modules standards : `hashlib`, `hmac`, `getpass`, `json`, `socket`
- Modules fournis : `glosocket`, `gloutils`

### Instructions
1. **Cloner le dépôt :**
   ```sh
   git clone https://github.com/ton-utilisateur/Email-Server-System.git
   cd Email-Server-System
   ```

2. **Démarrer le serveur :**
   ```sh
   python TP4_server.py
   ```

3. **Lancer un client :**
   ```sh
   python TP4_client.py -d 127.0.0.1
   ```

## 📊 Exemples d'Utilisation
### ⚡ Création d'un compte
```plaintext
Menu de connexion
1. Créer un compte
2. Se connecter
3. Quitter
Entrez votre choix [1-3]: 1
Entrez un nom d'utilisateur: user.name
Entrez un mot de passe: ********** (voir les conditions)
```

### ⚡ Envoi de courriels
```plaintext
Menu principal
1. Consultation de courriels
2. Envoi de courriels
Entrez votre choix [1-2]: 2
Entrez l'adresse du destinataire: friend@glo2000.ca
Entrez le sujet: Hello!
Entrez le contenu du courriel, terminez avec un '.' sur une ligne :
Ceci est un test.
.
```

### ⚡ Consultation des statistiques
```plaintext
Menu principal
3. Statistiques
Nombre de messages : 5
Taille du dossier : 2.1 Mo
```

## ✍️ Auteurs
**Fares Majdoub** - Université Laval, GLO-2000, Automne 2024  

## 📜 Licence
Sous licence **MIT**.

