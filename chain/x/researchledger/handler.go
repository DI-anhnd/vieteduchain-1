package researchledger

import (
	"github.com/cosmos/cosmos-sdk/types"
)

// Handle MsgRegisterHash
func HandleMsgRegisterHash(ctx types.Context, k Keeper, msg MsgRegisterHash) (*types.Result, error) {
	err := k.RegisterHash(ctx, msg.Creator, msg.Hash, msg.FileType)
	if err != nil {
		return nil, err
	}
	return &types.Result{}, nil
}

// Handle MsgMintDOINFT
func HandleMsgMintDOINFT(ctx types.Context, k Keeper, msg MsgMintDOINFT) (*types.Result, error) {
	err := k.MintDOINFT(ctx, msg.Creator, msg.DOI, msg.CID, msg.Authors)
	if err != nil {
		return nil, err
	}
	return &types.Result{}, nil
}

// Handle MsgSubmitPlagiarism
func HandleMsgSubmitPlagiarism(ctx types.Context, k Keeper, msg MsgSubmitPlagiarism) (*types.Result, error) {
	reward := types.NewCoin("research", types.NewInt(1000)) // fixed reward for demo
	err := k.SubmitPlagiarism(ctx, msg.Hunter, msg.Hash1, msg.Hash2, msg.Evidence, reward)
	if err != nil {
		return nil, err
	}
	return &types.Result{}, nil
}
