# EduPay Module (Tuition Settlement)

## Chức năng chính
- Thanh toán học phí/học bổng qua stablecoin eVND (ICS-20).
- Escrow contract: Khoá tiền giữa payer và school, chỉ release khi có ProofOfEnrollment.
- Tích hợp oracle giá VNĐ/USDC (Band Protocol).

## Thành phần
- **CosmWasm contract**: contracts/edupay/src/lib.rs (escrow logic)
- **Cosmos SDK module**: chain/x/edupay/ (Go, escrow settlement, API)

## API mẫu (Cosmos SDK)
- MsgSettleTuition: Payer gửi tiền vào escrow
- MsgReleaseTuition: Release tiền cho school khi có proof

## Tích hợp
- ICS-20: Đảm bảo eVND là token IBC
- Oracle: Nhận giá VNĐ/USDC từ BandChain hoặc relayer

## TODO
- Viết unit test cho contract và module Go
- Tích hợp xác thực proof thực tế (EduID/EduCert)
- Viết REST/gRPC API cho frontend
