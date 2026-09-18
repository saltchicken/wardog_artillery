import math
import sys
import speech_recognition as sr

def calculate_firing_solution(gun_x, gun_y, target_x, target_y):
    """Calculates map distance, compass bearing, and azimuth MILs."""
    delta_x = target_x - gun_x
    delta_y = target_y - gun_y
    
    # Distance: WARDOGS maps are 100m per coordinate unit
    distance = 100 * math.sqrt((delta_x ** 2) + (delta_y ** 2))
    
    # Bearing: Using atan2 ensures 0 degrees points North 
    bearing_rad = math.atan2(delta_x, delta_y)
    bearing_deg = math.degrees(bearing_rad)
    
    if bearing_deg < 0:
        bearing_deg += 360

    return distance, bearing_deg

def listen_for_input(prompt_text):
    """Activates the microphone and converts speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"\n[MIC ON] {prompt_text} (Speak now...)")
        # Adjust for ambient noise briefly
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # Listen for up to 5 seconds
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            # Use Google's free Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"> Heard: '{text}'")
            return text.strip().lower()
        except sr.WaitTimeoutError:
            print("> Timed out. No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("> Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"> Could not request results; {e}")
            return ""

def get_coordinate(prompt_text, current_val=None):
    """Helper to ask for coordinates via voice, allowing defaults and exiting."""
    while True:
        if current_val is not None:
            full_prompt = f"{prompt_text}. (Say 'keep' to use {current_val})"
        else:
            full_prompt = prompt_text
            
        user_in = listen_for_input(full_prompt)
        
        # Handle empty/silent input when there's a default
        if user_in == "" and current_val is not None:
            print(f"Keeping default: {current_val}")
            return current_val
            
        # Handle explicit 'keep' command
        if user_in in ['keep', 'skip', 'next', 'same'] and current_val is not None:
            return current_val
            
        if user_in in ['q', 'quit', 'exit', 'stop', 'abort']:
            print("Exiting calculator. Good hunting.")
            sys.exit()
            
        try:
            # Google STT generally formats spoken numbers ("forty two") as digits ("42")
            # Remove any accidental spaces or commas ("4,2" -> "4.2")
            clean_in = user_in.replace(',', '.').replace(' ', '')
            return float(clean_in)
        except ValueError:
            print("Error: Please say a numerical coordinate.")

def main():
    print("--- WARDOGS Voice Artillery Calculator ---")
    print("Say 'quit', 'stop', or 'abort' at any prompt to exit.\n")
    
    gun_x = None
    gun_y = None
    
    while True:
        print("\n=== NEW MISSION ===")
        gun_x = get_coordinate("State Gun X coordinate", gun_x)
        gun_y = get_coordinate("State Gun Y coordinate", gun_y)
        
        target_x = get_coordinate("State Target X coordinate")
        target_y = get_coordinate("State Target Y coordinate")
        
        distance, bearing = calculate_firing_solution(gun_x, gun_y, target_x, target_y)
        
        print("\n=== FIRING SOLUTION ===")
        print(f"Range:    {distance:.1f} meters")
        print(f"Bearing:  {bearing:.1f}°")

if __name__ == "__main__":
    main()
