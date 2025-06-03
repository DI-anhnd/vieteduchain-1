package eduid

import (
	"context"
	"github.com/cosmos/cosmos-sdk/types"
)

func NewHandler(k Keeper) types.Handler {
	return func(ctx types.Context, msg types.Msg) (*types.Result, error) {
		switch msg := msg.(type) {
		case *MsgRegisterDID:
			doc := DIDDocument{
				DID:     msg.DID,
				IPLDCID: msg.IPLDCID,
				Hash:    msg.Hash,
				Owner:   msg.Owner,
			}
			k.SetDID(ctx, doc)
			return &types.Result{Events: ctx.EventManager().Events()}, nil
		case *MsgUpdateDID:
			doc, found := k.GetDID(ctx, msg.DID)
			if !found || !doc.Owner.Equals(msg.Owner) {
				return nil, types.ErrUnauthorized.Wrap("not owner or not found")
			}
			doc.IPLDCID = msg.NewIPLDCID
			doc.Hash = msg.NewHash
			k.SetDID(ctx, doc)
			return &types.Result{Events: ctx.EventManager().Events()}, nil
		case *MsgRevokeDID:
			doc, found := k.GetDID(ctx, msg.DID)
			if !found || !doc.Owner.Equals(msg.Owner) {
				return nil, types.ErrUnauthorized.Wrap("not owner or not found")
			}
			k.DeleteDID(ctx, msg.DID)
			return &types.Result{Events: ctx.EventManager().Events()}, nil
		default:
			return nil, types.ErrUnknownRequest.Wrap("unrecognized eduid message type")
		}
	}
}
