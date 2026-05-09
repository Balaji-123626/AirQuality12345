# 🌍 AI-Powered Real-Time Air Quality Intelligence System

A state-of-the-art Environmental Intelligence Dashboard that provides real-time air quality monitoring, predictive forecasting, and smart health analytics. Built with Python, Streamlit, and Prophet ML, this system transforms raw environmental data into actionable intelligence without relying on external LLM APIs.

## ✨ Features

- **Real-Time Environmental Monitoring:** Fetches live Air Quality Index (AQI), temperature, humidity, wind speed, and pollutant levels (PM2.5, PM10, CO) using OpenWeather API.
- **Predictive Forecasting Engine:** Powered by Facebook's Prophet Machine Learning model to analyze historical trends and predict CO(GT) levels 24 hours into the future.
- **Smart AQI Assistant:** An offline, rule-based Environmental Response Engine that provides dynamic health recommendations and trend insights instantly.
- **Emergency Alert System:** Integrated Twilio functionality to broadcast critical AQI warnings to SMS/WhatsApp in real-time.
- **Premium UI/UX:** Built with dark glassmorphism, glowing neon highlights, animated waveform metrics, and an interactive Plotly charting system for a startup-grade look.

## 📸 Screenshots

*(Replace these placeholders with actual screenshots of your dashboard)*

![Dashboard View](assets/dashboard.png)
![Predictive Forecast](assets/forecast.png)
![Emergency Alerts & AI Assistant](assets/assistant.png)

## 🛠️ Technologies Used

- **Frontend:** Streamlit, Custom HTML/CSS (Glassmorphism UI)
- **Data Visualization:** Plotly
- **Machine Learning:** Prophet (Forecasting Engine), Pandas
- **APIs:** OpenWeather API (Live Data), Twilio API (SMS Alerts)
- **Backend Languages:** Python

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Balaji-123626/Your-Repo-Name.git
   cd Your-Repo-Name
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and configure your API keys. (See `.env.example` for reference).
   ```env
   OPENWEATHER_API_KEY=your_openweather_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_number
   ```
   *Note: Never commit your `.env` file to version control.*

## 💻 Usage

Run the Streamlit application using the following command:

```bash
streamlit run app.py
```

The application will launch in your default web browser (typically at `http://localhost:8501`).

1. Enter a city name in the sidebar.
2. View live metrics and health safety scores.
3. Chat with the Smart AQI Assistant for personalized recommendations.
4. Broadcast emergency alerts directly from the dashboard.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Balaji-123626/Your-Repo-Name/issues).
