# Contributing to ButterflyFX Kernel

Thank you for your interest in contributing to ButterflyFX Kernel!

## Philosophy

ButterflyFX Kernel is the **foundational infrastructure** of dimensional computing. It is released under CC BY 4.0 (Creative Commons Attribution) to enable anyone to use, modify, and build upon it.

**"Infrastructure is free. Build anything on it."**

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/butterflyfx_kernel.git
   cd butterflyfx_kernel
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest tests/ -v
   ```

## How to Contribute

### Reporting Bugs

- Use the GitHub Issues tracker
- Include Python version and OS
- Provide a minimal reproducible example

### Suggesting Enhancements

- Open an issue describing the enhancement
- Explain why it would be useful
- Provide examples if possible

### Pull Requests

1. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. Make your changes

3. Format code:
   ```bash
   black butterflyfx/
   isort butterflyfx/
   ```

4. Run tests:
   ```bash
   pytest tests/ -v
   ```

5. Commit with a clear message:
   ```bash
   git commit -m "Add amazing feature"
   ```

6. Push and create a Pull Request:
   ```bash
   git push origin feature/amazing-feature
   ```

## Code Style

- Follow PEP 8
- Use type hints where practical
- Write docstrings for public functions
- Use `black` for formatting (line length 100)

## Areas of Interest

### Mathematical Kernel
- Optimizations to the HelixKernel state machine
- Additional level semantics
- Spiral navigation algorithms

### Manifold & Substrate
- Token generation strategies
- Invocation optimization
- Multi-dimensional manifold operations

### Foundation
- Database storage optimization
- Graph traversal algorithms
- Query optimization

### Networking
- Transport protocol improvements
- Distributed computing extensions
- Real-time synchronization

## License

By contributing, you agree that your contributions will be licensed under CC BY 4.0.

## Contact

- Author: Kenneth Bingham
- Email: keneticsart@gmail.com
- Website: https://butterflyfx.us
