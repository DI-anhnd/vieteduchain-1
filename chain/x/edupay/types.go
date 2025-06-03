package edupay

import (
	"github.com/cosmos/cosmos-sdk/types"
)

// MsgSettleTuition defines a message for tuition escrow
// (payer -> escrow)
type MsgSettleTuition struct {
	Payer  string      `json:"payer"`
	School string      `json:"school"`
	Amount types.Coin  `json:"amount"`
}

// MsgReleaseTuition defines a message for releasing escrow to school
type MsgReleaseTuition struct {
	School string      `json:"school"`
	Amount types.Coin  `json:"amount"`
	Proof  string      `json:"proof"`
}
