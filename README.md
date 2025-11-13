# Information Security - Diffie-Hellman Analysis

## 專案概述 (Project Overview)

本專案分析不同 Diffie-Hellman (DH) 群的公開金鑰大小，使用 OpenSSL 指令來檢查和比較 OpenSSL 中所有可用的 DH 參數。

This project analyzes the public key sizes of different Diffie-Hellman (DH) groups, using OpenSSL commands to examine and compare all available DH parameters in OpenSSL.

## 檔案結構 (File Structure)

```
.
├── README.md                           # 本檔案 (This file)
├── DH_OpenSSL_Groups_Analysis.md      # 完整的中文分析報告 (Full analysis report in Chinese)
└── dh_analysis/                       # 實驗資料目錄 (Experimental data directory)
    ├── RESULTS_SUMMARY.txt            # 結果摘要 (Results summary)
    ├── test_dh_groups.sh              # 測試所有 DH 群 (Test all DH groups)
    ├── generate_keypairs.sh           # 生成金鑰對 (Generate keypairs)
    ├── detailed_analysis.sh           # 詳細分析 (Detailed analysis)
    ├── examine_structure.sh           # 檢查 DER 結構 (Examine DER structure)
    ├── *.pem                          # DH 參數檔案 (DH parameter files)
    ├── *_key.pem                      # 私鑰檔案 (Private key files)
    └── *_pubkey.der                   # 公鑰檔案 (Public key files)
```

## 快速開始 (Quick Start)

### 查看結果 (View Results)

```bash
# 查看完整分析報告 (View full analysis report)
cat DH_OpenSSL_Groups_Analysis.md

# 查看結果摘要 (View results summary)
cat dh_analysis/RESULTS_SUMMARY.txt
```

### 重現實驗 (Reproduce Experiments)

```bash
cd dh_analysis

# 測試所有 DH 群 (Test all DH groups)
./test_dh_groups.sh

# 生成金鑰對並分析 (Generate keypairs and analyze)
./generate_keypairs.sh

# 詳細分析 (Detailed analysis)
./detailed_analysis.sh

# 檢查 DER 結構 (Examine DER structure)
./examine_structure.sh
```

## 主要發現 (Key Findings)

### 1. 公鑰大小公式 (Public Key Size Formula)

```
Public Key Size (bytes) ≈ 2 × (bit_size / 8) + DER_overhead
```

### 2. 支援的 DH 群 (Supported DH Groups)

**RFC 7919 FFDHE Groups (推薦/Recommended):**
- ffdhe2048, ffdhe3072, ffdhe4096, ffdhe6144, ffdhe8192

**RFC 3526 MODP Groups (舊版/Legacy):**
- modp_1536, modp_2048, modp_3072, modp_4096, modp_6144, modp_8192

### 3. 結果總表 (Results Table)

| 群組 (Group) | 位元 (Bits) | 公鑰大小 (Bytes) | 比率 (Ratio) |
|-------------|------------|-----------------|-------------|
| ffdhe2048   | 2048       | 553             | 2.16        |
| ffdhe3072   | 3072       | 808             | 2.10        |
| ffdhe4096   | 4096       | 1064            | 2.07        |
| ffdhe6144   | 6144       | 1576            | 2.05        |
| ffdhe8192   | 8192       | 2088            | 2.03        |

## 常用 OpenSSL 指令 (Common OpenSSL Commands)

```bash
# 1. 生成命名群參數 (Generate named group parameters)
openssl genpkey -genparam -algorithm DH \
    -pkeyopt dh_param:ffdhe2048 -out ffdhe2048.pem

# 2. 查看參數 (View parameters)
openssl pkeyparam -in ffdhe2048.pem -text -noout

# 3. 生成金鑰對 (Generate keypair)
openssl genpkey -paramfile ffdhe2048.pem -out key.pem

# 4. 查看金鑰 (View key)
openssl pkey -in key.pem -text -noout

# 5. 匯出公鑰 (Export public key)
openssl pkey -in key.pem -pubout -outform DER -out pubkey.der

# 6. 分析 DER 結構 (Analyze DER structure)
openssl asn1parse -in pubkey.der -inform DER
```

## 安全建議 (Security Recommendations)

- ✅ **建議使用 (Recommended)**: ≥2048 位元 (bits)
- ✅ **更佳選擇 (Better)**: 3072 位元 (bits)
- ❌ **不安全 (Insecure)**: ≤1536 位元 (bits)

## 系統需求 (System Requirements)

- OpenSSL 3.0 或更高版本 (or higher)
- Bash shell
- Linux/Unix 環境 (environment)

## 參考文獻 (References)

- [RFC 7919: Negotiated Finite Field Diffie-Hellman Ephemeral Parameters for TLS](https://tools.ietf.org/html/rfc7919)
- [RFC 3526: More Modular Exponential (MODP) Diffie-Hellman groups for IKE](https://tools.ietf.org/html/rfc3526)
- [OpenSSL Documentation](https://www.openssl.org/docs/)

## 作者 (Author)

資訊安全課程作業 (Information Security Course Assignment)

## 授權 (License)

Educational use only.
