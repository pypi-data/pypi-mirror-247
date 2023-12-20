"""LDDTool Wrapper.

Tool that downloads PDS Local Data Dictionary Tool (LDDTool) and executes based upon
input arguments.
"""
import argparse
import logging
import os
import sys
import traceback
from datetime import datetime
from subprocess import CalledProcessError
from subprocess import PIPE
from subprocess import Popen
from subprocess import STDOUT

from .util import add_standard_arguments
from .util import Assets
from .util import convert_pds4_version_to_alpha
from .util import get_latest_release
from .util import LDDs


GITHUB_ORG = "NASA-PDS"
GITHUB_REPO = "pds4-information-model"

# LDDTool defaults
LDDTOOL_DEFAULT_ARGS = "-lpJ"

# Schema download constants
PDS_SCHEMA_URL = "https://pds.nasa.gov/pds4/pds/v1/"
PDS_DEV_SCHEMA_URL = "https://pds.nasa.gov/datastandards/schema/develop/pds/"
DOWNLOAD_PATH = "/tmp"

_logger = logging.getLogger(__name__)


def prep_ldd_output_path(ldd_output_path):
    """Create the necessary output directories."""
    # Crawl two directories up and remove everything
    parent_dir = os.path.dirname(os.path.dirname(ldd_output_path.rstrip(os.sep)))
    # parent_dir = ldd_output_path

    _logger.info(f"Cleaning up {parent_dir}")
    for path, _dirs, files in os.walk(parent_dir):
        for f in files:
            filepath = os.path.join(path, f)
            _logger.info(f"Removing {filepath}")
            os.remove(filepath)

    if not os.path.exists(ldd_output_path):
        os.makedirs(ldd_output_path)


def exec_lddtool(executable, execution_cwd, args, ingest_ldds, log_path=None):
    """Execute LDDTool."""
    if not log_path:
        log_path = os.path.expanduser("~")

    dtime = datetime.now().strftime("%Y%m%d%H%M%S")
    log_out = os.path.join(log_path, f"lddtool_run_log_{dtime}.txt")
    if not os.path.exists(os.path.dirname(log_out)):
        os.makedirs(os.path.dirname(log_out))

    cmd = ["bash", executable]
    args.extend(ingest_ldds)
    cmd.extend(args)
    _logger.info(cmd)

    with Popen(cmd, cwd=execution_cwd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as p:
        with open(log_out, "w") as f:
            for line in p.stdout:
                print(line, end="")  # process line here
                f.write(line)

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)


def main():
    """Main."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
    add_standard_arguments(parser)
    parser.add_argument("--deploy_dir", help="directory to deploy the validate tool on the file system", default="/tmp")
    parser.add_argument("--ldd_output_path", help="directory to output generated LDDs", required=True)
    parser.add_argument(
        "--ingest_ldd_src_dir",
        help="/path/to/src/ dir for IngestLDD file",
        default=os.path.join("tmp", "logs"),
        required=True,
    )
    parser.add_argument("--token", help="github token")
    parser.add_argument(
        "--output_log_path", help="path(s) to output validate run log file", default=os.path.join("tmp", "logs")
    )
    parser.add_argument(
        "--with_pds4_version",
        help=(
            "force the following PDS4 version. software will "
            "download and validate with this version of the "
            "PDS4 Information Model. this version should be "
            "the semantic numbered version. e.g. 1.14.0.0"
        ),
    )
    parser.add_argument(
        "--use_lddtool_unstable",
        help="force the use of the latest unstable LDDTool release. by default, uses latest stable release",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format="%(levelname)s %(message)s")

    token = args.token or os.environ.get("GITHUB_TOKEN")

    if not token:
        _logger.error("Github token must be provided or set as environment variable (GITHUB_TOKEN).")
        sys.exit(1)

    try:
        lddtool_args = [LDDTOOL_DEFAULT_ARGS]

        if args.with_pds4_version:
            lddtool_args.extend(["-V", convert_pds4_version_to_alpha(args.with_pds4_version)])

        # cleanup the LDD Output area before generating LDDs
        prep_ldd_output_path(args.ldd_output_path)

        latest_release = get_latest_release(token, GITHUB_ORG, GITHUB_REPO)
        pkg = Assets.download_asset(latest_release, args.deploy_dir, startswith="lddtool", file_extension=".zip")

        sw_dir = Assets.unzip_asset(pkg, args.deploy_dir)

        # Generate dependency LDDs
        ingest_ldds = LDDs.find_dependency_ingest_ldds(args.ingest_ldd_src_dir)
        for ingest in ingest_ldds:
            # execute LDDTool
            exec_lddtool(
                os.path.join(sw_dir, "bin", "lddtool"),
                args.ldd_output_path,
                lddtool_args[:],
                [ingest],
                log_path=args.output_log_path,
            )

        # Generate final LDDs
        ingest_ldds.extend(LDDs.find_primary_ingest_ldd(args.ingest_ldd_src_dir))

        # execute LDDTool
        exec_lddtool(
            os.path.join(sw_dir, "bin", "lddtool"),
            args.ldd_output_path,
            lddtool_args[:],
            ingest_ldds,
            log_path=args.output_log_path,
        )

    except CalledProcessError:
        _logger.error("FAILED: LDDTool failed unexpectedly. See output logs.")
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    _logger.info("SUCCESS: LDD Generation complete.")


if __name__ == "__main__":
    main()
