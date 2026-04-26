"""
Pytest configuration for clawrtc test suite
Bounty: Issue #426 - 25 RTC
"""
import pytest
import sys
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, '/home/gokhan/UniverseCreator-otonom/bounty-work/clawrtc-tests')

# Mock clawrtc modules before any imports
sys.modules['clawrtc'] = MagicMock()
sys.modules['clawrtc.wallet'] = MagicMock()
sys.modules['clawrtc.miner'] = MagicMock()
sys.modules['clawrtc.hardware'] = MagicMock()


@pytest.fixture
def mock_wallet():
    """Mock wallet fixture"""
    wallet = MagicMock()
    wallet.address = "rtc1q1234567890abcdef1234567890abcdef12345678"
    wallet.private_key = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    wallet.mnemonic = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
    wallet.get_balance.return_value = 1000.5
    return wallet


@pytest.fixture
def mock_miner():
    """Mock miner fixture"""
    miner = MagicMock()
    miner.wallet_address = "rtc1q1234567890abcdef1234567890abcdef12345678"
    miner.hardware_id = "hw_1234567890abcdef"
    miner.status = "idle"
    return miner


@pytest.fixture
def mock_hardware():
    """Mock hardware fixture"""
    hardware = MagicMock()
    hardware.fingerprint = "hw_fp_1234567890abcdef1234567890abcdef"
    hardware.cpu_cores = 8
    hardware.memory_gb = 32
    return hardware
