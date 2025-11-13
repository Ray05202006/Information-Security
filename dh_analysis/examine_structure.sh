#!/bin/bash

echo "=== Examining DER Structure and Components ==="
echo

echo "1. DER Structure Analysis (ffdhe2048):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Using openssl asn1parse to show DER structure:"
echo
openssl asn1parse -in ffdhe2048_pubkey.der -inform DER | head -20

echo
echo "2. Complete Parameter Details (showing p and g):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "For custom_512 (smaller, easier to read):"
echo
openssl pkeyparam -in custom_512.pem -text -noout

echo
echo "3. Component Sizes in Public Key:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# For each group, show breakdown
for group in custom_512 ffdhe2048 ffdhe4096 ffdhe8192; do
    if [ -f "${group}_pubkey.der" ]; then
        echo "Group: $group"
        echo "ASN.1 Structure:"
        openssl asn1parse -in ${group}_pubkey.der -inform DER 2>/dev/null | grep -E "SEQUENCE|OBJECT|INTEGER|BIT STRING" | head -10
        echo
    fi
done

echo
echo "4. Explanation of DH Public Key Format:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat << 'EXPLAIN'
A DH public key in DER format contains:
1. Outer SEQUENCE
   ├─ Algorithm Identifier SEQUENCE
   │  ├─ OBJECT IDENTIFIER (dhKeyAgreement OID: 1.2.840.113549.1.3.1)
   │  └─ Parameters SEQUENCE
   │     ├─ INTEGER p (prime modulus - same size as bit length)
   │     └─ INTEGER g (generator - usually small, 2 or 5)
   └─ BIT STRING containing
      └─ INTEGER public-key value (y = g^x mod p, approximately same size as p)

The public key size is approximately 2 * (bit_size/8) plus DER overhead.
EXPLAIN

