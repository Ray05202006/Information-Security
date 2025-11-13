# MD5 Collision Attack Lab

This directory contains all files and demonstrations for the MD5 Collision Attack Lab based on the SEED Labs curriculum.

## Lab Overview

This lab demonstrates the practical security implications of MD5's broken collision-resistance property. Through hands-on experiments, we show how attackers can exploit MD5 collisions to:

1. Create different files with identical hashes
2. Bypass code signing mechanisms
3. Distribute malicious software with valid certificates

## Files and Directories

### Documentation
- `LAB_REPORT.md` - Comprehensive lab report with all findings and analysis
- `README.md` - This file

### Task 1: Basic MD5 Collisions
- `fastcoll1.bin`, `fastcoll2.bin` - Collision file pair (same MD5, different content)
- `task1_analysis.py` - Analysis script for Task 1
- Demonstrates 6-byte difference producing same MD5 hash

### Task 2: MD5 Concatenation Property
- `task2_demo.py` - Demonstration of MD5(M||T) = MD5(N||T) property
- `collision1_with_suffix.bin`, `collision2_with_suffix.bin` - Collision files with appended data
- `result1.bin`, `result2.bin` - Concatenation test results
- `test_suffix.txt` - Test suffix file

### Task 3: Executable Collisions
- `program.c`, `base_program.c` - C source files with 200-byte arrays
- `program`, `base_program` - Compiled executables
- `exec_v1`, `exec_v2` - Modified executables with collision blocks
- `task3_complete.py` - Automation script for Task 3
- `selfread.c`, `selfread` - Self-reading executable demo

### Task 4: Benign vs Malicious Programs
- `task4_program.c` - Source code with behavior-switching logic
- `task4_base` - Base executable
- `benign_program` - Version with benign behavior (X==Y)
- `malicious_program` - Version with malicious behavior (X!=Y)
- Demonstrates how same MD5 can mask different behaviors

### Collision Data
- `coll_block_1.bin`, `coll_block_2.bin` - 128-byte collision blocks
- `prefix.txt` - Example prefix file

### Utilities
- `md5collgen.py` - Python-based collision generator
- Various intermediate files from experiments

## Quick Start

### View Lab Report
```bash
cat LAB_REPORT.md
```

### Task 1: Verify MD5 Collision
```bash
md5sum fastcoll1.bin fastcoll2.bin
# Both show: 4f3e848ad8608d795ba4f5c81ea59c7e
```

### Task 2: Test Concatenation Property
```bash
python3 task2_demo.py
```

### Task 4: See Different Behaviors
```bash
./benign_program      # Shows benign output
./malicious_program   # Shows malicious warning
```

## Key Findings

### MD5 Collision Characteristics
- **Only 6 bytes differ** in 192-byte collision files
- All differences are **single-bit flips** (MSB toggled)
- Collision generation takes **seconds** with modern tools
- **128 bytes** of collision data required per collision

### Security Implications

1. **Code Signing Bypass**
   - Attacker creates benign + malicious versions
   - Both have same MD5 hash
   - Certificate valid for both!

2. **Supply Chain Attacks**
   - Malicious software passes hash verification
   - Update mechanisms compromised
   - Trust relationships exploited

3. **Real-World Impact**
   - Flame malware (2012) - Used MD5 collision for code signing
   - Rogue CA certificates
   - Document forgery

## Countermeasures

### What NOT to Do ❌
- ❌ Use MD5 for security-critical applications
- ❌ Rely solely on hash-based verification
- ❌ Assume different hashes mean different files

### What TO Do ✅
- ✅ Use SHA-256 or SHA-3 for cryptographic hashing
- ✅ Implement multi-factor verification
- ✅ Monitor for anomalous behavior
- ✅ Maintain binary transparency logs
- ✅ Update security policies to ban MD5

## Technical Details

### MD5 Algorithm
- **Block Size:** 64 bytes
- **Hash Size:** 128 bits (16 bytes)
- **Rounds:** 4 rounds of 16 operations each
- **Vulnerable to:** Collision attacks, chosen-prefix collisions

### Collision Attack Method (FastColl)
- **Technique:** Differential cryptanalysis
- **Time:** ~2 seconds on modern hardware
- **Requirements:** 128 bytes of collision data
- **Limitations:** Prefix-dependent (IHV state matters)

### Concatenation Property
Based on Merkle-Damgård construction:
```
IHV₀ → [Block 1] → IHV₁ → [Block 2] → IHV₂ → ... → Final Hash

If IHVₙ(M) = IHVₙ(N), then IHVₙ₊ₖ(M||T) = IHVₙ₊ₖ(N||T)
```

## Running the Lab

### Prerequisites
- GCC compiler
- Python 3
- md5sum utility
- Basic understanding of hashing and cryptography

### Lab Environment
- OS: Ubuntu 20.04
- Compiler: GCC 9.x or later
- Python: 3.8+

### Execution Order
1. Task 1: Basic collision understanding
2. Task 2: Property demonstration  
3. Task 3: Executable manipulation
4. Task 4: Behavior divergence attack

## Educational Purpose

⚠️ **IMPORTANT:** All techniques demonstrated are for educational purposes only. This lab teaches:

- Understanding of hash collision vulnerabilities
- Defensive security measures
- Importance of modern cryptographic standards
- Real-world attack scenarios (for prevention)

**DO NOT** use these techniques for:
- Malicious activities
- Unauthorized system access
- Bypassing security controls
- Creating actual malware

## References

1. Wang et al., "Collisions for Hash Functions MD4, MD5, HAVAL-128 and RIPEMD", CRYPTO 2004
2. Marc Stevens, "HashClash - MD5 & SHA-1 cryptanalytic toolbox"
3. Stevens et al., "The First Collision for Full SHA-1", 2017
4. SEED Labs, "MD5 Collision Attack Lab", Syracuse University
5. NIST SP 800-131A, "Transitioning the Use of Cryptographic Algorithms"

## Lab Completion Checklist

- [x] Task 1: Generated MD5 collision files
- [x] Task 1: Answered all questions about prefix length and byte differences
- [x] Task 2: Demonstrated concatenation property with multiple suffixes
- [x] Task 3: Created executables with collision blocks
- [x] Task 4: Built benign vs malicious program pair
- [x] Documented all findings in comprehensive report
- [x] Understood security implications

## Contact

For questions about this lab or security research:
- SEED Labs: https://seedsecuritylabs.org/
- HashClash Project: https://github.com/cr-marcstevens/hashclash

---

**Lab completed:** November 13, 2025  
**Environment:** Ubuntu 20.04 (Docker)  
**Status:** All tasks completed successfully ✓
