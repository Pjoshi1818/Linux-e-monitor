import psutil
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

console = Console()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return cpu, memory, disk


def metric_cards(cpu, memory, disk):

    cards = [
        Panel(
            f"[bold white]{cpu}%[/bold white]",
            title="[cyan]CPU",
            border_style="cyan",
            expand=True,
        ),
        Panel(
            f"[bold white]{memory}%[/bold white]",
            title="[yellow]MEMORY",
            border_style="yellow",
            expand=True,
        ),
        Panel(
            f"[bold white]{disk}%[/bold white]",
            title="[red]DISK",
            border_style="red",
            expand=True,
        ),
    ]

    console.print(Columns(cards))


def process_table():

    table = Table(
        title="Top Running Processes",
        header_style="bold blue",
        expand=True
    )

    table.add_column("PID", width=10)
    table.add_column("Process")
    table.add_column("CPU %", justify="right", width=10)

    processes = []

    for proc in psutil.process_iter(
        ["pid", "name", "cpu_percent"]
    ):
        try:
            name = proc.info["name"]

            if not name:
                continue

            if name == "System Idle Process":
                continue

            processes.append(proc.info)

        except:
            continue

    processes = sorted(
        processes,
        key=lambda x: x["cpu_percent"],
        reverse=True
    )

    for proc in processes[:10]:
        table.add_row(
            str(proc["pid"]),
            proc["name"],
            str(proc["cpu_percent"])
        )

    console.print(table)

def search_process():

    keyword = input(
        "Enter process name to search: "
    ).lower()

    table = Table(
        title=f"Search Results: {keyword}",
        header_style="bold green",
        expand=True
    )

    table.add_column("PID")
    table.add_column("Process Name")
    table.add_column("CPU %")

    found = False

    for proc in psutil.process_iter(
        ["pid", "name", "cpu_percent"]
    ):

        try:
            name = proc.info["name"]

            if name and keyword in name.lower():

                table.add_row(
                    str(proc.info["pid"]),
                    name,
                    str(proc.info["cpu_percent"])
                )

                found = True

        except:
            continue

    if found:
        console.print(table)

    else:
        console.print(
            "[red]No matching process found[/red]"
        )

while True:

    clear_screen()

    console.print(
        Panel.fit(
            "[bold green]SYSTEM RESOURCE MONITOR[/bold green]",
            border_style="green"
        )
    )

    cpu, memory, disk = system_stats()

    metric_cards(cpu, memory, disk)

    console.print()

    process_table()

    console.print(
        "\n[bold cyan][K][/bold cyan] Kill Process    "
        "[bold green][S][/bold green] Search Process    "
        "[bold red][Q][/bold red] Quit    "
        "[bold yellow][Enter][/bold yellow] Refresh"
    )

    choice = input("Choose: ").lower()

    if choice == "s":
        search_process()
        input("Press Enter...")

    elif choice == "k":
        pid = input("Enter PID: ")

        try:
            os.kill(int(pid), 9)
            console.print("[green]Process killed successfully[/green]")

        except Exception as e:
            console.print(f"[red]{e}[/red]")

        input("Press Enter...")

    elif choice == "q":
        break