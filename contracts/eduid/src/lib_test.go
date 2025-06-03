package eduid

import (
	"encoding/json"
	"testing"
)

func TestRegisterAndQueryDID(t *testing.T) {
	RegisterDID("did:example:123", "QmCID", "hash123", "owner1")
	jsonStr, ok := QueryDID("did:example:123")
	if !ok {
		t.Fatal("DID not found after register")
	}
	var doc DIDDocument
	if err := json.Unmarshal([]byte(jsonStr), &doc); err != nil {
		t.Fatalf("Unmarshal error: %v", err)
	}
	if doc.DID != "did:example:123" || doc.IPLDCID != "QmCID" || doc.Hash != "hash123" || doc.Owner != "owner1" {
		t.Errorf("Unexpected DIDDocument: %+v", doc)
	}
}

func TestUpdateDID(t *testing.T) {
	RegisterDID("did:example:456", "QmOld", "oldhash", "owner2")
	ok := UpdateDID("did:example:456", "QmNew", "newhash", "owner2")
	if !ok {
		t.Fatal("UpdateDID failed")
	}
	jsonStr, ok := QueryDID("did:example:456")
	if !ok {
		t.Fatal("DID not found after update")
	}
	var doc DIDDocument
	_ = json.Unmarshal([]byte(jsonStr), &doc)
	if doc.IPLDCID != "QmNew" || doc.Hash != "newhash" {
		t.Errorf("Update failed: %+v", doc)
	}
}

func TestRevokeDID(t *testing.T) {
	RegisterDID("did:example:789", "QmCID", "hash789", "owner3")
	ok := RevokeDID("did:example:789", "owner3")
	if !ok {
		t.Fatal("RevokeDID failed")
	}
	_, ok = QueryDID("did:example:789")
	if ok {
		t.Error("DID should not exist after revoke")
	}
}

func TestUpdateDIDWrongOwner(t *testing.T) {
	RegisterDID("did:example:999", "QmCID", "hash999", "owner4")
	ok := UpdateDID("did:example:999", "QmNew", "newhash", "notowner")
	if ok {
		t.Error("UpdateDID should fail for wrong owner")
	}
}

func TestRevokeDIDWrongOwner(t *testing.T) {
	RegisterDID("did:example:888", "QmCID", "hash888", "owner5")
	ok := RevokeDID("did:example:888", "notowner")
	if ok {
		t.Error("RevokeDID should fail for wrong owner")
	}
}
