# Diffie-Hellman 群與公開金鑰大小分析

## 1. 實驗目的

本實驗旨在使用 OpenSSL 指令來檢查不同 Diffie-Hellman (DH) 群的公開金鑰大小，了解不同參數對金鑰大小的影響，並深入理解 DH 金鑰交換機制在不同群上的運作方式。

## 2. 背景知識

### 2.1 Diffie-Hellman 金鑰交換

Diffie-Hellman 是一種密鑰協商協議，允許雙方在不安全的通道上建立共享密鑰。其安全性基於離散對數問題的困難性。

**基本原理：**
- 選擇一個大質數 `p` (prime modulus) 和生成元 `g` (generator)
- Alice 選擇私鑰 `a`，計算公鑰 `A = g^a mod p`
- Bob 選擇私鑰 `b`，計算公鑰 `B = g^b mod p`
- 雙方交換公鑰後，共享密鑰為 `K = g^(ab) mod p`

### 2.2 不同的 DH 群

DH 可以在不同的群上運行，主要有：

1. **RFC 7919 FFDHE 群**：Finite Field Diffie-Hellman Ephemeral，現代標準推薦使用
2. **RFC 3526 MODP 群**：More Modular Exponential (MODP)，用於 IKE (Internet Key Exchange)
3. **自定義參數**：可以生成特定位元長度的自定義參數

## 3. 實驗方法

### 3.1 環境設置

```bash
# 檢查 OpenSSL 版本
openssl version
# OpenSSL 3.0.13 30 Jan 2024
```

### 3.2 測試 RFC 7919 FFDHE 群

RFC 7919 定義了五個標準的 FFDHE 群，分別為 2048、3072、4096、6144 和 8192 位元。

**指令流程：**

```bash
# 1. 生成 DH 參數（使用命名群）
openssl genpkey -genparam -algorithm DH \
    -pkeyopt dh_param:ffdhe2048 \
    -out ffdhe2048.pem

# 2. 查看參數詳細資訊
openssl pkeyparam -in ffdhe2048.pem -text -noout

# 3. 使用參數生成私鑰
openssl genpkey -paramfile ffdhe2048.pem \
    -out ffdhe2048_key.pem

# 4. 查看金鑰詳細資訊
openssl pkey -in ffdhe2048_key.pem -text -noout

# 5. 匯出公鑰（DER 格式）
openssl pkey -in ffdhe2048_key.pem \
    -pubout -outform DER \
    -out ffdhe2048_pubkey.der

# 6. 檢查公鑰大小
stat -c%s ffdhe2048_pubkey.der
```

### 3.3 測試 RFC 3526 MODP 群

MODP 群用於 IKE，提供 1536 到 8192 位元的群。

```bash
# 測試各個 MODP 群
for group in modp_1536 modp_2048 modp_3072 modp_4096 modp_6144 modp_8192; do
    openssl genpkey -genparam -algorithm DH \
        -pkeyopt dh_param:$group \
        -out ${group}.pem
done
```

### 3.4 測試自定義參數

可以生成任意位元長度的自定義 DH 參數。

```bash
# 生成自定義 512 位元參數
openssl genpkey -genparam -algorithm DH \
    -pkeyopt dh_paramgen_prime_len:512 \
    -out custom_512.pem

# 生成自定義 1024 位元參數
openssl genpkey -genparam -algorithm DH \
    -pkeyopt dh_paramgen_prime_len:1024 \
    -out custom_1024.pem
```

**注意：** 生成自定義參數需要較長時間，因為需要生成大質數並驗證其安全性。較大的位元長度（如 2048 或 4096）可能需要數分鐘。

### 3.5 分析公鑰結構

使用 `asn1parse` 分析 DER 編碼結構：

```bash
openssl asn1parse -in ffdhe2048_pubkey.der -inform DER
```

## 4. 實驗結果

### 4.1 所有群的測試結果總表

| 群名稱        | 位元大小 | 公鑰大小 (bytes) | 比率  | 類型           |
|--------------|---------|----------------|------|---------------|
| custom_512   | 512     | 157            | 2.45 | 自定義         |
| custom_1024  | 1024    | 291            | 2.27 | 自定義         |
| modp_1536    | 1536    | 420            | 2.18 | RFC 3526      |
| modp_2048    | 2048    | 552            | 2.15 | RFC 3526      |
| ffdhe2048    | 2048    | 553            | 2.16 | RFC 7919      |
| modp_3072    | 3072    | 808            | 2.10 | RFC 3526      |
| ffdhe3072    | 3072    | 808            | 2.10 | RFC 7919      |
| modp_4096    | 4096    | 1064           | 2.07 | RFC 3526      |
| ffdhe4096    | 4096    | 1064           | 2.07 | RFC 7919      |
| modp_6144    | 6144    | 1576           | 2.05 | RFC 3526      |
| ffdhe6144    | 6144    | 1576           | 2.05 | RFC 7919      |
| modp_8192    | 8192    | 2089           | 2.04 | RFC 3526      |
| ffdhe8192    | 8192    | 2088           | 2.03 | RFC 7919      |

**比率說明：** 比率 = 公鑰大小 (bytes) / (位元大小 / 8)

### 4.2 RFC 7919 FFDHE 群詳細結果

```
Group: ffdhe2048
  DH Parameters: (2048 bit)
  DH Private-Key: (2048 bit)
  Public key DER size: 553 bytes

Group: ffdhe3072
  DH Parameters: (3072 bit)
  DH Private-Key: (3072 bit)
  Public key DER size: 808 bytes

Group: ffdhe4096
  DH Parameters: (4096 bit)
  DH Private-Key: (4096 bit)
  Public key DER size: 1064 bytes

Group: ffdhe6144
  DH Parameters: (6144 bit)
  DH Private-Key: (6144 bit)
  Public key DER size: 1576 bytes

Group: ffdhe8192
  DH Parameters: (8192 bit)
  DH Private-Key: (8192 bit)
  Public key DER size: 2088 bytes
```

### 4.3 RFC 3526 MODP 群詳細結果

```
Group: modp_1536
  DH Parameters: (1536 bit)
  Public key DER size: 420 bytes

Group: modp_2048
  DH Parameters: (2048 bit)
  Public key DER size: 552 bytes

Group: modp_3072
  DH Parameters: (3072 bit)
  Public key DER size: 808 bytes

Group: modp_4096
  DH Parameters: (4096 bit)
  Public key DER size: 1064 bytes

Group: modp_6144
  DH Parameters: (6144 bit)
  Public key DER size: 1576 bytes

Group: modp_8192
  DH Parameters: (8192 bit)
  Public key DER size: 2089 bytes
```

### 4.4 公鑰 DER 結構分析

以 ffdhe2048 為例，公鑰的 ASN.1/DER 結構：

```
    0:d=0  hl=4 l= 549 cons: SEQUENCE          
    4:d=1  hl=4 l= 279 cons: SEQUENCE          
    8:d=2  hl=2 l=   9 prim: OBJECT            :dhKeyAgreement
   19:d=2  hl=4 l= 264 cons: SEQUENCE          
   23:d=3  hl=4 l= 257 prim: INTEGER           :p (2048 位元質數)
  284:d=3  hl=2 l=   1 prim: INTEGER           :g (生成元 = 2)
  287:d=1  hl=4 l= 262 prim: BIT STRING        (公鑰值 y = g^x mod p)
```

**結構說明：**

1. **外層 SEQUENCE**：整個公鑰結構
2. **演算法識別符 SEQUENCE**：
   - OBJECT IDENTIFIER：dhKeyAgreement (OID: 1.2.840.113549.1.3.1)
   - 參數 SEQUENCE：
     - INTEGER p：質數模數（與位元大小相同）
     - INTEGER g：生成元（通常是 2 或 5）
3. **BIT STRING**：包含實際的公鑰值
   - INTEGER：公鑰值 y = g^x mod p（大小接近 p）

### 4.5 自定義參數示例

以 custom_512 為例，顯示完整的參數：

```
DH Parameters: (512 bit)
P:   
    00:9e:97:1f:39:40:3d:88:28:67:b3:c9:6a:27:22:
    f4:af:b2:3f:25:2c:50:e8:0a:ad:ad:49:dc:50:ab:
    39:67:b4:6a:29:cd:4b:73:7b:b1:a0:22:27:ce:28:
    94:ee:5d:ab:16:79:9e:f0:8e:e4:f7:19:70:ad:b7:
    af:b5:67:71:e7
G:    2 (0x2)
```

其中：
- P 是 512 位元的質數
- G 是生成元，值為 2

## 5. 結果分析與討論

### 5.1 公鑰大小與位元長度的關係

從實驗結果可以觀察到：

1. **線性關係**：公鑰大小與位元長度呈線性關係
   - 位元大小每增加一倍，公鑰大小也大約增加一倍

2. **比率變化**：
   - 512 位元：比率 2.45（較高的 overhead）
   - 1024 位元：比率 2.27
   - 2048 位元：比率 2.15-2.16
   - 4096 位元：比率 2.07
   - 8192 位元：比率 2.03-2.04
   
   **原因**：較大的金鑰中，DER 編碼的固定 overhead（如 OID、SEQUENCE 標記等）相對於整體大小的比例較小。

3. **公式估算**：
   ```
   公鑰大小 ≈ 2 × (位元大小 / 8) + DER_overhead
   ```
   其中 DER_overhead 約為 30-50 bytes，主要包括：
   - ASN.1 結構標記
   - 長度欄位
   - OID (dhKeyAgreement)
   - 少量的其他元數據

### 5.2 為什麼公鑰大小約為位元長度的兩倍？

DH 公鑰實際上包含了兩個主要部分，每個都接近原始位元大小：

1. **參數（約等於位元大小）**：
   - 質數 p：正好是指定的位元大小
   - 生成元 g：非常小（通常是 2 或 5），可忽略

2. **公鑰值（約等於位元大小）**：
   - y = g^x mod p
   - 結果的大小最多為 p 的大小，平均約為位元大小

因此總大小 ≈ size(p) + size(y) ≈ 2 × 位元大小

### 5.3 FFDHE vs MODP 群的比較

從結果可以看出：

1. **相同位元大小的公鑰大小幾乎相同**
   - ffdhe2048 (553 bytes) vs modp_2048 (552 bytes)
   - ffdhe8192 (2088 bytes) vs modp_8192 (2089 bytes)

2. **主要差異在於質數的選擇**
   - FFDHE 使用的質數形式為 p = 2^n - 2^(n-64) - 1 + 2^64 × ⌊2^(n-130) × π⌋
   - MODP 使用不同的質數生成方式
   - 這些差異不影響金鑰的大小，但會影響安全性和性能

3. **安全性建議**
   - RFC 7919 FFDHE 群是現代標準推薦
   - MODP 群主要用於向後兼容

### 5.4 OpenSSL 中可用的所有 DH 群

通過測試，OpenSSL 3.0.13 支援以下命名群：

**RFC 7919 FFDHE 群：**
- ffdhe2048
- ffdhe3072
- ffdhe4096
- ffdhe6144
- ffdhe8192

**RFC 3526 MODP 群：**
- modp_1536
- modp_2048
- modp_3072
- modp_4096
- modp_6144
- modp_8192

**自定義參數：**
- 可使用 `dh_paramgen_prime_len` 選項生成任意位元長度

### 5.5 安全性考量

1. **最小位元長度建議**：
   - 目前建議至少使用 2048 位元
   - 3072 位元提供更好的長期安全性
   - 1536 位元及以下已被認為不安全

2. **性能與安全性權衡**：
   - 較大的群提供更好的安全性
   - 但會增加計算時間和傳輸大小
   - 2048-3072 位元是目前的最佳實踐平衡點

## 6. 結論

本實驗通過 OpenSSL 指令詳細檢查了不同 DH 群的公開金鑰大小，主要發現：

1. **公鑰大小規律**：
   - 公鑰大小約為參數位元長度的 2 倍（以位元組計算）
   - 這是因為公鑰包含了參數（質數 p）和公鑰值（y = g^x mod p）

2. **OpenSSL 支援的群**：
   - RFC 7919 FFDHE：5 個群（2048-8192 位元）
   - RFC 3526 MODP：6 個群（1536-8192 位元）
   - 自定義參數：任意位元長度

3. **實用建議**：
   - 使用 RFC 7919 FFDHE 群作為首選
   - 最小使用 2048 位元，推薦 3072 位元
   - 避免使用自定義參數，除非有特殊需求

4. **實驗技能**：
   - 掌握了使用 OpenSSL 生成和分析 DH 參數的方法
   - 了解了 DER 編碼結構和 ASN.1 解析
   - 建立了對 DH 金鑰交換機制在不同群上運作的深入理解

## 7. 參考資料

- RFC 7919: Negotiated Finite Field Diffie-Hellman Ephemeral Parameters for Transport Layer Security (TLS)
- RFC 3526: More Modular Exponential (MODP) Diffie-Hellman groups for Internet Key Exchange (IKE)
- OpenSSL Documentation: https://www.openssl.org/docs/
- NIST SP 800-56A Rev. 3: Recommendation for Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography

## 附錄：完整測試腳本

實驗中使用的完整測試腳本位於 `dh_analysis/` 目錄：

- `test_dh_groups.sh`：測試所有 DH 群
- `generate_keypairs.sh`：生成金鑰對並分析大小
- `detailed_analysis.sh`：詳細分析公鑰結構
- `examine_structure.sh`：檢查 DER 編碼結構

所有參數檔案（.pem）和公鑰檔案（.der）也保存在該目錄中供查驗。
