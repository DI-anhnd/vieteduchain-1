package researchledger

import (
	"encoding/json"
	"net/http"
)

// REST API: Register research hash
func RegisterHashHandler(w http.ResponseWriter, r *http.Request) {
	var req MsgRegisterHash
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	// TODO: call handler
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"result": "register hash accepted (mock)"}`))
}

// REST API: Mint DOI NFT
func MintDOINFTHandler(w http.ResponseWriter, r *http.Request) {
	var req MsgMintDOINFT
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	// TODO: call handler
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"result": "mint DOI NFT accepted (mock)"}`))
}

// REST API: Submit plagiarism bounty
func SubmitPlagiarismHandler(w http.ResponseWriter, r *http.Request) {
	var req MsgSubmitPlagiarism
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	// TODO: call handler
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"result": "plagiarism bounty submitted (mock)"}`))
}
