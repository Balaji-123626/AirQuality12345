<div align="center">
  <h1>🌍 AI-Powered Real-Time Air Quality Intelligence System</h1>
  <p><b>Real-time Monitoring • Predictive Forecasting • Smart Health Analytics</b></p>
</div>

---

## 📖 Overview

The **AI-Powered Real-Time Air Quality Intelligence System** is a state-of-the-art environmental dashboard. It seamlessly integrates real-time API data, advanced Machine Learning forecasting, and a rule-based intelligence engine into a premium, highly interactive user interface. 

The system transforms raw environmental data into actionable intelligence, alerting users to dangerous pollution levels, forecasting future trends, and providing dynamic health recommendations—all without the need for paid LLM APIs or external chat dependencies.

---

## ✨ Core Features

1. **Live Environmental Telemetry**
   - Fetches live AQI, temperature, humidity, wind speed, PM2.5, PM10, and CO levels using the **OpenWeather Air Pollution API**.
   - Displays metrics in custom glassmorphism cards with neon highlights.

2. **Predictive Forecasting Engine (Prophet ML)**
   - Utilizes Facebook's **Prophet** algorithm to analyze historical environmental data (`AirQualityUCI.csv`).
   - Generates a highly accurate 24-hour forecast of CO(GT) pollution levels.
   - Outputs an interactive Plotly chart with upper and lower confidence intervals.

3. **Smart AQI Assistant (Offline Rule-Based Engine)**
   - A highly reliable, offline conversational interface that simulates an AI.
   - Detects keywords (e.g., "safe", "jogging", "asthma") to provide instant, dynamic health recommendations based on live AQI and forecast data.
   - Includes simulated typing animations and chat bubbles for a premium user experience.

4. **Emergency Broadcast System**
   - Integrated with **Twilio API** for immediate crisis management.
   - Allows users to broadcast SMS/WhatsApp emergency alerts regarding dangerous AQI levels directly from the dashboard to predefined contacts.

5. **Premium UI/UX Design**
   - Built exclusively with **Streamlit** using heavily customized HTML/CSS injections.
   - Features a dark futuristic theme, neon gradients, glassmorphism containers, smooth hover animations, and custom styling that overrides default Streamlit components.

---

## 🏗️ Project Architecture

```text
AirQualityPrediction/
│
├── app.py                      # Main Streamlit dashboard and UI orchestration
├── AirQualityUCI.csv           # Historical dataset for Prophet ML training
├── .env                        # Secure environment variables (API keys)
├── requirements.txt            # Python dependencies
│
├── api/
│   └── openweather.py          # Handles live data fetching from OpenWeather API
│
├── model/
│   └── model.py                # Contains Facebook Prophet ML training & forecasting logic
│
├── alerts/
│   └── whatsapp.py             # Twilio integration for SMS/WhatsApp emergency alerts
│
└── utils/
    ├── intelligence.py         # Smart Assistant rule engine & trend calculation logic
    └── ui_helpers.py           # Custom CSS styling, glassmorphism, and HTML components
```

---

## 📸 Dashboard Previews

*(Add your screenshots here)*

- **Hero & Live Metrics:** `![Metrics](assets/metrics.png)`
- **Prophet ML Analytics:** `![Analytics](assets/analytics.png)`
- **Smart AQI Assistant:** `![Assistant](assets/assistant.png)`

---

## 🚀 Setup & Installation Guide

Follow these steps to run the project on your local machine.

### 1. Prerequisites
- Python 3.9 or higher
- Git installed on your system
- API Keys for OpenWeather and Twilio

### 2. Clone the Repository
```bash
git clone https://github.com/Balaji-123626/Your-Repository-Name.git
cd Your-Repository-Name
```

### 3. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a file named `.env` in the root directory of the project. Do **NOT** upload this file to GitHub. Add your API keys:
```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
```

### 6. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
The dashboard will automatically open in your default browser at `http://localhost:8501`.

---

## 💻 How to Use the Dashboard

1. **Search Location:** Use the sidebar to enter a city name (e.g., "London", "Delhi").
2. **Review Metrics:** Check the live AQI, weather, and specific pollutant values on the neon metric cards.
3. **Analyze Trends:** Scroll down to the Prophet ML section to see the 24-hour prediction chart. You can interact with the graph by zooming and hovering over data points.
4. **Chat with the Assistant:** Ask the Smart AQI Assistant questions like *"Is it safe to go jogging?"* or *"Will pollution increase tomorrow?"*
5. **Send Alerts:** In the Emergency Alert System section, enter a destination phone number in the sidebar, and click the Broadcast button to send a real-time warning.

---

## 🛡️ License & Contact

**Author:** Balaji
**GitHub:** [@Balaji-123626](https://github.com/Balaji-123626)

Feel free to fork this project, submit pull requests, or open issues if you find bugs or want to suggest new features!
