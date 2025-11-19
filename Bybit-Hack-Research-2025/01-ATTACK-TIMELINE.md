# Bybit Hack - Complete Attack Timeline (2025)

## 📋 Executive Summary

**Date:** February 21, 2025
**Loss Amount:** $1.4+ Billion USD (401,347 ETH + additional assets)
**Attack Type:** Supply Chain Attack + Social Engineering + Smart Contract Exploitation
**Attribution:** Lazarus Group (North Korean state-sponsored APT)
**Target:** Bybit Exchange Cold Wallet (via Safe{Wallet} compromise)

---

## 🕐 Detailed Timeline

### Phase 1: Initial Compromise (Early February 2025)

#### **February 4, 2025** - Developer Machine Compromise
- **Target:** Safe{Wallet} developer's macOS workstation compromised
- **Method:** Suspected social engineering vector
- **Evidence:**
  - Docker project named "MC-Based-Stock-Invest-Simulator-main" found in `~/Downloads` folder
  - Initiated network traffic to malicious domain: `getstockprice[.]com`
  - Suggests victim was tricked into downloading/running malicious Docker container

#### **February 19, 2025** - Malicious Code Injection
- **Action:** Attackers modified JavaScript resources in Safe{Wallet} infrastructure
- **Target:** Safe{Wallet}'s web interface served via AWS (Amazon Web Services)
- **Method:** Injected malicious JavaScript code into the transaction approval UI
- **Characteristic:** Code was designed to activate ONLY for Bybit wallet transactions (targeted attack)

---

### Phase 2: Attack Execution (February 21, 2025)

#### **14:15 UTC** - Test Transaction
- **Amount:** 90 USDT
- **Purpose:** Verify successful bypass of security controls
- **Significance:** Confirmed attackers had full control over transaction signing process

#### **14:16 UTC** - Main Theft Executed
- **Assets Stolen:**
  - 401,347 ETH
  - 90,375 stETH (Staked Ethereum)
  - 15,000 cmETH (Compound ETH)
  - 8,000 mETH (Mantle ETH)
- **Total Value:** ~$1.4 billion USD
- **Method:** Malicious smart contract executed via delegatecall
- **Victim Action:** 3+ authorized Bybit signers unknowingly approved the malicious transaction

#### **14:18 UTC** - Cover-Up Operations
- **Action:** Attackers removed malicious code from Safe{Wallet} web interface
- **Purpose:**
  - Cover tracks
  - Preserve attack vector for potential future use
  - Delay forensic investigation

#### **15:51 UTC** - Public Disclosure
- **Action:** Bybit officially acknowledged the attack via X (Twitter)
- **Response Time:** 82 minutes from theft to public acknowledgment

---

### Phase 3: Post-Attack (February 21+)

#### **Immediate Aftermath**
- Safe{Wallet} team initiated emergency response
- Complete infrastructure rebuild
- All credentials rotated
- AWS infrastructure reconfigured

#### **Forensic Investigation**
- Sygnia and NCC Group conducted independent investigations
- Public web archives (Wayback Machine) confirmed code injection and removal
- No evidence of Bybit infrastructure compromise found
- Root cause confirmed: Safe{Wallet} supply chain compromise

#### **Fund Dispersal**
- Lazarus Group began laundering stolen funds through:
  - Multiple wallet addresses
  - Decentralized exchanges (DEXs)
  - Cryptocurrency mixers/tumblers
  - Cross-chain bridges

---

## 🎯 Attack Kill Chain

```
[Feb 4] Social Engineering
    ↓
Developer Downloads Malicious Docker Container
    ↓
Workstation Compromise (macOS)
    ↓
[Feb 19] Persistent Access to Safe{Wallet} Infrastructure
    ↓
Malicious JS Code Injection (AWS-hosted Safe UI)
    ↓
[Feb 21 14:15] Test Transaction (90 USDT)
    ↓
[Feb 21 14:16] Signers Approve What Appears as Routine Transfer
    ↓
delegatecall Executes Malicious Smart Contract
    ↓
Contract Overwrites Storage SLOT[0] (Transfer Address)
    ↓
Sweep Functions Transfer All Assets to Attacker Wallets
    ↓
[14:18] Attackers Remove Malicious Code
    ↓
[15:51] Bybit Discovers and Announces Breach
```

---

## 📊 Impact Metrics

| Metric | Value |
|--------|-------|
| **Total Loss** | $1.4+ Billion USD |
| **Attack Duration** | ~3 minutes (test + execution) |
| **Preparation Time** | ~17 days (Feb 4 - Feb 21) |
| **Detection Time** | 82 minutes |
| **Number of Signers Deceived** | 3+ (multisig requirement) |
| **Crypto Ranking** | Largest cryptocurrency theft in history |

---

## 🔍 Key Indicators of Compromise (IOCs)

### Network Indicators
- Domain: `getstockprice[.]com`
- Malicious Docker container: "MC-Based-Stock-Invest-Simulator-main"

### Behavioral Indicators
- Unexpected Docker network activity to external domains
- Modifications to Safe{Wallet} JavaScript resources on Feb 19
- Unusual transaction patterns: test transaction followed by massive withdrawal

### Smart Contract Indicators
- delegatecall to unauthorized contract address
- SLOT[0] storage overwrite in Safe multisig contract
- Sweep function executions in malicious contract

---

## 📚 References

- NCC Group: "In-Depth Technical Analysis of the Bybit Hack"
- Sygnia: "Investigation into the Bybit Hack"
- Bybit Official Timeline and FAQs
- Chainalysis: "Collaboration in the Wake of Record-Breaking Bybit Theft"
- Multiple security researchers and blockchain forensics firms

---

**Note:** This timeline is compiled from publicly available information from cybersecurity firms, blockchain analytics companies, and official statements. It represents the current understanding of events based on forensic investigations.
