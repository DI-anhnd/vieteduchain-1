package utils

import (
    "crypto/sha256"
    "encoding/hex"
)

// HashData takes a byte slice and returns its SHA-256 hash as a hexadecimal string.
func HashData(data []byte) string {
    hash := sha256.Sum256(data)
    return hex.EncodeToString(hash[:])
}

// HashString takes a string and returns its SHA-256 hash as a hexadecimal string.
func HashString(data string) string {
    return HashData([]byte(data))
}