"""
GLO-2000 Travail pratique 4 - Serveur
Fares Majdoub 537 003 264 
Noah Ladouceur 536 946 412
Mathieu Roussel 537 292 242
"""

import argparse
import getpass
import json
import socket
import sys

import glosocket
import gloutils


class Client:
    """Client pour le serveur mail @glo2000.ca."""

    def __init__(self, destination: str) -> None:
        """
        Prépare et connecte le socket du client `_socket`.

        Prépare un attribut `_username` pour stocker le nom d'utilisateur
        courant. Laissé vide quand l'utilisateur n'est pas connecté.
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._socket.connect((destination, gloutils.APP_PORT))
        except socket.error as e:
            print(f"Erreur de connexion : {e}")
            sys.exit(1)
        self._username = ""

    def _register(self) -> None:
        """Demande un nom d'utilisateur et un mot de passe pour créer un compte."""
        username = input("Entrez un nom d'utilisateur : ")
        password = getpass.getpass("Entrez un mot de passe : ")
        payload = gloutils.AuthPayload(username=username, password=password)
        message = gloutils.GloMessage(header=gloutils.Headers.AUTH_REGISTER, payload=payload)
        try:
            glosocket.snd_mesg(self._socket, json.dumps(message))
            response = json.loads(glosocket.recv_mesg(self._socket))
            if response['header'] == gloutils.Headers.OK:
                self._username = username
                print("Compte créé avec succès.")
            else:
                print(f"Erreur : {response['payload']['error_message']}")
        except glosocket.GLOSocketError as e:
            print(f"Erreur de communication : {e}")

    def _login(self) -> None:
        """Demande un nom d'utilisateur et un mot de passe pour se connecter."""
        username = input("Entrez votre nom d'utilisateur : ")
        password = getpass.getpass("Entrez votre mot de passe : ")
        payload = gloutils.AuthPayload(username=username, password=password)
        message = gloutils.GloMessage(header=gloutils.Headers.AUTH_LOGIN, payload=payload)
        try:
            glosocket.snd_mesg(self._socket, json.dumps(message))
            response = json.loads(glosocket.recv_mesg(self._socket))
            if response['header'] == gloutils.Headers.OK:
                self._username = username
                print("Connexion réussie.")
            else:
                print(f"Erreur : {response['payload']['error_message']}")
        except glosocket.GLOSocketError as e:
            print(f"Erreur de communication : {e}")

    def _logout(self) -> None:
        """Déconnecte l'utilisateur courant."""
        message = gloutils.GloMessage(header=gloutils.Headers.AUTH_LOGOUT)
        try:
            glosocket.snd_mesg(self._socket, json.dumps(message))
            response = json.loads(glosocket.recv_mesg(self._socket))
            if response['header'] == gloutils.Headers.OK:
                self._username = ""
                print("Déconnexion réussie.")
            else:
                print(f"Erreur : {response['payload']['error_message']}")
        except glosocket.GLOSocketError as e:
            print(f"Erreur de communication : {e}")

    def _read_email(self) -> None:
        """Récupère la liste des emails de l'utilisateur et permet de lire un email spécifique."""
        message = gloutils.GloMessage(header=gloutils.Headers.INBOX_READING_REQUEST)
        try:
            glosocket.snd_mesg(self._socket, json.dumps(message))
            response = json.loads(glosocket.recv_mesg(self._socket))
            if response['header'] == gloutils.Headers.OK:
                emails = response['payload']['emails']
                if not emails:
                    print("Aucun courriel disponible.")
                    return
                for i, email in enumerate(emails, start=1):
                    print(f"{i}. {email['subject']} ({email['date']})")
                choice = int(input("Entrez le numéro du courriel à lire : ")) - 1
                if 0 <= choice < len(emails):
                    email = emails[choice]
                    # Ajouter les clés 'to' et 'body' si elles sont absentes
                    email['to'] = email.get('to', email.get('destination', ''))
                    email['body'] = email.get('body', email.get('content', ''))
                    print(gloutils.EMAIL_DISPLAY.format(**email))
                else:
                    print("Choix invalide.")
            else:
                print(f"Erreur : {response['payload']['error_message']}")
        except glosocket.GLOSocketError as e:
            print(f"Erreur de communication : {e}")

    def _send_email(self) -> None:
        """Permet à l'utilisateur d'envoyer un email."""
        destination = input("Entrez l'adresse email du destinataire : ")
        subject = input("Entrez le sujet : ")
        print("Entrez le contenu du courriel (terminez par un point seul sur une ligne) :")
        content = ""
        while True:
            line = input()
            if line == ".":
                break
            content += line + "\n"
        payload = gloutils.EmailContentPayload(
            sender=self._username,
            destination=destination,
            subject=subject,
            date=gloutils.get_current_utc_time(),
            content=content.strip()
        )
        message = gloutils.GloMessage(header=gloutils.Headers.EMAIL_SENDING, payload=payload)
        try:
            glosocket.snd_mesg(self._socket, json.dumps(message))
            response = json.loads(glosocket.recv_mesg(self._socket))
            if response['header'] == gloutils.Headers.OK:
                print("Courriel envoyé avec succès.")
            else:
                print(f"Erreur : {response['payload']['error_message']}")
        except glosocket.GLOSocketError as e:
            print(f"Erreur de communication : {e}")

    def _check_stats(self) -> None:
        """Demande les statistiques au serveur."""
        message = gloutils.GloMessage(header=gloutils.Headers.STATS_REQUEST)
        try:
            glosocket.snd_mesg(self._socket, json.dumps(message))
            response = json.loads(glosocket.recv_mesg(self._socket))
            if response['header'] == gloutils.Headers.OK:
                stats = response['payload']
                print(gloutils.STATS_DISPLAY.format(**stats))
            else:
                print(f"Erreur : {response['payload']['error_message']}")
        except glosocket.GLOSocketError as e:
            print(f"Erreur de communication : {e}")

    def run(self) -> None:
        """Point d'entrée du client."""
        while True:
            if not self._username:
                print(gloutils.CLIENT_AUTH_CHOICE)
                choice = input("Entrez votre choix [1-3] : ")
                if choice == "1":
                    self._register()
                elif choice == "2":
                    self._login()
                elif choice == "3":
                    print("Au revoir !")
                    sys.exit(0)
                else:
                    print("Choix invalide.")
            else:
                print(gloutils.CLIENT_USE_CHOICE)
                choice = input("Entrez votre choix [1-4] : ")
                if choice == "1":
                    self._read_email()
                elif choice == "2":
                    self._send_email()
                elif choice == "3":
                    self._check_stats()
                elif choice == "4":
                    self._logout()
                else:
                    print("Choix invalide.")


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination", required=True, help="Adresse IP du serveur.")
    args = parser.parse_args()
    client = Client(args.destination)
    client.run()
    return 0


if __name__ == "__main__":
    sys.exit(_main())
