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

    log = Path(config["log"]).resolve(strict=False)
    pw = Path(config["pw"]).resolve(strict=True)
    filter = Path(config["filter"]).resolve(strict=True)
    output = Path(config["output"]).resolve(strict=False)

    OME_Host = config["OME_Host"]
    OME_Login = config["OME_Login"]
    log_level = config["log_level"]
    log_size = config["log_size"]
    log_count = config["log_count"]
    name = config["name"]
    if "poolsize" in config.keys():
        poolsize = config["poolsize"]

    help_arguments = {
        "pgm": pgm,
        "--config": cf_file,
        "--filter": filter,
        "--log": log,
        "--log_level": log_level,
        "--log_size": log_size,
        "--log_count": log_count,
        "--output": output,
        "--poolsize": poolsize,
        "--pw": pw,
    }

    help_text = help_doc % help_arguments

    arguments = docopt(help_text, argv, version=version)
    for path in [
        "--config",
        "--filter",
        "--log",
        "--output",
        "--pw",
    ]:
        arguments[path] = Path(arguments[path]).resolve(strict=False)

    if cf_file != arguments["--config"]:
        CONF = config_file(arguments["--config"])
        data = CONF.read
        cf_file = CONF.name

        section = data["section"]
        config = data["config"][section - 1]

        if "filter" in config.keys():
            filter = Path(config["filter"]).resolve(strict=True)
        log = Path(config["log"]).resolve(strict=False)
        output = Path(config["output"]).resolve(strict=False)
        pw = Path(config["pw"]).resolve(strict=True)

        OME_Host = config["OME_Host"]
        OME_Login = config["OME_Login"]
        log_level = config["log_level"]
        log_size = config["log_size"]
        log_count = config["log_count"]
        name = config["name"]
        poolsize = config["poolsize"]

        help_arguments = {
            "pgm": pgm,
            "--config": cf_file,
            "--filter": filter,
            "--log": log,
            "--log_level": log_level,
            "--log_size": log_size,
            "--log_count": log_count,
            "--output": output,
            "--poolsize": poolsize,
            "--pw": pw,
        }

        help_text = help_doc % help_arguments

        arguments = docopt(help_text, argv, version=version)
        for path in [
            "--config",
            "--filter",
            "--log",
            "--output",
            "--pw",
        ]:
            arguments[path] = Path(arguments[path]).resolve(strict=False)

    arguments["OME_Host"] = OME_Host
    arguments["OME_Login"] = OME_Login
    arguments["name"] = name

    return arguments
