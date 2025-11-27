"""
Simple script to test OpenAI API connection.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

def test_api_connection():
    """Test the OpenAI API connection."""
    print("=" * 60)
    print("Testing OpenAI API Connection")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Check if API key exists
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in environment variables")
        return False
    
    print(f"✓ API Key found: {api_key[:20]}...")
    print(f"✓ Model: {model}")
    print()
    
    # Try to connect to OpenAI
    try:
        print("Attempting to connect to OpenAI API...")
        client = OpenAI(api_key=api_key)
        
        # Make a simple test request
        print("Sending test request...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello from Oman!' in one sentence."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        result = response.choices[0].message.content.strip()
        
        print()
        print("=" * 60)
        print("✅ SUCCESS! API Connection Verified")
        print("=" * 60)
        print(f"Response from {model}:")
        print(f"  {result}")
        print()
        print(f"Model used: {response.model}")
        print(f"Tokens used: {response.usage.total_tokens}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR: Failed to connect to OpenAI API")
        print("=" * 60)
        print(f"Error message: {str(e)}")
        print()
        print("Possible causes:")
        print("  1. Invalid API key")
        print("  2. API key doesn't have access to the specified model")
        print("  3. Network connection issues")
        print("  4. OpenAI service temporarily unavailable")
        print("=" * 60)
        
        return False

if __name__ == "__main__":
    test_api_connection()
