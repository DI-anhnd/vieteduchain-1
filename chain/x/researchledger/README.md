# ResearchLedger Module

## Chức năng chính
- Đăng ký băm SHA-256 của file nghiên cứu (PDF, CSV, Notebook...)
- Mint NFT chứa DOI và metadata (cid, authors, timestamp)
- Plagiarism bounty: thưởng token RESEARCH cho người phát hiện đạo văn

## API mẫu
- MsgRegisterHash: Đăng ký băm file
- MsgMintDOINFT: Mint NFT DOI
- MsgSubmitPlagiarism: Nộp cặp hash nghi đạo văn, nhận thưởng nếu đúng

## REST API
- POST /register-hash
- POST /mint-doi-nft
- POST /submit-plagiarism

## TODO
- Tích hợp kiểm tra hash trùng thực tế
- Tích hợp NFT module chuẩn Cosmos SDK
- Viết unit test cho module
