#!/bin/bash

echo "=== Generating DH Key Pairs and Analyzing Public Key Sizes ==="
echo

# Function to generate keypair and analyze
analyze_group() {
    local group=$1
    local param_file="${group}.pem"
    local key_file="${group}_key.pem"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Group: $group"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ -f "$param_file" ] && [ -s "$param_file" ]; then
        # Generate private key
        openssl genpkey -paramfile $param_file -out $key_file 2>/dev/null
        
        # Show parameter details
        echo "Parameters:"
        openssl pkeyparam -in $param_file -text -noout 2>/dev/null | grep -E "(DH Parameters|GROUP|prime:|generator:)" | head -4
        
        echo
        echo "Generated Key Information:"
        # Show key details
        openssl pkey -in $key_file -text -noout 2>/dev/null | grep -E "(DH Private-Key:|public-key:)" | head -2
        
        # Get public key size in bytes
        openssl pkey -in $key_file -pubout -outform DER -out ${group}_pubkey.der 2>/dev/null
        pubkey_size=$(stat -c%s ${group}_pubkey.der 2>/dev/null)
        echo "Public key DER size: $pubkey_size bytes"
        
        # Extract just the public key value size
        openssl pkey -in $key_file -text -noout 2>/dev/null | grep -A 100 "public-key:" | grep -E "^    [0-9a-f]" | wc -l | xargs echo "Public key value lines:"
        
        echo
    fi
}

# Analyze all FFDHE groups
echo "═══════════════════════════════════════════════════════════"
echo "RFC 7919 FFDHE Groups"
echo "═══════════════════════════════════════════════════════════"
echo

for group in ffdhe2048 ffdhe3072 ffdhe4096 ffdhe6144 ffdhe8192; do
    analyze_group $group
done

echo
echo "═══════════════════════════════════════════════════════════"
echo "RFC 3526 MODP Groups"
echo "═══════════════════════════════════════════════════════════"
echo

for group in modp_1536 modp_2048 modp_3072 modp_4096 modp_6144 modp_8192; do
    analyze_group $group
done

echo
echo "═══════════════════════════════════════════════════════════"
echo "Custom Generated Parameters"
echo "═══════════════════════════════════════════════════════════"
echo

for bits in 512 1024; do
    analyze_group "custom_${bits}"
done

