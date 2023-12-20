import subprocess
import platform
from getpass import getpass
from typing import Union, Optional, Any
from rich.color import ANSI_COLOR_NAMES
from rich.console import Console
from ci.utility import validation

console = Console()


def write(
    obj: Union[str, Any],
    color: Optional[str] = None,
    style: Optional[str] = None,
    pn: bool = False,
    verbose: bool = True,
) -> None:
    """
    verbose print utility with rich formatting

    Args:
        obj (Union[str, Any]): object to print
        color (Optional[str], optional): color of string if string. Defaults to None.
        pn (bool, optional): prepend newline if string. Defaults to False.
        verbose (bool, optional): print object. Defaults to True.

    Raises:
        ValueError: invalid color
    """
    if verbose:
        if isinstance(obj, str):
            if pn:
                obj = f"{obj}"
            if color is None:
                console.print(obj)
            else:
                if color in ANSI_COLOR_NAMES.keys():
                    console.print(f"[{color}]{obj}[/{color}]", style=style)
                else:
                    for acn in ANSI_COLOR_NAMES.keys():
                        console.print(acn, style=style)
                    raise ValueError(
                        f"argument passed to 'color' must be one of the colors listed above"
                    )
        else:
            console.print(obj)


# 🛰


def to_clipboard(text: str) -> None:
    """
    Copies input text to clipboard.

    Args:
        text (str): text to copy to clipboard

    NOTE
    It detects the operating system and uses the appropriate command:

    - pbcopy on MacOS
    - clip on Windows
    - xclip or xsel on Linux

    """
    try:
        os_name = platform.system()
        if os_name == "Darwin":  # MacOS
            process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        elif os_name == "Windows":
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
        elif os_name == "Linux":
            # Use xclip or xsel, checking which one is installed
            if subprocess.call("command -v xclip", shell=True) == 0:
                process = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
                )
            elif subprocess.call("command -v xsel", shell=True) == 0:
                process = subprocess.Popen(
                    ["xsel", "--clipboard", "--input"], stdin=subprocess.PIPE
                )
            else:
                print("No suitable clipboard utility found on your system.")
                return
        else:
            error_output("Unsupported OS")
        process.communicate(text.encode("utf-8"))
    except Exception as e:
        error_output(str(e))


def visible_input(message: str, color: str = "dark_orange", icon: str = "➜"):
    write(f"{message}", color=color)
    user_input = str(input(f"{icon} "))
    return user_input


def secure_input(message: str, color: str = "dark_orange", icon: str = "🔑"):
    write(f"[{color}]{message}[/{color}]")
    user_input = getpass(f"{icon} ")
    return user_input


def password_input():
    return secure_input(message="\nEnter your password.\n")


def first_name_input() -> str:
    return visible_input(message="\nEnter your first name.\n")


def last_name_input() -> str:
    return visible_input(message="\nEnter your last name.\n")


def email_input() -> str:
    return visible_input(message="\nEnter your email address.\n")


def warn_output(message: str) -> None:
    write(f"{message}", color="yellow")


def info_output(message: str) -> None:
    write(f"{message}", color="deep_sky_blue3")


def success_output(message: str) -> None:
    write(f"{message}", color="light_green")


def failure_output(message: str) -> None:
    write(f"{message}", color="red")


def error_output(message: str) -> None:
    write(f"{message}", color="red")


def command_output(command: str, copy: bool = False) -> None:
    write(f"❯ {command}", color="green")
    if copy:
        to_clipboard(text=command)
        info_output("This command has been copied to your clipboard.")


def set_new_password_input() -> str:
    length = 16
    numeric = 1
    special = 1
    uppercase = 1
    lowercase = 1
    info_output("\nYour new password must meet the following criteria: ")
    info_output(
        f"\n• Greater than {str(length)} characters long"
        f"\n• Has at least {str(numeric)} numeric characters"
        f"\n• Has at least {str(special)} special characters"
        f"\n• Has at least {str(uppercase)} uppercase characters"
        f"\n• Has at least {str(lowercase)} lowercase characters"
    )
    info_output(
        "\nWe strongly recommend using a password manager capable of generating randomized passwords."
    )

    while True:
        password = secure_input("\nPlease enter your new password.\n")
        valid_password, results = validation.check_password(
            password=password,
            length=length,
            numeric=numeric,
            special=special,
            uppercase=uppercase,
            lowercase=lowercase,
        )

        if not valid_password:
            failure_output("\nPassword does not meet the criteria, please try again.\n")
            for key, val in results.items():
                write(
                    f"[cyan]{key}[/cyan]: {'[light_green]passed' if val[0] else '[red]failed'}"
                )
            continue

        confirm_password = secure_input("Please re-enter your password for confirmation.")

        if password == confirm_password:
            return password
        else:
            failure_output("Passwords do not match. Please try again.")
