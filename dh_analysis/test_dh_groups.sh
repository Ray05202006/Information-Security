#!/bin/bash

echo "=== Testing RFC 7919 FFDHE Groups ==="
echo

# Test all FFDHE groups
for group in ffdhe2048 ffdhe3072 ffdhe4096 ffdhe6144 ffdhe8192; do
    echo "Testing group: $group"
    openssl genpkey -genparam -algorithm DH -pkeyopt dh_param:$group -out ${group}.pem 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Successfully generated parameters for $group"
        openssl pkeyparam -in ${group}.pem -text -noout 2>&1 | grep -E "(bit|GROUP)"
        echo
    else
        echo "✗ Failed to generate parameters for $group"
        echo
    fi
done

echo "=== Testing modp Groups (IKE/RFC 3526) ==="
echo

# Test modp groups
for group in modp_1536 modp_2048 modp_3072 modp_4096 modp_6144 modp_8192; do
    echo "Testing group: $group"
    openssl genpkey -genparam -algorithm DH -pkeyopt dh_param:$group -out ${group}.pem 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Successfully generated parameters for $group"
        openssl pkeyparam -in ${group}.pem -text -noout 2>&1 | grep -E "(bit|GROUP)"
        echo
    else
        echo "✗ Failed to generate parameters for $group"
        echo
    fi
done

echo "=== Testing Custom Bit Sizes ==="
echo

# Test custom bit sizes (these take longer to generate)
for bits in 512 1024 2048; do
    echo "Testing custom $bits-bit parameters (this may take a moment)..."
    timeout 30 openssl genpkey -genparam -algorithm DH -pkeyopt dh_paramgen_prime_len:$bits -out custom_${bits}.pem 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Successfully generated custom $bits-bit parameters"
        openssl pkeyparam -in custom_${bits}.pem -text -noout 2>&1 | grep -E "DH Parameters: \([0-9]+ bit\)"
        echo
    else
        echo "✗ Failed or timeout for custom $bits-bit parameters"
        echo
    fi
done

