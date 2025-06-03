// Cosmos SDK module skeleton for EduPay (Tuition Settlement)
package edupay

import (
	"github.com/cosmos/cosmos-sdk/types"
)

// AppModule implements the Cosmos SDK AppModule interface
// (register routes, handlers, etc.)
type AppModule struct{}

func NewAppModule() AppModule {
	return AppModule{}
}

func (am AppModule) Name() string { return "edupay" }

// RegisterInvariants, RegisterServices, etc. (implement as needed)
