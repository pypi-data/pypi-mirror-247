from time import sleep
import path
import sys
from citros import Citros
from pathlib import Path
from rich import print, inspect, print_json
from rich.rule import Rule
from rich.panel import Panel
from rich.padding import Padding
from rich.logging import RichHandler
from rich.console import Console
from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter
from citros.utils import str_to_bool, suppress_ros_lan_traffic
from citros.batch import Batch
from rich.table import Table
from rich.console import Console
from rich import pretty
from rich import box

import json


pretty.install()


import glob
from .config import config

from citros import CitrosNotFoundException

directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)


from InquirerPy import prompt, inquirer
from prompt_toolkit.validation import Validator, ValidationError


class NumberValidator(Validator):
    """
    small helper class for validating user input during an interactive session.
    """

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message="Please enter a number", cursor_position=len(document.text)
            )


############################# CLI implementation ##############################
def init(args, argv):
    """
    :param args.dir:
    :param args.debug:
    :param args.verbose:
    """
    print(f'initializing CITROS at "{Path(args.dir).resolve()}". ')
    citros = Citros(new=True, root=args.dir, verbose=args.verbose, debug=args.debug)
    if args.debug:
        print("[green]done initializing CITROS")


def run(args, argv):
    """
    :param args.simulation_name:
    :param args.index:
    :param args.completions:

    :param args.batch_name:
    :param args.batch_message:

    :param args.lan_traffic:

    :param args.debug:
    :param args.verbose:
    """
    try:
        citros = Citros(root=args.dir, verbose=args.verbose, debug=args.debug)
    except CitrosNotFoundException:
        print(
            f'[red] "{Path(args.dir).expanduser().resolve()}" has not been initialized. cant run "citros run" on non initialized directory.'
        )
        return

    if args.debug:
        print("[green]done initializing CITROS")

    batch_name = args.batch_name
    batch_message = args.batch_message

    if not batch_name and str_to_bool(citros.settings["force_batch_name"]):
        print("[red]Please supply a batch name with flag -n <name>.")
        print(
            Panel.fit(
                Padding('You may run [green]"citros run -n <name>" ', 1), title="help"
            )
        )
        return False

    if not batch_message and str_to_bool(citros.settings["force_message"]):
        print("[red]Please supply a batch message with flag -m <message>.")
        print(
            Panel.fit(
                Padding('You may run [green]"citros run -m <message>"', 1), title="help"
            )
        )
        return False

    simulation = choose_simulation(
        citros,
        args.simulation_name,
    )

    root_rec_dir = f"{args.dir}/.citros/data"
    if config.RECORDINGS_DIR:
        root_rec_dir = config.RECORDINGS_DIR

    batch = Batch(
        root_rec_dir,
        simulation,
        name=batch_name,
        mesaage=batch_message,
        version=args.version,
        verbose=args.verbose,
        debug=args.debug,
    )
    batch.run(
        args.completions,
        args.index,
        ros_domain_id=config.ROS_DOMAIN_ID,
        trace_context=config.TRACE_CONTEXT,
    )

    # TODO: check if database is running. if so, send data to database.
    print(f"[green]CITROS run completed successfully. ")
    print(
        f"[green]You may run [blue]'citros data service'[/blue] to get access to your data using CITROS API."
    )


# helper function
def choose_simulation(citros: Citros, simulation_name):
    simulations_dict = {}
    for s in citros.simulations:
        simulations_dict[s.name] = s

    if simulation_name:
        return simulations_dict[simulation_name]
    sim_names = simulations_dict.keys()

    # sanity check - should never happen because internal_sync will fail if there
    #                isn't at least one simulation file.
    if not sim_names:
        print(
            f"[red]There are currently no simulations in your {citros.SIMS_DIR} folder. \
                	 Please create at least one simulation for your project."
        )
        return

    # interactive
    answers = prompt(
        [
            {
                "type": "list",
                "name": "sim_names",
                "message": "Please choose the simulation you wish to run:",
                "choices": sim_names,
            }
        ]
    )

    sim_name = answers.get("sim_names")
    return simulations_dict[sim_name]


def doctor(args, argv):
    # TODO[critical]: implement doctor
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


############################# Simulation implementation ##############################
def simulation_list(args, argv):
    # TODO[critical]: implement data_status
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


def simulation_run(args, argv):
    # TODO[critical]: implement data_status
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


####################### parameter setup implementation ##############################
def parameter_setup_new(args, argv):
    # TODO[critical]: implement data_status
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


def parameter_setup_list(args, argv):
    # TODO[critical]: implement data_status
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


def parameter_setup(args, argv):
    # TODO[critical]: implement data_status
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


############################# DATA implementation ##############################
def data(args, argv):
    # -s simulation
    # -n name
    # -i version index
    # print batch info.
    root = Path(args.dir).expanduser().resolve() / ".citros/data"

    # simulation
    simulations_glob = sorted(glob.glob(f"{str(root)}/*"))
    simulations = []
    for sim in simulations_glob:
        if Path(sim).is_dir():
            simulations.append(str(sim).split("/")[-1])

    if simulations == []:
        print(f"There are currently no simulations in {root} folder.")
        print("Go wild and run as many simulation as you can with CITROS. ")
        print(
            Panel.fit(
                Padding('[green]citros run -n <name>" -m <message', 1),
                title="help",
            )
        )
        return
    chosen_simulation = inquirer.fuzzy(
        message="Select Simulation:", choices=simulations, default="", border=True
    ).execute()

    # batch
    batch_glob = sorted(glob.glob(f"{str(root / chosen_simulation)}/*"))
    batches = []
    for batch in batch_glob:
        if Path(batch).is_dir():
            batches.append(str(batch).split("/")[-1])

    chosen_batch = inquirer.fuzzy(
        message="Select Batch:", choices=batches, default="", border=True
    ).execute()

    # version
    version_glob = sorted(glob.glob(f"{str(root / chosen_simulation/ chosen_batch)}/*"))
    versions = []
    for version in version_glob:
        if Path(version).is_dir():
            versions.append(str(version).split("/")[-1])

    version = inquirer.fuzzy(
        message="Select Version:", choices=versions, default="", border=True
    ).execute()

    # root / chosen_simulation / chosen_batch / version

    action = inquirer.fuzzy(
        message="Select Action:",
        choices=["info", "load", "unload", "delete"],
        default="",
        border=True,
    ).execute()

    if action == "info":
        batch = Batch(
            root,
            chosen_simulation,
            name=chosen_batch,
            version=version,
            debug=args.debug,
            verbose=args.verbose,
        )
        # inspect(batch)
        console = Console()
        console.rule(f"{chosen_simulation} / {chosen_batch} / {version}")
        console.print_json(data=batch.data)

    elif action == "load":
        print(
            f"Uploading data to DB... {root / chosen_simulation / chosen_batch / version}"
        )
        batch = Batch(
            root,
            chosen_simulation,
            name=chosen_batch,
            version=version,
            debug=args.debug,
            verbose=args.verbose,
        )
        batch.upload()
        console = Console()
        console.rule(f"{chosen_simulation} / {chosen_batch} / {version}")
        console.print_json(data=batch.data)

    elif action == "unload":
        print(
            f"Dropping data from DB... {root / chosen_simulation / chosen_batch / version}"
        )
        batch = Batch(
            root,
            chosen_simulation,
            name=chosen_batch,
            version=version,
            debug=args.debug,
            verbose=args.verbose,
        )
        batch.unload()

    elif action == "delete":
        print(f"deleting data from {root / chosen_simulation / chosen_batch / version}")
        import shutil

        shutil.rmtree(root / chosen_simulation / chosen_batch / version)


def data_list(args, argv):
    root = Path(args.dir).expanduser().resolve() / ".citros/data"

    table = Table(title=f"Simulation Runs in: [blue]{root}", box=box.SQUARE)
    table.add_column("Simulation", style="cyan", no_wrap=True)
    table.add_column("Run name", style="magenta", justify="left")
    table.add_column("Versions", justify="left", style="green")
    table.add_column("Data", justify="right", style="green")

    simulations = sorted(glob.glob(f"{str(root)}/*"))
    for sim in simulations:
        names = sorted(glob.glob(f"{sim}/*"))
        _simulation = sim.split("/")[-1]
        for name in names:
            versions = sorted(glob.glob(f"{name}/*"))
            _name = name.split("/")[-1]

            for version in versions:
                data_status = json.loads((Path(version) / "info.json").read_text())[
                    "data_status"
                ]

                if data_status == "LOADED":
                    data_status_clore = "green"
                elif data_status == "UNLOADED":
                    data_status_clore = "yellow"
                else:
                    data_status_clore = "red"

                table.add_row(
                    _simulation,
                    _name,
                    version.split("/")[-1],
                    f"[{data_status_clore}]{data_status}",
                )

                # for printing.
                _simulation = None
                _name = None

    console = Console()
    console.print(table)


def data_service(args, argv):
    """
    :param args.dir
    :param args.debug:
    :param args.verbose:
    :param args.project_name:
    """
    from citros import data_access_service, NoDataFoundException

    root = Path(args.dir).expanduser().resolve() / ".citros/data"
    print(
        Panel.fit(
            f"""started at [green]http://{args.host}:{args.port}[/green].
API: open [green]http://{args.host}:{args.port}/redoc[/green] for documantation
Listening on: [green]{str(root)}""",
            title="[green]CITROS service",
        )
    )
    try:
        # TODO[important]: make async
        data_access_service(
            str(root),
            time=args.time,
            host=args.host,
            port=int(args.port),
            debug=args.debug,
            verbose=args.verbose,
        )
    except NoDataFoundException:
        print(
            f'[red] "{Path(args.dir).expanduser().resolve()}" has not been initialized. cant run "citros data service" on non initialized directory.'
        )
        return


def data_service_status(args, argv):
    # TODO[important]: implement data_status after making this sevice async. return status of service.
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


# Hot Reload
def data_load(args, argv):
    pass


# Hot Reload
def data_unload(args, argv):
    pass


def init_db():
    """
    initializing the DB
    """
    from citros import CitrosDB

    citrosDB = CitrosDB(
        config.POSTGRES_USERNAME,
        config.POSTGRES_PASSWORD,
        config.CITROS_DATA_HOST,
        config.CITROS_DATA_PORT,
        config.POSTGRES_DATABASE,
    )

    citrosDB.init_db()


def data_db_create(args, argv):
    import docker

    inspect(config)
    try:
        client = docker.from_env()
    except Exception as e:
        print(
            "[red]Docker is not running. Please start docker and try again. exiting..."
        )
        if args.verbose:
            raise e
        return

    try:
        container = client.containers.get(config.DB_CONTAINER_NAME)
        container.start()
        # inspect(container)
        print(f"[green]CITROS DB is created")
        return
    except docker.errors.NotFound:
        container = None

    container = client.containers.run(
        "postgres",
        name=config.DB_CONTAINER_NAME,
        environment=[
            f"POSTGRES_USER={config.POSTGRES_USERNAME}",
            f"POSTGRES_PASSWORD={config.POSTGRES_PASSWORD}",
            f"POSTGRES_DB={config.POSTGRES_DATABASE}",
        ],
        detach=True,
        ports={"5432/tcp": config.CITROS_DATA_PORT},
    )
    sleep(1)
    print(f"[green]CITROS Initializing DB...")
    init_db()
    print(
        f"[green]CITROS DB is running at: {config.CITROS_DATA_HOST}:{config.CITROS_DATA_PORT}"
    )


def data_db_status(args, argv):
    import docker

    try:
        client = docker.from_env()
    except Exception as e:
        print(
            "[red]Docker is not running. Please start docker and try again. exiting..."
        )
        if args.verbose:
            raise e
        return

    container = client.containers.get(config.DB_CONTAINER_NAME)
    # print(container)
    if container:
        print(
            f"[green]CITROS DB is running at: {container.attrs['NetworkSettings']['IPAddress']}:{container.attrs['NetworkSettings']['Ports']['5432/tcp'][0]['HostPort']}"
        )
    else:
        print(
            f"[red]CITROS DB is not running. Please run 'citros data db create' to create a new DB."
        )

    # console = Console()
    # with console.screen(hide_cursor=False) as screen:
    #     for line in container.stats(stream=True):
    #         stat = line.strip()
    #         stat = json.loads(stat)
    #         stat = json.dumps(stat, indent=4)
    #         # console.print(stat)
    #         screen.update(Panel(str(stat)))
    #         # inspect(stat)
    #         # sleep(5)
    #         #TODO: create status panel.


def data_db_stop(args, argv):
    import docker

    try:
        client = docker.from_env()
    except Exception as e:
        print(
            "[red]Docker is not running. Please start docker and try again. exiting..."
        )
        if args.verbose:
            raise e
        return

    try:
        container = client.containers.get(config.DB_CONTAINER_NAME)
        container.stop()
        print(f"[green]CITROS DB is stopped.")
    except docker.errors.NotFound:
        print(f"[green]CITROS DB is not running.")


def data_db_logs(args, argv):
    import docker

    try:
        client = docker.from_env()
    except Exception as e:
        print(
            "[red]Docker is not running. Please start docker and try again. exiting..."
        )
        if args.verbose:
            raise e
        return

    try:
        container = client.containers.get(config.DB_CONTAINER_NAME)
        console = Console()
        console.rule(
            f" Logs from CITROS database container: {config.DB_CONTAINER_NAME}"
        )
        for line in container.logs(stream=True, follow=False):
            print(line.decode("utf8").strip())
            # console.line(line.decode("utf8").strip())
            # console.log(line.decode("utf8").strip())

        console.rule()
    except docker.errors.NotFound:
        print(
            f"[red]CITROS DB is not running. Please run 'citros data db create' to create a new DB."
        )
        print(
            Panel.fit(
                Padding('You may run [green]"citros data db create" ', 1), title="help"
            )
        )


def data_db_clean(args, argv):
    import docker

    try:
        client = docker.from_env()
    except Exception as e:
        print(
            "[red]Docker is not running. Please start docker and try again. exiting..."
        )
        if args.verbose:
            raise e
        return

    container = client.containers.get(config.DB_CONTAINER_NAME)
    try:
        container.remove()
    except docker.errors.APIError as e:
        if e.status_code == 409:
            print("[red]CITROS DB is running. Please stop it before cleaning.")
            print(
                Panel.fit(
                    Padding('You may run [green]"citros data db stop" ', 1),
                    title="help",
                )
            )
        else:
            raise e


############################# REPORT implementation ##############################
def report_generate(args, argv):
    # TODO[critical]: implement report_generate
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")


def report_validate(args, argv):
    # TODO[critical]: implement report_validate
    print(f"[red] 'citros {args.func.__name__}' is Not implemented yet")
