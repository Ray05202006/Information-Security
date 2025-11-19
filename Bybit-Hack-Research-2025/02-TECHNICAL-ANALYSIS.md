# Bybit Hack - Deep Technical Analysis

## 🎯 Attack Vector Overview

The Bybit hack represents a sophisticated **supply chain attack** that combined multiple exploitation techniques:

1. **Social Engineering** → Initial Access
2. **Developer Workstation Compromise** → Persistence
3. **Infrastructure Injection** → Code Manipulation
4. **UI Manipulation** → Trust Exploitation
5. **Smart Contract Exploitation** → Fund Extraction

---

## 🔓 Phase 1: Initial Access & Compromise

### Social Engineering Attack

#### Target Selection
- **Victim:** Safe{Wallet} developer with access to production infrastructure
- **Platform:** macOS workstation
- **Attack Vector:** Malicious Docker container

#### Delivery Mechanism
```
Attacker Creates Legitimate-Looking Project:
  "MC-Based-Stock-Invest-Simulator-main"

Likely Distribution Channels:
  • GitHub repository (cloned/forked)
  • Professional networking (LinkedIn)
  • Direct messaging with "collaboration" pretext
  • Fake job interview technical challenge

Victim Actions:
  1. Downloads project to ~/Downloads
  2. Executes Docker container (docker-compose up / docker run)
  3. Container establishes C2 connection to getstockprice[.]com
```

#### Technical Indicators
```bash
# Malicious Docker container characteristics:
Location: ~/Downloads/MC-Based-Stock-Invest-Simulator-main/
Network Activity: Outbound connection to getstockprice[.]com
Timeline: February 4, 2025

# What the container likely contained:
- Backdoor payload
- Credential harvester
- Keylogger
- AWS credential stealer (for Safe{Wallet} infrastructure access)
```

### Workstation Compromise Details

**macOS Exploitation:**
```
Potential Persistence Mechanisms:
  • LaunchAgent/LaunchDaemon installation
  • Shell profile modification (.zshrc, .bash_profile)
  • Docker container auto-restart configuration
  • SSH key theft (for AWS/GitHub access)
  • Browser cookie/token extraction

Critical Assets Targeted:
  • AWS IAM credentials
  • GitHub personal access tokens
  • SSH private keys
  • Safe{Wallet} deployment credentials
  • Development environment secrets
```

---

## 🕸️ Phase 2: Infrastructure Infiltration

### AWS Infrastructure Compromise

#### Access Method
```
Developer Workstation Compromise
        ↓
Extract AWS Credentials (IAM keys/temporary tokens)
        ↓
Access Safe{Wallet} AWS Infrastructure
        ↓
Identify Web Hosting Configuration (S3/CloudFront/EC2)
        ↓
Inject Malicious JavaScript into UI Assets
```

#### Injection Point
- **Target:** Safe{Wallet} web interface (React/JavaScript application)
- **Hosting:** Amazon Web Services (likely S3 + CloudFront CDN)
- **Modified Files:** JavaScript bundles/modules served to users
- **Modification Date:** February 19, 2025

### Malicious Code Injection

#### Targeted Injection Strategy
```javascript
// Simplified representation of malicious code logic

// The injected code was highly targeted - only activated for Bybit
function isTargetWallet(walletAddress) {
  const BYBIT_WALLET_ADDRESS = "0x[Bybit's Cold Wallet Address]";
  return walletAddress === BYBIT_WALLET_ADDRESS;
}

// Hook into transaction approval flow
if (isTargetWallet(currentWallet)) {
  // Intercept and modify transaction data
  interceptTransactionApproval();
}
```

#### UI Manipulation Technique
```javascript
// What Bybit signers SAW:
Transaction Details:
  From: Bybit Cold Wallet (0xAAA...)
  To: Bybit Internal Wallet (0xBBB...)
  Amount: [Routine Internal Transfer]
  Function: transferOwnership() or similar
  Status: ✅ Verified Safe Transaction

// What was ACTUALLY submitted to blockchain:
Transaction Details:
  From: Bybit Cold Wallet (0xAAA...)
  To: Malicious Contract (0xEVIL...)
  Amount: ALL ASSETS
  Function: delegatecall to attacker contract
  Status: ⚠️ MALICIOUS - Control Handover
```

---

## ⛓️ Phase 3: Smart Contract Exploitation

### Safe{Wallet} Multisig Architecture

#### How Safe{Wallet} Multisig Works (Normal Operation)
```solidity
// Simplified Safe Multisig Contract Structure
contract SafeMultisig {
    address[] public owners;          // List of authorized signers
    uint256 public threshold;         // Required approvals (e.g., 3 of 5)
    mapping(bytes32 => uint256) approvals;

    function executeTransaction(
        address to,
        uint256 value,
        bytes data,
        Enum.Operation operation  // CALL or DELEGATECALL
    ) public {
        require(approvals[txHash] >= threshold);

        if (operation == Enum.Operation.CALL) {
            // Normal external call
            to.call{value: value}(data);
        } else if (operation == Enum.Operation.DELEGATECALL) {
            // Execute code in context of Safe contract
            to.delegatecall(data);
        }
    }
}
```

### The Malicious Contract

#### Attack Smart Contract Structure
```solidity
// Attacker's malicious contract (simplified)
contract MaliciousContract {
    // CRITICAL: This variable occupies SLOT[0] in storage
    address public _transfer;

    // Constructor sets attacker's address
    constructor() {
        _transfer = msg.sender; // Attacker's wallet
    }

    // This function is called via delegatecall
    function executePayload() external {
        // When executed via delegatecall from Safe contract:
        // - Code runs in Safe contract's context
        // - Storage writes affect Safe contract's storage
        // - This overwrites SLOT[0] of Safe contract

        _transfer = msg.sender; // Overwrites critical Safe storage
    }

    // Sweep functions to extract funds
    function sweepETH() external {
        payable(_transfer).transfer(address(this).balance);
    }

    function sweepERC20(address token) external {
        IERC20(token).transfer(_transfer, IERC20(token).balanceOf(address(this)));
    }
}
```

### Storage Slot Manipulation Attack

#### Understanding delegatecall Vulnerability
```
delegatecall Behavior:
  • Executes code from Contract B in context of Contract A
  • Uses Contract A's storage
  • Uses Contract A's msg.sender and msg.value
  • Storage slots are determined by variable declaration order

The Exploit:
  Safe Contract SLOT[0]: [Critical Control Variable]
  Malicious Contract SLOT[0]: address _transfer

  When Safe executes delegatecall(MaliciousContract.executePayload):
    → Malicious code writes to SLOT[0]
    → Overwrites Safe's critical control variable
    → Transfers control to attacker
```

#### Visual Representation
```
BEFORE delegatecall:
Safe Contract Storage:
  SLOT[0]: [Owner/Module Address: 0xLEGIT...]
  SLOT[1]: [Threshold Value]
  SLOT[2]: [...]

AFTER malicious delegatecall:
Safe Contract Storage:
  SLOT[0]: [ATTACKER ADDRESS: 0xEVIL...] ← OVERWRITTEN!
  SLOT[1]: [Threshold Value]
  SLOT[2]: [...]

Result: Attacker now has control over the Safe contract
```

---

## 💸 Phase 4: Fund Extraction

### Transaction Execution Flow

#### Step-by-Step Fund Drain
```
1. Test Transaction (14:15 UTC)
   Transaction:
     - Amount: 90 USDT
     - Purpose: Verify exploit success
     - Result: ✅ Successful

2. Main Theft (14:16 UTC)
   First delegatecall:
     - Overwrites storage SLOT[0]
     - Grants attacker control

   Subsequent calls to sweep functions:
     - sweepETH() → 401,347 ETH
     - sweepERC20(stETH) → 90,375 stETH
     - sweepERC20(cmETH) → 15,000 cmETH
     - sweepERC20(mETH) → 8,000 mETH

   Total Time: < 1 minute
```

#### Blockchain Transaction Details
```
Test Transaction:
  Block: ~[block number]
  From: Bybit Cold Wallet (via multisig)
  To: Malicious Contract
  Value: 90 USDT
  Gas Used: [standard]
  Status: Success ✅

Main Theft Transaction:
  Block: ~[block number + few blocks]
  From: Bybit Cold Wallet (via multisig)
  To: Malicious Contract (delegatecall)
  Value: 0 ETH (but triggers sweeps)
  Internal Transactions:
    → 401,347 ETH to Attacker Wallet 1
    → 90,375 stETH to Attacker Wallet 2
    → 15,000 cmETH to Attacker Wallet 3
    → 8,000 mETH to Attacker Wallet 4
  Gas Used: [high due to multiple token transfers]
  Status: Success ✅
```

---

## 🧹 Phase 5: Cover-Up & Evidence Removal

### Code Removal Strategy

#### Timeline
```
14:16 UTC: Theft executed
14:18 UTC: Malicious code removed from Safe{Wallet} UI
```

#### Why Remove Code?
1. **Delay Discovery:** Forensic investigation harder without live sample
2. **Preserve Attack Vector:** Could potentially reuse same method
3. **Reduce Attribution:** Less evidence of specific techniques
4. **Create Confusion:** Makes incident response more difficult

#### Forensic Evidence
```bash
# Investigators used public web archives to prove code injection/removal
# Example Wayback Machine analysis:

Feb 19, 2025 - Malicious JS present:
  https://web.archive.org/web/[timestamp]/safe-wallet.io/app.js
  → Contains malicious transaction interception code

Feb 21, 2025 14:18+ - Malicious JS removed:
  https://web.archive.org/web/[timestamp]/safe-wallet.io/app.js
  → Clean version restored
```

---

## 🔬 Technical Deep Dives

### 1. Why Multisig Didn't Protect Bybit

```
Expected Security:
  Multiple signers review transaction → Catch suspicious activity

Why It Failed:
  ✗ UI showed legitimate-looking transaction details
  ✗ All signers saw the same manipulated interface
  ✗ No independent verification of actual blockchain transaction
  ✗ Trust in Safe{Wallet} infrastructure was implicit
  ✗ delegatecall risks not apparent in UI
```

### 2. delegatecall Security Risks

```solidity
// Why delegatecall is dangerous:

// SAFE usage:
contract A {
    uint256 public value;

    function safeCall(address lib) external {
        lib.call(abi.encodeWithSignature("doSomething()"));
        // 'lib' executes in its own context - cannot modify A's storage
    }
}

// UNSAFE usage:
contract A {
    uint256 public value;

    function unsafeCall(address lib) external {
        lib.delegatecall(abi.encodeWithSignature("doSomething()"));
        // 'lib' executes in A's context - CAN modify A's storage!
    }
}
```

### 3. Supply Chain Attack Surface

```
Trust Dependencies in This Attack:
  User → Safe{Wallet} UI
  Safe{Wallet} UI → AWS Infrastructure
  AWS Infrastructure → Developer Credentials
  Developer Credentials → Developer Workstation Security
  Developer Workstation → Developer Vigilance

Broken Link: Developer Workstation (social engineering)
Result: Entire chain compromised
```

---

## 🛡️ Detection Opportunities (Missed)

### Where This Could Have Been Stopped

#### 1. Developer Workstation (Feb 4)
```
❌ No EDR/XDR alert on:
  - Unusual Docker network activity
  - Connection to getstockprice[.]com
  - Credential access attempts

✅ Should have had:
  - Network monitoring with DNS filtering
  - Endpoint detection for suspicious containers
  - AWS credential access alerts
```

#### 2. AWS Infrastructure (Feb 19)
```
❌ No alert on:
  - Unauthorized modification of production JavaScript
  - Changes to web assets without deployment pipeline
  - Unusual IAM credential usage

✅ Should have had:
  - S3 object modification alerts
  - CloudTrail monitoring for unusual API calls
  - Immutable infrastructure with code signing
```

#### 3. Transaction Approval (Feb 21)
```
❌ No warning on:
  - delegatecall operation in transaction
  - High-value transfer from cold wallet
  - Destination address not in whitelist

✅ Should have had:
  - Hardware wallet with on-device transaction verification
  - Automated smart contract analysis before approval
  - Mandatory waiting period for large cold wallet transfers
  - Out-of-band verification of transaction details
```

---

## 🎓 Key Technical Lessons

### 1. Supply Chain Security
- Every dependency is a potential attack vector
- Third-party wallet providers need stringent security
- Developer workstation security is critical infrastructure

### 2. Smart Contract Security
- delegatecall should be heavily restricted
- Storage slot manipulation is a real threat
- UI cannot be trusted for transaction verification

### 3. Defense in Depth
- Multiple layers of security all failed
- Need independent verification at multiple stages
- Trust but verify - especially for high-value transactions

### 4. Incident Response
- 82 minutes detection time is too slow for crypto
- Need real-time blockchain monitoring
- Automatic circuit breakers for anomalous transactions

---

## 📖 References & Further Reading

- **Solidity Security:** Understanding delegatecall risks
- **Smart Contract Auditing:** Storage slot collision attacks
- **Supply Chain Security:** Developer environment hardening
- **Multisig Best Practices:** Transaction verification methods
- **Blockchain Forensics:** Analyzing on-chain transaction flows

---

**⚠️ EDUCATIONAL PURPOSE DISCLAIMER**

This analysis is provided for **educational and defensive security purposes only**. The techniques described should be understood to:
- Improve security awareness
- Enhance defensive capabilities
- Design better security controls
- Conduct authorized security research

**DO NOT** use this information to:
- Attack any system without explicit authorization
- Steal funds or assets
- Compromise infrastructure
- Engage in any illegal activity

Always follow responsible disclosure practices and obtain proper authorization before conducting security testing.
