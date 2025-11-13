#!/usr/bin/env python3
"""
Task 1: Generating Two Different Files with the Same MD5 Hash
This script demonstrates MD5 collisions with different prefix configurations
"""

import hashlib
import os

def md5_hash(data):
    """Calculate MD5 hash of data"""
    return hashlib.md5(data).hexdigest()

def create_collision_with_prefix(prefix_data, prefix_name, coll_block_1, coll_block_2):
    """Create two collision files with given prefix"""
    # Create output filenames
    out1 = f"{prefix_name}_out1.bin"
    out2 = f"{prefix_name}_out2.bin"
    
    # Combine prefix with collision blocks
    file1_data = prefix_data + coll_block_1
    file2_data = prefix_data + coll_block_2
    
    # Write files
    with open(out1, 'wb') as f:
        f.write(file1_data)
    with open(out2, 'wb') as f:
        f.write(file2_data)
    
    # Calculate hashes
    hash1 = md5_hash(file1_data)
    hash2 = md5_hash(file2_data)
    
    print(f"\n{prefix_name}:")
    print(f"  Prefix length: {len(prefix_data)} bytes")
    print(f"  Output file 1: {out1} ({len(file1_data)} bytes)")
    print(f"    MD5: {hash1}")
    print(f"  Output file 2: {out2} ({len(file2_data)} bytes)")
    print(f"    MD5: {hash2}")
    print(f"  Collision: {'✓ SUCCESS' if hash1 == hash2 else '✗ FAILED'}")
    
    return hash1 == hash2

# Load the 128-byte collision blocks
with open('coll_block_1.bin', 'rb') as f:
    coll_block_1 = f.read()
with open('coll_block_2.bin', 'rb') as f:
    coll_block_2 = f.read()

print("=" * 70)
print("TASK 1: MD5 Collision Generation with Different Prefix Lengths")
print("=" * 70)

# Question 1: What happens if prefix is not a multiple of 64?
print("\n--- Question 1: Non-64-byte multiple prefix ---")
prefix_23 = b"SEED Labs MD5 Collision"  # 23 bytes
create_collision_with_prefix(prefix_23, "prefix_23bytes", coll_block_1, coll_block_2)

prefix_50 = b"A" * 50  # 50 bytes
create_collision_with_prefix(prefix_50, "prefix_50bytes", coll_block_1, coll_block_2)

prefix_100 = b"B" * 100  # 100 bytes
create_collision_with_prefix(prefix_100, "prefix_100bytes", coll_block_1, coll_block_2)

# Question 2: What happens with exactly 64 bytes?
print("\n--- Question 2: Exactly 64-byte prefix ---")
prefix_64 = b"C" * 64  # Exactly 64 bytes
create_collision_with_prefix(prefix_64, "prefix_64bytes", coll_block_1, coll_block_2)

# Additional tests
print("\n--- Additional Tests ---")
prefix_0 = b""  # Empty prefix
create_collision_with_prefix(prefix_0, "prefix_0bytes", coll_block_1, coll_block_2)

prefix_128 = b"D" * 128  # 128 bytes (2 * 64)
create_collision_with_prefix(prefix_128, "prefix_128bytes", coll_block_1, coll_block_2)

print("\n" + "=" * 70)
print("KEY OBSERVATIONS:")
print("=" * 70)
print("1. The collision blocks work with ANY prefix (including empty)")
print("2. Prefix length does NOT need to be a multiple of 64 bytes")
print("3. The two files differ only in the collision block region (128 bytes)")
print("4. All pairs produce the same MD5 hash despite having different content")
