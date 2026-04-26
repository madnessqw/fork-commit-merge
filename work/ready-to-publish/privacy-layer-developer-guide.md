# PrivacyLayer Developer Guide: Building Confidential dApps

## Introduction

PrivacyLayer is a zero-knowledge privacy infrastructure for blockchain applications. This guide covers everything developers need to build confidential decentralized applications (dApps) using PrivacyLayer's ZK primitives.

## What is PrivacyLayer?

PrivacyLayer provides:
- **Private Transactions**: Hide sender, recipient, and amount
- **Anonymous Identity**: Prove membership without revealing identity
- **Confidential Computation**: Execute logic without exposing inputs
- **Selective Disclosure**: Reveal only what's necessary

## Core Concepts

### Zero-Knowledge Proofs (ZKPs)

A ZKP allows one party (prover) to prove to another (verifier) that a statement is true, without revealing any information beyond the validity of the statement.

```javascript
// Conceptual example
const proof = await zkProver.generateProof({
    privateInputs: {
        senderBalance: 1000,
        transferAmount: 100,
        senderPrivateKey: "0x..."
    },
    publicInputs: {
        senderCommitment: "0xabc...",
        recipientCommitment: "0xdef...",
        newBalanceCommitment: "0x123..."
    }
});

// Verifier checks proof without seeing actual values
const isValid = await zkVerifier.verify(proof, publicInputs);
// isValid = true, but verifier never learned senderBalance or transferAmount
```

### Commitment Schemes

PrivacyLayer uses Pedersen commitments to hide values while allowing verification:

```solidity
// Solidity implementation
contract PrivacyLayer {
    struct Commitment {
        uint256 value;
        uint256 blindingFactor;
        bytes32 hash;
    }

    function createCommitment(uint256 value) internal returns (Commitment memory) {
        uint256 blinding = uint256(keccak256(abi.encodePacked(block.timestamp, msg.sender)));
        bytes32 hash = keccak256(abi.encodePacked(value, blinding));
        return Commitment(value, blinding, hash);
    }

    function verifyCommitment(Commitment memory c) internal pure returns (bool) {
        return c.hash == keccak256(abi.encodePacked(c.value, c.blindingFactor));
    }
}
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │  Wallet  │ │   DAO    │ │  DEX     │ │  Gaming  │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
└───────┼────────────┼────────────┼────────────┼──────────────┘
        │            │            │            │
┌───────┴────────────┴────────────┴────────────┴──────────────┐
│                   PrivacyLayer SDK                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│  │ ZK Circuit   │ │ Proof Gen    │ │ Verification │         │
│  │ Generator    │ │              │ │              │         │
│  └──────────────┘ └──────────────┘ └──────────────┘         │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────┴──────────────────────────────────────┐
│                   Blockchain Layer                           │
│              (Ethereum, Polygon, etc.)                       │
└──────────────────────────────────────────────────────────────┘
```

## Getting Started

### Installation

```bash
npm install @privacylayer/sdk
# or
yarn add @privacylayer/sdk
```

### Basic Setup

```typescript
import { PrivacyLayer } from '@privacylayer/sdk';

const pl = new PrivacyLayer({
    network: 'mainnet', // or 'testnet'
    provider: window.ethereum,
    circuitPath: './circuits'
});

await pl.initialize();
```

## Building a Private Payment dApp

### Step 1: Create the Circuit

```circom
// private_transfer.circom
pragma circom 2.0.0;

include "circomlib/poseidon.circom";
include "circomlib/comparators.circom";

template PrivateTransfer() {
    // Private inputs
    signal input senderBalance;
    signal input transferAmount;
    signal input senderPrivateKey;
    
    // Public inputs
    signal input senderCommitment;
    signal input recipientCommitment;
    signal input newSenderCommitment;
    
    // Verify sender has sufficient balance
    component sufficient = GreaterThan(64);
    sufficient.in[0] <== senderBalance;
    sufficient.in[1] <== transferAmount;
    sufficient.out === 1;
    
    // Calculate new balance
    signal newBalance;
    newBalance <== senderBalance - transferAmount;
    
    // Verify commitments (simplified)
    // In production, use proper Pedersen commitments
    component poseidon = Poseidon(2);
    poseidon.inputs[0] <== senderPrivateKey;
    poseidon.inputs[1] <== senderBalance;
    
    // Output signals
    signal output senderProof;
    senderProof <== poseidon.out;
}

component main = PrivateTransfer();
```

### Step 2: Compile and Generate Proving Key

```javascript
const { compile, setup } = require('@privacylayer/sdk');

async function setupCircuit() {
    // Compile circuit
    const compiled = await compile('./circuits/private_transfer.circom');
    
    // Generate proving and verification keys
    const { provingKey, verificationKey } = await setup(compiled);
    
    // Save keys
    await fs.writeFile('./keys/proving_key.zkey', provingKey);
    await fs.writeFile('./keys/verification_key.json', JSON.stringify(verificationKey));
}
```

### Step 3: Generate Proofs in Your dApp

```typescript
import { ProofGenerator } from '@privacylayer/sdk';

async function sendPrivatePayment(recipient: string, amount: bigint) {
    const generator = new ProofGenerator({
        circuit: './circuits/private_transfer.circom',
        provingKey: './keys/proving_key.zkey'
    });
    
    // Get current balance (from private storage)
    const currentBalance = await getPrivateBalance();
    
    // Generate proof
    const { proof, publicSignals } = await generator.generate({
        privateInputs: {
            senderBalance: currentBalance,
            transferAmount: amount,
            senderPrivateKey: await wallet.getPrivateKey()
        },
        publicInputs: {
            senderCommitment: await getCommitment(currentBalance),
            recipientCommitment: await getCommitment(amount, recipient),
            newSenderCommitment: await getCommitment(currentBalance - amount)
        }
    });
    
    // Submit to blockchain
    const tx = await privacyLayerContract.transfer(proof, publicSignals);
    await tx.wait();
    
    return tx.hash;
}
```

### Step 4: Verify Proofs On-Chain

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@privacylayer/contracts/Verifier.sol";

contract PrivatePayment is Verifier {
    mapping(bytes32 => uint256) public commitments;
    
    event PrivateTransfer(
        bytes32 indexed senderCommitment,
        bytes32 indexed recipientCommitment,
        bytes32 indexed newSenderCommitment
    );
    
    function transfer(
        uint256[8] calldata proof,
        uint256[3] calldata publicSignals
    ) external {
        bytes32 senderCommitment = bytes32(publicSignals[0]);
        bytes32 recipientCommitment = bytes32(publicSignals[1]);
        bytes32 newSenderCommitment = bytes32(publicSignals[2]);
        
        // Verify proof
        require(
            verifyProof(proof, publicSignals),
            "Invalid proof"
        );
        
        // Update commitments
        commitments[senderCommitment] = 0; // Spent
        commitments[recipientCommitment] += 1; // Received
        commitments[newSenderCommitment] = 1; // Change
        
        emit PrivateTransfer(senderCommitment, recipientCommitment, newSenderCommitment);
    }
}
```

## Advanced Features

###