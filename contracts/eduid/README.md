# EduID CosmWasm Smart Contract

## Chức năng
- Đăng ký, cập nhật, thu hồi DID (Self-Sovereign Identity)
- Lưu trữ hash/CID của DID Document (IPLD/IPFS)
- Truy vấn DID Document qua DID

## Thư mục
- `src/lib.rs`: Mã nguồn smart contract
- `Cargo.toml`: Thông tin package Rust

## Triển khai
1. Build contract:
   ```sh
   cd contracts/eduid
   cargo wasm
   ```
2. Deploy lên node wasmd:
   ```sh
   wasmd tx wasm store target/wasm32-unknown-unknown/release/eduid.wasm --from <key> --chain-id <chain-id>
   ```
3. Khởi tạo contract:
   ```sh
   wasmd tx wasm instantiate <code_id> '{}' --from <key> --label "EduID" --chain-id <chain-id>
   ```
4. Gửi message đăng ký DID:
   ```sh
   wasmd tx wasm execute <contract_addr> '{"register_did":{"did":"did:example:123","ipld_cid":"Qm...","hash":"..."}}' --from <key> --chain-id <chain-id>
   ```
5. Truy vấn DID:
   ```sh
   wasmd query wasm contract-state smart <contract_addr> '{"query_did":{"did":"did:example:123"}}'
   ```
