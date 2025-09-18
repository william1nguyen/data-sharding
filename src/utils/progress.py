import time

G, B, Y, R, C, M, BOLD, RESET = (
    "\033[92m",
    "\033[94m",
    "\033[93m",
    "\033[91m",
    "\033[96m",
    "\033[95m",
    "\033[1m",
    "\033[0m",
)


def progress_bar(current, total, title="", start_time=None):
    """Ultra compact colorful progress bar"""
    if start_time is None:
        start_time = time.time()

    pct = (current / total) * 100
    bar = "█" * int(20 * current / total) + "░" * (20 - int(20 * current / total))
    elapsed = time.time() - start_time
    speed = int(current / elapsed) if elapsed > 0.5 else 0

    if current == total:
        print(
            f"\r{C}{title}{RESET} [{G}{bar}{RESET}] {G}✓ {total:,} done{RESET}     ",
            end="\n",
            flush=True,
        )
    else:
        speed_str = f" {Y}{speed}{RESET}/s" if speed > 0 else ""
        print(
            f"\r{C}{title}{RESET} [{B}{bar}{RESET}] {Y}{pct:.0f}%{RESET}{speed_str}   ",
            end="",
            flush=True,
        )


def info(msg):
    """Info message with blue color"""
    print(f"{B}ℹ {msg}{RESET}")


def success(msg):
    """Success message with green color"""
    print(f"{G}✓ {msg}{RESET}")


def error(msg):
    """Error message with red color"""
    print(f"{R}❌ {msg}{RESET}")


def warn(msg):
    """Warning message with yellow color"""
    print(f"{Y}⚠ {msg}{RESET}")


def header(msg):
    """Header message with bold cyan"""
    print(f"\n{BOLD}{C}🚀 {msg}{RESET}")


def inline_success(msg):
    """Inline success without newline"""
    print(f"{G}✓ {msg}{RESET}", end=" ")


def inline_error(msg):
    """Inline error without newline"""
    print(f"{R}❌ {msg}{RESET}", end=" ")
