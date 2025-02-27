"""Command line interface for running jobs."""

import click as ck 

from pathlib import Path

from pbs_server import PBSServer

debug = False

@ck.command()
@ck.argument("hostname", type=str)
@ck.argument("remote_path", type=ck.Path(
    exists=False, path_type=Path,
))
def launch(
    hostname: str,
    remote_path: Path
):
    if debug:
        print(f"Launching job on {hostname} with remote path {remote_path}")
        print(type(remote_path))

    katana = PBSServer("katana", verbose=False, print_output=False)



    






if __name__ == "__main__":
    launch()


