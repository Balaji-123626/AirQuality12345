import streamlit as st

def get_status_color(status):
    """Returns a color hex code based on AQI status."""
    colors = {
        "Good": "#00FFAA",       # Neon Green
        "Moderate": "#FFD700",   # Neon Yellow
        "Poor": "#FF6B00",       # Neon Orange
        "Dangerous": "#FF003C"   # Neon Red
    }
    return colors.get(status, "#00FFAA")

def apply_custom_css():
    """Applies premium glassmorphism dark-themed CSS."""
    st.markdown(
        """
        <style>
        /* General Background */
        .stApp {
            background: linear-gradient(135deg, #0A0F1A 0%, #111A2E 100%);
            color: #E2E8F0;
            font-family: 'Inter', sans-serif;
        }
        
        /* Glassmorphism Cards for standard Streamlit containers */
        div[data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 20px;
            border-radius: 16px;
            color: #FFFFFF;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 255, 170, 0.15);
            border: 1px solid rgba(0, 255, 170, 0.3);
        }
        
        div[data-testid="metric-container"] > label {
            color: #94A3B8;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #FFFFFF;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }
        
        /* Custom styled card for AQI Status */
        .aqi-card {
            padding: 40px 20px;
            border-radius: 24px;
            text-align: center;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid var(--glow-color);
            box-shadow: 0 10px 40px -10px var(--glow-color);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .aqi-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; height: 6px;
            background: var(--glow-color);
            box-shadow: 0 0 30px var(--glow-color);
        }
        
        .aqi-card:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 50px -5px var(--glow-color);
        }
        
        .aqi-value {
            font-size: 5rem;
            font-weight: 900;
            margin: 0;
            line-height: 1.1;
            text-shadow: 0 0 30px var(--glow-color), 0 0 10px #FFFFFF;
            color: #FFFFFF;
        }
        
        .aqi-status {
            font-size: 2rem;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 900;
            margin-top: 15px;
            color: var(--glow-color);
            text-shadow: 0 0 20px var(--glow-color);
        }
        
        /* Trend Card */
        .trend-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            margin-top: 10px;
            text-align: center;
        }
        
        .trend-direction {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        /* AI Chat Message Styling */
        .ai-chat-bubble {
            background: rgba(0, 255, 170, 0.1);
            border-left: 4px solid #00FFAA;
            padding: 15px 20px;
            border-radius: 8px 16px 16px 8px;
            margin-bottom: 15px;
            color: #E2E8F0;
            font-size: 1.05rem;
            line-height: 1.5;
        }
        
        /* Loading Animation */
        .loader {
            border: 4px solid rgba(255,255,255,0.1);
            border-top: 4px solid #00FFAA;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
            margin: 30px auto;
            box-shadow: 0 0 20px rgba(0, 255, 170, 0.4);
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Voice Assistant Section */
        .voice-section {
            background: rgba(0, 255, 170, 0.05);
            border: 1px solid rgba(0, 255, 170, 0.3);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0, 255, 170, 0.1);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .voice-section:hover {
            box-shadow: 0 0 30px rgba(0, 255, 170, 0.3);
        }
        
        /* Waveform Animation */
        .waveform {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            height: 40px;
            margin-top: 15px;
        }
        
        .bar {
            width: 5px;
            background: #00FFAA;
            border-radius: 5px;
            animation: pulse 1s infinite ease-in-out;
        }
        
        .bar:nth-child(1) { height: 10px; animation-delay: 0.1s; }
        .bar:nth-child(2) { height: 20px; animation-delay: 0.2s; }
        .bar:nth-child(3) { height: 40px; animation-delay: 0.3s; }
        .bar:nth-child(4) { height: 25px; animation-delay: 0.4s; }
        .bar:nth-child(5) { height: 15px; animation-delay: 0.5s; }
        
        @keyframes pulse {
            0%, 100% { transform: scaleY(0.5); opacity: 0.5; }
            50% { transform: scaleY(1.2); opacity: 1; box-shadow: 0 0 10px #00FFAA; }
        }
        
        /* Expander Header Visibility Fix */
        div[data-testid="stExpander"] details summary {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px;
            padding: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #FFFFFF !important;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stExpander"] details summary:hover {
            background-color: rgba(0, 255, 170, 0.15) !important;
            border-color: #00FFAA !important;
            box-shadow: 0 0 15px rgba(0, 255, 170, 0.3);
        }
        
        div[data-testid="stExpander"] details summary p {
            color: #00FFAA !important;
            font-weight: 900 !important;
            font-size: 1.2rem !important;
            text-shadow: 0 0 10px rgba(0, 255, 170, 0.3);
            margin: 0 !important;
        }
        
        div[data-testid="stExpander"] details summary svg {
            fill: #00FFAA !important;
            color: #00FFAA !important;
        }
        
        /* General Button Styling Fix */
        .stButton > button, .stDownloadButton > button {
            background-color: rgba(0, 255, 170, 0.1) !important;
            color: #00FFAA !important;
            border: 1px solid #00FFAA !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover, .stDownloadButton > button:hover {
            background-color: #00FFAA !important;
            color: #0A0F1A !important;
            box-shadow: 0 0 20px rgba(0, 255, 170, 0.6) !important;
            transform: translateY(-2px);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_aqi_card(aqi, status):
    """Displays a custom styled premium HTML card for the AQI."""
    glow_color = get_status_color(status)
    
    html = f"""
    <div class="aqi-card" style="--glow-color: {glow_color}; border: 1px solid {glow_color}40;">
        <p class="aqi-value">{aqi}</p>
        <p class="aqi-status">{status}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def display_custom_metric(label, value, color="#00FFAA"):
    """Displays a custom styled metric card with glassmorphism and neon glows."""
    # Convert hex color to rgba for box-shadows
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    
    html = f"""
    <div style="
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 20px;
        border-radius: 16px;
        color: #FFFFFF;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    " 
    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 40px 0 rgba({r}, {g}, {b}, 0.2)'; this.style.borderColor='rgba({r}, {g}, {b}, 0.5)';" 
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px 0 rgba(0, 0, 0, 0.3)'; this.style.borderColor='rgba(255, 255, 255, 0.1)';">
        <div style="color: #94A3B8; font-weight: 600; font-size: 1.1rem; letter-spacing: 0.5px; margin-bottom: 8px;">{label}</div>
        <div style="color: {color}; font-weight: 800; font-size: 2.2rem; text-shadow: 0 0 15px rgba({r}, {g}, {b}, 0.6);">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

