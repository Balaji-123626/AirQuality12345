import pandas as pd

def analyze_trend(forecast_df):
    """
    Analyzes the Prophet forecast DataFrame to determine the pollution trend.
    Returns: trend_direction, percentage_change, peak_time, trend_text
    """
    if forecast_df is None or forecast_df.empty:
        return "Stable →", 0.0, None, "No forecast data available."

    # Compare current (first) value with future (last) value of the 24h window
    current_val = forecast_df['yhat'].iloc[0]
    future_val = forecast_df['yhat'].iloc[-1]
    
    # Calculate percentage change
    if current_val > 0:
        pct_change = ((future_val - current_val) / current_val) * 100
    else:
        pct_change = 0.0
        
    # Determine direction
    if pct_change > 5.0:
        direction = "Rising ↑"
        trend_text = f"Pollution expected to rise by {abs(pct_change):.1f}% over the next 24 hours."
    elif pct_change < -5.0:
        direction = "Falling ↓"
        trend_text = f"Air quality likely to improve gradually, dropping by {abs(pct_change):.1f}% tomorrow."
    else:
        direction = "Stable →"
        trend_text = "Pollution levels are expected to remain stable over the next 24 hours."
        
    # Find peak pollution time
    peak_row = forecast_df.loc[forecast_df['yhat'].idxmax()]
    peak_time = peak_row['ds'].strftime("%I:%M %p")
    
    # Find safest outdoor time (minimum pollution)
    safe_row = forecast_df.loc[forecast_df['yhat'].idxmin()]
    safe_time = safe_row['ds'].strftime("%I:%M %p")

    return direction, pct_change, peak_time, safe_time, trend_text

def get_health_risk_analysis(aqi_val):
    """
    Returns health risk level, outdoor activity score, and recommended precautions based on AQI.
    """
    if aqi_val <= 50:
        return {
            "risk_level": "Low",
            "score": "95/100",
            "severity": 1,
            "precautions": ["Safe for outdoor activities", "Enjoy the fresh air", "Keep windows open"]
        }
    elif aqi_val <= 100:
        return {
            "risk_level": "Moderate",
            "score": "70/100",
            "severity": 2,
            "precautions": ["Unusually sensitive individuals should limit prolonged outdoor exertion", "Keep windows closed if sensitive"]
        }
    elif aqi_val <= 150:
        return {
            "risk_level": "High",
            "score": "40/100",
            "severity": 3,
            "precautions": ["Wear mask outdoors", "Avoid jogging or heavy exercise", "Keep windows closed"]
        }
    else:
        return {
            "risk_level": "Severe",
            "score": "10/100",
            "severity": 4,
            "precautions": ["Avoid all outdoor physical activities", "Stay indoors", "Use air purifiers", "Wear N95 mask if going out is necessary"]
        }

def generate_smart_response(user_input, city, aqi_val, status, trend_text, safe_time, health_data):
    """
    Rule-based response engine that analyzes keywords and returns intelligent environmental advice.
    """
    prompt = user_input.lower()
    
    # 1. Safe / Safety Check
    if "safe" in prompt or "dangerous" in prompt:
        if aqi_val <= 50:
            return f"Yes, the current AQI in {city} is {status.upper()} ({aqi_val}). Air quality is completely safe for outdoor activities."
        elif aqi_val <= 100:
            return f"The AQI in {city} is {status.upper()} ({aqi_val}). It is generally safe, but unusually sensitive individuals should take precautions."
        else:
            return f"Warning: The AQI in {city} is {status.upper()} ({aqi_val}). It is not considered safe for prolonged outdoor exposure. Please stay indoors."

    # 2. Jogging / Exercise / Outdoor
    if "jogging" in prompt or "run" in prompt or "exercise" in prompt or "outside" in prompt:
        if aqi_val <= 100:
            return f"Outdoor exercise is currently safe. The AQI is {aqi_val} ({status})."
        else:
            return f"I do not recommend outdoor exercise right now. The AQI is {status.upper()} ({aqi_val}). Consider indoor workouts instead. The safest time to go out is around {safe_time}."

    # 3. Children / Kids
    if "child" in prompt or "kid" in prompt or "baby" in prompt:
        if aqi_val <= 50:
            return "It is perfectly safe for children to play outside right now."
        else:
            return f"Since children are more sensitive to pollution, please be cautious. The current AQI is {aqi_val}. It is best to limit their outdoor playtime today."

    # 4. Asthma / Medical
    if "asthma" in prompt or "patient" in prompt or "sick" in prompt:
        if aqi_val > 50:
            return f"Asthma patients and sensitive individuals should stay indoors. The AQI is {aqi_val}. {health_data['precautions'][0]}."
        else:
            return "Air quality is good right now, but asthma patients should always carry their inhalers as a precaution."

    # 5. Trend / Pollution / Tomorrow
    if "trend" in prompt or "pollution" in prompt or "tomorrow" in prompt or "future" in prompt or "increase" in prompt:
        return f"Based on our Prophet ML analytics: {trend_text} The safest time is predicted to be at {safe_time}."

    # 6. General Fallback
    return f"The current AQI in {city} is {aqi_val} ({status.upper()}). {health_data['precautions'][0]}. Is there a specific activity you are planning?"
