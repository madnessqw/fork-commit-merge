# Contributing to PPC Tiger Tools

Thank you for your interest in contributing to PPC Tiger Tools! This project preserves and extends the capabilities of 20-year-old PowerPC Macs running Mac OS X Tiger (10.4) and Leopard (10.5).

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [AltiVec Guidelines](#altivec-guidelines)
- [PowerPC Architecture Considerations](#powerpc-architecture-considerations)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [RTC Bounties](#rtc-bounties)

## Code of Conduct

This project welcomes contributors who:
- Respect the legacy hardware and its limitations
- Share knowledge about PowerPC optimization techniques
- Help others run modern software on vintage systems
- Document their work for future maintainers

## Getting Started

### Prerequisites

**Hardware (one of the following):**
- Power Mac G4/G5 (preferred for development)
- PowerBook G4
- iMac G4/G5
- Mac mini G4
- Or use QEMU emulation (see below)

**Software:**
- Mac OS X Tiger (10.4.11) or Leopard (10.5.8)
- Xcode 2.5 (Tiger) or Xcode 3.1 (Leopard)
- GCC 4.0+ with AltiVec support
- Python 2.3 (system default on Tiger)
- Git 1.6+ (compile from source or use MacPorts)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Scottcjn/ppc-tiger-tools.git
cd ppc-tiger-tools

# Build a sample AltiVec program
gcc -O3 -mcpu=7450 -maltivec -o test_altivec altivec_test.c
./test_altivec
```

## Development Environment

### Using QEMU for Development (No Hardware Required)

If you don't have PowerPC hardware, you can use QEMU:

```bash
# Install QEMU (on a modern system)
brew install qemu  # macOS
apt-get install qemu-system-ppc  # Debian/Ubuntu

# Download Mac OS X Tiger for PowerPC ISO
# Create a QEMU disk image
qemu-img create -f qcow2 tiger_ppc.img 20G

# Boot with QEMU
qemu-system-ppc -M mac99 -m 1024 \
  -hda tiger_ppc.img \
  -cdra tiger.iso \
  -boot d
```

### Cross-Compilation from Modern macOS

```bash
# Install powerpc-apple-darwin-gcc (if available)
# Or use the provided Makefile.ppc with proper cross-compiler
make -f Makefile.ppc CC=powerpc-apple-darwin-gcc
```

## How to Contribute

### Types of Contributions

1. **AltiVec Optimizations**: Vectorize compute-intensive code
2. **Python 2.3 Compatibility**: Port modern Python scripts
3. **TLS/Security**: Improve TLS 1.2 shims
4. **Documentation**: Write guides, fix typos
5. **Testing**: Test on different G4/G5 models
6. **Bug Fixes**: Fix issues on legacy systems

### Finding Issues

Check the [GitHub Issues](https://github.com/Scottcjn/ppc-tiger-tools/issues) for:
- `good first issue` - Easy tasks for newcomers
- `help wanted` - Tasks needing community help
- `G4` or `G5` - Architecture-specific issues
- `AltiVec` - Vectorization opportunities

## Coding Standards

### C Code Style

```c
/* Use traditional K&R style with 4-space indentation */
#include <stdio.h>
#include <altivec.h>

/* Function names: lowercase_with_underscores */
int altivec_transform_matrix(float *input, float *output, int size)
{
    /* AltiVec register variables */
    vector float v_input, v_output;
    
    /* Comments explain WHY, not WHAT */
    /* AltiVec requires 16-byte aligned memory */
    if ((uintptr_t)input % 16 != 0) {
        fprintf(stderr, "Input not aligned\n");
        return -1;
    }
    
    /* Implementation */
    for (int i = 0; i < size; i += 4) {
        v_input = vec_ld(0, &input[i]);
        /* ... processing ... */
        vec_st(v_output, 0, &output[i]);
    }
    
    return 0;
}
```

### Python 2.3 Compatibility

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module docstring explaining purpose.
Compatible with Python 2.3 (Tiger default).
"""

import sys
import os

# Python 2.3 doesn't have 'with' statement
# Use explicit try/finally
def process_file(filename):
    """Function docstring."""
    fp = None
    try:
        fp = open(filename, 'r')
        data = fp.read()
        return data
    finally:
        if fp:
            fp.close()

# Use old-style string formatting
print "Processing %d items" % len(items)

# No 'as' keyword in except blocks
try:
    risky_operation()
except ValueError, e:
    print "Error: %s" % str(e)
```

### Compiler Flags

**For G4 (PowerPC 7450/7455):**
```bash
gcc -O3 -mcpu=7450 -maltivec -mtune=7450 -o output input.c
```

**For G5 (PowerPC 970):**
```bash
gcc -O3 -mcpu=970 -maltivec -mtune=970 -o output input.c
```

**For Universal Binary (G4+G5):**
```bash
gcc -O3 -arch ppc -arch ppc64 -maltivec -o output input.c
```

## AltiVec Guidelines

### When to Use AltiVec

Use AltiVec for:
- Matrix operations (4x speedup typical)
- Signal processing
- Image/audio processing
- Cryptographic operations
- Any loop processing arrays of floats/ints

### AltiVec Best Practices

```c
#include <altivec.h>

/* 1. Always check for AltiVec support at runtime */
int has_altivec(void)
{
    /* Check for G4 or later */
    return (get_cpu_type() >= CPU_TYPE_7450);
}

/* 2. Ensure 16-byte alignment */
float *aligned_buffer;
posix_memalign((void **)&aligned_buffer, 16, size * sizeof(float));

/* 3. Use proper AltiVec types */
vector float vf;      /* 4 floats */
vector unsigned int vi;   /* 4 unsigned ints */
vector signed char vc;    /* 16 signed chars */

/* 4. Avoid scalar operations in AltiVec loops */
/* BAD: Mixing scalar and vector */
for (i = 0; i < n; i++) {
    vector float v = vec_ld(0, &data[i]);
    scalar_var += v[0];  /* Scalar extraction in loop */
}

/* GOOD: Process all 4 elements */
vector float sum = vec_splat_f32(0.0);
for (i = 0; i < n; i += 4) {
    vector float v = vec_ld(0, &data[i]);
    sum = vec_add(sum, v);
}

/* 5. Handle remainder for non-multiple-of-4 sizes */
int main_count = (size / 4) * 4;
for (i = 0; i < main_count; i += 4) {
    /* AltiVec processing */
}
for (; i < size; i++) {
    /* Scalar cleanup */
}
```

### Common AltiVec Patterns

```c
/* Load/store with offset */
vector float v = vec_ld(offset, pointer);
vec_st(v, offset, pointer);

/* Splat (broadcast) scalar to all elements */
vector float v_one = vec_splat_f32(1.0);

/* Arithmetic */
vector float sum = vec_add(a, b);
vector float prod = vec_madd(a, b, c);  /* a*b + c */

/* Permute/shuffle */
vector float shuffled = vec_perm(a, b, mask);

/* Compare */
vector bool int cmp = vec_cmplt(a, b);
vector float result = vec_sel(a, b, cmp);  /* Select based on comparison */
```

## PowerPC Architecture Considerations

### Memory Alignment

PowerPC requires strict alignment:
- 4-byte alignment for 32-bit values
- 8-byte alignment for 64-bit values (long long, double)
- 16-byte alignment for AltiVec vectors

```c
/* Check alignment */
#define IS_ALIGNED(ptr, align) (((uintptr_t)(ptr) & ((align)-1)) == 0)

/* Safe unaligned read (slower but portable) */
uint32_t read_unaligned(uint8_t *p) {
    return ((uint32_t)p[0] << 24) |
           ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |
           (uint32_t)p[3];
}
```

### Endianness

PowerPC is big-endian. Be careful with:
- Network protocols (usually big-endian, so native)
- File formats from x86 systems (little-endian)
- Binary data exchange

```c
/* Byte swap for little-endian data */
uint32_t swap32(uint32_t x) {
    return ((x & 0xFF000000) >> 24) |
           ((x & 0x00FF0000) >> 8)  |
           ((x & 0x0000FF00) << 8)  |
           ((x & 0x000000FF) << 24);
}
```

### Cache Considerations

G4/G5 have different cache sizes:
- G4: 32KB L1, 256KB-1MB L2
- G5: 64KB L1, 512KB-1MB L2

Optimize for cache lines (32 bytes on G4, 128 bytes on G5):

```c
/* Cache-friendly matrix traversal */
/* BAD: Column-major access on row-major matrix */
for (col = 0; col < n; col++) {
    for (row = 0; row < n; row++) {
        sum += matrix[row][col];  /* Cache miss every access */
    }
}

/* GOOD: Row-major access */
for (row = 0; row < n; row++) {
    for (col = 0; col < n; col++) {
        sum += matrix[row][col];  /* Sequential access, cache hits */
    }
}
```

## Testing

### Testing on Real Hardware

**Minimum test matrix:**
- Test on at least one G4 and one G5 if possible
- Test with 512MB RAM (minimum supported)
- Test with Spotlight disabled (performance baseline)

### Testing with QEMU

```bash
# Basic functionality test
qemu-system-ppc -M mac99 -m 1024 -hda tiger_ppc.img \
  -kernel ppc_tiger_tools_test

# Performance test (compare to native if possible)
time ./benchmark_transformer
```

### Python Testing

```bash
# Test Python 2.3 compatibility
python2.3 -m py_compile your_script.py

# Run tests
python2.3 test_suite.py
```

### Test Checklist

Before submitting:
- [ ] Code compiles without warnings (`-Wall -Wextra`)
- [ ] Runs correctly on target hardware/QEMU
- [ ] AltiVec code paths tested on G4/G5
- [ ] Non-AltiVec fallback works on G3
- [ ] Python 2.3 compatibility verified
- [ ] Memory alignment checked
- [ ] No memory leaks (test with long-running processes)

## Submitting Changes

### Commit Message Format

```
component: Brief description

Detailed explanation of what changed and why.
Include performance numbers if applicable.

- Bullet points for multiple changes
- Reference issues: Fixes #123
```

Examples:
```
altivec: Optimize transformer matrix multiplication

Use vec_madd for fused multiply-add operations.
4.2x speedup on G4 1.42GHz, 3.8x on G5 2.0GHz.

- Added aligned memory allocation
- Added scalar fallback for non-AltiVec systems
- Updated benchmarks in README

Fixes #45
```

```
python: Port wallet to Python 2.3

Replace 'with' statements with try/finally.
Use % formatting instead of .format().
Compatible with Tiger's default Python.

Fixes #67
```

### Pull Request Process

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** following this guide
4. **Test** thoroughly
5. **Commit** with clear messages
6. **Push** to your fork
7. **Submit PR** with:
   - Clear description of changes
   - Test results (hardware/software used)
   - Performance impact (if applicable)
   - Screenshots for UI changes

### PR Review Criteria

Maintainers will check for:
- Code compiles on Tiger/Leopard
- Follows style guidelines
- Includes appropriate tests
- Documentation updated
- Backward compatibility maintained

## RTC Bounties

Earn RTC (RustChain Tokens) for contributions!

### Current Bounties

Check [rustchain-bounties](https://github.com/Scottcjn/rustchain-bounties) for active bounties related to this project.

### Common Bounty Types

- **AltiVec Optimization**: 10-50 RTC for significant speedups
- **Python 2.3 Ports**: 5-20 RTC per script
- **Documentation**: 1-10 RTC for guides/improvements
- **Bug Fixes**: 5-30 RTC depending on severity
- **New Tools**: 20-100 RTC for substantial additions

### Claiming Bounties

1. Comment on the bounty issue expressing interest
2. Complete the work
3. Submit PR referencing the bounty issue
4. Comment on bounty issue with PR link
5. Bounty paid in RTC upon merge

---

## Questions?

- **Discord**: [RustChain Discord](https://discord.gg/tQ4q3z4M)
- **Issues**: [GitHub Issues](https://github.com/Scottcjn/ppc-tiger-tools/issues)
- **Email**: See repository maintainer

## Attribution

When contributing, you agree that:
- Your contributions are licensed under AGPL v3
- You have the right to submit the code
- You will be credited in the project history

Thank you for keeping PowerPC alive! 🐯

---

*This CONTRIBUTING.md was created to help the open-source community contribute to PPC Tiger Tools. For issues with this guide, please open an issue.*