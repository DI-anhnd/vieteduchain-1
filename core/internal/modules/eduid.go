package modules

import (
    "errors"
    "sync"
)

// EduID represents a self-sovereign identity structure.
type EduID struct {
    DID         string // Decentralized Identifier
    PublicKey   string // Public key associated with the DID
    Service     string // Service endpoint for the identity
}

// EduIDManager manages the self-sovereign identities.
type EduIDManager struct {
    mu    sync.RWMutex
    store map[string]*EduID // Store of EduIDs indexed by DID
}

// NewEduIDManager creates a new EduIDManager.
func NewEduIDManager() *EduIDManager {
    return &EduIDManager{
        store: make(map[string]*EduID),
    }
}

// CreateEduID creates a new EduID and stores it.
func (m *EduIDManager) CreateEduID(did, publicKey, service string) (*EduID, error) {
    m.mu.Lock()
    defer m.mu.Unlock()

    if _, exists := m.store[did]; exists {
        return nil, errors.New("EduID already exists")
    }

    eduID := &EduID{
        DID:       did,
        PublicKey: publicKey,
        Service:   service,
    }
    m.store[did] = eduID
    return eduID, nil
}

// GetEduID retrieves an EduID by its DID.
func (m *EduIDManager) GetEduID(did string) (*EduID, error) {
    m.mu.RLock()
    defer m.mu.RUnlock()

    eduID, exists := m.store[did]
    if !exists {
        return nil, errors.New("EduID not found")
    }
    return eduID, nil
}

// RevokeEduID revokes an EduID by its DID.
func (m *EduIDManager) RevokeEduID(did string) error {
    m.mu.Lock()
    defer m.mu.Unlock()

    if _, exists := m.store[did]; !exists {
        return errors.New("EduID not found")
    }

    delete(m.store, did)
    return nil
}