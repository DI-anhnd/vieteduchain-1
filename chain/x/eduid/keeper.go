package eduid

import (
	"github.com/cosmos/cosmos-sdk/store/prefix"
	"github.com/cosmos/cosmos-sdk/types"
	"github.com/cosmos/cosmos-sdk/codec"
	"github.com/cosmos/cosmos-sdk/store/types"
)

type Keeper struct {
	storeKey types.StoreKey
	cdc      codec.BinaryCodec
}

func NewKeeper(cdc codec.BinaryCodec, key types.StoreKey) Keeper {
	return Keeper{
		storeKey: key,
		cdc:      cdc,
	}
}

func (k Keeper) SetDID(ctx types.Context, doc DIDDocument) {
	store := prefix.NewStore(ctx.KVStore(k.storeKey), []byte("did/"))
	bz := k.cdc.MustMarshal(&doc)
	store.Set([]byte(doc.DID), bz)
}

func (k Keeper) GetDID(ctx types.Context, did string) (DIDDocument, bool) {
	store := prefix.NewStore(ctx.KVStore(k.storeKey), []byte("did/"))
	bz := store.Get([]byte(did))
	if bz == nil {
		return DIDDocument{}, false
	}
	var doc DIDDocument
	k.cdc.MustUnmarshal(bz, &doc)
	return doc, true
}

func (k Keeper) DeleteDID(ctx types.Context, did string) {
	store := prefix.NewStore(ctx.KVStore(k.storeKey), []byte("did/"))
	store.Delete([]byte(did))
}
