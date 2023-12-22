#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Thu Dec 21 10:49:20 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

import sys

from autologging import logged, traced
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from docopt import docopt
from getpass import getpass
from io import StringIO
from jinja2 import Template
from pandas import json_normalize
from pathlib import Path
import pandas as pd

import ecspylibs
from ecspylibs.configfile import config_file
from ecspylibs.logging import Logging
from ecspylibs.parallel import Parallel
from ecspylibs.password import Password

import ecscmdb
from ecscmdb.api import API
from ecscmdb.format import set_col_widths, get_col_widths
from ecscmdb.updatecells import UpdateCells


@traced
@logged
def main() -> None:
    """
    Program to download the data from the OpenManage DB and build a spreadsheet.

    Some default option values listed below can be overridden within the
    configuration file.

    Usage:
      %(pgm)s [-v] [-l FILE] [-L LEVEL] [-f] [-c FILE] [-s SECTION] [-F FILE] [-o FILE] [-p FILE] [-P SIZE]
      %(pgm)s [-v] [-l FILE] [-L LEVEL] [-c FILE] [-s SECTION] [--list] [--add=ID]... [--delete=ID]... [-p FILE]
      %(pgm)s (-h | --help | -V | --version)

      There are no required options.

    Options:
      -h, --help                     Show this help message and exit.
      -V, --version                  Show version information and exit.
      -v, --verbose                  Print verbose messages.
      -f, --full                     Show all data, no filtering.
      -c FILE, --config=FILE         The configuration file.
                                     [Default: %(--config)s]
      -s SECTION, --section=SECTION  The configuration file section.
                                     [Default: %(--section)s]
      -F FILE, --filter=FILE         The filter file to filter the OpenManage data.
                                     [Default: %(--filter)s]
      -o FILE, --output=FILE         Output file.
                                     [Default: %(--output)s]
      -p FILE, --pw=FILE             The password file.  This file is used when a
                                     login to a website or webpage is required.
                                     [Default: %(--pw)s]
      -l FILE, --log=FILE            Log file.
                                     [Default: %(--log)s]
      -L LEVEL, --log_level=LEVEL    Print log messages at log value LEVEL.
                                     Valid levels are: TRACE, DEBUG, INFO, WARNING,
                                     ERROR, and CRITICAL.
                                     [Default: %(--log_level)s]
      --list                         List all of the IDs in the password file and
                                     exit.  If both the --list and --verbose
                                     options are included, list both IDs and
                                     Passwords and exit.
      --add=ID                       Add (or update) an ID and Password and exit.
                                     Program will prompt for the Password to be
                                     saved to the password file.
      --delete=ID                    Delete an ID (if it exists) from the
                                     password file and exit.
      -P SIZE, --poolsize=SIZE       Call OpenManage using pools of size SIZE.
                                     [Default: %(--poolsize)s]
    """

    FQ_PGM_FILE = Path(__file__).resolve(strict=True)
    PGM = Path(FQ_PGM_FILE.stem)
    PKG = Path(__package__)

    pgm_version = (
        f"{PGM}: {PKG}({ecscmdb.__version__}), ecspylibs({ecspylibs.__version__})"
    )

    # Get current TOD.

    TOD = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    replace_tod = {
        "TOD": TOD,
    }

    # Get default values.

    FQ_RUN_DIR = Path.cwd().resolve(strict=True)

    ETC_DIR = Path("etc")
    LOG_DIR = Path("log")
    OUTPUT_DIR = Path("output")

    CONF_FILE = PGM.with_suffix(".yml")
    LOG_FILE = PGM.with_suffix(".log")
    OUTPUT_FILE = Path(f"OpenManage-{PGM}.{TOD}.xlsx")
    PW_FILE = PGM.with_suffix(".pw")
    FILTER_FILE = Path("filter.yml")

    # Setup default values if config file doesn't exist.

    default_config = ETC_DIR / PKG / CONF_FILE
    default_log = LOG_DIR / LOG_FILE
    default_output = OUTPUT_DIR / OUTPUT_FILE
    default_pw = ETC_DIR / PKG / PW_FILE
    default_filter = ETC_DIR / PKG / FILTER_FILE

    default_section = "1"
    default_log_level = "WARNING"
    default_log_size = 50 * 1024 ^ 2
    default_log_count = 5
    default_poolsize = 0

    default_OME_Host = "wayneome.cit.wayne.edu"
    default_OME_Login = "CMDB"

    CLA_config = ""
    CLA_section = ""

    # Set CMDB variables if the config file does exist.

    while True:
        if CLA_config:
            default_config = CLA_config

        if default_config.is_file():
            try:
                cmdb_config = config_file(default_config).read
            except Exception as e:
                print(
                    f"\nException, '{e}', while reading CMDB Config file '{default_config}'.  Process terminating.\n",
                    file=sys.stderr,
                )
                sys.exit(1)

            try:
                if CLA_section:
                    cmdb_section = CLA_section
                else:
                    cmdb_section = cmdb_config["section"]

                cmdb_config_section = cmdb_config["config"][cmdb_section - 1]
            except Exception as e:
                print(
                    f"\nException, '{e}', while processing CMDB Config file '{default_config}'.  Process terminating.\n",
                    file=sys.stderr,
                )
                sys.exit(1)

            try:
                cmdb_name = cmdb_config_section["name"]

                OME_Host = cmdb_config_section["OME_Host"]
                OME_Login = cmdb_config_section["OME_Login"]
                cmdb_filter = cmdb_config_section["filter"]
                cmdb_log = cmdb_config_section["log"]
                cmdb_log_level = cmdb_config_section["log_level"]
                cmdb_log_size = cmdb_config_section["log_size"]
                cmdb_log_count = cmdb_config_section["log_count"]
                cmdb_output = cmdb_config_section["output"]
                cmdb_poolsize = cmdb_config_section["poolsize"]
                cmdb_pw = cmdb_config_section["pw"]
            except Exception as e:
                print(
                    f"\nMissing entry, {e}, from CMDB Config file '{default_config}'.  Process terminating.\n",
                    file=sys.stderr,
                )
                sys.exit(1)

        # Use the default variables if the config file does not exist.
        else:
            cmdb_name = "Default config name"
            cmdb_section = default_section
            OME_Host = default_OME_Host
            OME_Login = default_OME_Login
            cmdb_filter = default_filter
            cmdb_log = default_log
            cmdb_log_level = default_log_level
            cmdb_log_size = default_log_size
            cmdb_log_count = default_log_count
            cmdb_output = default_output
            cmdb_poolsize = default_poolsize
            cmdb_pw = default_pw

        cmdb_output = Path(Template(cmdb_output).render(replace_tod))

        help_arguments = {
            "pgm": PGM,
            "--config": default_config,
            "--section": cmdb_section,
            "--log": cmdb_log,
            "--log_level": cmdb_log_level,
            "--output": cmdb_output,
            "--pw": cmdb_pw,
            "--filter": cmdb_filter,
            "--poolsize": cmdb_poolsize,
        }

        help_text = main.__doc__ % help_arguments

        arguments = docopt(help_text, version=pgm_version)

        arguments["--log_level"] = arguments["--log_level"].upper()

        for i in [
            "--config",
            "--log",
            "--output",
            "--pw",
            "--filter",
        ]:
            arguments[i] = Path(arguments[i]).resolve(strict=False)

        if default_config == arguments["--config"] and cmdb_section == int(
            arguments["--section"]
        ):
            break

        CLA_config = arguments["--config"]
        CLA_section = int(arguments["--section"])

    # Setup variables based on the CLAs and the config file.
    config = arguments["--config"]
    verbose = arguments["--verbose"]
    full = arguments["--full"]
    log = arguments["--log"]
    log_level = arguments["--log_level"]
    log_size = cmdb_log_size
    log_count = cmdb_log_count
    filter = arguments["--filter"]
    output = arguments["--output"]
    pw = arguments["--pw"]

    add_id = arguments["--add"]
    delete_id = arguments["--delete"]
    list_id = arguments["--list"]

    poolsize = arguments["--poolsize"]
    if poolsize.isnumeric():
        poolsize = int(poolsize)
    else:
        poolsize = 0

    if log.is_dir():
        log = log / PGM.with_suffix(".log")
        log.touch()

    logger = Logging(log, log_size=log_size, log_level=log_level, log_count=log_count)

    logger._log.info(f"Starting program {pgm_version}.")
    if verbose:
        print(f"\nStarting program {pgm_version}.\n", file=sys.stdout)

    PW = Password(pw)
    OME_PW = PW.get(OME_Login)

    # The real stuff goes here.

    if add_id or delete_id or list_id:
        logger._log.info("ID Maintenance.")
        if add_id:
            logger._log.info("Add/Update ID.")
            for id in add_id:
                logger._log.debug(f"Add/Update ID {id}.")
                pw = getpass(prompt=f"Enter password for user '{id}': ")
                PW.set(id, pw)
            del pw

        if delete_id:
            logger._log.info("Delete ID.")
            for id in delete_id:
                logger._log.debug(f"Delete ID {id}")
                PW.delete(id)

        if list_id:
            logger._log.info("List IDs.")
            if verbose:
                PW.list_pws
            else:
                PW.list_ids

        del PW
        logger._log.info(f"Ending program {pgm_version}.")
        if verbose:
            print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
        sys.exit(0)

    if filter:
        try:
            FILTER_DATA = config_file(filter).read
        except Exception as e:
            print(
                f"\nException, '{e}', while reading CMDB Filter file '{filter}'.  Process terminating.\n",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            FILTER_SECTION = FILTER_DATA["section"]
            FILTER_CONFIG = FILTER_DATA["config"][FILTER_SECTION - 1]
        except Exception as e:
            print(
                f"\nException, '{e}', while processing CMDB Filter file '{filter}'.  Process terminating.\n",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            FILTER_NAME = FILTER_CONFIG["name"]
            FILTER_COLUMN_HEADER = FILTER_CONFIG["column_header"]
            FILTER_RENAME_COLUMNS = FILTER_CONFIG["rename_columns"]
            FILTER_SORT_COLUMNS = FILTER_CONFIG["sort_columns"]
            FILTER_ROWS = FILTER_CONFIG["filters"]
        except Exception as e:
            print(
                f"\nMissing entry, {e}, from CMDB Filter file '{filter}'.  Process terminating.\n",
                file=sys.stderr,
            )
            sys.exit(1)

        NEW_FIELDS = []

        for i in FILTER_ROWS:
            row = i["row"]
            columns = i["columns"]
            if FILTER_COLUMN_HEADER not in columns:
                columns.append(FILTER_COLUMN_HEADER)
            if "update" in i:
                update = i["update"]
                for k in update.keys():
                    if k in columns:
                        columns.remove(k)
                    columns.append([k, update[k]])
            NEW_FIELDS.append([row, columns])
    else:
        FILTER_RENAME_COLUMNS = []
        FILTER_SORT_COLUMNS = []
        NEW_FIELDS = []
        full = True

    logger._log.info("Initialize the OpenManage REST API.")
    OME_api = API(OME_Login, OME_PW, OME_Host)

    logger._log.info(
        f"login into the OpenManage REST API with with user '{OME_Login}'."
    )
    OME_api.login()

    logger._log.info("Get list of all OpenManage devices.")
    if verbose:
        print("Get list of all OpenManage devices.", file=sys.stdout)
    df_device_list = OME_api.get_device_list()

    logger._log.debug(f"{df_device_list = }.")

    logger._log.info("Initialize Pandas.")
    df_spreadsheet = pd.DataFrame()
    logger._log.info("Initialize ExcelWriter.")
    excel = pd.ExcelWriter(output)

    records_openmanage = {}
    records_inv_details = {}
    device_list = []
    device_id = {}

    logger._log.info("Create list of OpenManage devices.")
    if verbose:
        print("Create list OpenManage devices.", file=sys.stdout)

    for device in df_device_list["value"]:
        logger._log.debug(f"{device = }")
        for device_mgt in device["DeviceManagement"]:
            logger._log.debug(f"{device_mgt = }")
            for device_tag in ["DnsName", "MacAddress"]:
                logger._log.debug(f"{device_tag = }")
                if device_tag not in records_openmanage:
                    records_openmanage[device_tag] = []

                logger._log.debug(f"{device_mgt[device_tag] = })")
                logger._log.debug(
                    f"records_openmanage[{device_tag}].append(device_mgt[{device_tag}])"
                )
                records_openmanage[device_tag].append(device_mgt[device_tag])

        for device_tag in [
            "DeviceName",
            "DeviceServiceTag",
            "Model",
            "InventoryDetails@odata.navigationLink",
        ]:
            logger._log.debug(f"{device_tag = }")
            if device_tag not in records_openmanage:
                records_openmanage[device_tag] = []

            logger._log.debug(f"{device[device_tag] = }")
            logger._log.debug(
                f"records_openmanage[{device_tag}].append(device[{device_tag}]"
            )
            records_openmanage[device_tag].append(device[device_tag])

        device_name = device["DeviceName"][:31]
        logger._log.debug(f"{device_name = }")

        id = device["Id"]
        logger._log.debug(f"{id = }")

        model = device["Model"]
        logger._log.debug(f"{model = }")

        logger._log.debug(f"device_list.append({device_name})")
        device_list.append(device_name)
        device_id[device_name] = id

    logger._log.info("Create the VMWare worksheet.")
    if verbose:
        print("Create the VMWare worksheet.", file=sys.stdout)

    logger._log.info("Create df_spreadsheet from pd.DataFrame(records_openmanage).")
    # df_spreadsheet = df_spreadsheet.append(pd.DataFrame(records_openmanage))
    df_spreadsheet = pd.DataFrame(records_openmanage)

    logger._log.info("Sort df_spreadsheet.")
    df_spreadsheet = df_spreadsheet.sort_values(by=df_spreadsheet.columns.tolist())

    logger._log.info("Reindex df_spreadsheet.")
    df_spreadsheet = df_spreadsheet.reindex(sorted(df_spreadsheet.columns), axis=1)

    logger._log.info("Move column DnsName to column 1.")
    cols = df_spreadsheet.columns.tolist()
    cols.insert(0, cols.pop(cols.index("DnsName")))
    df_spreadsheet = df_spreadsheet.reindex(columns=cols)

    logger._log.info("Write df_spreadsheet to excel file as VMWare.")
    df_spreadsheet.to_excel(excel, "VMWare", index=False)

    logger._log.info("Update column widths of worksheet VMWare.")
    worksheet = excel.sheets["VMWare"]
    set_col_widths(worksheet, df_spreadsheet)

    device_list.sort()

    if full:
        logger._log.info("All Rows/Columns will be displayed.")

    else:
        logger._log.info(
            "Configure which Rows and Columns to copy for each device type."
        )

        update_cells = UpdateCells()

        fields = NEW_FIELDS

    rename_columns = FILTER_RENAME_COLUMNS
    sort_field_names = FILTER_SORT_COLUMNS

    logger._log.info("Create a worksheet for each device.")
    if verbose:
        print("Create a worksheet for each device.", file=sys.stdout)

    device_count = 0
    device_length = len(device_list)

    logger._log.debug(
        f"Calling Parallel(OME_api.getInventoryDetails, pool_size={poolsize})"
    )

    if verbose:
        if poolsize > 0:
            print(
                f"Creating {poolsize} pools to process {device_length} calls to the OpenManage REST API.",
                file=sys.stdout,
            )
        else:
            print(
                f"Creating one pool per CPU to process {device_length} calls to the OpenManage REST API.",
                file=sys.stdout,
            )

    try:
        get_inv_details = Parallel(
            OME_api.get_inventory_details, ProcessPoolExecutor, pool_size=poolsize
        )
    except Exception as e:
        logger._log.critical(
            "Error processing OME_api.getInventoryDetails.  Process terminating."
        )
        logger._log.exception(f"Exception: {e=}")
        print(
            "Error processing OME_api.getInventoryDetails.  Process terminating.",
            file=sys.stderr,
        )
        sys.exit(1)

    logger._log.debug(f"{poolsize} pools created.")
    if verbose:
        if poolsize:
            print(f"{poolsize} pools created.", file=sys.stdout)
        else:
            print(f"One pool per CPU created.", file=sys.stdout)

    device_ids = list(device_id.values())
    logger._log.debug(f"{device_ids=}")

    logger._log.debug(f"Calling get_inv_details.run({device_ids})")
    if verbose:
        print(
            f"Calling OpenManage REST API with pool size of {poolsize} to retrieve {device_length} device records.",
            file=sys.stdout,
        )

    try:
        results = get_inv_details.run(device_ids)
    except Exception as e:
        logger._log.critical(
            f"Error processing get_inv_details.run({device_ids}).  Process terminating."
        )
        logger._log.exception(f"Exception: {e=}")
        print(
            f"Error processing get_inv_details.run({device_ids}).  Process terminating.",
            file=sys.stderr,
        )
        sys.exit(1)

    if verbose:
        print(
            f"The call to OpenManage took {get_inv_details.run_time:.2f} seconds",
            f"to fetch {device_length} OpenManage device records.",
            file=sys.stdout,
        )
    logger._log.debug(
        f"get_inv_details.run took {get_inv_details.run_time} seconds to fetch {device_length} devices."
    )

    for result in results:
        id, data = result[0], result[1]
        logger._log.debug(f"{id=}")
        logger._log.debug(f"{type(data)=}")
        if data:
            logger._log.debug(f"Found data for id '{id}'.")
            records_inv_details[id] = data
        else:
            logger._log.error(f"Did not find data for id '{id}'.")
            print(
                f"Error processing get_inv_details.run({device_ids}).  Process terminating.",
                file=sys.stderr,
            )
            sys.exit(1)

    for device in device_list:
        device_count += 1
        id = device_id[device]

        logger._log.info(
            f"Creating worksheet[{device_count}:{device_length}] for device '{device}[{id}]'."
        )
        if verbose:
            print(
                f"Creating worksheet[{device_count}:{device_length}] for device '{device}[{id}]'.",
                file=sys.stdout,
            )
        if id in records_inv_details:
            logger._log.debug(f"records_inv_details[{id}] : {records_inv_details[id]}")
        else:
            logger._log.error(f"Couldn't find id '{id}' in records_inv_details.")
            print(
                "Error processing Detail records.  Process terminating.",
                file=sys.stderr,
            )
            sys.exit(1)

        df_inv_details = pd.read_json(StringIO(records_inv_details[id]))
        logger._log.debug(f"df_inv_details : {df_inv_details}")
        logger._log.debug(f"df_inv_details['value'] : {df_inv_details['value']}")
        sheet = json_normalize(
            df_inv_details["value"], "InventoryInfo", ["InventoryType"]
        )

        if not full:
            logger._log.info(
                f"If device '{device}' is a server or enclosure, filter out unnecessary data."
            )

            out_fields = {}

            for row, columns in fields:
                logger._log.info(f"Looking for row '{row}' for device '{device}'.`")

                if sheet["InventoryType"].str.contains(row).any():
                    logger._log.info(f"Found row '{row}' for device '{device}'.`")

                    if row not in out_fields:
                        out_fields[row] = []

                    for column in columns:
                        if type(column) is list:
                            column, cmd = column
                        else:
                            cmd = None

                        logger._log.info(
                            f"Looking for row:column '{row}:{column}' for device '{device}'."
                        )

                        if column in sheet.columns:
                            logger._log.info(
                                f"Found row:column '{row}:{column}' for device '{device}'.`"
                            )
                            out_fields[row].append(column)
                            logger._log.debug(f"out_fields[{row}] : {out_fields[row]}")

                        else:
                            logger._log.info(
                                f"Can't find row:column '{row}:{column}' for device '{device}'.`"
                            )

                else:
                    logger._log.info(f"Can't find row '{row}' for device '{device}'.")

            out = {}

            for key in out_fields.keys():
                logger._log.debug(f"out_fields[{key}] : '{out_fields[key]}'")
                out[key] = sheet.loc[(sheet["InventoryType"] == key), out_fields[key]]

            logger._log.info(f"Recreate sheet for device '{device}'.")
            sheet = pd.concat([out[key] for key in out], sort=False)

            logger._log.debug(f"Sheet = '{sheet}'.")

            for row, columns in fields:
                logger._log.info(f"Looking for row '{row}' for device '{device}'.`")

                if sheet["InventoryType"].str.contains(row).any():
                    logger._log.info(f"Found row '{row}' for device '{device}'.`")

                    for column in columns:
                        if type(column) is list:
                            column, cmd = column
                        else:
                            continue

                        logger._log.info(
                            f"Looking for row:column '{row}:{column}' for device '{device}'."
                        )

                        if column in sheet.columns:
                            logger._log.info(
                                f"Found row:column '{row}:{column}' for device '{device}'.`"
                            )
                            if not update_cells.run(cmd, sheet):
                                logger._log.error(
                                    f"Error calling update_cell('{cmd}', {device})"
                                )
                                print(
                                    f"Error updating cell information using module '{cmd}' for sheet {device}.",
                                    file=sys.stderr,
                                )
                                sys.exit(1)
                else:
                    logger._log.info(f"Can't find row '{row}' for device '{device}'.")

            logger._log.info(
                f"Rename, if necessary, column names for device '{device}'."
            )
            logger._log.debug(f"{rename_columns=}")
            sheet = sheet.rename(columns=rename_columns)

        logger._log.info(f"Sort the columns for sheet '{device}'.")
        sheet = sheet.reindex(sorted(sheet.columns), axis=1)

        logger._log.info(
            f"Move column 'InventoryType' to the beginning of the spreadsheet for device '{device}'."
        )
        cols = sheet.columns.tolist()
        logger._log.debug(f"sheet : {sheet}")
        logger._log.debug(f"sheet.columns : {sheet.columns}")
        logger._log.debug(f"sheet.columns.tolist() : {sheet.columns.tolist()}")
        cols.insert(0, cols.pop(cols.index("InventoryType")))
        sheet = sheet.reindex(columns=cols)

        sort_fields = []
        logger._log.debug(f"sort_field_names = {sort_field_names}")

        for field_name in sort_field_names:
            logger._log.debug(f"field_name = {field_name}")
            logger._log.debug(f"Is '{field_name}' in {sheet.columns.tolist()}")
            if field_name in sheet.columns:
                if field_name not in sort_fields:
                    logger._log.debug(f"Add '{field_name}' to {sort_fields}")
                    sort_fields.append(field_name)
                else:
                    logger._log.debug(f"'{field_name}' already in {sort_fields}")

        if sort_fields:
            logger._log.debug(f"'{device}.sort_fields' = {sort_fields}")
            sheet.sort_values(by=sort_fields, inplace=True, ignore_index=True)

        logger._log.info(f"Update the spreadsheet for device {device}.")
        sheet.to_excel(excel, device, index=False)

        worksheet = excel.sheets[device]
        set_col_widths(worksheet, sheet)

    logger._log.info("Close the spreadsheet file.")
    if verbose:
        print("Close the spreadsheet file.", file=sys.stdout)
    excel.close()

    logger._log.info(f"Ending program {pgm_version}.")
    if verbose:
        print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
