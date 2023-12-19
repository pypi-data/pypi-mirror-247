# stdlib
import os, sys

# local
from .utils import StatusWriter
from .utils.ci_detection import detected_CI
from . import __version__ as __package_version

# installed
import click

CONFIG_PREFIX = 'ATST'
CLICK_CONTEXT_SETTINGS = { 'auto_envvar_prefix': CONFIG_PREFIX }

Status = StatusWriter()
CI = detected_CI()

@click.group(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option('--debug', is_flag=True, hidden=True,
    default=os.getenv('DEBUG', False) or os.getenv(f'{CONFIG_PREFIX}_DEBUG', False))
@click.pass_context
def main(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['script'] = os.path.abspath(sys.argv[0])
    ctx.obj['scriptdir'] = os.path.dirname(ctx.obj['script'])
    ctx.obj['ci'] = CI
    if debug:
        Status.loglevel = Status.DEBUG
    
    Status.info(f"Starting {ctx.info_name} {__package_version}" +  (f" from {ctx.obj['script']}" if debug else ''))
    Status.debug(f"CI type is {type(CI)}, named '{CI.name}'")
    Status.debug(f"Repo working directory is '{CI.repo_dir}'")
    Status.info(f"Running in {CI.name}")
