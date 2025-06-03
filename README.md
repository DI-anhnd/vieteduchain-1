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

## Conclusion
VietEduChain aims to revolutionize the educational landscape in Vietnam by leveraging blockchain technology to create a secure, transparent, and efficient system for managing educational credentials and processes.