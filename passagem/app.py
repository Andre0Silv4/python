from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Credenciais da Amadeus API
API_KEY = "G3KhjckWskA035zpqgMGZ3kFy4QRpoJM"
API_SECRET = "4On5VWFkbUYLO3Tk"  # Substitua pelo seu segredo da API

# URLs da Amadeus API
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_OFFERS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

def get_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': API_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    token = response.json().get('access_token')
    return token

def fetch_flight_data(origin, destination, date):
    token = get_access_token()
    if not token:
        return None, "Failed to get access token"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1,
        "max": 5
    }
    response = requests.get(FLIGHT_OFFERS_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json(), None
    else:
        return None, response.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')

    data, error = fetch_flight_data(origin, destination, date)

    if error:
        return jsonify({"error": error}), 500

    # Removido o print para evitar dados desnecessários no terminal
    # print(data)

    # Obter o dicionário de transportadoras
    carriers = data.get('dictionaries', {}).get('carriers', {})

    results = []
    if "data" in data:
        for flight in data["data"]:
            for segment in flight["itineraries"][0]["segments"]:
                carrier_code = segment.get("carrierCode", "Desconhecido")
                agency_name = carriers.get(carrier_code, "Desconhecido")
                flight_number = segment.get("carrierCode", "") + segment.get("number", "")
                results.append({
                    "agency": agency_name,
                    "price": flight["price"].get("total", "Desconhecido"),
                    "flight_number": flight_number
                })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
