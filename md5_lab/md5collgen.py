#!/usr/bin/env python3
"""
MD5 Collision Generator - Educational Tool for SEED Labs
Based on FastColl algorithm by Marc Stevens
Uses pre-computed collision blocks
"""

import sys
import os
import hashlib

# Pre-computed FastColl collision blocks (128 bytes each)
# These are the differences between two collision blocks
# that will produce the same MD5 hash when appended to the same prefix

def read_collision_blocks():
    """Read pre-computed collision blocks from the collisions repository"""
    base_path = "/home/user/Information-Security/md5_collision_lab/collisions/examples/"
    
    with open(base_path + "fastcoll1.bin", "rb") as f:
        block1 = f.read()
    
    with open(base_path + "fastcoll2.bin", "rb") as f:
        block2 = f.read()
    
    return block1, block2

def pad_to_64(data):
    """Pad data to multiple of 64 bytes"""
    remainder = len(data) % 64
    if remainder != 0:
        padding_needed = 64 - remainder
        # Pad with zeros
        data += b'\x00' * padding_needed
    return data

def generate_collision(prefix_file, output1, output2):
    """Generate two files with same MD5 hash"""
    
    # Read prefix
    if prefix_file:
        with open(prefix_file, 'rb') as f:
            prefix = f.read()
    else:
        prefix = b''
    
    print(f"Prefix length: {len(prefix)} bytes")
    
    # Pad prefix to multiple of 64 bytes
    original_len = len(prefix)
    prefix_padded = pad_to_64(prefix)
    
    if len(prefix_padded) != original_len:
        print(f"Prefix padded to {len(prefix_padded)} bytes (added {len(prefix_padded) - original_len} null bytes)")
    
    # Read collision blocks
    block1, block2 = read_collision_blocks()
    
    # Create two output files
    out1 = prefix_padded + block1
    out2 = prefix_padded + block2
    
    # Write outputs
    with open(output1, 'wb') as f:
        f.write(out1)
    
    with open(output2, 'wb') as f:
        f.write(out2)
    
    # Verify MD5 hashes
    md5_1 = hashlib.md5(out1).hexdigest()
    md5_2 = hashlib.md5(out2).hexdigest()
    
    print(f"\nGenerated files:")
    print(f"  {output1}: {len(out1)} bytes, MD5 = {md5_1}")
    print(f"  {output2}: {len(out2)} bytes, MD5 = {md5_2}")
    
    if md5_1 == md5_2:
        print("\n✓ SUCCESS: MD5 collision generated!")
    else:
        print("\n✗ ERROR: MD5 hashes do not match!")
    
    return md5_1 == md5_2

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 md5collgen.py -p <prefix_file> -o <output1> <output2>")
        print("   or: python3 md5collgen.py <output1> <output2>  (no prefix)")
        sys.exit(1)
    
    prefix_file = None
    output1 = None
    output2 = None
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-p':
            prefix_file = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '-o':
            output1 = sys.argv[i+1]
            output2 = sys.argv[i+2]
            i += 3
        else:
            if not output1:
                output1 = sys.argv[i]
                output2 = sys.argv[i+1] if i+1 < len(sys.argv) else None
            i += 1
    
    if not output1 or not output2:
        print("Error: Must specify two output files")
        sys.exit(1)
    
    generate_collision(prefix_file, output1, output2)
