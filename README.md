# Tank Arena

Tank Arena is a real-time multiplayer tank battle game built with Python and Pygame. Players control tanks, navigate an arena, and compete to defeat opponents in fast-paced battles. The project is structured for easy development and extension.

## Features
- Real-time multiplayer gameplay
- Smooth tank movement and shooting mechanics
- Lobby system for player matchmaking
- Networked game state synchronization
- Modular codebase (client, server, shared logic)

## Project Structure
```
README.md              # Project documentation
client/                # Game client (Python, Pygame)
server/                # Game server (Python)
shared/                # Shared code (protocols, types, utils)
requirements.txt       # Python dependencies
```

## Getting Started
### Prerequisites
- Python 3.8 or newer
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd tank-arena
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Server
```sh
cd server
python main.py
```

### Running the Client
```sh
cd client
python main.py
```

## How to Play
- Start the server and client as described above.
- Join a lobby and wait for other players.
- Use keyboard controls to move and shoot (see in-game instructions).
- Compete to be the last tank standing!

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.
