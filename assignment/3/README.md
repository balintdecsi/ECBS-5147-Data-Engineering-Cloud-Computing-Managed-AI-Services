# Comparative Sentiment Analysis: M1 Híradó vs. BBC News

**Course:** Data Engineering 1: Cloud Computing and Managed AI Services  
**Group:** Alina Imanakhunova (2508355) and Bálint Décsi (2506626).

## 📌 Overview

This project investigates whether sentiment differs between two comparable news sources — **M1 Híradó** (Hungary’s official public broadcaster) and **BBC News** (the UK’s official public service broadcaster) — when reporting on the same topic: **gas sanctions affecting Hungary**.

For a detailed analysis of the results, visualizations, and interpretation, please read our **[Medium Article](https://medium.com/@imanakhunova.a/680f847d9bb1)**.

## 🚀 How to Run

### Prerequisites
*   Python 3.x
*   AWS Credentials configured (e.g., in `~/.aws/credentials`) with access to S3, Transcribe, Translate, and Comprehend.
*   We used poetry for package dependency management. Required Python packages:
    ```bash
    poetry add boto3 matplotlib wordcloud tabulate numpy
    ```

### Execution
1.  Place your `.mp3` files in `data/raw/` (e.g., `british.mp3`, `hungarian.mp3`).
2.  Run the main pipeline:
    ```bash
    python3 main.py
    ```

The script will:
1.  Upload files to S3.
2.  Transcribe them.
3.  Download transcripts to `data/transcribed/`.
4.  Analyze sentiment (saving results to `data/sentiment/`).
5.  Generate charts in `data/visualizations/`.
6.  Print a cost estimate to `data/cost_estimate.txt`.

### Architecture

The solution is implemented in Python using the `boto3` SDK.

*   `src/transcribe_audio.py`: Handles S3 uploads and Transcribe jobs.
*   `src/analyze_sentiment.py`: Orchestrates translation (if needed) and sentiment analysis.
*   `src/visualize_results.py`: Generates bar charts and word clouds.
*   `src/estimate_costs.py`: Calculates the estimated AWS costs for the run.
*   `main.py`: Runs the full end-to-end pipeline.

## 📝 Methodology & Data Sources

We analyzed audio extracted from YouTube news reports from **M1 Híradó** (Hungarian) and **BBC News** (British).

The pipeline:
1.  **Data Acquisition**: Audio extracted from YouTube.
2.  **Storage**: Upload to **Amazon S3**.
3.  **Transcription**: **Amazon Transcribe** (Speech-to-Text).
4.  **Translation**: **Amazon Translate** (Hungarian -> English).
5.  **Analysis**: **Amazon Comprehend** (Sentiment Analysis).
6.  **Visualization**: Python libraries (`matplotlib`, `wordcloud`).

## 🔎 Research Results Summary

*   **Hungarian News (M1)**: Overwhelmingly neutral (89%), suggesting a formal, factual tone.
*   **British News (BBC)**: Mostly neutral (71%) but with more emotional variation (higher negative/mixed scores), suggesting a more analytical framing.

*Full interpretation and visualizations are available in the [Medium Article](https://medium.com/@imanakhunova.a/680f847d9bb1).*

## 💰 Cost Breakdown

Below is the estimated cost for running this analysis in the **eu-west-1** region.

```text
AWS Cost Estimate
=================

Service              Usage Metric         Quantity        Rate (EU-West-1)     Est. Cost ($)  
------------------------------------------------------------------------------------------
Amazon Transcribe    Audio Duration (min) 13.93           $0.024/min           $0.3343        
Amazon Translate     Characters           4067            $15.00/1M chars      $0.061005      
Amazon Comprehend    Units (100 chars)    88              $0.0001/unit         $0.0088        
Amazon S3            Storage              Negligible      $0.023/GB            < $0.01        
---------------      ---------------      ----------      ---------------      ----------     
TOTAL                                                                          $0.4041        
```

*Note: These are estimates based on public pricing. Actual costs may vary.*
