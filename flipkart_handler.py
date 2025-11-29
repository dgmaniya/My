import requests
import streamlit as st
import json
import os
import time

# Constants
TOKEN_FILE = "auth_token.json"
AUTH_URL = "https://api.flipkart.net/oauth-service/oauth/token"

def get_saved_token():
    """
    Saved file se token read karta hai.
    """
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                return data.get("access_token")
        except Exception as e:
            return None
    return None

def generate_and_save_token():
    """
    Flipkart API se naya token mangwata hai aur file me save karta hai.
    """
    try:
        # 1. Secrets se ID/Pass lena
        app_id = st.secrets["flipkart"]["app_id"]
        app_secret = st.secrets["flipkart"]["app_secret"]
        
        # 2. API Call lagana
        response = requests.get(
            AUTH_URL, 
            params={"grant_type": "client_credentials", "scope": "Seller_Api"},
            auth=(app_id, app_secret),
            timeout=10
        )
        
        # 3. Agar success ho to save karna
        if response.status_code == 200:
            token_data = response.json()
            
            # Save to JSON file
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_data, f)
            
            return token_data.get("access_token")
        else:
            st.error(f"Failed to generate token: {response.text}")
            return None

    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None