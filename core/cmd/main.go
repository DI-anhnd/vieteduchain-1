package main

import (
	"log"
	"time"
	"vieteduchain/core/internal/blockchain"
	"vieteduchain/core/internal/consensus"
)

func main() {
	// Initialize the blockchain
	chain := blockchain.NewChain()

	// Start the consensus mechanism
	consensus.StartHotStuff(chain)

	log.Println("VietEduChain is running...")
	// Giữ tiến trình chạy foreground đúng chuẩn, tránh deadlock
	for {
		time.Sleep(time.Hour)
	}
}