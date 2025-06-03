package edupay

import (
	"encoding/json"
	"net/http"
	"github.com/cosmos/cosmos-sdk/types"
)

// REST API: Settle Tuition (payer gửi tiền vào escrow)
func SettleTuitionHandler(w http.ResponseWriter, r *http.Request) {
	var req MsgSettleTuition
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	// TODO: Lấy context, keeper từ app
	// ctx := ...
	// keeper := ...
	// result, err := HandleMsgSettleTuition(ctx, keeper, req)
	// if err != nil {
	// 	http.Error(w, err.Error(), http.StatusInternalServerError)
	// 	return
	// }
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"result": "settle tuition request accepted (mock)"}`))
}

// REST API: Release Tuition (release tiền cho school khi có proof)
func ReleaseTuitionHandler(w http.ResponseWriter, r *http.Request) {
	var req MsgReleaseTuition
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	// TODO: Lấy context, keeper từ app
	// ctx := ...
	// keeper := ...
	// result, err := HandleMsgReleaseTuition(ctx, keeper, req)
	// if err != nil {
	// 	http.Error(w, err.Error(), http.StatusInternalServerError)
	// 	return
	// }
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"result": "release tuition request accepted (mock)"}`))
}
