#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Wed Dec 20 17:47:18 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

import sys
import pandas as pd
from pathlib import Path
from autologging import logged, traced
from datetime import datetime


class Summary:
    def __init__(self, columns: list):
        self.df = pd.DataFrame()
        for column in columns:
            self.df[column] = ""
        cols = self.df.columns.tolist()
        cols.insert(0, cols.pop(cols.index(columns[0])))
        self.df = self.df.reindex(columns=cols)

    def add(self, data: list) -> None:
        self.df.loc[len(self.df)] = data

    def get(self) -> pd.DataFrame:
        return self.df
