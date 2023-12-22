#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Tue Dec 19 15:41:32 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

import sys
from pathlib import Path
from autologging import logged, traced
from docopt import docopt
from ecspylibs2.configfile import *


@traced
@logged
def parse_args(
    pgm: str,
    argv: list,
    help_doc: str,
    version: str,
    file: PosixPath,
    directories: Optional[List[PosixPath]] = None,
) -> dict:
    CONF = config_file(file, directories)
    data = CONF.read
    cf_file = CONF.name

    section = data["section"]
    config = data["config"][section - 1]

    for i in config.keys():
        print(f"config[{i}] = '{config[i]}'", file=sys.stderr)

    log = Path(config["log"]).resolve(strict=False)
    report = Path(config["report"]).resolve(strict=False)

    print(f"\n{log=}\n")
    print(f"\n{report=}\n")

    log_level = config["log_level"]
    log_size = config["log_size"]
    log_count = config["log_count"]
    name = config["name"]

    help_arguments = {
        "pgm": pgm,
        "--config": cf_file,
        "--log": log,
        "--log_level": log_level,
        "--log_size": log_size,
        "--log_count": log_count,
        "--report": report,
    }

    help_text = help_doc % help_arguments
    print(f"\n{help_text=}")
    print(f"\n{report=}")
    print(f"\n{argv=}")
    print(f"\n{version=}\n")

    arguments = docopt(help_text, argv, version=version)
    print(f"\n{arguments=}\n")

    if arguments["--config"] == None:
        arguments["--config"] = Path(cf_file).resolve(strict=False)

    if arguments["--report"] == None:
        arguments["--report"] = Path(report).resolve(strict=False)

    if arguments["--log"] == None:
        arguments["--log"] = Path(log).resolve(strict=False)

    print("\nBefore\n")

    for path in [
        "--config",
        "--log",
        "--report",
    ]:
        print(f"\narguments[{path}] = {arguments[path]}\n")
        arguments[path] = Path(arguments[path]).resolve(strict=False)
        print("\nNext\n")

    print("\nAfter\n")

    if cf_file != arguments["--config"]:
        CONF = config_file(arguments["--config"])
        data = CONF.read
        cf_file = CONF.name

        section = data["section"]
        config = data["config"][section - 1]

        if "filter" in config.keys():
            filter = Path(config["filter"]).resolve(strict=True)
        log = Path(config["log"]).resolve(strict=False)
        report = Path(config["report"]).resolve(strict=False)

        log_level = config["log_level"]
        log_size = config["log_size"]
        log_count = config["log_count"]
        name = config["name"]

        help_arguments = {
            "pgm": pgm,
            "--config": cf_file,
            "--log": log,
            "--log_level": log_level,
            "--log_size": log_size,
            "--log_count": log_count,
            "--report": report,
        }

        help_text = help_doc % help_arguments

        arguments = docopt(help_text, argv, version=version)
        for path in [
            "--config",
            "--log",
            "--report",
        ]:
            arguments[path] = Path(arguments[path]).resolve(strict=False)

    arguments["name"] = name

    return arguments
