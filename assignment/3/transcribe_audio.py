import boto3
import os
import time
import json
import random
import string

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
TRANSCRIBED_DIR = os.path.join(DATA_DIR, 'transcribed')

# Ensure output directory exists
os.makedirs(TRANSCRIBED_DIR, exist_ok=True)

# AWS Clients
# MAke sure to use eu-west-1
REGION = 'eu-west-1'
s3 = boto3.client('s3', region_name=REGION)
transcribe = boto3.client('transcribe', region_name=REGION)

# Set bucket name
BUCKET_NAME = "ceu-balint-2025"

def upload_files():
    """Upload audio files from raw directory to S3"""
    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.mp3')]
    uploaded_files = []
    
    for file in files:
        file_path = os.path.join(RAW_DIR, file)
        print(f"⬆️  Uploading {file} to {BUCKET_NAME}...")
        try:
            s3.upload_file(file_path, BUCKET_NAME, file)
            uploaded_files.append(file)
            print(f"✅ Uploaded {file}")
        except Exception as e:
            print(f"❌ Error uploading {file}: {e}")
            
    return uploaded_files

def get_language_code(filename):
    """Map filename to AWS Transcribe language code"""
    name = os.path.splitext(filename)[0].lower()
    if 'british' in name:
        return 'en-GB'
    elif 'hungarian' in name:
        return 'hu-HU'
    else:
        # Default or error? Let's default to US English or raise error
        print(f"⚠️  Unknown language for {filename}, defaulting to en-US")
        return 'en-US'

def transcribe_file(filename):
    """Start a transcription job for a file"""
    # Create a unique job name
    job_name = f"transcribe-{os.path.splitext(filename)[0]}-{int(time.time())}"
    file_uri = f"s3://{BUCKET_NAME}/{filename}"
    language_code = get_language_code(filename)
    
    print(f"🎙️  Starting transcription job for {filename} (Language: {language_code})...")
    
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat='mp3',
            LanguageCode=language_code,
            OutputBucketName=BUCKET_NAME
        )
        return job_name
    except Exception as e:
        print(f"❌ Error starting transcription job: {e}")
        return None

def get_transcript(job_name):
    """Wait for job completion and retrieve transcript"""
    print(f"⏳ Waiting for job {job_name} to complete...")
    
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        
        if job_status in ['COMPLETED', 'FAILED']:
            break
        
        print(f"   Status: {job_status} - Waiting 5s...")
        time.sleep(5)
    
    if job_status == 'COMPLETED':
        print(f"✅ Job {job_name} completed!")
        
        # The result file key in S3
        result_key = f"{job_name}.json"
        local_json_path = os.path.join(TRANSCRIBED_DIR, result_key)
        
        # Download the JSON result
        try:
            s3.download_file(BUCKET_NAME, result_key, local_json_path)
            
            # Parse JSON to get the text
            with open(local_json_path, 'r') as f:
                data = json.load(f)
                
            transcript_text = data['results']['transcripts'][0]['transcript']
            return transcript_text
        except Exception as e:
            print(f"❌ Error retrieving result: {e}")
            return None
    else:
        print(f"❌ Job {job_name} failed")
        return None

if __name__ == "__main__":
    print("🚀 Starting Transcription Process")

    # 2. Upload Files
    files = upload_files()
    
    # 3. Start Transcription Jobs
    jobs = {}
    for file in files:
        job_name = transcribe_file(file)
        if job_name:
            jobs[file] = job_name
    
    # 4. Wait for results and save
    for file, job_name in jobs.items():
        transcript = get_transcript(job_name)
        if transcript:
            output_filename = os.path.splitext(file)[0] + ".txt"
            output_path = os.path.join(TRANSCRIBED_DIR, output_filename)
            
            with open(output_path, 'w') as f:
                f.write(transcript)
            
            print(f"📝 Transcript saved to: {output_path}")
            print("-" * 40)
            print(transcript[:200] + "..." if len(transcript) > 200 else transcript)
            print("-" * 40)

    print("\n✨ Process completed!")
    print(f"ℹ️  Resources (Bucket {BUCKET_NAME}) were NOT deleted. Please delete them manually if needed.")
