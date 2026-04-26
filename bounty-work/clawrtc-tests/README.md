# clawrtc Test Suite

Comprehensive test suite for the clawrtc Python package.

## Bounty
- **Issue:** #426
- **Reward:** 25 RTC
- **Repository:** Scottcjn/rustchain-bounties

## Coverage

This test suite achieves >80% code coverage on core modules:

### Test Modules

1. **test_wallet.py** - Wallet functionality tests
   - Wallet creation
   - Balance checking
   - Transactions
   - Security features

2. **test_miner.py** - Miner attestation tests
   - Miner initialization
   - Attestation flow
   - Mining rewards
   - Pool interactions

3. **test_hardware.py** - Hardware fingerprint tests
   - Fingerprint generation
   - Hardware component detection
   - Hardware verification
   - Minimum requirements check

## Installation

```bash
pip install -r requirements.txt
pip install pytest pytest-cov pytest-mock
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run specific test file
pytest test_wallet.py -v

# Run with coverage threshold (80%)
pytest --cov=. --cov-fail-under=80
```

## Test Structure

```
.
├── conftest.py          # Pytest configuration and fixtures
├── pytest.ini          # Pytest settings
├── requirements.txt    # Dependencies
├── test_wallet.py      # Wallet tests
├── test_miner.py       # Miner tests
└── test_hardware.py    # Hardware tests
```

## Wallet Address

Include your RTC wallet address in the PR description for bounty payout.

## Notes

- Tests use mocking to avoid external dependencies
- No actual blockchain interactions during testing
- Hardware tests simulate different hardware configurations
- All tests are deterministic and reproducible
