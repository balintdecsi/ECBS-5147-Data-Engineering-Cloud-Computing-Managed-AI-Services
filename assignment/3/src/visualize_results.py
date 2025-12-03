import os
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
SENTIMENT_DIR = os.path.join(DATA_DIR, 'sentiment')
VISUALIZATION_DIR = os.path.join(DATA_DIR, 'visualizations')

# Ensure output directory exists
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

def load_sentiment_data():
    data = []
    if not os.path.exists(SENTIMENT_DIR):
        print(f"❌ Sentiment directory not found: {SENTIMENT_DIR}")
        return data

    files = [f for f in os.listdir(SENTIMENT_DIR) if f.endswith('.json')]
    for file in files:
        with open(os.path.join(SENTIMENT_DIR, file), 'r') as f:
            data.append(json.load(f))
    return data

def create_sentiment_chart(data):
    if not data:
        return

    filenames = [d['filename'].replace('.txt', '') for d in data]
    sentiments = ['Positive', 'Negative', 'Neutral', 'Mixed']
    
    # Prepare data for plotting
    scores_data = {s: [] for s in sentiments}
    for d in data:
        for s in sentiments:
            scores_data[s].append(d['scores'][s])

    x = np.arange(len(filenames))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, sentiment in enumerate(sentiments):
        offset = width * i
        # Use x + offset for bar positions
        ax.bar(x + offset, scores_data[sentiment], width, label=sentiment)

    ax.set_ylabel('Score')
    ax.set_title('Sentiment Analysis Scores by File')
    # Center ticks
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(filenames)
    ax.legend()

    output_path = os.path.join(VISUALIZATION_DIR, 'sentiment_chart.png')
    plt.savefig(output_path)
    plt.close()
    print(f"📊 Saved sentiment chart to {output_path}")

def create_wordclouds(data):
    if not data:
        return

    for d in data:
        text = d['analyzed_text']
        filename = d['filename'].replace('.txt', '')
        
        print(f"   Generating word cloud for {filename}...")
        # Generate word cloud
        try:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title(f"Word Cloud - {filename}")
            
            output_path = os.path.join(VISUALIZATION_DIR, f'{filename}_wordcloud.png')
            plt.savefig(output_path)
            plt.close()
            print(f"☁️  Saved word cloud to {output_path}")
        except Exception as e:
            print(f"❌ Error generating word cloud for {filename}: {e}")

def main():
    print("🎨 Starting Visualization Process")
    
    data = load_sentiment_data()
    if not data:
        print("⚠️  No sentiment data found to visualize.")
        return

    create_sentiment_chart(data)
    create_wordclouds(data)
    
    print("\n✨ Visualization completed!")

if __name__ == "__main__":
    main()
