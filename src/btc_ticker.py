import requests
import time

def get_btc_price():
    """
    Récupère le prix actuel du Bitcoin en USD depuis CoinGecko API.
    
    Returns:
        float: Prix du BTC en USD si succès
        None: Si échec avec message d'erreur affiché
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    
    try:
        # Requête avec timeout de 10 secondes
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Lève une exception pour les codes 4xx/5xx
        
        data = response.json()
        
        # Validation de la structure de la réponse
        if "bitcoin" not in data:
            print("Erreur: Clé 'bitcoin' manquante dans la réponse")
            return None
            
        bitcoin_data = data["bitcoin"]
        
        if "usd" not in bitcoin_data:
            print("Erreur: Clé 'usd' manquante dans la réponse")
            return None
            
        price = bitcoin_data["usd"]
        
        # Validation que le prix est un nombre valide
        if not isinstance(price, (int, float)):
            print("Erreur: Le prix n'est pas un nombre valide")
            return None
            
        price_float = float(price)
        
        # Validation supplémentaire (prix réaliste)
        if price_float <= 0 or price_float > 1000000:  # Plausibilité
            print(f"Erreur: Prix {price_float} USD peu réaliste")
            return None
            
        return price_float
        
    except requests.exceptions.Timeout:
        print("Erreur: Timeout de la requête (10 secondes)")
        return None
    except requests.exceptions.ConnectionError:
        print("Erreur: Problème de connexion internet")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP {e.response.status_code}: {e.response.reason}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête: {e}")
        return None
    except ValueError as e:
        print(f"Erreur de conversion: {e}")
        return None
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return None

def main():
    try:
        while True:
            prix = get_btc_price()
            if prix is not None:
                print(f"Prix actuel: ${prix:.2f} USD")
            time.sleep(120)
    except KeyboardInterrupt:
        print("\nProgramme arrêté par l'utilisateur")

if __name__ == "__main__":
    main()