// DID Registry module for EduID (Go version)
// This file replaces the previous Rust CosmWasm contract with a Go Cosmos SDK module interface example.

package eduid

import (
	"encoding/json"
)

type DIDDocument struct {
	DID      string `json:"did"`
	IPLDCID  string `json:"ipld_cid"`
	Hash     string `json:"hash"`
	Owner    string `json:"owner"`
}

// Example: Register a DID (in-memory, for demo)
var didRegistry = map[string]DIDDocument{}

func RegisterDID(did, ipldCID, hash, owner string) {
	didRegistry[did] = DIDDocument{
		DID: did,
		IPLDCID: ipldCID,
		Hash: hash,
		Owner: owner,
	}
}

func UpdateDID(did, newIPLDCID, newHash, owner string) bool {
	doc, ok := didRegistry[did]
	if !ok || doc.Owner != owner {
		return false
	}
	doc.IPLDCID = newIPLDCID
	doc.Hash = newHash
	didRegistry[did] = doc
	return true
}

func RevokeDID(did, owner string) bool {
	doc, ok := didRegistry[did]
	if !ok || doc.Owner != owner {
		return false
	}
	delete(didRegistry, did)
	return true
}

func QueryDID(did string) (string, bool) {
	doc, ok := didRegistry[did]
	if !ok {
		return "", false
	}
	b, _ := json.Marshal(doc)
	return string(b), true
}
