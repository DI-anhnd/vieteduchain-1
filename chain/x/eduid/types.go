package eduid

import (
	"encoding/json"
	"github.com/cosmos/cosmos-sdk/types"
)

type DIDDocument struct {
	DID     string         `json:"did"`
	IPLDCID string         `json:"ipld_cid"`
	Hash    string         `json:"hash"`
	Owner   types.AccAddress `json:"owner"`
}
