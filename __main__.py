import math
import sys
import speech_recognition as sr
import keyboard

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

def get_coordinate(prompt_text, use_voice=True, allow_new=False):
    """Helper to ask for coordinates via voice or text, handling 'new' keyword and exiting."""
    if allow_new:
        action_word = "say" if use_voice else "type"
        full_prompt = f"{prompt_text} (or {action_word} 'new' to move gun)"
    else:
        full_prompt = prompt_text

    while True:
        if use_voice:
            user_in = listen_for_input(full_prompt)
        else:
            user_in = input(f"{full_prompt}: ").strip().lower()
            
        if user_in in ['q', 'quit', 'exit', 'stop', 'abort']:
            print("Exiting calculator. Good hunting.")
            sys.exit()

        if user_in == 'new':
            if allow_new:
                return 'new'
            else:
                input_type = "say" if use_voice else "type"
                print(f"Error: 'new' command not valid here. Please {input_type} a coordinate.")
                continue
            
        try:
            # Google STT generally formats spoken numbers ("forty two") as digits ("42")
            # Remove any accidental spaces or commas ("4,2" -> "4.2")
            clean_in = user_in.replace(',', '.').replace(' ', '')
            return float(clean_in)
        except ValueError:
            input_type = "say" if use_voice else "type"
            print(f"Error: Please {input_type} a numerical coordinate.")

def main():
    print("--- WARDOGS Artillery Calculator ---")
    
    # Prompt for input mode at launch
    mode_selection = input("Select input mode - (1) Type or (2) Voice: ").strip()
    use_voice = (mode_selection == '2')
    
    print("\nSay 'quit', 'stop', or 'abort' at any prompt to exit." if use_voice else "\nType 'quit', 'stop', or 'abort' at any prompt to exit.")
    
    gun_x = None
    gun_y = None
    
    while True:
        print("\n[STANDBY] Press 'F13' to start the next mission calculation...")
        keyboard.wait('f13')  # Pauses execution entirely until F13 is pressed
        
        print("\n=== NEW MISSION ===")
        
        # Only ask for Gun coords if they haven't been set yet (first run)
        if gun_x is None or gun_y is None:
            gun_x = get_coordinate("Gun X coordinate", use_voice)
            gun_y = get_coordinate("Gun Y coordinate", use_voice)
        
        # Ask for Target X, allowing the 'new' keyword here
        target_x = get_coordinate("Target X coordinate", use_voice, allow_new=True)
        
        # If the user says 'new', ask for the gun coordinates again, then ask for Target X
        if target_x == 'new':
            print("\n[UPDATING GUN POSITION]")
            gun_x = get_coordinate("New Gun X coordinate", use_voice)
            gun_y = get_coordinate("New Gun Y coordinate", use_voice)
            target_x = get_coordinate("Target X coordinate", use_voice)
            
        target_y = get_coordinate("Target Y coordinate", use_voice)
        
        distance, bearing = calculate_firing_solution(gun_x, gun_y, target_x, target_y)
        
        print("\n=== FIRING SOLUTION ===")
        print(f"Gun Pos:  ({gun_x}, {gun_y})")
        print(f"Range:    {distance:.1f} meters")
        print(f"Bearing:  {bearing:.1f}°")

if __name__ == "__main__":
    main()
