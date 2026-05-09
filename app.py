import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import os
from dotenv import load_dotenv

# Load custom modules
from model.model import train_and_forecast
from api.openweather import get_real_time_aqi
from alerts.whatsapp import send_twilio_alert, send_pywhatkit_alert

from utils.ui_helpers import apply_custom_css, display_aqi_card, display_custom_metric
from utils.intelligence import analyze_trend, get_health_risk_analysis, generate_smart_response

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(
    page_title="AI Environmental Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Premium Dark CSS
apply_custom_css()

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your AI Environmental Assistant. Ask me anything about the local air quality, health safety, or weather conditions."}
    ]

# --- Caching the Model ---
# We train the Prophet model once and cache it to avoid retraining on every interaction
@st.cache_resource(show_spinner="Initializing AI Forecasting Engine...")
def load_and_train_model():
    try:
        model, forecast, data = train_and_forecast(csv_path="./AirQualityUCI.csv", periods=24)
        return model, forecast, data
    except Exception as e:
        st.error(f"Error loading AI model: {e}")
        return None, None, None

model, forecast, historical_data = load_and_train_model()

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3344/3344383.png", width=100)
    st.title("Environmental Controls")
    
    st.header("📍 Location")
    city_input = st.text_input("Enter City Name", placeholder="e.g., Chennai, London")
    
    st.header("📱 Alert System")
    alert_phone = st.text_input("Your Phone Number", placeholder="+919876543210")
    
    st.markdown("---")
    st.markdown("### ℹ️ About Project")
    st.info("AI-Powered Real-Time Air Quality Intelligence System. Real-time Monitoring • Predictive Forecasting • Smart Health Analytics. Powered by Prophet ML.")

# Load credentials from backend (.env) silently
openweather_key = os.getenv("OPENWEATHER_API_KEY", "")
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
twilio_auth = os.getenv("TWILIO_AUTH_TOKEN", "")
twilio_from = os.getenv("TWILIO_PHONE_NUMBER", "")

# --- Hero Section ---
st.markdown("<h1 style='text-align: center; color: #00FFAA; text-shadow: 0 0 10px rgba(0,255,170,0.5);'>🌍 AI-Powered Real-Time Air Quality Intelligence System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #94A3B8; margin-bottom: 30px;'>Real-time Monitoring • Predictive Forecasting • Smart Health Analytics</h4>", unsafe_allow_html=True)



# Processing the City Input
if city_input:
    with st.spinner(f"Gathering Environmental Intelligence for {city_input.title()}..."):
        real_time_data = get_real_time_aqi(city_input, openweather_key)
        
    if "error" in real_time_data:
        st.error(f"Error fetching data: {real_time_data['error']}")
    else:
        status = real_time_data['status']
        aqi_val = real_time_data['aqi']
        weather = real_time_data.get('weather', {})
        components = real_time_data['components']
        
        # Trend Analysis
        future_forecast = forecast.tail(24) if forecast is not None else None
        trend_dir, pct_change, peak_time, safe_time, trend_text = analyze_trend(future_forecast)
        
        # Health Analysis
        health_data = get_health_risk_analysis(aqi_val)

        # --- SECTION 1: LIVE DATA & WEATHER COMBO ---
        st.subheader(f"📍 Live Metrics: {city_input.title()}")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            display_aqi_card(aqi_val, status)
        with c2:
            display_custom_metric("🌡️ Temperature", f"{weather.get('temp', 0)} °C", color="#FF6B00")
            display_custom_metric("💧 Humidity", f"{weather.get('humidity', 0)} %", color="#00BFFF")
        with c3:
            display_custom_metric("💨 Wind Speed", f"{weather.get('wind_speed', 0)} m/s", color="#E0FFFF")
            display_custom_metric("🌫️ PM2.5", f"{components.get('pm2_5', 0)} µg/m³", color="#FFD700")
        with c4:
            display_custom_metric("⚠️ PM10", f"{components.get('pm10', 0)} µg/m³", color="#FFD700")
            display_custom_metric("🚗 CO Level", f"{components.get('co', 0)} µg/m³", color="#00FFAA")
            


        # --- SECTION 2: AI TREND INTELLIGENCE & SUMMARY ---
        st.markdown("<br>", unsafe_allow_html=True)
        t1, t2 = st.columns([1, 2])
        
        with t1:
            st.markdown("### 📈 Trend Intelligence")
            st.markdown(f"""
            <div class="trend-card">
                <div class="trend-direction" style="color: {'#FF003C' if trend_dir=='Rising ↑' else '#00FFAA' if trend_dir=='Falling ↓' else '#FFD700'}">{trend_dir}</div>
                <p>{trend_text}</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <p><strong>Peak Pollution:</strong> {peak_time}</p>
                <p><strong>Safest Time:</strong> {safe_time}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with t2:

            
            st.markdown("### ⚕️ Health & Risk Analysis")
            h1, h2, h3 = st.columns(3)
            with h1:
                risk_color = "#FF003C" if health_data['severity'] > 2 else "#FFD700" if health_data['severity'] == 2 else "#00FFAA"
                display_custom_metric("Risk Level", health_data['risk_level'], color=risk_color)
            with h2:
                display_custom_metric("Outdoor Score", health_data['score'], color="#00BFFF")
            with h3:
                display_custom_metric("Severity", f"{health_data['severity']} / 4", color="#FF6B00")
            
            with st.expander("🛡️ Recommended Precautions", expanded=True):
                for p in health_data['precautions']:
                    st.markdown(f"- {p}")

        # --- SECTION 3: ADVANCED VISUALIZATIONS ---
        if forecast is not None:
            st.markdown("---")
            st.subheader("🔮 24-Hour AI Predictive Analytics (Prophet ML)")
            
            v1, v2 = st.columns([3, 1])
            
            with v1:
                # Plotly Forecast Graph
                fig = go.Figure()
                
                # Add historical data (last 100 points for context)
                hist_plot = historical_data.tail(100)
                fig.add_trace(go.Scatter(
                    x=hist_plot['ds'], y=hist_plot['y'],
                    mode='lines', name='Historical Data',
                    line=dict(color='#888888', width=2)
                ))
                
                # Add forecast
                fig.add_trace(go.Scatter(
                    x=future_forecast['ds'], y=future_forecast['yhat'],
                    mode='lines+markers', name='Predicted CO(GT)',
                    line=dict(color='#00FFAA', width=3)
                ))
                
                # Add confidence intervals
                fig.add_trace(go.Scatter(
                    x=future_forecast['ds'].tolist() + future_forecast['ds'].tolist()[::-1],
                    y=future_forecast['yhat_upper'].tolist() + future_forecast['yhat_lower'].tolist()[::-1],
                    fill='toself',
                    fillcolor='rgba(0, 255, 170, 0.1)',
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip",
                    showlegend=False,
                    name='Confidence Interval'
                ))
                
                fig.update_layout(
                    title="Predicted CO(GT) Levels for Next 24 Hours",
                    xaxis_title="Time",
                    yaxis_title="CO(GT) Level",
                    template="plotly_dark",
                    hovermode="x unified",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            with v2:
                # Gauge Meter for Current AQI
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = aqi_val,
                    title = {'text': "Current AQI"},
                    gauge = {
                        'axis': {'range': [None, 300]},
                        'bar': {'color': "#00FFAA"},
                        'steps' : [
                            {'range': [0, 50], 'color': "rgba(0, 255, 170, 0.2)"},
                            {'range': [50, 100], 'color': "rgba(255, 215, 0, 0.2)"},
                            {'range': [100, 150], 'color': "rgba(255, 107, 0, 0.2)"},
                            {'range': [150, 300], 'color': "rgba(255, 0, 60, 0.2)"}],
                        }
                ))
                fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Download CSV
                csv = future_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(index=False)
                st.download_button(
                    label="📥 Download Forecast Data",
                    data=csv,
                    file_name=f"{city_input}_aqi_prediction.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                


        # --- SECTION 4: EMERGENCY ALERT SYSTEM ---
        st.markdown("---")
        st.markdown("<h2 style='color: #FF6B00; text-shadow: 0 0 15px rgba(255, 107, 0, 0.5); font-weight: 800;'>🚨 Emergency Alert System</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #E2E8F0; font-size: 1.1rem;'>Instantly notify authorities, loved ones, or your own device about dangerous air quality levels via SMS/WhatsApp.</p>", unsafe_allow_html=True)
        
        st.markdown("<div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 107, 0, 0.4); padding: 30px; border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); transition: all 0.3s ease;'>", unsafe_allow_html=True)
        
        alert_col1, alert_col2 = st.columns([2, 1])
        with alert_col1:
            st.markdown(f"""
            <div style='background: rgba(255, 107, 0, 0.1); border-left: 5px solid #FF6B00; padding: 15px 20px; border-radius: 8px;'>
                <p style='color: #FFD700; font-weight: bold; font-size: 1.1rem; margin-bottom: 5px;'>Ready to broadcast message:</p>
                <p style='color: #FFFFFF; font-size: 1.2rem; font-style: italic; text-shadow: 0 0 10px rgba(255,255,255,0.3); margin: 0;'>
                "🚨 AQI ALERT: Current AQI in {city_input} is {status} ({aqi_val}). Trend: {trend_dir}. Stay safe!"
                </p>
            </div>
            """, unsafe_allow_html=True)
        with alert_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚨 Broadcast Emergency Alert", use_container_width=True):
                if not alert_phone:
                    st.error("Please configure your phone number in the sidebar first.")
                else:
                    with st.spinner("Broadcasting alert..."):
                        alert_msg = f"🚨 AQI ALERT: Current AQI in {city_input} is {status} ({aqi_val}). Trend: {trend_dir}. Stay safe!"
                        success, msg = send_twilio_alert(alert_phone, alert_msg, twilio_sid, twilio_auth, twilio_from)
                        if success:
                            st.success(msg)
                        else:
                            st.error(f"Failed to send alert: {msg}")
        
        st.markdown("</div>", unsafe_allow_html=True)

        # --- SECTION 5: AI CHAT ASSISTANT ---
        st.markdown("---")
        st.subheader("💬 Smart AQI Assistant")
        st.markdown("Ask me anything about the local air quality, health risks, or weather conditions.")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "assistant":
                st.markdown(f"<div class='ai-chat-bubble'><b>🤖 Assistant:</b> {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: right; margin-bottom: 15px; color: #94A3B8;'><b>🧑 You:</b> {message['content']}</div>", unsafe_allow_html=True)
                
        # Chat Input
        if prompt := st.chat_input("E.g., Is it safe to go for a run right now?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.markdown(f"<div style='text-align: right; margin-bottom: 15px; color: #94A3B8;'><b>🧑 You:</b> {prompt}</div>", unsafe_allow_html=True)
            
            # Simulated AI Thinking
            import time
            typing_placeholder = st.empty()
            typing_placeholder.markdown("<div class='ai-chat-bubble' style='color: #00FFAA;'><i>🤖 Analyzing environmental data...</i></div>", unsafe_allow_html=True)
            time.sleep(1.2) # Simulate processing time
            typing_placeholder.empty()
            
            # Generate Rule-Based Response
            response_text = generate_smart_response(prompt, city_input, aqi_val, status, trend_text, safe_time, health_data)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            st.markdown(f"<div class='ai-chat-bubble'><b>🤖 Assistant:</b> {response_text}</div>", unsafe_allow_html=True)

else:
    st.info("👈 Please enter a city name in the sidebar to begin environmental analysis.")
    
    # Show generic model status
    if forecast is not None:
        st.success("✅ Prophet ML Forecasting Engine is Online and Ready.")
