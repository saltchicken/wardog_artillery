import math
import sys

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

def get_coordinate(prompt_text, current_val=None):
    """Helper to ask for coordinates, allowing defaults and exiting."""
    while True:
        if current_val is not None:
            user_in = input(f"{prompt_text} (Press Enter to keep {current_val}): ").strip()
            if user_in == "":
                return current_val
        else:
            user_in = input(f"{prompt_text}: ").strip()
            
        if user_in.lower() in ['q', 'quit']:
            print("Exiting calculator. Good hunting.")
            sys.exit()
            
        try:
            return float(user_in)
        except ValueError:
            print("Error: Please enter a numerical coordinate.")

def main():
    print("--- WARDOGS Artillery Calculator ---")
    print("Type 'q' at any prompt to quit the calculator.\n")
    
    # Store these outside the loop so they persist between missions
    gun_x = None
    gun_y = None
    
    while True:
        print("\n--- NEW MISSION ---")
        gun_x = get_coordinate("Enter Gun X coordinate", gun_x)
        gun_y = get_coordinate("Enter Gun Y coordinate", gun_y)
        
        target_x = get_coordinate("Enter Target X coordinate")
        target_y = get_coordinate("Enter Target Y coordinate")
        
        distance, bearing = calculate_firing_solution(gun_x, gun_y, target_x, target_y)
        
        print("\n--- FIRING SOLUTION ---")
        print(f"Range:    {distance:.1f} meters")
        print(f"Bearing:  {bearing:.1f}°")

if __name__ == "__main__":
    main()
