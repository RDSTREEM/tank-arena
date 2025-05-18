package main

import (
	"fmt"
	"net"
)

func main() {
	fmt.Println("🚀 Server starting on :8080")

	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("❌ Failed to accept connection:", err)
			continue
		}
		fmt.Println("✅ New client connected")

		// Start handling the client in a new goroutine
		go handleClient(conn)
	}
}
