"""
Quick setup script for Rainforest API
"""

import os

def setup_rainforest_api():
    """Set up Rainforest API key."""
    print("🌧️ Setting up Rainforest API for product images...")
    print()
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("✅ .env file already exists")
    else:
        print("📝 Creating .env file from template...")
        with open('env.example', 'r') as src:
            with open('.env', 'w') as dst:
                dst.write(src.read())
        print("✅ .env file created")
    
    print()
    print("🔑 Next steps:")
    print("1. Open the .env file")
    print("2. Replace 'your_rainforest_api_key_here' with your actual API key")
    print("3. Your API key is: 967A30D6573646428C3C29138EEF131B")
    print()
    print("🧪 Test the setup:")
    print("python -c \"from rainforest_api import RainforestAPI; api = RainforestAPI(); print(api.get_product_image('B09JQMJHXY'))\"")
    print()
    print("🚀 Then restart your Streamlit app to see real product images!")

if __name__ == "__main__":
    setup_rainforest_api()
