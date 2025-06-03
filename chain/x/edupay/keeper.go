package edupay

import (
	"github.com/cosmos/cosmos-sdk/types"
)

type Keeper struct {
	bankKeeper types.BankKeeper
}

func NewKeeper(bankKeeper types.BankKeeper) Keeper {
	return Keeper{bankKeeper: bankKeeper}
}

// Example: Escrow settlement logic (simplified)
func (k Keeper) SettleTuition(ctx types.Context, payer, school types.AccAddress, amount types.Coin) error {
	// Lock funds from payer (escrow)
	if err := k.bankKeeper.SendCoinsFromAccountToModule(ctx, payer, "edupay_escrow", types.NewCoins(amount)); err != nil {
		return err
	}
	return nil
}

func (k Keeper) ReleaseTuition(ctx types.Context, school types.AccAddress, amount types.Coin) error {
	// Release funds to school
	return k.bankKeeper.SendCoinsFromModuleToAccount(ctx, "edupay_escrow", school, types.NewCoins(amount))
}
