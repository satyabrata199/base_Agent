from rich.console import Console

console = Console()

def log_info(message: str):
    console.print(f"[bold green][INFO][/bold green] {message}")

def log_error(message: str):
    console.print(f"[bold red][ERROR][/bold red] {message}")

def log_debug(message: str):
    console.print(f"[bold blue][DEBUG][/bold blue] {message}")