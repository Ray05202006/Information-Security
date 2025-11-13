#!/bin/bash

echo "=== Detailed Analysis of DH Parameters and Keys ==="
echo
echo "Let's examine ffdhe2048 in detail to understand the structure:"
echo

# Show full parameter details for ffdhe2048
echo "1. Full Parameter Details (ffdhe2048):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
openssl pkeyparam -in ffdhe2048.pem -text -noout | head -30

echo
echo "2. Full Key Details (ffdhe2048_key.pem):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
openssl pkey -in ffdhe2048_key.pem -text -noout | head -40

echo
echo "3. Public Key Sizes Comparison:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
printf "%-20s %15s %15s %15s\n" "Group" "Bit Size" "Public Key (bytes)" "Ratio"
printf "%-20s %15s %15s %15s\n" "────────────────────" "─────────────" "─────────────────" "─────────────"

for file in *_pubkey.der; do
    group=$(basename $file _pubkey.der)
    size=$(stat -c%s $file)
    
    # Get bit size from parameter file
    param_file="${group}.pem"
    if [ -f "$param_file" ]; then
        bits=$(openssl pkeyparam -in $param_file -text -noout 2>/dev/null | grep "DH Parameters:" | grep -oE '[0-9]+')
        if [ -n "$bits" ]; then
            ratio=$(echo "scale=2; $size / ($bits / 8)" | bc)
            printf "%-20s %15s %15s %15s\n" "$group" "$bits" "$size" "$ratio"
        fi
    fi
done

echo
echo "4. Understanding the Numbers:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "- Bit Size: The size of the prime modulus p"
echo "- Public Key (bytes): Total DER-encoded public key size"
echo "- Ratio: Public key bytes / (bits/8) - shows overhead from DER encoding"
echo "  (The overhead includes DER structure, algorithm identifiers, and parameters)"

