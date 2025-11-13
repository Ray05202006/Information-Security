#!/usr/bin/env python3
"""
Task 2: Understanding MD5's Property
Demonstrating that if MD5(M) = MD5(N), then MD5(M||T) = MD5(N||T)
"""

import hashlib

def md5_hash(data):
    """Calculate MD5 hash"""
    return hashlib.md5(data).hexdigest()

print("=" * 70)
print("TASK 2: Demonstrating MD5's Concatenation Property")
print("=" * 70)

# Load the collision files M and N
with open('fastcoll1.bin', 'rb') as f:
    M = f.read()
with open('fastcoll2.bin', 'rb') as f:
    N = f.read()

print("\nProperty to Demonstrate:")
print("  If MD5(M) = MD5(N), then MD5(M || T) = MD5(N || T)")
print("  where || represents concatenation and T is any suffix")

print("\n1. Verify initial condition: MD5(M) = MD5(N)")
hash_M = md5_hash(M)
hash_N = md5_hash(N)
print(f"   MD5(M) = {hash_M}")
print(f"   MD5(N) = {hash_N}")
print(f"   Equal: {hash_M == hash_N} ✓")

# Test with different suffixes
suffixes = [
    (b"Hello World!", "Text suffix: 'Hello World!'"),
    (b"SEED Lab MD5 Collision Test\n", "Text with newline"),
    (b"A" * 100, "100 'A' characters"),
    (b"\x00\x01\x02\x03\x04\x05", "Binary data"),
    (b"The quick brown fox jumps over the lazy dog", "Long text"),
    (b"", "Empty suffix (edge case)"),
]

print("\n2. Testing with various suffixes T:")
print("-" * 70)

all_passed = True
for i, (suffix, description) in enumerate(suffixes, 1):
    # Concatenate suffix to both files
    M_T = M + suffix
    N_T = N + suffix
    
    # Calculate hashes
    hash_M_T = md5_hash(M_T)
    hash_N_T = md5_hash(N_T)
    
    # Check if they match
    match = hash_M_T == hash_N_T
    all_passed = all_passed and match
    
    print(f"\nTest {i}: {description}")
    print(f"   Suffix length: {len(suffix)} bytes")
    print(f"   MD5(M || T) = {hash_M_T}")
    print(f"   MD5(N || T) = {hash_N_T}")
    print(f"   Match: {match} {'✓' if match else '✗'}")

# Save examples to files for verification
print("\n3. Creating example files for verification:")
test_suffix = b"SEED Labs - MD5 Collision Property Demo\n"
file_M_T = M + test_suffix
file_N_T = N + test_suffix

with open('collision1_with_suffix.bin', 'wb') as f:
    f.write(file_M_T)
with open('collision2_with_suffix.bin', 'wb') as f:
    f.write(file_N_T)

print(f"   Created: collision1_with_suffix.bin ({len(file_M_T)} bytes)")
print(f"   Created: collision2_with_suffix.bin ({len(file_N_T)} bytes)")
print(f"   MD5 of collision1_with_suffix.bin: {md5_hash(file_M_T)}")
print(f"   MD5 of collision2_with_suffix.bin: {md5_hash(file_N_T)}")

# Verify with cat command approach
print("\n4. Verification using file concatenation (simulating 'cat' command):")
suffix_file = "test_suffix.txt"
with open(suffix_file, 'wb') as f:
    f.write(test_suffix)

print(f"   Created suffix file: {suffix_file}")
print(f"   Command equivalent: cat fastcoll1.bin test_suffix.txt > result1.bin")
print(f"   Command equivalent: cat fastcoll2.bin test_suffix.txt > result2.bin")

# Create the concatenated files
with open('result1.bin', 'wb') as f:
    f.write(M + test_suffix)
with open('result2.bin', 'wb') as f:
    f.write(N + test_suffix)

hash_result1 = md5_hash(M + test_suffix)
hash_result2 = md5_hash(N + test_suffix)

print(f"   MD5 of result1.bin: {hash_result1}")
print(f"   MD5 of result2.bin: {hash_result2}")
print(f"   Match: {hash_result1 == hash_result2} ✓")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
if all_passed:
    print("✓ ALL TESTS PASSED!")
    print("The property MD5(M || T) = MD5(N || T) holds for all tested suffixes.")
    print("This demonstrates a fundamental property of MD5 and other hash functions")
    print("based on the Merkle-Damgård construction.")
else:
    print("✗ Some tests failed!")

print("\nWhy this property holds:")
print("MD5 processes data in 64-byte blocks sequentially. The hash of each")
print("block depends only on that block and the hash of the previous block.")
print("Since M and N produce the same hash (same final state), appending")
print("the same suffix T will process identical blocks in the same state,")
print("resulting in the same final hash.")
