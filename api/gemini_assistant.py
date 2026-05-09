import os
import google.generativeai as genai

# Configure API Key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def generate_ai_summary(city, aqi, status, trend_text, weather):
    """
    Generates a natural language summary based on current environmental data.
    """
    if not api_key:
        return "⚠️ Gemini API Key not configured. Please add it to your .env file to enable AI insights."
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""
        You are an advanced AI Environmental Intelligence Assistant.
        Analyze the following real-time data for {city} and provide a concise, professional 2-3 sentence summary.
        Include a quick health recommendation.
        
        Data:
        - Current AQI: {aqi} ({status})
        - Forecast Trend: {trend_text}
        - Weather: {weather.get('temp')}°C, Humidity {weather.get('humidity')}%, Wind {weather.get('wind_speed')} m/s.
        
        Format: Return only the summary text without any markdown or conversational filler.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating AI summary: {str(e)}"

def get_chat_response(messages, city, aqi_data, forecast_trend):
    """
    Handles conversational responses using Gemini, injecting the environmental context.
    messages: list of dicts [{'role': 'user/assistant', 'content': '...'}, ...]
    """
    if not api_key:
        return "I need a Gemini API Key to function. Please add `GEMINI_API_KEY` to your `.env` file."

    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Build system context
        context = f"""
        You are an AI Environmental Intelligence Assistant built into a real-time Air Quality dashboard.
        Current context for {city}:
        - AQI: {aqi_data.get('aqi')} ({aqi_data.get('status')})
        - Weather: {aqi_data.get('weather', {}).get('temp')}°C
        - Future Trend: {forecast_trend}
        
        Answer the user's questions based on this data. Keep responses concise, professional, and directly address health and safety concerns.
        """
        
        # Convert Streamlit messages format to Gemini format
        chat_history = []
        for msg in messages[:-1]:  # Exclude the very last message which is the current prompt
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg["content"]]})
            
        chat = model.start_chat(history=chat_history)
        
        # Prepend the system context to the user's current query behind the scenes
        current_query = messages[-1]["content"]
        full_prompt = f"[System Context: {context}]\n\nUser Question: {current_query}"
        
        response = chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"
