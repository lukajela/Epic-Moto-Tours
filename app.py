from flask import Flask, render_template, request, redirect
from mailjet_rest import Client
from dotenv import load_dotenv
import os

# Naloži okoljske spremenljivke iz .env
load_dotenv()

app = Flask(__name__)

# Nastavi Mailjet Client
mailjet = Client(
    auth=(
        os.getenv("MAILJET_API_KEY"),
        os.getenv("MAILJET_SECRET_KEY")
    ),
    version='v3.1'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ture')
def ture():
    return render_template('ture.html')

@app.route('/prijava', methods=['GET', 'POST'])
def prijava():
    if request.method == 'POST':
        ime = request.form['ime']
        email = request.form['email']
        telefon = request.form['telefon']
        tura = request.form['tura']

        html_sporocilo = render_template('email_prijava.html', ime=ime, email=email, telefon=telefon, tura=tura)
        potrdilo_html = render_template('email_potrditev.html', ime=ime, tura=tura)

        data = {
            'Messages': [
                {
                    "From": {"Email": "mototoursepic@gmail.com", "Name": "Epic Moto Tours"},
                    "To": [{"Email": "mototoursepic@gmail.com", "Name": "Epic Moto Tours"}],
                    "Subject": "Nova prijava na turo",
                    "HTMLPart": html_sporocilo
                },
                {
                    "From": {"Email": "mototoursepic@gmail.com", "Name": "Epic Moto Tours"},
                    "To": [{"Email": email, "Name": ime}],
                    "Subject": "Hvala za prijavo!",
                    "HTMLPart": potrdilo_html
                }
            ]
        }

        mailjet.send.create(data=data)
        return redirect('/')
    return render_template('prijava.html')

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    if request.method == 'POST':
        ime = request.form['ime']
        email = request.form['email']
        sporocilo = request.form['sporocilo']

        html_kontakt = render_template('email_kontakt.html', ime=ime, email=email, sporocilo=sporocilo)

        data = {
            'Messages': [
                {
                    "From": {"Email": "mototoursepic@gmail.com", "Name": "Epic Moto Tours"},
                    "To": [{"Email": "mototoursepic@gmail.com"}],
                    "Subject": f"Novo sporočilo od {ime}",
                    "HTMLPart": html_kontakt
                }
            ]
        }

        mailjet.send.create(data=data)
        return redirect('/kontakt')
    return render_template('kontakt.html')

if __name__ == '__main__':
    app.run(debug=True)
