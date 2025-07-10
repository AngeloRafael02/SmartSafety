# Contributing to the SmartSafety App
We welcome contributions from everyone! By participating in this project, you agree to abide by our Code of Conduct (please create this file if it doesn't exist).

This document outlines guidelines for contributing to the PPE (Personal Protective Equipment) Detection Raspberry Pi App, powered by YOLOv8. Whether you're reporting a bug, suggesting an enhancement, or contributing code, your efforts are greatly appreciated.

## 1. How to Contribute
There are several ways you can contribute to this project:
- Reporting Bugs: If you find a bug, please let us know.
- Suggesting Enhancements: Have an idea for a new feature or improvement? Share it!
- Writing Code: Contribute code to fix bugs, implement new features, or improve existing ones.
- Improving Documentation: Help us make our documentation clearer and more comprehensive.
- Testing: Help us test new features and bug fixes.

## 2. Reporting Bugs
If you encounter a bug, please open an issue on our [GitHub Issues page](https://github.com/AngeloRafael02/SmartSafety/issues).
When reporting a bug, please include as much detail as possible:

- A clear and concise description of the bug.
- Steps to reproduce the behaviour:
- Expected behaviour.
- Actual behaviour.
- Screenshots or video (if applicable).
- Your environment

## 3. Suggesting Enhancements
We love new ideas! To suggest an enhancement:
- Open an issue on our GitHub Issues page.
- Use a descriptive title for your suggestion (e.g., "Feature Request: Add real-time notification for PPE violations").
- Clearly describe the enhancement and why you think it would be valuable.
- If possible, provide examples or use cases.

## 4. Your First Code Contribution
New to contributing to open source? Here's how to get started:
- Fork the repository: Click the "Fork" button at the top right of this repository's GitHub page.
- Clone your forked repository to your local machine:
```
git clone https://github.com/YOUR_USERNAME/ppe-detection-rpi.git
cd ppe-detection-rpi
```
- Create a new branch for your changes:
```
git checkout -b feature/your-feature-name

or

git checkout -b bugfix/issue-number
```
- Make your changes.
- Test your changes thoroughly.
- Commit your changes with a clear and concise commit message.
- Push your branch to your forked repository.
- Open a Pull Request (PR) to the main branch of the original repository.

5. Setting Up Your Development Environment
This project is designed for Raspberry Pi, leveraging Python and YOLOv8.


## 5. Submitting Changes (Pull Requests)
When submitting a Pull Request, please ensure:
- One logical change per PR: Keep your PRs focused on a single feature or bug fix.
- Clear and descriptive title: Summarise your changes concisely.
- Detailed description: Explain what your PR does, why it's needed, and how it addresses the issue.
- Reference related issues: Link to any issues that your PR resolves (e.g., Closes #123).
- Tests: If applicable, include unit tests or integration tests for your changes.
- Rebase your branch: Before submitting, rebase your branch on the latest main branch to avoid merge conflicts.
```
git fetch origin
git rebase origin/main
```

## 6. Coding Style Guidelines
Please adhere to the following coding standards:
- Python: Follow PEP 8 for code formatting. We recommend using linters like flake8 or pylint.
- Comments: Add clear and concise comments to explain complex logic, functions, and non-obvious parts of the code.
- Docstrings: Use PEP 257 for docstrings on modules, classes, and functions.

## 7. License
By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---
Thank you for contributing to the PPE Detection SmartSafety App!
