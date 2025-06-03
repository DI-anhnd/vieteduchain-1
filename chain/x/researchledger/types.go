package researchledger

import (
	"github.com/cosmos/cosmos-sdk/types"
	"time"
)

// 1. Data Fingerprint
// MsgRegisterHash: Đăng ký băm SHA-256 của file nghiên cứu
// (hash có thể là PDF, CSV, Notebook...)
type MsgRegisterHash struct {
	Creator   string    `json:"creator"`
	Hash      string    `json:"hash"`
	FileType  string    `json:"file_type"`
	Timestamp time.Time `json:"timestamp"`
}

type RegisteredHash struct {
	Hash      string    `json:"hash"`
	FileType  string    `json:"file_type"`
	Timestamp time.Time `json:"timestamp"`
	Creator   string    `json:"creator"`
}

// 2. DOI-NFT
// MsgMintDOINFT: Mint NFT chứa DOI và metadata
// (cid: content id, authors, timestamp)
type MsgMintDOINFT struct {
	Creator   string    `json:"creator"`
	DOI       string    `json:"doi"`
	CID       string    `json:"cid"`
	Authors   []string  `json:"authors"`
	Timestamp time.Time `json:"timestamp"`
}

type DOINFT struct {
	DOI       string    `json:"doi"`
	CID       string    `json:"cid"`
	Authors   []string  `json:"authors"`
	Timestamp time.Time `json:"timestamp"`
	Owner     string    `json:"owner"`
}

// 3. Plagiarism Bounty
// MsgSubmitPlagiarism: Nộp cặp hash nghi đạo văn, nhận thưởng nếu đúng
type MsgSubmitPlagiarism struct {
	Hunter    string    `json:"hunter"`
	Hash1     string    `json:"hash1"`
	Hash2     string    `json:"hash2"`
	Evidence  string    `json:"evidence"`
}

type PlagiarismBounty struct {
	Hunter    string    `json:"hunter"`
	Hash1     string    `json:"hash1"`
	Hash2     string    `json:"hash2"`
	Reward    types.Coin `json:"reward"`
	Resolved  bool      `json:"resolved"`
}
