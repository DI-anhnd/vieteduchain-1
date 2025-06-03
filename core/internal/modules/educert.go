package modules

import (
    "encoding/json"
    "errors"
    "sync"
)

// EduCert represents the structure for issuing and revoking verifiable credentials.
type EduCert struct {
    sync.Mutex
    credentials map[string]Credential
}

// Credential represents a verifiable credential.
type Credential struct {
    ID     string `json:"id"`
    Issuer string `json:"issuer"`
    Subject string `json:"subject"`
    Type   string `json:"type"`
    Status string `json:"status"`
}

// NewEduCert initializes a new EduCert module.
func NewEduCert() *EduCert {
    return &EduCert{
        credentials: make(map[string]Credential),
    }
}

// IssueCredential issues a new verifiable credential.
func (ec *EduCert) IssueCredential(credential Credential) error {
    ec.Lock()
    defer ec.Unlock()

    if _, exists := ec.credentials[credential.ID]; exists {
        return errors.New("credential already exists")
    }

    ec.credentials[credential.ID] = credential
    return nil
}

// RevokeCredential revokes an existing verifiable credential.
func (ec *EduCert) RevokeCredential(id string) error {
    ec.Lock()
    defer ec.Unlock()

    if _, exists := ec.credentials[id]; !exists {
        return errors.New("credential not found")
    }

    credential := ec.credentials[id]
    credential.Status = "revoked"
    ec.credentials[id] = credential
    return nil
}

// GetCredential retrieves a verifiable credential by ID.
func (ec *EduCert) GetCredential(id string) (Credential, error) {
    ec.Lock()
    defer ec.Unlock()

    credential, exists := ec.credentials[id]
    if !exists {
        return Credential{}, errors.New("credential not found")
    }

    return credential, nil
}

// MarshalJSON customizes the JSON output for EduCert.
func (ec *EduCert) MarshalJSON() ([]byte, error) {
    ec.Lock()
    defer ec.Unlock()

    return json.Marshal(ec.credentials)
}