# VietEduChain Project

## Overview
VietEduChain is a Layer-1 blockchain solution specifically designed for the education sector in Vietnam. It aims to enhance transparency, security, and efficiency in educational processes through the use of blockchain technology.

## Objectives
1. **Infrastructure Performance**: Achieve a throughput of at least 30,000 transactions per second, with a finality time of approximately 1.2 seconds and transaction fees below 0.1% of the transaction value.
2. **International Data Standards**: Fully support Verifiable Credentials (VC) and Decentralized Identifiers (DID) as per W3C recommendations, and be ready for inter-blockchain communication (IBC).
3. **Comprehensive Educational Cycle**: Facilitate the entire educational process from credential issuance, enrollment, tuition payments, to research traceability, ensuring data transparency, security, and long-term scalability.

## Project Scope
### Core Components
- **Core Layer-1**: Implements HotStuff-PoAA, DAG mempool, Block-STM, and CosmWasm for performance and scalability.
- **Functional Modules**:
  - EduCert: Credential issuance and revocation.
  - EduID: Self-sovereign identity management.
  - EduPay: Tuition payment and scholarship handling.
  - ResearchLedger: Research integrity and plagiarism detection.
  - EduAdmission: Admission transparency.
- **API & SDK**: REST/gRPC, GraphQL, and JS/Flutter light-client for integration with LMS, admission portals, and mobile wallets.
- **Interoperability Infrastructure**: IBC relay, ICS-20 stablecoin bridge, and cross-chain seat transfer.
- **Monitoring Tools**: Prometheus + Grafana, BigDipper, and Cosmos-Graph indexer for real-time KPI measurement and data transparency.
- **Legal Framework & Compliance**: Adherence to PDPA Vietnam 2023, GDPR mapping, and Decree 13/2023 for personal data safety and international compatibility.

## Design Principles
- **Open-First**: Prioritize open-source development with Apache-2.0 or GPL-compatible licenses.
- **Interoperability by Design**: Ensure all modules are IBC compatible and adhere to JSON-LD/VC data standards.
- **Security & Privacy by Default**: Integrate Zero-Knowledge Proof (ZKP) for selective disclosure and end-to-end encryption of research data.
- **User-Centric**: Empower users with self-sovereign DID management and social recovery mechanisms for educational wallets.

## Functional Modules
Each module is implemented as an independent CosmWasm package (Rust smart contract) and can be upgraded using the Cosmos SDK migrate mechanism. Sensitive data is not stored on-chain; instead, only hashes and metadata are recorded.

## Migration & Troubleshooting Log (Cosmos SDK + CosmWasm)

### 1. Chuyển đổi kiến trúc
- Chuyển hệ thống từ backend tập trung sang blockchain phi tập trung sử dụng Cosmos SDK (Go) và CosmWasm (Rust smart contract).
- Tổ chức lại workspace, xóa backend cũ, tạo thư mục cho smart contract (CosmWasm) và Cosmos SDK module (Go).

### 2. Thiết lập Docker Compose
- Chỉ giữ lại các service blockchain cần thiết: node0, node1, relayer, prometheus, grafana.
- Loại bỏ explorer do không có image phù hợp.
- Sửa image node0, node1 thành cosmwasm/wasmd:v0.45.0 để đảm bảo CLI đầy đủ.

### 3. Khởi tạo chain & genesis
- Xóa dữ liệu node0, node1, khởi tạo lại genesis cho node0 bằng đúng image.
- Khởi tạo validator cho node0:
  - Tạo key: `wasmd keys add validator --keyring-backend test`
  - Thêm tài khoản vào genesis: `wasmd genesis add-genesis-account <address> 1000000000stake --keyring-backend test`
  - Tạo gentx: `wasmd genesis gentx validator 1000000000stake --chain-id <chain-id> --keyring-backend test --moniker node0`
  - Thu thập gentx: `wasmd genesis collect-gentxs`
- Copy genesis từ node0 sang node1, đảm bảo node1 join cùng chain.

### 4. Vận hành multi-node
- Nếu node0 báo lỗi `validator set is empty after InitGenesis`, cần đảm bảo đã add-genesis-account và gentx đúng, sau đó xóa data node0, reset lại state:
  - Dừng node0, xóa data: `Remove-Item -Recurse -Force ./data/node0/data`
  - Reset state: `wasmd tendermint unsafe-reset-all`
  - Khởi động lại node0.
- Nếu node1 báo lỗi thiếu genesis, copy lại file genesis.json từ node0.

### 5. Kiểm thử module nghiệp vụ
- Đã chuyển logic EduID sang Go (Cosmos SDK module), tạo file lib.go, lib_test.go, xóa code Rust.
- Tạo module Go cho Cosmos SDK (chain/x/eduid/...), hướng dẫn tích hợp vào app.go.
- Tạo unit test Go cho DID Registry.

### 6. Các lưu ý khác
- Cảnh báo `the attribute version is obsolete` trong docker-compose.yml có thể bỏ qua.
- Nếu node không lên, luôn kiểm tra log bằng `docker compose logs node0 --tail=50`.
- Đảm bảo các file keyring-test, priv_validator_key.json, priv_validator_state.json tồn tại đúng vị trí.

### 7. Các lưu ý khi build và chạy Docker
- Luôn kiểm tra version của Docker Engine và docker-compose, nên dùng bản mới để tránh lỗi không tương thích.
- Nếu gặp cảnh báo `the attribute version is obsolete` trong docker-compose.yml, có thể bỏ qua hoặc xóa dòng version khỏi file.
- Khi đổi image hoặc cấu trúc volume, nên xóa sạch dữ liệu cũ trong thư mục data/ để tránh lỗi state cũ không tương thích.
- Nếu service không lên, kiểm tra log bằng `docker compose logs <service> --tail=50` để xác định nguyên nhân.
- Khi chạy lệnh CLI với wasmd, nên dùng `docker compose run --rm node0 ...` thay vì exec nếu container node0 đang crash-loop.
- Đảm bảo các volume được mount đúng đường dẫn, đặc biệt là ./data/node0:/root/.wasmd và ./data/node1:/root/.wasmd.
- Nếu cần reset node, dùng lệnh `wasmd tendermint unsafe-reset-all` để xóa state blockchain mà không làm mất file cấu hình.
- Khi copy genesis.json giữa các node, đảm bảo file không bị chỉnh sửa thủ công gây lỗi định dạng.
- Nếu cần xóa orphan container, dùng `docker compose down --remove-orphans`.

### Bảng tổng hợp lỗi & cách xử lý

| STT | Lỗi gặp phải                                                                 | Nguyên nhân/chú thích                                                                                 | Cách xử lý                                                                                                 | Phương án xử lý thực tế đã thực hiện                                                                                 |
|-----|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| 1   | validator set is empty after InitGenesis                                     | Genesis chưa có validator/self-delegation hoặc chưa collect-gentxs đúng                               | Thực hiện add-genesis-account, gentx, collect-gentxs; nếu vẫn lỗi thì xóa data node0, reset lại state      | Đã chạy: wasmd genesis add-genesis-account, gentx, collect-gentxs; xóa data node0, reset state, khởi động lại node0 |
| 2   | couldn't read GenesisDoc file: .../genesis.json: no such file or directory   | Node1 chưa có file genesis.json hoặc file genesis bị lỗi                                              | Copy genesis.json từ node0 sang node1, đảm bảo đúng định dạng                                              | Đã copy genesis.json từ node0 sang node1 bằng PowerShell Copy-Item, xác nhận node1 join chain thành công           |
| 3   | service "node0" is not running                                             | Container node0 bị crash do lỗi genesis hoặc state                                                    | Kiểm tra log, fix genesis, xóa data, reset lại state, khởi động lại node0                                  | Đã kiểm tra log, xóa data node0, reset lại state, khởi động lại node0 bằng docker compose up -d node0              |
| 4   | unknown command "add-genesis-account" for "wasmd"                         | Dùng sai cú pháp, phải là `wasmd genesis add-genesis-account ...`                                     | Sử dụng đúng subcommand: `wasmd genesis add-genesis-account ...`                                           | Đã sửa lại lệnh đúng cú pháp: wasmd genesis add-genesis-account ...                                               |
| 5   | open /root/.wasmd/data/priv_validator_state.json: no such file or directory  | Xóa data node0 nhưng chưa init lại node hoặc chưa reset state                                         | Chạy `wasmd tendermint unsafe-reset-all` hoặc `wasmd init ...` để tạo lại file cần thiết                   | Đã chạy: wasmd tendermint unsafe-reset-all, sau đó khởi động lại node0                                         |
| 6   | Error: unknown command "unsafe-reset-all" for "wasmd"                     | Dùng sai namespace, phải là `wasmd tendermint unsafe-reset-all`                                       | Sử dụng đúng: `wasmd tendermint unsafe-reset-all`                                                          | Đã sửa lại lệnh đúng: wasmd tendermint unsafe-reset-all                                                          |
| 7   | Cảnh báo the attribute version is obsolete trong docker-compose.yml          | Docker Compose bản mới không cần trường version                                                       | Có thể bỏ qua hoặc xóa dòng version khỏi file docker-compose.yml                                           | Đã xác nhận cảnh báo không ảnh hưởng, không cần sửa, có thể xóa dòng version nếu muốn                            |
| 8   | Node không lên, không thấy log                                              | Có thể do volume mount sai, thiếu file cấu hình, hoặc state cũ không tương thích                      | Kiểm tra lại volume, xóa sạch data, đảm bảo file cấu hình/keyring đúng vị trí, kiểm tra log container      | Đã kiểm tra volume, xóa sạch data, xác nhận file cấu hình/keyring đúng vị trí, kiểm tra log container           |
| 9   | Crash-loop khi chạy CLI với exec                                            | Container node0 crash-loop nên không thể exec vào                                                     | Dùng `docker compose run --rm node0 ...` để chạy CLI trên container tạm thời                               | Đã dùng docker compose run --rm node0 ... để chạy các lệnh CLI khi node0 crash-loop                            |
| 10  | Lỗi khi copy genesis.json giữa các node                                     | File genesis bị chỉnh sửa thủ công hoặc copy sai                                                      | Đảm bảo copy đúng file, không chỉnh sửa thủ công, kiểm tra lại định dạng JSON                              | Đã copy đúng file genesis.json, không chỉnh sửa thủ công, xác nhận node1 nhận genesis thành công                |

---

## Conclusion
VietEduChain aims to revolutionize the educational landscape in Vietnam by leveraging blockchain technology to create a secure, transparent, and efficient system for managing educational credentials and processes.