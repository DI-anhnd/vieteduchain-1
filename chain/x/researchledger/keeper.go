package researchledger

import (
	"github.com/cosmos/cosmos-sdk/types"
	"time"
)

type Keeper struct {
	bankKeeper types.BankKeeper
}

func NewKeeper(bankKeeper types.BankKeeper) Keeper {
	return Keeper{bankKeeper: bankKeeper}
}

// Store for hashes, NFTs, bounties
var (
	RegisteredHashes = make(map[string]RegisteredHash)
	DOINFTs         = make(map[string]DOINFT)
	Bounties        = make(map[string]PlagiarismBounty)
)

// Register a research hash
func (k Keeper) RegisterHash(ctx types.Context, creator, hash, fileType string) error {
	RegisteredHashes[hash] = RegisteredHash{
		Hash: hash,
		FileType: fileType,
		Timestamp: ctx.BlockTime(),
		Creator: creator,
	}
	return nil
}

// Mint a DOI NFT
func (k Keeper) MintDOINFT(ctx types.Context, creator, doi, cid string, authors []string) error {
	DOINFTs[doi] = DOINFT{
		DOI: doi,
		CID: cid,
		Authors: authors,
		Timestamp: ctx.BlockTime(),
		Owner: creator,
	}
	return nil
}

// Submit plagiarism bounty
func (k Keeper) SubmitPlagiarism(ctx types.Context, hunter, hash1, hash2, evidence string, reward types.Coin) error {
	key := hash1 + ":" + hash2
	Bounties[key] = PlagiarismBounty{
		Hunter: hunter,
		Hash1: hash1,
		Hash2: hash2,
		Reward: reward,
		Resolved: false,
	}
	// Lock reward in bounty pool (escrow)
	return k.bankKeeper.SendCoinsFromAccountToModule(ctx, types.AccAddress(hunter), "bounty_pool", types.NewCoins(reward))
}

// Resolve bounty (admin/manual for demo)
func (k Keeper) ResolveBounty(ctx types.Context, key string, winner string) error {
	bounty, ok := Bounties[key]
	if !ok || bounty.Resolved {
		return types.ErrUnknownRequest.Wrap("Bounty not found or already resolved")
	}
	bounty.Resolved = true
	Bounties[key] = bounty
	return k.bankKeeper.SendCoinsFromModuleToAccount(ctx, "bounty_pool", types.AccAddress(winner), types.NewCoins(bounty.Reward))
}
