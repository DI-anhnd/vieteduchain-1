package eduid

import (
	"github.com/cosmos/cosmos-sdk/types/module"
)

type AppModuleBasic struct{}

func (AppModuleBasic) Name() string { return "eduid" }

func (AppModuleBasic) RegisterCodec(cdc *codec.LegacyAmino) {}

func (AppModuleBasic) DefaultGenesis(cdc codec.JSONCodec) json.RawMessage {
	return cdc.MustMarshalJSON(struct{}{})
}

func (AppModuleBasic) ValidateGenesis(cdc codec.JSONCodec, config client.TxEncodingConfig, bz json.RawMessage) error {
	return nil
}

// ...implement other required methods for AppModuleBasic and AppModule as needed...
