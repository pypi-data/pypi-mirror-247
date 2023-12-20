import regex as re
from ci.utility import terminal
from rich.console import Console

c = Console()


def check_email_format(email: str, verbose: bool = False) -> bool:
    "returns True if valid, else False"
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    valid = bool(re.match(pattern, email))
    if (verbose) and (not valid):
        c.print("[red]\nEmail address failed regex validation.")
    return valid


def check_password(
    password: str,
    length: int = 16,
    numeric: int = 1,
    special: int = 1,
    uppercase: int = 1,
    lowercase: int = 1,
    verbose: bool = False,
) -> tuple[bool, dict[str, bool]]:
    results = {
        "length": (len(password) >= length, length),
        "numeric": (len(re.findall(r"\d", password)) >= numeric, numeric),
        "special": (
            len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) >= special,
            special,
        ),
        "uppercase": (len(re.findall(r"[A-Z]", password)) >= uppercase, uppercase),
        "lowercase": (len(re.findall(r"[a-z]", password)) >= lowercase, lowercase),
    }
    valid = all([val[0] for val in results.values()])
    failures = [key for key, val in results.items() if not val[0]]
    if verbose and len(failures):
        terminal.error_output("Password failed the required password validation checks:")
        for key, val in results.items():
            if not val[0]:
                if key == "length":
                    terminal.info_output(f"• Must contain more than {val[1]} characters")
                else:
                    terminal.info_output(
                        f"• Must contain more than {val[1]} {key} characters"
                    )
    return valid, results
