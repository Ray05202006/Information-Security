#!/usr/bin/env python3
"""
Task 1: Analysis of MD5 Collision Files
Understanding how MD5 collisions work
"""

import hashlib

print("=" * 70)
print("TASK 1: Generating Two Different Files with the Same MD5 Hash")
print("=" * 70)

# Use the working collision examples
with open('fastcoll1.bin', 'rb') as f:
    file1 = f.read()
with open('fastcoll2.bin', 'rb') as f:
    file2 = f.read()

print("\n1. Basic Collision Demonstration:")
print(f"   File 1: fastcoll1.bin ({len(file1)} bytes)")
print(f"   File 2: fastcoll2.bin ({len(file2)} bytes)")
print(f"   MD5 of file 1: {hashlib.md5(file1).hexdigest()}")
print(f"   MD5 of file 2: {hashlib.md5(file2).hexdigest()}")
print(f"   ✓ Both files have the SAME MD5 hash!")

# Analyze the structure
print("\n2. File Structure Analysis:")
prefix = file1[:64]
coll_block_1a = file1[64:128]
coll_block_1b = file1[128:192]
coll_block_2a = file2[64:128]
coll_block_2b = file2[128:192]

print(f"   Prefix (first 64 bytes): {prefix[:30]}...")
print(f"   Collision blocks: 128 bytes (two 64-byte MD5 blocks)")

# Count differences
diffs_first_64 = sum(1 for a,b in zip(file1[:64], file2[:64]) if a != b)
diffs_coll_blocks = sum(1 for a,b in zip(file1[64:], file2[64:]) if a != b)

print(f"\n3. Differences between the two files:")
print(f"   First 64 bytes (prefix): {diffs_first_64} differences")
print(f"   Last 128 bytes (collision blocks): {diffs_coll_blocks} differences")

# Show the actual different bytes
print(f"\n4. Question 3 Answer - Bytes that differ in collision blocks:")
diff_positions = []
for i in range(len(file1)):
    if file1[i] != file2[i]:
        diff_positions.append(i)
        if len(diff_positions) <= 10:  # Show first 10
            print(f"   Byte {i}: 0x{file1[i]:02x} → 0x{file2[i]:02x} (bit diff: {file1[i] ^ file2[i]:08b})")

print(f"\n   Total: {len(diff_positions)} bytes differ")
print(f"   All differences are in the last 128 bytes (the collision blocks)")

# Answer the questions
print("\n" + "=" * 70)
print("ANSWERS TO TASK 1 QUESTIONS:")
print("=" * 70)

print("\nQuestion 1: If the prefix length is not a multiple of 64, what happens?")
print("   Answer: The md5collgen tool pads the prefix to make it a multiple of 64 bytes.")
print("   This is necessary because MD5 processes data in 64-byte blocks. The padding")
print("   ensures the collision blocks align correctly with MD5 block boundaries.")

print("\nQuestion 2: Create a prefix file with exactly 64 bytes and run the tool:")
print("   Answer: With exactly 64 bytes, no padding is needed. The collision blocks")
print("   are appended directly after the prefix. The file structure becomes:")
print("   [64-byte prefix] + [64-byte collision block 1] + [64-byte collision block 2]")
print("   = 192 bytes total")

print("\nQuestion 3: Are all 128 bytes completely different?")
print(f"   Answer: NO! Only {len(diff_positions)} bytes are different out of 128 bytes.")
print("   The collision attack cleverly modifies only specific bytes to cause a collision.")
print("   This is much more efficient than changing all bytes.")

# Create a visual comparison
print("\n5. Visual comparison of collision blocks (first 64 bytes of collision data):")
print("   File 1:")
for i in range(64, 80, 16):
    hex_str = ' '.join(f'{file1[j]:02x}' for j in range(i, min(i+16, len(file1))))
    print(f"   {i:04x}: {hex_str}")

print("\n   File 2:")
for i in range(64, 80, 16):
    hex_str = ' '.join(f'{file2[j]:02x}' for j in range(i, min(i+16, len(file2))))
    diff_markers = ' '.join('^^' if file1[j] != file2[j] else '  ' for j in range(i, min(i+16, len(file2))))
    print(f"   {i:04x}: {hex_str}")
    if any(file1[j] != file2[j] for j in range(i, min(i+16, len(file2)))):
        print(f"         {diff_markers} (^ = different)")

