import os
import json
from tabulate import tabulate

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
TRANSCRIBED_DIR = os.path.join(DATA_DIR, 'transcribed')
SENTIMENT_DIR = os.path.join(DATA_DIR, 'sentiment')
RAW_DIR = os.path.join(DATA_DIR, 'raw')

# Pricing Constants (EU-West-1, approx as of late 2024)
PRICING = {
    'Transcribe': {'rate': 0.024, 'unit': 'minute', 'note': 'Standard batch transcription'},
    'Translate': {'rate': 15.00 / 1000000, 'unit': 'character', 'note': 'Standard translation'},
    'Comprehend': {'rate': 0.0001, 'unit': 'unit (100 chars)', 'note': 'Sentiment Analysis (min 3 units)'},
    'S3': {'rate': 0.023, 'unit': 'GB/month', 'note': 'Standard storage (negligible here)'}
}

def estimate_transcribe_cost():
    # Try to find duration from raw files or transcribed json
    # Since we can't easily read mp3 duration without libs, we'll estimate based on file size
    # Approx 1MB = 1 min for 128kbps mp3.
    
    total_minutes = 0
    if os.path.exists(RAW_DIR):
        for f in os.listdir(RAW_DIR):
            if f.endswith('.mp3'):
                size_bytes = os.path.getsize(os.path.join(RAW_DIR, f))
                # Estimate: 128kbps = 16KB/s. 
                # Duration (s) = size / 16384
                seconds = size_bytes / (128 * 1024 / 8)
                # AWS bills per second, min 15s? Actually Transcribe is per second, min 15s.
                # Let's just convert to minutes.
                minutes = max(seconds, 15) / 60
                total_minutes += minutes
    
    cost = total_minutes * PRICING['Transcribe']['rate']
    return cost, total_minutes

def estimate_translate_cost():
    # Check sentiment files to see what was translated
    total_chars = 0
    if os.path.exists(SENTIMENT_DIR):
        for f in os.listdir(SENTIMENT_DIR):
            if f.endswith('.json'):
                with open(os.path.join(SENTIMENT_DIR, f), 'r') as json_file:
                    data = json.load(json_file)
                    # If original language was not en, we translated it
                    if data.get('original_language') != 'en':
                        # Translate charges based on source characters
                        total_chars += len(data.get('original_text', ''))
    
    cost = total_chars * PRICING['Translate']['rate']
    return cost, total_chars

def estimate_comprehend_cost():
    # Check sentiment files for analyzed text length
    total_units = 0
    if os.path.exists(SENTIMENT_DIR):
        for f in os.listdir(SENTIMENT_DIR):
            if f.endswith('.json'):
                with open(os.path.join(SENTIMENT_DIR, f), 'r') as json_file:
                    data = json.load(json_file)
                    text = data.get('analyzed_text', '')
                    chars = len(text)
                    # 1 unit = 100 chars, min 3 units
                    units = max(3, (chars + 99) // 100)
                    total_units += units
    
    cost = total_units * PRICING['Comprehend']['rate']
    return cost, total_units

def main():
    print("💰 Estimating AWS Costs")
    print("=" * 60)

    transcribe_cost, duration = estimate_transcribe_cost()
    translate_cost, trans_chars = estimate_translate_cost()
    comprehend_cost, comp_units = estimate_comprehend_cost()
    
    # S3 is negligible for this assignment, assume < $0.01
    s3_cost = 0.00001 

    total_cost = transcribe_cost + translate_cost + comprehend_cost + s3_cost

    # Create Table
    headers = ["Service", "Usage Metric", "Quantity", "Rate (EU-West-1)", "Est. Cost ($)"]
    rows = [
        ["Amazon Transcribe", "Audio Duration (min)", f"{duration:.2f}", f"${PRICING['Transcribe']['rate']}/min", f"${transcribe_cost:.4f}"],
        ["Amazon Translate", "Characters", f"{trans_chars}", f"${PRICING['Translate']['rate']*1000000:.2f}/1M chars", f"${translate_cost:.6f}"],
        ["Amazon Comprehend", "Units (100 chars)", f"{comp_units}", f"${PRICING['Comprehend']['rate']}/unit", f"${comprehend_cost:.4f}"],
        ["Amazon S3", "Storage", "Negligible", f"${PRICING['S3']['rate']}/GB", f"< $0.01"],
        ["-"*15, "-"*15, "-"*10, "-"*15, "-"*10],
        ["TOTAL", "", "", "", f"${total_cost:.4f}"]
    ]

    # Formatting
    col_widths = [20, 20, 15, 20, 15]
    
    def print_row(row):
        print("".join(str(x).ljust(w) for x, w in zip(row, col_widths)))

    print_row(headers)
    print("-" * sum(col_widths))
    for row in rows:
        print_row(row)
    
    print("=" * sum(col_widths))
    print("\n📝 Pricing Sources:")
    print("- Transcribe: https://aws.amazon.com/transcribe/pricing/")
    print("- Translate: https://aws.amazon.com/translate/pricing/")
    print("- Comprehend: https://aws.amazon.com/comprehend/pricing/")
    print("- S3: https://aws.amazon.com/s3/pricing/")
    print("\n⚠️  Note: These are estimates based on public pricing in eu-west-1.")
    print("   Actual costs may vary due to free tier, taxes, or minimum charges.")

    # Save to file
    output_path = os.path.join(DATA_DIR, 'cost_estimate.txt')
    with open(output_path, 'w') as f:
        # Redirect stdout to file temporarily or just reconstruct string
        # Simple reconstruction for file
        f.write("AWS Cost Estimate\n")
        f.write("=================\n\n")
        line_format = "{:<20} {:<20} {:<15} {:<20} {:<15}\n"
        f.write(line_format.format(*headers))
        f.write("-" * 90 + "\n")
        for row in rows:
            f.write(line_format.format(*row))
        f.write("\nSources:\n")
        f.write("- Transcribe: https://aws.amazon.com/transcribe/pricing/\n")
        f.write("- Translate: https://aws.amazon.com/translate/pricing/\n")
        f.write("- Comprehend: https://aws.amazon.com/comprehend/pricing/\n")
    
    print(f"\n💾 Saved cost estimate to {output_path}")

if __name__ == "__main__":
    main()
