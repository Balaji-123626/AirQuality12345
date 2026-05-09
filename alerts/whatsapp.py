from twilio.rest import Client
import pywhatkit
import time
import os

def send_twilio_alert(to_number, message, account_sid, auth_token, from_number):
    """
    Sends a WhatsApp message using the Twilio API.
    """
    try:
        if not account_sid or account_sid == "dummy":
            print("Twilio API keys not configured. Simulating alert.")
            return True, "Simulated Twilio alert sent (dummy keys)."

        client = Client(account_sid, auth_token)
        
        # Check if the Twilio number is configured for WhatsApp or standard SMS
        if from_number.startswith("whatsapp:"):
            # WhatsApp Mode
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"
            channel = "WhatsApp"
        else:
            # SMS Mode (Remove whatsapp prefix if it exists)
            if to_number.startswith("whatsapp:"):
                to_number = to_number.replace("whatsapp:", "")
            channel = "SMS"

        message_obj = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        return True, f"{channel} alert sent successfully! SID: {message_obj.sid}"
    except Exception as e:
        return False, str(e)

def send_pywhatkit_alert(to_number, message):
    """
    Sends a WhatsApp message using PyWhatKit.
    Note: This requires a browser session to be open and takes control of the keyboard/mouse briefly.
    """
    try:
        # Ensures phone number has + prefix
        if not to_number.startswith("+"):
            return False, "Phone number must start with country code (e.g., +91)"

        print(f"Sending PyWhatKit message to {to_number}...")
        # Send message instantly (waits 15 seconds, closes tab after 2 seconds)
        pywhatkit.sendwhatmsg_instantly(to_number, message, wait_time=15, tab_close=True, close_time=2)
        return True, "Alert sent successfully via PyWhatKit!"
    except Exception as e:
        return False, str(e)
