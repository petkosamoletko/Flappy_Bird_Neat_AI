
# Flappy Bird AI 🐦

Welcome to this Flappy Bird AI project. This initiative leverages the power of the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to train an AI to ace the game of Flappy Bird.

## 🌌 Project Overview
This project uses the NEAT algorithm to train an AI to play the popular game Flappy Bird. Users can train their own models, showcase the performance of the best-trained bird, or play the game manually.

![Train Simulation](train.gif)
## 🚀 Installation and Setup
1. Ensure you have `pygame` and `neat` installed. You can install them using pip:
   ```bash
   pip install pygame neat-python
   ```
2. Clone this repository to your local machine.
3. Navigate to the project directory.

## 🕹 Usage
Run the `flappy_bird.py` script and choose one of the following modes:
1. `train`: Train the Flappy Bird AI using the NEAT algorithm.
2. `showcase`: Display the best-performing bird's gameplay.
3. `manual`: Play the game yourself without AI assistance.

```bash
python flappy_bird.py
```

## 📂 File Descriptions
- `flappy_bird.py`: Main script that allows users to choose between training, showcasing, or manual modes.
- `game_modes.py`: Contains functions and logic for different game modes.
- `game_objects.py`: Defines game objects such as the bird, pipes, and other assets.
- `best_bird.pkl`: Serialized model of the best-performing bird.
- `neat_config.txt`: Configuration file for the NEAT algorithm.

Bask in this AI-powered flight, and may your bird fly ever onward and upward! 🌄
