package blockchain

import (
	"sync"
	"time"
)

// Block represents a single block in the blockchain.
type Block struct {
	Index        int       `json:"index"`
	Timestamp    time.Time `json:"timestamp"`
	Data         string    `json:"data"`
	PreviousHash string    `json:"previous_hash"`
	Hash         string    `json:"hash"`
}

// Blockchain represents the chain of blocks.
type Blockchain struct {
	blocks []*Block
	mutex  sync.Mutex
}

// NewBlockchain creates a new instance of Blockchain.
func NewBlockchain() *Blockchain {
	return &Blockchain{
		blocks: []*Block{createGenesisBlock()},
	}
}

// createGenesisBlock creates the first block in the blockchain.
func createGenesisBlock() *Block {
	return &Block{
		Index:        0,
		Timestamp:    time.Now(),
		Data:         "Genesis Block",
		PreviousHash: "",
		Hash:         "",
	}
}

// AddBlock adds a new block to the blockchain.
func (bc *Blockchain) AddBlock(data string) {
	bc.mutex.Lock()
	defer bc.mutex.Unlock()

	newBlock := &Block{
		Index:        len(bc.blocks),
		Timestamp:    time.Now(),
		Data:         data,
		PreviousHash: bc.blocks[len(bc.blocks)-1].Hash,
		Hash:         "", // Hash will be calculated later
	}
	bc.blocks = append(bc.blocks, newBlock)
}

// GetBlocks returns all blocks in the blockchain.
func (bc *Blockchain) GetBlocks() []*Block {
	bc.mutex.Lock()
	defer bc.mutex.Unlock()
	return bc.blocks
}

// Chain represents the blockchain.
type Chain struct{}

// NewChain creates a new instance of Chain.
func NewChain() *Chain {
	return &Chain{}
}