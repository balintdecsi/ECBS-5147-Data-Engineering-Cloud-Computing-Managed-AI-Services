import os
import sys

# Ensure we can import modules from the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src import transcribe_audio
from src import analyze_sentiment
from src import visualize_results
from src import estimate_costs

def main():
    print("🚀 Starting End-to-End Processing Pipeline")
    print("=" * 50)

    # Check for raw data
    raw_dir = os.path.join(current_dir, 'data', 'raw')
    if not os.path.exists(raw_dir):
        print(f"❌ Error: Raw data directory not found at {raw_dir}")
        print("Please ensure 'data/raw' exists and contains .mp3 files.")
        return

    # Step 1: Transcribe
    print("\n[Step 1/4] Transcribing Audio Files...")
    try:
        transcribe_audio.main()
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return

    print("\n" + "-" * 50)

    # Step 2: Analyze Sentiment
    print("\n[Step 2/4] Analyzing Sentiment...")
    try:
        analyze_sentiment.main()
    except Exception as e:
        print(f"❌ Sentiment analysis failed: {e}")
        return

    print("\n" + "-" * 50)

    # Step 3: Visualize
    print("\n[Step 3/4] Visualizing Results...")
    try:
        visualize_results.main()
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
        return

    print("\n" + "-" * 50)

    # Step 4: Estimate Costs
    print("\n[Step 4/4] Estimating Costs...")
    try:
        estimate_costs.main()
    except Exception as e:
        print(f"❌ Cost estimation failed: {e}")
        return

    print("\n" + "=" * 50)
    print("✨ Pipeline execution completed successfully!")

if __name__ == "__main__":
    main()
