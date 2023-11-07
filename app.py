from flask import Flask, request, render_template
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Inizializza un elenco vuoto per i partecipanti
participants = []

# Pagina principale con il modulo di registrazione
@app.route('/', methods=['GET', 'POST'])
def secret_santa():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Verifica se l'email o il nome esistono già nella lista dei partecipanti
        for participant in participants:
            if name == participant['name'] or email == participant['email']:
                return "Nome o email già registrati. Riprova."

        participants.append({'name': name, 'email': email})

    return render_template('registration.html', participants=participants)

# Pagina per il sorteggio e l'invio delle email
@app.route('/draw')
def draw_secret_santa():
    if len(participants) < 2:
        return "Devi avere almeno due partecipanti per il sorteggio."

    random.shuffle(participants)
    for i in range(len(participants)):
        giver = participants[i]
        receiver = participants[(i + 1) % len(participants)]  # Evita l'auto-assegnazione

        # Invia email con il destinatario segreto
        send_email(giver['name'], giver['email'], receiver['name'])

    return "Il sorteggio è stato effettuato e le email sono state inviate."

def send_email(sender_name, sender_email, receiver_name):
    # Configura il server SMTP e invia l'email
    # Assicurati di inserire le tue informazioni SMTP reali qui
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = 'your_email@example.com'
    smtp_password = 'your_password'

    message = MIMEText(f"Ciao {sender_name}! Il tuo destinatario segreto è {receiver_name}. Buon Natale!")
    message['From'] = sender_email
    message['To'] = sender_email
    message['Subject'] = 'Il tuo Destinatario Segreto'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, sender_email, message.as_string())

if __name__ == '__main__':
    app.run(debug=True)
