# Contributing to Titan Terminal Pro

Thanks for your interest in contributing! 🎉

## 🐛 Reporting Bugs

1. Check if the issue already exists in [Issues](../../issues)
2. Create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your Python/Ollama version

## 💡 Feature Requests

Open an issue with:
- Description of the feature
- Why it would be useful
- Any implementation ideas (optional)

## 🔧 Pull Requests

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** and test locally
4. **Commit**: `git commit -m "Add: brief description"`
5. **Push**: `git push origin feature/your-feature-name`
6. **Open a PR** with a clear description

## 📝 Code Style

- Follow PEP 8 for Python
- Use descriptive variable names
- Add docstrings to functions
- Keep modules focused (one responsibility per file)

## 🧪 Testing

Before submitting:
- [ ] Run `python3 titan_terminal.py` and test affected features
- [ ] Ensure Ollama integration still works
- [ ] Test with both Indian (.NS/.BO) and US stocks

## 📁 Where to Contribute

| Area | File(s) |
|------|---------|
| New data module | `modules/your_module.py` |
| UI improvements | `titan_terminal.py` |
| Formatting/display | `utils/formatters.py`, `utils/charts.py` |
| AI prompts | `modules/ai_engine.py`, `modules/ownership.py` |

## 🤝 Code of Conduct

Be respectful and constructive. We're all here to learn and build cool stuff!

---

Questions? Open an issue or start a discussion. Happy coding! 🚀
