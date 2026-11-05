# AtmoSync: Micro-Climate Arbitrage Analytics

## Project Overview

AtmoSync is a Python-based weather analytics dashboard developed using Streamlit. It provides interactive visualizations, location-wise weather comparisons, and live weather information for Indian cities.

The project aims to make micro-climate data easier to explore, compare, and understand.

## Key Features

- Interactive weather analytics dashboard
- Temperature and humidity visualizations
- Location-wise weather comparison
- Temperature heatmap
- Average temperature and humidity metrics
- Live weather search for Indian cities
- Real-time comparison of two locations
- Downloadable weather dataset in CSV format

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- Requests
- Open-Meteo API
- GitHub

## Project Structure

```text
AtmoSync-Micro-Climate-Analytics/
├── data/
│   ├── raw/
│   │   └── extracted_data.csv
│   └── processed/
│       └── Cleaned_Weather_Data.csv
├── notebooks/
├── src/
│   └── app.py
├── visualizations/
├── reports/
├── presentation/
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone the GitHub repository.
2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:

```bash
streamlit run src/app.py
```

4. Open the local URL displayed in the terminal.

## Data Sources

- Weather datasets collected and processed during the project
- Open-Meteo API for live weather information

## Live Dashboard
https://atmosync-micro-climate-analytics-scb9dwyed2myhtwu3tpb7x.streamlit.app/?utm_source=chatgpt.com

The AtmoSync dashboard is deployed using Streamlit Community Cloud.

## Future Improvements

- Historical weather trend analysis
- Weather forecasting
- Additional geographical visualizations
- Advanced micro-climate insights

## Project Type

Internship Project — Weather Data Analytics and Visualization
