# Football Match Outcome Prediction & Betting Strategy Analysis

## Overview
This project is a comprehensive, end-to-end data science pipeline focused on predicting the probability of home team victories in English Premier League football matches. The prediction model leverages recent performance metrics of teams, including rolling averages of goals, win ratios, and other historical statistics. Built as a self-initiated portfolio project, it demonstrates advanced skills in data engineering, exploratory data analysis, machine learning, and high-performance computing. The workflow covers everything from raw data acquisition and feature engineering to predictive modeling, cluster analysis, and simulation of real-world betting strategies—both locally and at scale using Databricks and Apache Spark.

## Key Features
- **Automated Data Collection:** Aggregates and cleans over a decade of EPL match data from public sources.
- **Advanced Feature Engineering:** 
  - Calculates rolling performance metrics for home teams (win ratios, goal stats, form indicators)
  - Computes historical head-to-head statistics
  - Processes bookmaker-implied probabilities
- **Exploratory Data Analysis:** Visualizes home team performance distributions, correlations between metrics, and winning trends; applies PCA for dimensionality reduction.
- **Unsupervised Learning:** Uses K-means clustering on PCA components to uncover patterns in home team performance.
- **Predictive Modeling:** Trains and compares multiple ML models (Random Forest, SVM, KNN, Logistic Regression, Neural Network) specifically to predict home team win probability.
- **Model Evaluation:** Benchmarks models using cross-validation and ROC/AUC, comparing predicted home win probabilities against bookmaker odds.
- **Betting Strategy Simulation:** Simulates and analyzes profits/ROI for model-driven betting strategies focused on home team victories.
- **Scalable Computing:** Implements the full pipeline on Databricks with Apache Spark for distributed, high-performance analysis.

## Tech Stack
- **Languages:** Python
- **Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, openpyxl
- **Machine Learning:** scikit-learn, Spark MLlib, MLPClassifier (Neural Network)
- **Distributed Computing:** Apache Spark, Databricks
- **Data Sources:** football-data.co.uk (public football datasets)

The project showcases expertise in the full data science lifecycle, from raw data wrangling to actionable business insights and scalable machine learning.

## How It Works
1. **Data Preparation:**
   - Downloads and merges multiple seasons of EPL data.
   - Cleans and standardizes features, computes rolling stats, and derives bookmaker-implied probabilities.
   - Outputs a feature-rich dataset for analysis and modeling.

2. **Exploratory Data Analysis (EDA):**
   - Visualizes key statistics and relationships.
   - Applies PCA to reduce feature space and reveal underlying patterns.
   - Clusters matches/teams using K-means to identify performance archetypes.

3. **Predictive Modeling:**
   - Selects principal components and engineered features as model inputs.
   - Trains and cross-validates several ML models to predict home team wins.
   - Evaluates models using accuracy, precision, recall, F1, and ROC/AUC metrics.
   - Compares model predictions to bookmaker odds for real-world relevance.

4. **Betting Strategy Simulation:**
   - Simulates betting based on model confidence vs. bookmaker implied probability.
   - Benchmarks model-driven strategies against random and bookmaker-based approaches.
   - Analyzes profit, ROI, and risk across strategies.

5. **High-Performance & Scalable Analysis:**
   - Re-implements the pipeline on Databricks using Apache Spark for distributed data processing and model training.
   - Enables scalable experimentation with large datasets and parallelized ML workflows.

---