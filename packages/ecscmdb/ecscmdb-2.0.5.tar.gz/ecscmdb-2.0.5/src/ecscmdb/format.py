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
import pandas as pd


@traced
@logged
def get_col_widths(df: pd.DataFrame) -> list:
    return [
        int(max([len(str(s)) for s in df[col].values] + [len(col)]) + 2.0)
        for col in df.columns
    ]


@traced
@logged
def set_col_widths(ws: pd.DataFrame, df: pd.DataFrame) -> None:
    for i, width in enumerate(get_col_widths(df)):
        ws.set_column(i, i, width)


@traced
@logged
def reformat_text(text: str, max_len: int = 100) -> str:
    """
    Doc String
    """

    text_out = ""
    for i in text.splitlines():
        line = ""
        for w in i.split(" "):
            if len(f"{line} {w}") > max_len:
                text_out += line + "\n"
                line = w
            elif len(w) == 0:
                text_out += "\n"
            elif len(line) == 0:
                line = w
            else:
                line += f" {w}"
        if len(line) > 0:
            text_out += line + "\n"
    return text_out
