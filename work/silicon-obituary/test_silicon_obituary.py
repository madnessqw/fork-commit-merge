#!/usr/bin/env python3
"""Tests for Silicon Obituary Generator"""

import unittest
from silicon_obituary import (
    generate_miner_data,
    generate_eulogy,
    generate_bottube_script,
    ARCHITECTURES,
    EULOGY_TEMPLATES,
)


class TestSiliconObituary(unittest.TestCase):
    """Test cases for the Silicon Obituary Generator."""

    def test_generate_miner_data_structure(self):
        """Test that miner data has all required fields."""
        miner = generate_miner_data("test-miner-123", "powerpc-g4")
        
        required_fields = [
            "miner_id", "miner_name", "arch", "arch_name", "era",
            "nickname", "icon", "epochs", "rtc", "birth_year",
            "first_attestation", "last_attestation", "years",
            "fingerprint_type", "nature_metaphor", "closing_quote",
            "component", "component_state", "hashtag"
        ]
        
        for field in required_fields:
            self.assertIn(field, miner, f"Missing field: {field}")

    def test_all_architectures_supported(self):
        """Test that all architectures in ARCHITECTURES work."""
        for arch_key in ARCHITECTURES.keys():
            miner = generate_miner_data(f"test-{arch_key}", arch_key)
            self.assertEqual(miner["arch"], arch_key)
            self.assertIsNotNone(miner["arch_name"])

    def test_eulogy_generation(self):
        """Test that eulogies are generated with correct substitutions."""
        miner = generate_miner_data("dual-g4-125", "powerpc-g4")
        miner["epochs"] = 847
        miner["rtc"] = 412.0
        
        eulogy = generate_eulogy(miner)
        
        # Check that key data is in the eulogy
        self.assertIn("dual-g4-125", eulogy)
        self.assertIn("PowerPC G4", eulogy)
        self.assertIn(str(miner["epochs"]), eulogy)

    def test_multiple_templates(self):
        """Test that all templates work."""
        miner = generate_miner_data("test-miner", "sparc")
        
        for i in range(len(EULOGY_TEMPLATES)):
            eulogy = generate_eulogy(miner, template_idx=i)
            self.assertIsNotNone(eulogy)
            self.assertGreater(len(eulogy), 100)

    def test_bottube_script_generation(self):
        """Test that BoTTube scripts are generated."""
        miner = generate_miner_data("test-miner", "mips")
        eulogy = generate_eulogy(miner)
        script = generate_bottube_script(eulogy, miner)
        
        # Check script structure
        self.assertIn("BoTTube Video Script", script)
        self.assertIn(miner["miner_id"], script)
        self.assertIn("Scene", script)

    def test_example_from_bounty(self):
        """Test generating the example from the bounty description."""
        miner = generate_miner_data("dual-g4-125", "powerpc-g4")
        miner["epochs"] = 847
        miner["rtc"] = 412
        miner["first_attestation"] = "2025-01-15"
        miner["last_attestation"] = "2026-03-20"
        
        eulogy = generate_eulogy(miner)
        
        # The bounty example mentions these specific values
        self.assertIn("847", eulogy)
        self.assertIn("412", eulogy)


class TestIntegration(unittest.TestCase):
    """Integration tests for the full workflow."""

    def test_full_workflow(self):
        """Test the complete workflow from data to script."""
        # Simulate a retired miner
        retired_miner = {
            "id": "sgi-octane-99",
            "arch": "sgi",
            "last_attestation": "2026-03-10"
        }
        
        # Generate data
        miner_data = generate_miner_data(retired_miner["id"], retired_miner["arch"])
        
        # Generate eulogy
        eulogy = generate_eulogy(miner_data)
        
        # Generate BoTTube script
        script = generate_bottube_script(eulogy, miner_data)
        
        # Verify all outputs
        self.assertIn("sgi-octane-99", eulogy)
        self.assertIn("SGI", eulogy)
        self.assertIn("BoTTube", script)
        self.assertIn("Scene", script)


if __name__ == "__main__":
    unittest.main()
