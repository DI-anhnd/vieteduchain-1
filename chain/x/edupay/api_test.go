package edupay

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestSettleTuitionHandler(t *testing.T) {
	body := MsgSettleTuition{
		Payer:  "cosmos1payeraddress",
		School: "cosmos1schooladdress",
		Amount: amountMock(),
	}
	b, _ := json.Marshal(body)
	req := httptest.NewRequest("POST", "/settle-tuition", bytes.NewReader(b))
	w := httptest.NewRecorder()
	SettleTuitionHandler(w, req)
	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}
}

func TestReleaseTuitionHandler(t *testing.T) {
	body := MsgReleaseTuition{
		School: "cosmos1schooladdress",
		Amount: amountMock(),
		Proof:  "valid",
	}
	b, _ := json.Marshal(body)
	req := httptest.NewRequest("POST", "/release-tuition", bytes.NewReader(b))
	w := httptest.NewRecorder()
	ReleaseTuitionHandler(w, req)
	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}
}

func amountMock() MsgAmount {
	return MsgAmount{
		Denom:  "evnd",
		Amount: "1000000",
	}
}

// Mock types for test (if not defined elsewhere)
type MsgAmount struct {
	Denom  string `json:"denom"`
	Amount string `json:"amount"`
}

type MsgSettleTuition struct {
	Payer  string    `json:"payer"`
	School string    `json:"school"`
	Amount MsgAmount `json:"amount"`
}

type MsgReleaseTuition struct {
	School string    `json:"school"`
	Amount MsgAmount `json:"amount"`
	Proof  string    `json:"proof"`
}
