import boto3
import os
import json
import pprint
from .translate2en import translate_to_english

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
TRANSCRIBED_DIR = os.path.join(DATA_DIR, 'transcribed')
SENTIMENT_DIR = os.path.join(DATA_DIR, 'sentiment')

# Ensure output directory exists
os.makedirs(SENTIMENT_DIR, exist_ok=True)

# AWS Clients
REGION = 'eu-west-1'
comprehend = boto3.client('comprehend', region_name=REGION)

pp = pprint.PrettyPrinter(indent=2)

def get_language_code(filename):
    """Map filename to language code"""
    name = os.path.splitext(filename)[0].lower()
    if 'british' in name:
        return 'en'
    elif 'hungarian' in name:
        return 'hu'
    else:
        return 'en' # Default

def analyze_file(filename):
    print(f"\n🔍 Processing {filename}...")
    
    file_path = os.path.join(TRANSCRIBED_DIR, filename)
    
    try:
        with open(file_path, 'r') as f:
            text = f.read()
            
        if not text:
            print("   ⚠️  File is empty, skipping.")
            return

        original_lang = get_language_code(filename)
        print(f"   📝 Original Language: {original_lang}")
        
        text_to_analyze = text
        
        # Translate if not English (Comprehend works best with English, though it supports others, 
        # but for this assignment we might want to standardize or handle the Hungarian case explicitly)
        # Actually Comprehend supports: en, es, fr, de, it, pt, ar, hi, ja, ko, zh, zh-TW.
        # Hungarian (hu) is NOT supported for Sentiment Analysis.
        
        if original_lang == 'hu':
            print("   🔄 Translating Hungarian to English for sentiment analysis...")
            try:
                text_to_analyze = translate_to_english(text, 'hu')
                print("   ✅ Translation complete")
                # print(f"   Translated text: {text_to_analyze[:100]}...")
            except Exception as e:
                print(f"   ❌ Translation failed: {e}")
                return

        # Analyze Sentiment
        print("   🧠 Analyzing sentiment...")
        sentiment_response = comprehend.detect_sentiment(
            Text=text_to_analyze,
            LanguageCode='en' # We are analyzing the English text (either original or translated)
        )
        
        sentiment = sentiment_response['Sentiment']
        scores = sentiment_response['SentimentScore']
        
        print(f"   ✨ Sentiment: {sentiment}")
        print("   📊 Scores:")
        for k, v in scores.items():
            print(f"      - {k}: {v:.4f}")
            
        # Save results
        result = {
            'filename': filename,
            'original_text': text,
            'analyzed_text': text_to_analyze,
            'original_language': original_lang,
            'sentiment': sentiment,
            'scores': scores
        }
        
        output_filename = os.path.splitext(filename)[0] + "_sentiment.json"
        output_path = os.path.join(SENTIMENT_DIR, output_filename)
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
            
        print(f"   💾 Saved result to {output_path}")

    except Exception as e:
        print(f"   ❌ Error processing {filename}: {e}")

def main():
    print("🚀 Starting Sentiment Analysis")
    
    if not os.path.exists(TRANSCRIBED_DIR):
        print(f"❌ Transcribed directory not found: {TRANSCRIBED_DIR}")
        return

    files = [f for f in os.listdir(TRANSCRIBED_DIR) if f.endswith('.txt')]
    
    if not files:
        print("⚠️  No transcribed files found.")
        return
        
    for file in files:
        analyze_file(file)
        
    print("\n✨ Analysis completed!")

if __name__ == "__main__":
    main()
