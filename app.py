import pygame
import time
import sys

MUSIC_FILE = "Feast - O Tuan (Lyrics Video) (mp3cut.net).mp3"
lyrics = [
    (0.0,   "Berbungkus fiksi"),                   
    (3.0,   "Aaaaaaaaaa kuuuuuuuuu takuttttttttttttttttt..."), 
    (6.0,   "Untuk nya, O Tuan"),                 
    (11.0,  "Wahai kematiannn"),                 
    (15.0,  "Ku Tak Bisa Melawan"),           
    (19.0,  "Jamah Perhentian"),                  
    (22.0,  "Berjanji ku ikhlaskan dengan relaaa"), 
]

def typewriter_print(text, delay=0.05, no_newline=False):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if not no_newline:
        print()

def calculate_optimal_speed(text, available_time):
    if available_time <= 0 or len(text) == 0:
        return 0.05
    
    optimal_speed = (available_time * 0.8) / len(text)
    
    return max(0.02, min(0.15, optimal_speed))

def main():
    pygame.mixer.init()
    
    try:
        pygame.mixer.music.load(MUSIC_FILE)
    except pygame.error as e:
        typewriter_print(f"❌ Error loading music file: {e}")
        return

    print("-" * 50)
    
    pygame.mixer.music.play()
    start_time = time.time()
    current_line = 0
    typing_in_progress = False
    current_char_index = 0
    typing_speed = 0.05

    while pygame.mixer.music.get_busy() or current_line < len(lyrics):
        elapsed = time.time() - start_time
        
        if (current_line < len(lyrics) and 
            elapsed >= lyrics[current_line][0] and 
            not typing_in_progress):
            
            typing_in_progress = True
            current_char_index = 0

            current_text = lyrics[current_line][1]
            if current_line + 1 < len(lyrics):
                next_time = lyrics[current_line + 1][0]
                available_time = next_time - elapsed
            else:
                available_time = 5.0  
                
            typing_speed = calculate_optimal_speed(current_text, available_time)
            
            print(f"\n", end="", flush=True)

        if typing_in_progress and current_line < len(lyrics):
            text = lyrics[current_line][1]
            
            if current_char_index < len(text):
                char = text[current_char_index]
                
                if char in '.,!?;:':
                    time.sleep(typing_speed * 4)  
                elif char in ' ':
                    time.sleep(typing_speed * 1.5)
                elif char in '-—':
                    time.sleep(typing_speed * 2) 
                
                sys.stdout.write(char)
                sys.stdout.flush()
                current_char_index += 1
                time.sleep(typing_speed)
                
            else:
                typing_in_progress = False
                current_line += 1

        time.sleep(0.01) 

    print(f"\n\n{'-' * 50}")

if __name__ == "__main__":
    main()