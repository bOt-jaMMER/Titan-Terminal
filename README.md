# 🏛️ TITAN TERMINAL PRO
**A Bloomberg-style financial analysis terminal powered by local LLMs**
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-orange.svg)
> Your investment data stays on YOUR machine. No cloud. No API keys. Full privacy.
---
## ✨ Features
| Module | Description |
|--------|-------------|
| 📊 **Company Profile** | Business overview, executives, key statistics |
| 💰 **Financials** | Income statement, balance sheet, cash flow, ratios |
| 📈 **Technical Analysis** | ASCII price charts, RSI, MACD, Bollinger Bands, support/resistance |
| 🏢 **Peer Comparison** | Sector peers with relative valuation metrics |
| 👔 **Ownership** | Promoter holdings, institutional ownership, short interest |
| 🎯 **Analyst Ratings** | Price targets, buy/sell recommendations, estimates |
| 📜 **Options Chain** | Calls/puts, implied volatility, unusual activity |
| 📰 **News & Sentiment** | Headlines with AI-powered sentiment analysis |
| 🔗 **Supply Chain** | Suppliers and customers relationship mapping |
| 🤖 **Multi-Model AI Analysis** | 6 local LLMs analyze in parallel with executive summary |
---
## 🔐 Privacy-First Design
| Component | Where it runs |
|-----------|---------------|
| All AI/LLM processing | **100% Local** (Ollama) |
| Investment analysis | **Never leaves your PC** |
| Stock data | Yahoo Finance (public API) |
Unlike cloud-based solutions, your prompts, analysis, and investment thoughts **never touch external AI servers**.
---
## 🚀 Quick Start
### Prerequisites
1. **Python 3.11+**
2. **Ollama** - [Install from ollama.ai](https://ollama.ai)
3. **GPU recommended** (8GB+ VRAM for best performance)
### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/titan-terminal.git
cd titan-terminal
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
# Pull required LLM models
ollama pull deepseek-r1
ollama pull gemma3
ollama pull phi4
ollama pull qwen2.5
ollama pull llama3.2
ollama pull glm4:9b
```
### Run
```bash
python3 titan_terminal.py
```
---
## 📸 Screenshots
```
╭────────────────────────────────────────────────────────────────────────────────╮
│  🏛️  TITAN TERMINAL PRO   │ Apple Inc. (AAPL) │ $178.25 +2.15 (+1.22%)        │
╰────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────── 📋 Menu ────────────────────────────────────╮
│     [1] Company Profile    [5] Ownership          [9] Watchlist                │
│     [2] Financials         [6] Analyst            [M] Market Overview          │
│     [3] Technical Charts   [7] Options            [H] Help                     │
│     [4] Peer Comparison    [8] News & Sentiment   [Q] Exit                     │
│                                                                                │
│     [S] Supply Chain          [0] Full AI Analysis (Multi-Model)               │
╰────────────────────────────────────────────────────────────────────────────────╯
```
---
## 🧠 AI Models Used
The terminal runs **6 local LLMs in parallel** for comprehensive analysis:
| Model | Strength |
|-------|----------|
| DeepSeek-R1 | Reasoning & executive summary |
| Gemma 3 | Balanced analysis |
| Phi-4 | Microsoft's reasoning model |
| Qwen 2.5 | Alibaba's flagship |
| LLaMA 3.2 | Meta's latest |
| GLM-4 | Alternative perspective |
Each model provides an independent investment verdict, then a consensus is calculated with an executive summary.
---
## 🌍 Multi-Currency Support
Automatically detects and displays correct currency symbols:
- 🇺🇸 USD ($) for US stocks
- 🇮🇳 INR (₹) for Indian stocks (.NS, .BO)
- 🇪🇺 EUR (€) for European stocks
- 🇬🇧 GBP (£) for UK stocks
- And more...
---
## 📁 Project Structure
```
Finance_Terminal/
├── titan_terminal.py      # Main entry point
├── modules/
│   ├── company_profile.py # Company information
│   ├── financials.py      # Financial statements
│   ├── technicals.py      # Technical indicators
│   ├── ownership.py       # Shareholding patterns
│   ├── analyst.py         # Analyst recommendations
│   ├── options.py         # Options chain data
│   ├── news.py            # News & sentiment
│   ├── peer_analysis.py   # Peer comparison
│   ├── supply_chain.py    # Supply chain mapping
│   ├── economic.py        # Market overview
│   └── ai_engine.py       # Multi-LLM orchestration
├── utils/
│   ├── formatters.py      # Currency & number formatting
│   ├── charts.py          # ASCII chart rendering
│   └── data_cache.py      # Caching utilities
└── watchlist.json         # Your saved stocks
```
---
## 🛠️ Tech Stack
- **Python 3.11** - Core language
- **Rich** - Beautiful terminal UI
- **yfinance** - Yahoo Finance data
- **Ollama** - Local LLM inference
- **pandas/numpy** - Data processing
---
## 📄 License
MIT License - See [LICENSE](LICENSE) for details.
---
## 🤝 Contributing
Contributions welcome! Please read the contributing guidelines before submitting PRs.
---
## ⚠️ Disclaimer
This tool is for informational purposes only. Not financial advice. Always do your own research before making investment decisions.
---
**Built with ❤️ for privacy-conscious investors**
