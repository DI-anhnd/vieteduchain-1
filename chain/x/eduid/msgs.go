package eduid

import (
	"github.com/cosmos/cosmos-sdk/types"
)

type MsgRegisterDID struct {
	DID     string         `json:"did"`
	IPLDCID string         `json:"ipld_cid"`
	Hash    string         `json:"hash"`
	Owner   types.AccAddress `json:"owner"`
}

type MsgUpdateDID struct {
	DID        string         `json:"did"`
	NewIPLDCID string         `json:"new_ipld_cid"`
	NewHash    string         `json:"new_hash"`
	Owner      types.AccAddress `json:"owner"`
}

type MsgRevokeDID struct {
	DID   string         `json:"did"`
	Owner types.AccAddress `json:"owner"`
}
