# imports
import os 
from game_modes import *

if __name__ == "__main__":
    choice = input("Do you want to 'train', 'showcase' the best bird, or play 'manual'? ").lower()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")

    if choice == 'train':
        run(config_path)
    elif choice == 'showcase':
        best_bird_net = load_bird_model()
        showcase_best_bird(best_bird_net)
    elif choice == 'manual':
        manual_mode()
    else:
        print("Invalid choice, enter a valid prompt")






