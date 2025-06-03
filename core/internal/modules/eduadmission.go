package modules

import (
	"errors"
	"time"
)

// SeatNFT represents a seat in the admission process.
type SeatNFT struct {
	ID        string    `json:"id"`
	University string    `json:"university"`
	CandidateID string   `json:"candidate_id"`
	Score     float64   `json:"score"`
	CreatedAt time.Time `json:"created_at"`
}

// AdmissionManager manages the admission process.
type AdmissionManager struct {
	seatNFTs map[string]SeatNFT
}

// NewAdmissionManager creates a new AdmissionManager.
func NewAdmissionManager() *AdmissionManager {
	return &AdmissionManager{
		seatNFTs: make(map[string]SeatNFT),
	}
}

// MintSeatNFT mints a new SeatNFT for a candidate.
func (am *AdmissionManager) MintSeatNFT(university string, candidateID string, score float64) (SeatNFT, error) {
	if score < 0 {
		return SeatNFT{}, errors.New("invalid score")
	}

	id := generateNFTID(candidateID)
	seatNFT := SeatNFT{
		ID:        id,
		University: university,
		CandidateID: candidateID,
		Score:     score,
		CreatedAt: time.Now(),
	}

	am.seatNFTs[id] = seatNFT
	return seatNFT, nil
}

// BurnSeatNFT burns a SeatNFT when a candidate confirms their admission.
func (am *AdmissionManager) BurnSeatNFT(id string) error {
	if _, exists := am.seatNFTs[id]; !exists {
		return errors.New("seat NFT not found")
	}

	delete(am.seatNFTs, id)
	return nil
}

// generateNFTID generates a unique ID for the SeatNFT.
func generateNFTID(candidateID string) string {
	// Implement a unique ID generation logic here
	return candidateID // Placeholder for unique ID generation
}