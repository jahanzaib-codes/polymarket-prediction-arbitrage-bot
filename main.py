import time
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from config import get_config
from scanner import PolymarketScanner
from executor import PolymarketExecutor

console = Console()

def print_banner():
    banner = """[bold cyan]
  ╔════════════════════════════════════════════════════════════════════╗
  ║    ⚡ POLYMARKET PREDICTION & ARBITRAGE BOT v1.0.0                 ║
  ║    ⚡ CLOB API | Bundle Mispricing | 5-Min BTC Market Engine        ║
  ║    ⚡ Developed by Jahanzaib (https://github.com/jahanzaib-codes)   ║
  ╚════════════════════════════════════════════════════════════════════╝
    [/bold cyan]"""
    console.print(banner)

def main():
    print_banner()
    config = get_config()

    console.print(f"[bold yellow]Mode:[/bold yellow] {'[bold green]SIMULATION (Dry-Run)[/bold green]' if config.simulation_mode else '[bold red]LIVE TRADING[/bold red]'}")
    console.print(f"[bold yellow]Min Spread Edge:[/bold yellow] {config.min_spread_percent}% | [bold yellow]Trade Size:[/bold yellow] ${config.trade_size_usdc} USDC\n")

    scanner = PolymarketScanner(config)
    executor = PolymarketExecutor(config)

    console.print("[cyan]Connecting to Polymarket CLOB endpoints & scanning active markets...[/cyan]\n")

    try:
        markets = scanner.fetch_active_markets(limit=8)
        table = Table(title="Live Polymarket Monitored Markets", show_header=True, header_style="bold magenta")
        table.add_column("Market Question", style="dim", width=40)
        table.add_column("YES Ask", justify="right")
        table.add_column("NO Ask", justify="right")
        table.add_column("Bundle Cost", justify="right")
        table.add_column("Arbitrage Edge", justify="right")
        table.add_column("Status", justify="center")

        for m in markets:
            opp = scanner.evaluate_arbitrage(m)
            if opp:
                edge_style = "bold green" if opp.is_arbitrage_profitable else "white"
                status_badge = "[bold green]OPPORTUNITY[/bold green]" if opp.is_arbitrage_profitable else "[dim]Scanning[/dim]"

                table.add_row(
                    opp.question[:38] + "...",
                    f"${opp.yes_best_ask:.3f}",
                    f"${opp.no_best_ask:.3f}",
                    f"${opp.bundle_cost:.3f}",
                    f"[{edge_style}]{opp.spread_edge_percent}%[/{edge_style}]",
                    status_badge
                )

                if opp.is_arbitrage_profitable:
                    res = executor.execute_arbitrage(opp)
                    console.print(f"\n[bold green]🚀 Arbitrage Executed:[/bold green] {opp.question[:30]} | Edge: {opp.spread_edge_percent}% | Latency: {res['latency_ms']}ms")

        console.print(table)
        console.print("\n[dim]Daemon active. Press Ctrl+C to exit.[/dim]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Engine shut down gracefully.[/yellow]")
        sys.exit(0)

if __name__ == "__main__":
    main()
