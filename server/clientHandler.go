package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net"
	"sync"

	"tank-arena/shared"
)

var (
	clients    = make(map[string]net.Conn)         // Active client connections
	tankStates = make(map[string]shared.TankState) // All player tank states
	mutex      = sync.Mutex{}                      // For safe concurrent access
)

func handleClient(conn net.Conn) {
	defer conn.Close()

	id := conn.RemoteAddr().String() // Use IP:port as temporary unique ID
	fmt.Println("🎮 Player ID:", id)

	// Add to active clients
	mutex.Lock()
	clients[id] = conn
	mutex.Unlock()

	reader := bufio.NewReader(conn)

	// Start goroutine to send world updates to this client
	go sendWorldState(conn, id)

	for {
		data, err := reader.ReadBytes('\n')
		if err != nil {
			fmt.Println("❌ Disconnected:", id)
			break
		}

		msg, err := shared.DecodeMessage(data)
		if err != nil {
			fmt.Println("⚠️ Invalid message from", id)
			continue
		}

		switch msg.Type {
		case "update":
			var tank shared.TankState
			json.Unmarshal(msg.Data, &tank)
			tank.ID = id

			mutex.Lock()
			tankStates[id] = tank
			mutex.Unlock()
		}
	}

	// Cleanup
	mutex.Lock()
	delete(clients, id)
	delete(tankStates, id)
	mutex.Unlock()
}
