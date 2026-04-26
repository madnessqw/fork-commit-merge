#!/usr/bin/env python3
"""
Secure Password Generator - Standalone Python Tool
Generates cryptographically secure passwords with customizable options.

Features:
- Variable length (8-128 characters)
- Character type selection (uppercase, lowercase, digits, symbols)
- Password strength estimation
- Bulk generation mode
- Export to file

Usage:
    python secure_password_generator.py
    python secure_password_generator.py --length 20 --count 10

Author: UniverseCreator
Version: 1.0.0
"""

import secrets
import string
import argparse
import sys
from typing import List, Optional


class PasswordGenerator:
    """Cryptographically secure password generator."""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        """
        Generate a secure password.
        
        Args:
            length: Password length (8-128)
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_digits: Include digits
            use_symbols: Include special symbols
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, 1, etc.)
        
        Returns:
            Generated password string
        """
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")
        if length > 128:
            raise ValueError("Password length cannot exceed 128 characters")
        
        # Build character pool
        chars = ""
        required_chars = []
        
        if use_lowercase:
            chars += self.lowercase
            required_chars.append(secrets.choice(self.lowercase))
        if use_uppercase:
            chars += self.uppercase
            required_chars.append(secrets.choice(self.uppercase))
        if use_digits:
            chars += self.digits
            required_chars.append(secrets.choice(self.digits))
        if use_symbols:
            chars += self.symbols
            required_chars.append(secrets.choice(self.symbols))
        
        if not chars:
            raise ValueError("At least one character type must be selected")
        
        # Remove ambiguous characters if requested
        if exclude_ambiguous:
            ambiguous = "0O1lI"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        # Generate password with required characters
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [secrets.choice(chars) for _ in range(remaining_length)]
        
        # Shuffle to randomize position of required characters
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def estimate_strength(self, password: str) -> dict:
        """
        Estimate password strength.
        
        Returns:
            Dictionary with strength metrics
        """
        length = len(password)
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_symbol = any(c in self.symbols for c in password)
        
        char_types = sum([has_lower, has_upper, has_digit, has_symbol])
        
        # Calculate entropy
        pool_size = 0
        if has_lower: pool_size += 26
        if has_upper: pool_size += 26
        if has_digit: pool_size += 10
        if has_symbol: pool_size += len(self.symbols)
        
        entropy = length * (pool_size.bit_length() - 1) if pool_size > 0 else 0
        
        # Determine strength level
        if length < 8:
            strength = "Very Weak"
            score = 1
        elif entropy < 50:
            strength = "Weak"
            score = 2
        elif entropy < 80:
            strength = "Fair"
            score = 3
        elif entropy < 120:
            strength = "Strong"
            score = 4
        else:
            strength = "Very Strong"
            score = 5
        
        return {
            "length": length,
            "char_types": char_types,
            "entropy": round(entropy, 2),
            "strength": strength,
            "score": score
        }
    
    def generate_bulk(self, count: int, **kwargs) -> List[str]:
        """Generate multiple passwords."""
        return [self.generate(**kwargs) for _ in range(count)]


def interactive_mode():
    """Run interactive password generation."""
    print("=" * 60)
    print("🔐 Secure Password Generator")
    print("=" * 60)
    
    generator = PasswordGenerator()
    
    try:
        length = int(input("\nPassword length (default 16): ") or "16")
    except ValueError:
        length = 16
    
    use_upper = input("Include uppercase letters? (Y/n): ").lower() != 'n'
    use_lower = input("Include lowercase letters? (Y/n): ").lower() != 'n'
    use_digits = input("Include digits? (Y/n): ").lower() != 'n'
    use_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
    exclude_ambiguous = input("Exclude ambiguous characters (0, O, l, 1)? (y/N): ").lower() == 'y'
    
    try:
        password = generator.generate(
            length=length,
            use_uppercase=use_upper,
            use_lowercase=use_lower,
            use_digits=use_digits,
            use_symbols=use_symbols,
            exclude_ambiguous=exclude_ambiguous
        )
        
        strength = generator.estimate_strength(password)
        
        print("\n" + "=" * 60)
        print(f"Generated Password: {password}")
        print("=" * 60)
        print(f"\nStrength Analysis:")
        print(f"  Length: {strength['length']} characters")
        print(f"  Character types: {strength['char_types']}/4")
        print(f"  Entropy: {strength['entropy']} bits")
        print(f"  Rating: {'⭐' * strength['score']} ({strength['strength']})")
        
        save = input("\nSave to file? (y/N): ").lower() == 'y'
        if save:
            filename = input("Filename (default: password.txt): ") or "password.txt"
            with open(filename, 'w') as f:
                f.write(password)
            print(f"✅ Saved to {filename}")
        
        print("\n⚠️  Remember to store your password securely!")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point with CLI support."""
    parser = argparse.ArgumentParser(
        description="Secure Password Generator - Generate cryptographically secure passwords",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Interactive mode
  %(prog)s --length 20               # Generate 20-character password
  %(prog)s --length 32 --no-symbols  # Generate without symbols
  %(prog)s --count 10 --export passwords.txt  # Generate 10 passwords to file
        """
    )
    
    parser.add_argument('-l', '--length', type=int, default=16,
                        help='Password length (default: 16, min: 8, max: 128)')
    parser.add_argument('-c', '--count', type=int, default=1,
                        help='Number of passwords to generate (default: 1)')
    parser.add_argument('--no-upper', action='store_true',
                        help='