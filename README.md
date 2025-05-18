# Tank Arena

Tank Arena is a real-time multiplayer tank battle game. Players control tanks, navigate an arena, and compete to defeat opponents. The project is structured with a Go backend server and a client for gameplay.

## Features
- Real-time multiplayer gameplay
- Smooth tank movement and shooting mechanics
- Lobby system for player matchmaking
- Networked game state synchronization
- Modular codebase (client, server, shared logic)

## Project Structure
```
go.mod, go.sum         # Go module files
README.md              # Project documentation
client/                # Game client (Go)
server/                # Game server (Go)
shared/                # Shared code (protocols, types, utils)
```

## Getting Started
### Prerequisites
- Go 1.18 or newer

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd tank-arena
   ```
2. Install dependencies:
   ```sh
   go mod download
   ```

### Running the Server
```sh
cd server
go run main.go
```

### Running the Client
```sh
cd client
go run main.go
```

## How to Play
- Start the server and client as described above.
- Join a lobby and wait for other players.
- Use keyboard controls to move and shoot (see in-game instructions).
- Compete to be the last tank standing!

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.
