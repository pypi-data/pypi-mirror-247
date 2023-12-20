import subprocess
from pick import pick
import rich_click as click
from pycooltext import cooltext
from ci.utility import terminal, validation, streamlit
from ci.core import cephalon
from ci import var


class ConsoleSequence:
    @staticmethod
    def run_account_register():
        first_name = terminal.first_name_input()
        last_name = terminal.last_name_input()
        email = terminal.email_input()
        while not validation.check_email_format(email=email, verbose=True):
            email = terminal.email_input()
        result = cephalon.account.register(
            email=email, first_name=first_name, last_name=last_name
        )
        print()
        if result.is_ok():
            terminal.success_output(result.ok_value)
            terminal.info_output("Please check your email for a temporary password.")
        else:
            terminal.failure_output(result.err_value)

    # todo: implement
    @staticmethod
    def run_account_confirm():
        raise NotImplementedError()
        temporary_password = terminal.secure_input(
            "\nPlease enter the temporary password emailed to you.\n"
        )
        new_password = terminal.set_new_password_input()
        while not validation.check_password(new_password, verbose=True):
            new_password = terminal.set_new_password_input()
        # result = nexus.account.confirm(email=
        #     temporary_password=temporary_password, new_password=new_password
        # )

    @staticmethod
    def run_account_login():
        # todo: check if already logged in (tokens cached), warn logging in again overrides previous
        email = terminal.email_input()
        while not validation.check_email_format(email=email, verbose=True):
            email = terminal.email_input()
        password = terminal.password_input()
        result = cephalon.account.login(email=email, password=password)
        print()
        if result.is_ok():
            terminal.success_output(result.ok_value)
        else:
            terminal.failure_output(result.err_value)


@click.group(name="ci", invoke_without_command=True, help="Cephalon Interface CLI.")
@click.version_option(var.PACKAGE_VERSION, prog_name=var.PACKAGE_NAME)
@click.pass_context
def entry(ctx):
    if ctx.invoked_subcommand is None:
        cooltext("CI")
        terminal.write(f"[deep_sky_blue3]version [dark_orange]{var.PACKAGE_VERSION}")
        if cephalon.account.authenticated:
            terminal.write("authenticated", color="light_green")
        else:
            terminal.write("not logged in", color="red")


@entry.group(name="account", help="Account interface utilities.")
def account():
    pass


# todo: implement
# @account.command(name="status")
# def account_status() -> None:
#     _status = status()
#     terminal.write(f"\nAccount Status: {_status.value.upper()}\n")
#     if _status == LocalAccountStatus.UNINITIALIZED:
#         terminal.info_output("To register, run the following command:")
#         terminal.command_output("ci account register\n")
#         terminal.info_output("To login, run the following command:")
#         terminal.command_output("ci account login")
#     elif _status == LocalAccountStatus.EMAIL_UNVERIFIED:
#         pass


@account.command(name="register", help="Register a new account.")
@click.option(
    "--confirm/--no-confirm",
    "-c/-nc",
    type=bool,
    default=True,
    help="Include the email confirmation step",
)
def account_register(confirm: bool) -> None:
    ConsoleSequence.run_account_register()
    if confirm:
        ConsoleSequence.run_account_confirm()


@account.command(name="confirm", help="Confirm your email address.")
def account_confirm():
    ConsoleSequence.run_account_confirm()


@account.command(name="logout", help="Log out of currently logged in account.")
def account_logout():
    cephalon.account.logout()


@account.command(name="login", help="Login to an existing account.")
def account_login():
    ConsoleSequence.run_account_login()


@account.command(name="recover", help="Request a password reset.")
def account_recover():
    raise NotImplementedError()


@account.command(name="info", help="View account information.")
def account_info():
    raise NotImplementedError()


@account.command(name="access", help="View table of available resources.")
def account_access():
    pass


@account.command(name="request", help="Request access to a particular resource.")
def account_request():
    pass


@entry.group(name="app", help="Graphical user interface utilities.")
def app():
    pass


@app.command(name="start", help="Start graphical user interface.")
@click.option(
    "--open-browser/--no-open-browser",
    "-o/-no",
    type=bool,
    default=False,
    required=True,
    help="Open the app automatically in a browser window.",
)
# todo: implement options
# todo.sub: add run in background option
# @click.option(
#     "--force/--no-force",
#     "-f/-nf",
#     type=bool,
#     help="Force app start even if not authenticated.",
# )
# @click.option(
#     "--dev/--no-dev",
# )
# @click.option(
#     "--port",
# )
def gui_start(open_browser: bool) -> None:
    subprocess.run(
        streamlit.make_app_start_command(
            app_path=str(var.PATH_APP_ENTRY),
            open_browser=open_browser,
        )
    )
