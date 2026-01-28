#!/usr/bin/env python3
"""
TITAN TERMINAL PRO - Bloomberg-Style Finance Terminal
A comprehensive financial analysis terminal using local LLMs.
"""

import sys
import json
import os
import requests
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich.prompt import Prompt

# Import modules
from modules.company_profile import get_company_profile, render_company_profile
from modules.financials import get_financials, render_financials
from modules.technicals import get_technicals, render_technicals
from modules.peer_analysis import get_peer_analysis, render_peer_analysis
from modules.ownership import get_ownership, render_ownership
from modules.analyst import get_analyst_data, render_analyst_data
from modules.options import get_options_data, render_options_data
from modules.news import get_news, render_news
from modules.economic import get_market_data, render_market_overview
from modules.supply_chain import get_supply_chain, render_supply_chain
from modules.ai_engine import (
    AIEngine, get_engine, build_analysis_prompt, render_ai_analysis
)

# Configuration
WATCHLIST_FILE = Path(__file__).parent / "watchlist.json"
MODELS = [
    "deepseek-r1:latest",   # Reasoning specialist
    "gemma3:latest",        # Google's balanced model
    "glm4:9b",              # ChatGLM4 - Chinese AI
    "phi4:latest",          # Microsoft's reasoning model
    "qwen2.5:latest",       # Alibaba's flagship
    "llama3.2:latest",      # Meta's latest
]

console = Console()


def get_ticker_from_name(company_name):
    """Search for stock ticker based on company name."""
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_name}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if 'quotes' in data and len(data['quotes']) > 0:
            best_match = data['quotes'][0]
            return {
                "symbol": best_match['symbol'],
                "name": best_match.get('longname', best_match.get('shortname', best_match['symbol'])),
                "exchange": best_match.get('exchange', 'Unknown'),
                "type": best_match.get('quoteType', 'EQUITY')
            }
        return None
    except Exception as e:
        return None


def load_watchlist():
    """Load watchlist from file."""
    if WATCHLIST_FILE.exists():
        try:
            with open(WATCHLIST_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"stocks": []}
    return {"stocks": []}


def save_watchlist(watchlist):
    """Save watchlist to file."""
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, f, indent=2)


def check_ollama_status():
    """Check if Ollama is running and display status."""
    try:
        response = requests.get("http://localhost:11434/api/ps", timeout=5)
        if response.status_code == 200:
            data = response.json()
            running = data.get('models', [])
            
            if running:
                model_names = [m.get('name', '?') for m in running]
                console.print(f"[dim]📊 GPU: {len(running)} model(s) loaded: {', '.join(model_names)}[/dim]")
            else:
                console.print("[dim]📊 Ollama running. Models will load on demand.[/dim]")
            return True
        return False
    except:
        console.print("[yellow]⚠️ Ollama not running. AI analysis will be unavailable.[/yellow]")
        return False


def display_header(ticker_info=None):
    """Display terminal header with domestic currency."""
    console.clear()
    
    header_text = "[bold white on dark_blue] 🏛️  TITAN TERMINAL PRO  [/bold white on dark_blue]"
    
    if ticker_info:
        from utils.formatters import get_currency_symbol
        
        symbol = ticker_info.get("symbol", "")
        name = ticker_info.get("name", "")
        price = ticker_info.get("price", 0)
        change = ticker_info.get("change", 0)
        change_pct = ticker_info.get("change_pct", 0)
        
        # Get correct currency symbol for the stock
        currency = get_currency_symbol(symbol)
        
        color = "green" if change >= 0 else "red"
        header_text = f"[bold white on dark_blue] 🏛️  TITAN TERMINAL PRO  [/bold white on dark_blue] │ {name} ({symbol}) │ [{color}]{currency}{price:,.2f} {change:+.2f} ({change_pct:+.2f}%)[/{color}]"
    
    console.print(Panel(header_text, style="blue"))


def display_menu():
    """Display the main menu."""
    menu = """
    [cyan][1][/cyan] Company Profile    [cyan][5][/cyan] Ownership          [cyan][9][/cyan] Watchlist
    [cyan][2][/cyan] Financials         [cyan][6][/cyan] Analyst            [cyan][M][/cyan] Market Overview
    [cyan][3][/cyan] Technical Charts   [cyan][7][/cyan] Options            [cyan][H][/cyan] Help
    [cyan][4][/cyan] Peer Comparison    [cyan][8][/cyan] News & Sentiment   [cyan][Q][/cyan] Exit
    
    [magenta][S][/magenta] Supply Chain (SPLC)   [yellow][0][/yellow] Full AI Analysis (Multi-Model)
    """
    console.print(Panel(menu, title="📋 Menu", border_style="cyan"))


def display_help():
    """Display help information."""
    help_text = """
## 🏛️ TITAN TERMINAL PRO - Help

### Navigation
- Enter a **company name** or **ticker symbol** to search
- Use **number keys (0-9)** to access different analysis modules
- Press **M** for market overview, **H** for help, **Q** to exit

### Modules
| Key | Module | Description |
|-----|--------|-------------|
| 1 | Company Profile | Business overview, executives, key stats |
| 2 | Financials | Income, balance sheet, cash flow, ratios |
| 3 | Technical Charts | Price charts, indicators (RSI, MACD, etc.) |
| 4 | Peer Comparison | Sector peers, relative valuation |
| 5 | Ownership | Institutional, insider, short interest |
| 6 | Analyst | Ratings, price targets, estimates |
| 7 | Options | Options chain, IV, unusual activity |
| 8 | News | Headlines with sentiment analysis |
| 9 | Watchlist | Manage your saved stocks |
| M | Market Overview | Indices, sectors, currencies, commodities |
| 0 | AI Analysis | Full multi-model investment analysis |

### AI Models
The terminal uses local LLMs via Ollama:
- **deepseek-r1** - Reasoning-focused analysis
- **gemma3** - Balanced perspective
- **glm4** - Alternative viewpoint

### Tips
- Search with company names: "Apple", "Microsoft", "Tesla"
- Or use tickers directly: "AAPL", "MSFT", "TSLA"
- Watchlist is saved automatically between sessions
    """
    console.print(Markdown(help_text))
    Prompt.ask("\n[dim]Press Enter to continue[/dim]")


def manage_watchlist():
    """Manage the watchlist."""
    watchlist = load_watchlist()
    
    while True:
        console.clear()
        console.print(Panel("[bold]📋 WATCHLIST[/bold]", border_style="yellow"))
        
        if watchlist["stocks"]:
            wl_table = Table(show_header=True, header_style="bold")
            wl_table.add_column("#", width=3)
            wl_table.add_column("Symbol")
            wl_table.add_column("Name")
            wl_table.add_column("Added")
            
            for i, stock in enumerate(watchlist["stocks"], 1):
                wl_table.add_row(
                    str(i),
                    stock.get("symbol", ""),
                    stock.get("name", "")[:30],
                    stock.get("added", "")[:10]
                )
            
            console.print(wl_table)
        else:
            console.print("[dim]Watchlist is empty.[/dim]")
        
        console.print("\n[cyan][A][/cyan] Add  [cyan][R][/cyan] Remove  [cyan][B][/cyan] Back")
        choice = Prompt.ask("Choose").strip().upper()
        
        if choice == "B":
            break
        elif choice == "A":
            query = Prompt.ask("Enter ticker or company name")
            result = get_ticker_from_name(query)
            if result:
                watchlist["stocks"].append({
                    "symbol": result["symbol"],
                    "name": result["name"],
                    "added": datetime.now().strftime("%Y-%m-%d")
                })
                save_watchlist(watchlist)
                console.print(f"[green]Added {result['symbol']}[/green]")
            else:
                console.print("[red]Could not find company[/red]")
            Prompt.ask("[dim]Press Enter[/dim]")
        elif choice == "R":
            if watchlist["stocks"]:
                idx = Prompt.ask("Enter number to remove")
                try:
                    idx = int(idx) - 1
                    if 0 <= idx < len(watchlist["stocks"]):
                        removed = watchlist["stocks"].pop(idx)
                        save_watchlist(watchlist)
                        console.print(f"[yellow]Removed {removed['symbol']}[/yellow]")
                except:
                    console.print("[red]Invalid number[/red]")
                Prompt.ask("[dim]Press Enter[/dim]")


def run_ai_analysis(ticker, ticker_info):
    """Run full multi-model AI analysis with executive summary."""
    company_name = ticker_info.get('name', ticker)
    console.print(Panel(f"[bold]🤖 AI ANALYSIS: {company_name}[/bold]\n[dim]Running {len(MODELS)} models in parallel...[/dim]", border_style="cyan"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task1 = progress.add_task("[cyan]Fetching fundamental data...", total=None)
        fundamentals = get_financials(ticker)
        
        task2 = progress.add_task("[magenta]Calculating technicals...", total=None)
        technicals = get_technicals(ticker)
        
        task3 = progress.add_task("[yellow]Fetching news...", total=None)
        news_data = get_news(ticker)
        news_items = news_data.get("news", [])
        
        # Show which models are running
        model_names = [m.split(':')[0] for m in MODELS]
        task4 = progress.add_task(f"[green]Running {len(MODELS)} AI models: {', '.join(model_names)}...", total=None)
        
        # Build prompt
        prompt = build_analysis_prompt(
            ticker,
            company_name,
            fundamentals,
            technicals,
            news_items
        )
        
        # Get AI engine and generate reports
        engine = get_engine(MODELS)
        system_prompt = "You are a decisive Wall Street equity analyst. Every company is DIFFERENT - your verdicts must reflect their UNIQUE data. Always cite specific numbers. Be decisive."
        
        reports = engine.generate_multi_model_reports(prompt, system_prompt)
        consensus = engine.get_consensus(reports)
        
        # Generate executive summary
        task5 = progress.add_task("[magenta]Synthesizing executive summary (deepseek-r1)...", total=None)
        executive_summary = engine.generate_executive_summary(reports, consensus, ticker, company_name)
    
    # Render results with executive summary
    render_ai_analysis(reports, consensus, console, executive_summary)



def analyze_company(ticker, ticker_info):
    """Main analysis loop for a company."""
    
    # Cache for fetched data
    cache = {}
    
    while True:
        display_header(ticker_info)
        display_menu()
        
        choice = Prompt.ask("Enter command").strip().upper()
        
        if choice == "Q":
            return "exit"
        
        if choice == "B" or choice == "":
            return "search"
        
        console.print()
        
        try:
            if choice == "1":
                # Company Profile
                with console.status("[cyan]Loading company profile...[/cyan]"):
                    if "profile" not in cache:
                        cache["profile"] = get_company_profile(ticker)
                render_company_profile(cache["profile"], console)
            
            elif choice == "2":
                # Financials
                with console.status("[cyan]Loading financial data...[/cyan]"):
                    if "financials" not in cache:
                        cache["financials"] = get_financials(ticker)
                render_financials(cache["financials"], console)
            
            elif choice == "3":
                # Technical Analysis
                with console.status("[cyan]Calculating technicals...[/cyan]"):
                    if "technicals" not in cache:
                        cache["technicals"] = get_technicals(ticker)
                render_technicals(cache["technicals"], console)
            
            elif choice == "4":
                # Peer Comparison
                with console.status("[cyan]Analyzing peers...[/cyan]"):
                    if "peers" not in cache:
                        cache["peers"] = get_peer_analysis(ticker)
                render_peer_analysis(cache["peers"], console)
            
            elif choice == "5":
                # Ownership
                with console.status("[cyan]Loading ownership data...[/cyan]"):
                    if "ownership" not in cache:
                        cache["ownership"] = get_ownership(ticker)
                render_ownership(cache["ownership"], console)
            
            elif choice == "6":
                # Analyst Data
                with console.status("[cyan]Loading analyst data...[/cyan]"):
                    if "analyst" not in cache:
                        cache["analyst"] = get_analyst_data(ticker)
                render_analyst_data(cache["analyst"], console)
            
            elif choice == "7":
                # Options
                with console.status("[cyan]Loading options chain...[/cyan]"):
                    if "options" not in cache:
                        cache["options"] = get_options_data(ticker)
                render_options_data(cache["options"], console)
            
            elif choice == "8":
                # News
                with console.status("[cyan]Fetching news...[/cyan]"):
                    if "news" not in cache:
                        cache["news"] = get_news(ticker)
                render_news(cache["news"], console)
            
            elif choice == "9":
                # Watchlist
                manage_watchlist()
                continue
            
            elif choice == "M":
                # Market Overview
                with console.status("[cyan]Loading market data...[/cyan]"):
                    market_data = get_market_data()
                render_market_overview(market_data, console)
            
            elif choice == "0":
                # Full AI Analysis
                run_ai_analysis(ticker, ticker_info)
            
            elif choice == "S":
                # Supply Chain (SPLC)
                with console.status("[magenta]Loading supply chain data...[/magenta]"):
                    if "supply_chain" not in cache:
                        cache["supply_chain"] = get_supply_chain(ticker)
                render_supply_chain(cache["supply_chain"], console)
            
            elif choice == "H":
                display_help()
                continue
            
            else:
                # Try as a new search
                result = get_ticker_from_name(choice)
                if result:
                    return ("new_ticker", result)
                console.print(f"[yellow]Unknown command: {choice}[/yellow]")
        
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")


def main():
    """Main terminal loop."""
    display_header()
    check_ollama_status()
    
    # Show all models that power the terminal
    model_names = [m.split(':')[0] for m in MODELS]
    console.print(f"""
    [bold white]Welcome to TITAN TERMINAL PRO[/bold white]
    
    [dim]Powered by {len(MODELS)} local LLMs: {', '.join(model_names)}[/dim]
    """)
    
    while True:
        console.print()
        query = Prompt.ask("[bold cyan]Search company (or 'M' for market, 'Q' to quit)[/bold cyan]").strip()
        
        if not query:
            continue
        
        if query.upper() == "Q":
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        if query.upper() == "M":
            with console.status("[cyan]Loading market data...[/cyan]"):
                market_data = get_market_data()
            render_market_overview(market_data, console)
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            continue
        
        if query.upper() == "H":
            display_help()
            continue
        
        # Search for company
        with console.status(f"[cyan]Searching for '{query}'...[/cyan]"):
            result = get_ticker_from_name(query)
        
        if not result:
            console.print(f"[red]Could not find company matching '{query}'[/red]")
            continue
        
        ticker = result["symbol"]
        console.print(f"[green]✔ Found:[/green] {result['name']} ({ticker}) on {result['exchange']}")
        
        # Get current price for header
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            result["price"] = info.get("regularMarketPrice") or info.get("currentPrice") or 0
            result["change"] = result["price"] - (info.get("previousClose") or result["price"])
            result["change_pct"] = (result["change"] / info.get("previousClose", 1)) * 100 if info.get("previousClose") else 0
        except:
            result["price"] = 0
            result["change"] = 0
            result["change_pct"] = 0
        
        # Enter analysis mode
        while True:
            action = analyze_company(ticker, result)
            
            if action == "exit":
                console.print("[yellow]Goodbye![/yellow]")
                return
            
            if action == "search":
                break
            
            if isinstance(action, tuple) and action[0] == "new_ticker":
                result = action[1]
                ticker = result["symbol"]
                
                # Fetch price data for new ticker
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    result["price"] = info.get("regularMarketPrice") or info.get("currentPrice") or 0
                    result["change"] = result["price"] - (info.get("previousClose") or result["price"])
                    result["change_pct"] = (result["change"] / info.get("previousClose", 1)) * 100 if info.get("previousClose") else 0
                except:
                    result["price"] = 0
                    result["change"] = 0
                    result["change_pct"] = 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
        sys.exit(0)
