package consensus

import (
	"errors"
	"sync"
)

// Proposal represents a proposed block in the HotStuff consensus algorithm.
type Proposal struct {
	Height int
	Leader string
	Block  []byte
}

// Vote represents a vote for a proposal.
type Vote struct {
	Height int
	Voter  string
	Choice string
}

// HotStuff represents the HotStuff consensus algorithm.
type HotStuff struct {
	mu        sync.Mutex
	proposals map[int]*Proposal
	votes     map[int]map[string]string
	quorum    int
}

// NewHotStuff creates a new instance of the HotStuff consensus algorithm.
func NewHotStuff(quorum int) *HotStuff {
	return &HotStuff{
		proposals: make(map[int]*Proposal),
		votes:     make(map[int]map[string]string),
		quorum:    quorum,
	}
}

// Propose adds a new proposal to the consensus.
func (hs *HotStuff) Propose(height int, leader string, block []byte) error {
	hs.mu.Lock()
	defer hs.mu.Unlock()

	if _, exists := hs.proposals[height]; exists {
		return errors.New("proposal already exists")
	}

	hs.proposals[height] = &Proposal{
		Height: height,
		Leader: leader,
		Block:  block,
	}
	return nil
}

// Vote adds a vote for a proposal.
func (hs *HotStuff) Vote(height int, voter string, choice string) error {
	hs.mu.Lock()
	defer hs.mu.Unlock()

	if _, exists := hs.proposals[height]; !exists {
		return errors.New("proposal does not exist")
	}

	if hs.votes[height] == nil {
		hs.votes[height] = make(map[string]string)
	}

	hs.votes[height][voter] = choice

	if len(hs.votes[height]) >= hs.quorum {
		// Handle consensus reached
	}

	return nil
}

// GetProposal retrieves a proposal by height.
func (hs *HotStuff) GetProposal(height int) (*Proposal, error) {
	hs.mu.Lock()
	defer hs.mu.Unlock()

	proposal, exists := hs.proposals[height]
	if !exists {
		return nil, errors.New("proposal not found")
	}
	return proposal, nil
}

// StartHotStuff starts the HotStuff consensus algorithm.
func StartHotStuff(chain interface{}) {
	// TODO: implement consensus logic
}