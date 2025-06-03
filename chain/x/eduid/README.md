# EduID Cosmos SDK Module (Go)

## Chức năng
- Đăng ký, cập nhật, thu hồi DID (Self-Sovereign Identity)
- Lưu trữ hash/CID của DID Document (IPLD/IPFS)
- Truy vấn DID Document qua DID

## Thư mục
- `types.go`: Định nghĩa DIDDocument
- `keeper.go`: Lưu trữ/truy vấn DID
- `msgs.go`: Định nghĩa message
- `handler.go`: Xử lý message
- `module.go`: Đăng ký module với Cosmos SDK

## Tích hợp vào app
1. Thêm module vào `app.go`:
   - Import `x/eduid`
   - Khởi tạo keeper, handler, module basic
   - Đăng ký route, query
2. Build lại chain:
   ```sh
   cd chain
   go build -o vieteduchain
   ```
3. Khởi động lại node:
   ```sh
   ./vieteduchain start
   ```

## Sử dụng
- Gửi MsgRegisterDID, MsgUpdateDID, MsgRevokeDID qua CLI/REST/gRPC
- Truy vấn DID qua CLI/REST/gRPC
