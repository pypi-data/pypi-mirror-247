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
from datetime import datetime
from docopt import docopt
from jinja2 import Template
from pathlib import Path
from socket import gethostname
import pandas as pd

import ecspylibs
from ecspylibs.configfile import config_file
from ecspylibs.logging import Logging
from ecspylibs.sendemail import SendEmail

import ecscmdb
from ecscmdb.finddifferences import FindDifferences
from ecscmdb.format import set_col_widths, get_col_widths
from ecscmdb.summary import Summary


@traced
@logged
def main() -> None:
    """
    Program to analyze two spreadsheets for differences.

    Some default option values listed below can be overridden within the initialization file.

    Usage:
      %(pgm)s [-v] [-l FILE] [-L LEVEL] [-c FILE] [-s SECTION] [-r FILE] [-D] SPREADSHEET1 SPREADSHEET2
      %(pgm)s (-h | --help | -V | --version)

      Variables SPREADSHEET1 and SPREADSHEET2 are required, all other parameters are optional.

    Options:
          -h, --help                          Show this help message and exit.
          -V, --version                       Show version information and exit.
          -v, --verbose                       Print verbose messages.
          -c FILE, --config=FILE              The configuration file.
                                              [Default: %(--config)s]
          -s SECTION, --section=SECTION       The configuration file section.
                                              [Default: %(--section)s]
          -r FILE, --report=FILE              Report directory or file.
                                              [Default: %(--report)s]
          -l FILE, --log=FILE                 Log file or directory.
                                              [Default: %(--log)s]
          -L LEVEL, --log_level=LEVEL         Print log messages at log value LEVEL.
                                              Valid levels are: TRACE, DEBUG, INFO, WARNING,
                                              ERROR, and CRITICAL.
                                              [Default: %(--log_level)s]
    """

    FQ_PGM_FILE = Path(__file__).resolve(strict=True)
    PGM = Path(FQ_PGM_FILE.stem)
    PKG = Path(__package__)

    pgm_version = (
        f"{PGM}: {PKG}({ecscmdb.__version__}), ecspylibs({ecspylibs.__version__})"
    )

    # Get current TOD.

    TOD = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    DATE = datetime.now().strftime("%A, %B %e, %Y")
    TIME = datetime.now().strftime("%r")
    replace_tod = {
        "TOD": TOD,
    }

    # Get hostname.

    HOST = gethostname()

    # Get default values.

    FQ_RUN_DIR = Path.cwd().resolve(strict=True)

    ETC_DIR = Path("etc")
    LOG_DIR = Path("log")
    REPORT_DIR = Path("report")

    CONF_FILE = PGM.with_suffix(".yml")
    LOG_FILE = PGM.with_suffix(".log")
    REPORT_FILE = Path(f"OpenManage-{PGM}.{TOD}.xlsx")

    # Setup default values if config file doesn't exist.

    default_config = ETC_DIR / PKG / CONF_FILE
    default_log = LOG_DIR / LOG_FILE
    default_report = REPORT_DIR / REPORT_FILE

    default_section = "1"
    default_log_level = "WARNING"
    default_log_size = 50 * 1024 ^ 2
    default_log_count = 5
    default_poolsize = 0

    CLA_config = ""
    CLA_section = ""

    # Set CMDBDIFF variables if the config file exist.

    while True:
        if CLA_config:
            default_config = CLA_config

        if default_config.is_file():
            try:
                cmdbdiff_config = config_file(default_config).read
            except Exception as e:
                print(
                    f"\nException, '{e}', while reading CMDBDIFF Config file '{default_config}'.  Process terminating.\n",
                    file=sys.stderr,
                )
                sys.exit(1)

            try:
                if CLA_section:
                    cmdbdiff_section = CLA_section
                else:
                    cmdbdiff_section = cmdbdiff_config["section"]

                cmdbdiff_config_section = cmdbdiff_config["config"][
                    cmdbdiff_section - 1
                ]
            except Exception as e:
                print(
                    f"\nException, '{e}', while processing CMDBDIFF Config file '{default_config}'.  Process terminating.\n",
                    file=sys.stderr,
                )
                sys.exit(1)

            try:
                cmdbdiff_name = cmdbdiff_config_section["name"]

                cmdbdiff_log = cmdbdiff_config_section["log"]
                cmdbdiff_log_level = cmdbdiff_config_section["log_level"]
                cmdbdiff_log_size = cmdbdiff_config_section["log_size"]
                cmdbdiff_log_count = cmdbdiff_config_section["log_count"]
                cmdbdiff_report = cmdbdiff_config_section["report"]
                cmdbdiff_email = cmdbdiff_config_section["email"]
                cmdbdiff_admin = cmdbdiff_config_section["admin"]
            except Exception as e:
                print(
                    f"\nMissing entry, {e}, from CMDBDIFF Config file '{default_config}'.  Process terminating.\n",
                    file=sys.stderr,
                )
                sys.exit(1)

        # Use the default variables if the config file does not exist.
        else:
            cmdbdiff_name = "Default config name"
            cmdbdiff_section = default_section
            cmdbdiff_log = default_log
            cmdbdiff_log_level = default_log_level
            cmdbdiff_log_size = default_log_size
            cmdbdiff_log_count = default_log_count
            cmdbdiff_report = default_report

        cmdbdiff_report = Path(Template(cmdbdiff_report).render(replace_tod))

        help_arguments = {
            "pgm": PGM,
            "--config": default_config,
            "--section": cmdbdiff_section,
            "--log": cmdbdiff_log,
            "--log_level": cmdbdiff_log_level,
            "--report": cmdbdiff_report,
        }

        help_text = main.__doc__ % help_arguments

        arguments = docopt(help_text, version=pgm_version)

        arguments["--log_level"] = arguments["--log_level"].upper()

        for i in [
            "--config",
            "--log",
            "--report",
        ]:
            arguments[i] = Path(arguments[i]).resolve(strict=False)

        if default_config == arguments["--config"] and cmdbdiff_section == int(
            arguments["--section"]
        ):
            break

        CLA_config = arguments["--config"]
        CLA_section = int(arguments["--section"])

    # Setup variables based on the CLAs and the config file.
    config = arguments["--config"]
    section = arguments["--section"]
    verbose = arguments["--verbose"]
    log = arguments["--log"]
    log_level = arguments["--log_level"]
    log_size = cmdbdiff_log_size
    log_count = cmdbdiff_log_count
    report = arguments["--report"]

    if log.is_dir():
        log = log / PGM.with_suffix(".log")
        log.touch()

    logger = Logging(log, log_size=log_size, log_level=log_level, log_count=log_count)

    logger._log.info(f"Starting program {pgm_version}.")
    if verbose:
        print(f"\nStarting program {pgm_version}.\n", file=sys.stdout)

    admin_name = cmdbdiff_admin["name"]
    admin_email = cmdbdiff_admin["email"]
    admin_phone = cmdbdiff_admin["phone"]

    email_subject = cmdbdiff_email["subject"]

    email_from = f"{cmdbdiff_email['from']['name']} <{cmdbdiff_email['from']['email']}>"

    if "to" in cmdbdiff_email.keys():
        email_to = [
            f"{email['name']} <{email['email']}>" for email in cmdbdiff_email["to"]
        ]
    else:
        email_to = []

    if "cc" in cmdbdiff_email.keys():
        email_cc = [
            f"{email['name']} <{email['email']}>" for email in cmdbdiff_email["cc"]
        ]
    else:
        email_cc = []

    email_text_with_changes = cmdbdiff_email["text"]["with_changes"]
    email_text_without_changes = cmdbdiff_email["text"]["without_changes"]

    spread_sheet1 = Path(arguments["SPREADSHEET1"]).resolve(strict=True)
    spread_sheet2 = Path(arguments["SPREADSHEET2"]).resolve(strict=True)

    try:
        spread_sheet1 = spread_sheet1.resolve(strict=True)
    except FileNotFoundError as e:
        logger._log.error(f"SPREADSHEET1 is missing or invalid: '{spread_sheet1}'")
        print(
            f"\nError: SPREADSHEET1 is missing or invalid: '{spread_sheet1}'\n",
            file=sys.stderr,
        )
    except Exception as e:
        logger._log.error(f"\nException: {e=}")
        print(f"\nException: {e=}\n", file=sys.stderr)
        sys.exit(1)

    try:
        spread_sheet2 = spread_sheet2.resolve(strict=True)
    except FileNotFoundError as e:
        logger._log.error(f"SPREADSHEET2 is missing or invalid: '{spread_sheet2}'")
        print(
            f"\nError: SPREADSHEET2 is missing or invalid: '{spread_sheet2}'\n",
            file=sys.stderr,
        )
    except Exception as e:
        print(f"\nException: {e=}\n", file=sys.stderr)
        sys.exit(1)

    short_spread_sheet1 = spread_sheet1.name
    short_spread_sheet2 = spread_sheet2.name

    # The real stuff goes here.

    excel = pd.ExcelWriter(report)

    logger._log.debug(f"Create df_spread_sheet1 from file '{spread_sheet1}'.")
    try:
        df_spread_sheet1 = pd.read_excel(spread_sheet1, sheet_name=None)
    except Exception as e:
        logger._log.critical(f"Failed to read '{spread_sheet1}' Spreadsheet.")
        logger._log.exception(f"Exception: '{e}'.")
        logger._log.info(f"Ending program {pgm_version}.")
        if verbose:
            print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
        sys.exit(1)

    logger._log.debug(f"Create df_spread_sheet2 from file '{spread_sheet2}'.")
    try:
        df_spread_sheet2 = pd.read_excel(spread_sheet2, sheet_name=None)
    except Exception as e:
        logger._log.critical(f"Failed to read '{spread_sheet2}' spreadsheet.")
        logger._log.exception(f"Exception: '{e}'.")
        logger._log.info(f"Ending program {pgm_version}..")
        if verbose:
            print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
        sys.exit(1)

    sheet_names1 = set(df_spread_sheet1.keys())
    logger._log.debug(f"sheet_names1: '{sheet_names1}'")
    worksheets1 = len(sheet_names1)
    logger._log.debug(f"worksheets1: '{worksheets1}'")

    sheet_names2 = set(df_spread_sheet2.keys())
    logger._log.debug(f"sheet_names2: '{sheet_names2}'")
    worksheets2 = len(sheet_names2)
    logger._log.debug(f"worksheets2: '{worksheets2}'")

    deleted_sheet_names1 = sheet_names1.difference(sheet_names2)
    logger._log.debug(f"deleted_sheet_names1: '{deleted_sheet_names1}'")

    deleted_sheet_names2 = sheet_names2.difference(sheet_names1)
    logger._log.debug(f"deleted_sheet_names2: '{deleted_sheet_names2}'")

    common_sheet_names = list(sheet_names1.intersection(sheet_names2))
    common_sheet_names.sort()
    logger._log.debug(f"common_sheet_names: '{common_sheet_names}'")

    if verbose:
        print(
            f"\n=====================================================\n",
            file=sys.stdout,
        )
        print(f"Analyzing spreadsheet:\n\t '{short_spread_sheet1}'\n", file=sys.stdout)
        print(f"with spreadsheet:\n\t '{short_spread_sheet2}'", file=sys.stdout)
        print(
            f"\n=====================================================\n",
            file=sys.stdout,
        )

    logger._log.info(f"Creating the Summary sheet.")

    # details_column = f"See sheet tab for details."
    # df_summary = pd.DataFrame()
    # df_summary["Summary of changes."] = ""
    # df_summary["See sheet tab for details."] = ""

    df_summary = Summary(["Summary of changes.", "See sheet tab for details."])
    df_summary.df.to_excel(excel, "Summary", index=False)

    # cols = df_summary.columns.tolist()
    # cols.insert(0, cols.pop(cols.index("Summary of changes.")))

    # df_summary = df_summary.reindex(columns=cols)
    # df_summary.to_excel(excel, "Summary", index=False)

    df_summary.add(
        [
            f"Comparing '{short_spread_sheet1}' with '{short_spread_sheet2}' on {DATE} {TIME}.",
            "",
        ]
    )

    df_summary.add(
        [
            f"All changes listed in this Summary page are relative to '{short_spread_sheet2}'.",
            "",
        ]
    )

    df_summary.add([f"", ""])

    data_changes = False

    if verbose:
        print(
            f"Looking for added or deleted sheet names in spreadsheets:",
            end="",
            file=sys.stdout,
        )

    if deleted_sheet_names1 or deleted_sheet_names2:
        data_changes = True

        if verbose:
            print(
                f"\n\nThe following sheet name(s) changed in the spreadsheet:\n",
                file=sys.stdout,
            )

        if deleted_sheet_names2:
            if verbose:
                print(f"Sheet name(s) added:", file=sys.stdout)

            for added in deleted_sheet_names2:
                if verbose:
                    print(f"\t{added}", file=sys.stdout)

                df_summary.add(
                    [
                        f"Sheet '{added}' added.",
                        f"{added}",
                    ]
                )

                df_sheet = pd.DataFrame(df_spread_sheet2[added])
                df_sheet.to_excel(excel, added, index=False)
                set_col_widths(excel.sheets[added], df_sheet)

        if deleted_sheet_names1 and deleted_sheet_names2:
            if verbose:
                print(f"", file=sys.stdout)

        if deleted_sheet_names1:
            if verbose:
                print(f"Sheet name(s) deleted:", file=sys.stdout)

            for deleted in deleted_sheet_names1:
                if verbose:
                    print(f"\t{deleted}", file=sys.stdout)

                df_summary.add(
                    [
                        f"Sheet '{deleted}' deleted.",
                        f"{deleted}",
                    ]
                )

                df_sheet = pd.DataFrame(df_spread_sheet1[deleted])
                df_sheet.to_excel(excel, deleted, index=False)
                set_col_widths(excel.sheets[deleted], df_sheet)

        if verbose:
            print(
                f"\nThe sheet name(s) listed above will be ignored when analyzing the spreadsheets.\n",
                file=sys.stdout,
            )

    else:
        logger._log.info(
            f"There were no sheets added or deleted in either of the CMDB spreadsheets."
        )
        if verbose:
            print(f" None", file=sys.stdout)

        df_summary.add(
            [
                f"There were no sheets added or deleted in either of the CMDB spreadsheets.",
                f"None",
            ]
        )

    data_changes = False

    print(f"Looking for sheets with data changes.", file=sys.stdout)

    find_diffs = FindDifferences(df_spread_sheet1, df_spread_sheet2, df_summary)

    for sheet in common_sheet_names:
        df_spread_sheet1[sheet] = df_spread_sheet1[sheet].fillna("")
        df_spread_sheet2[sheet] = df_spread_sheet2[sheet].fillna("")

        if not df_spread_sheet2[sheet].equals(df_spread_sheet1[sheet]):
            logger._log.info(f"Sheet '{sheet}' has changes.")
            print(f"Sheet '{sheet}' has changes.", file=sys.stdout)

            df_style, df_sheet, df_summary = find_diffs.find_differences(sheet)
            df_style = df_sheet.style.apply(
                find_diffs.set_style, style=df_style, axis=None
            )

            data_changes = True

            df_style.to_excel(excel, sheet, index=False)
            set_col_widths(excel.sheets[sheet], df_sheet)

        else:
            logger._log.info(f"Sheet '{sheet}' has no changes.")

    if not data_changes:
        logger._log.info(
            f"There was no data changes in any sheet in either of the CMDB spreadsheets."
        )
        if verbose:
            print(
                f"There was no data changes in any sheet in either of the CMDB spreadsheets.",
                file=sys.stdout,
            )

        df_summary.add(
            [
                f"There was no data changes in any sheet in either of the CMDB spreadsheets.",
                f"None",
            ]
        )

        print(
            f"\n=====================================================\n",
            file=sys.stdout,
        )

    logger._log.info(f"Update the Summary sheet.")
    df_summary.df.to_excel(excel, "Summary", index=False)

    logger._log.info(f"Fix Column Widths for the Summary sheet.")
    set_col_widths(excel.sheets["Summary"], df_summary.df)

    logger._log.info(f"Write out the Report spreadsheet.")
    excel.close()

    logger._log.info(f"Create report.")

    # Fix all jinja2 strings.

    replacement = {
        "ADMINEMAIL": admin_email,
        "ADMINNAME": admin_name,
        "ADMINPHONE": admin_phone,
        "DATE": DATE,
        "HOST": HOST,
        "REPORT": report,
        "SPREADSHEET1": short_spread_sheet1,
        "SPREADSHEET2": short_spread_sheet2,
        "TIME": TIME,
        "VERSION": pgm_version,
        "WORKSHEETS1": worksheets1,
        "WORKSHEETS2": worksheets2,
    }

    if data_changes:
        logger._log.info(f"Using text for when data changed between spreadsheets.")
        text = email_text_with_changes
    else:
        logger._log.info(
            f"Using text for when data did not change between spreadsheets."
        )
        text = email_text_without_changes

    logger._log.debug(f"text(1) : {text}")

    logger._log.info(f"Updating variables email_from, subject, and text.")
    email_from = Template(email_from).render(replacement)
    email_subject = Template(email_subject).render(replacement)
    text = Template(text).render(replacement)

    logger._log.debug(f"email_from : '{email_from}'.")
    logger._log.debug(f"email_to : '{email_to}'.")
    logger._log.debug(f"email_cc : '{email_cc}'.")
    logger._log.debug(f"subject : '{email_subject}'.")
    logger._log.debug(f"text(2) : '{text}'")

    sm = SendEmail()
    sm.send_email(
        email_from,
        email_to,
        email_cc,
        email_subject,
        text,
        text_type="plain",
        files=[spread_sheet1, spread_sheet2, report],
        server="localhost",
    )

    logger._log.info(f"Ending program {pgm_version}.")
    if verbose:
        print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
