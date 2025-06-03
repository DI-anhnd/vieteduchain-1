package edupay

import (
	"context"
	"github.com/cosmos/cosmos-sdk/types"
)

// Handle MsgSettleTuition (payer gửi tiền vào escrow)
func HandleMsgSettleTuition(ctx types.Context, k Keeper, msg MsgSettleTuition) (*types.Result, error) {
	payer, err := types.AccAddressFromBech32(msg.Payer)
	if err != nil {
		return nil, err
	}
	school, err := types.AccAddressFromBech32(msg.School)
	if err != nil {
		return nil, err
	}
	err = k.SettleTuition(ctx, payer, school, msg.Amount)
	if err != nil {
		return nil, err
	}
	return &types.Result{}, nil
}

// Handle MsgReleaseTuition (release tiền cho school khi có proof)
func HandleMsgReleaseTuition(ctx types.Context, k Keeper, msg MsgReleaseTuition) (*types.Result, error) {
	school, err := types.AccAddressFromBech32(msg.School)
	if err != nil {
		return nil, err
	}
	// TODO: verify proof (integration with EduID/EduCert)
	if msg.Proof != "valid" {
		return nil, types.ErrUnknownRequest.Wrap("Invalid proof")
	}
	err = k.ReleaseTuition(ctx, school, msg.Amount)
	if err != nil {
		return nil, err
	}
	return &types.Result{}, nil
}
