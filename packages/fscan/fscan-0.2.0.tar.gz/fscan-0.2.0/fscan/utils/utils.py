# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#               Evan Goetz (2023)
#
# This file is part of fscan

import re


# simple snippet to handle various ways of specifying True
def str_to_bool(choice):
    return bool(str(choice).lower() in ('yes', 'y', 'true', 't', '1'))


def sft_vals_from_makesft_dag_vars(vars_line):
    """ Get SFT information from MakeSFTDAG dag file VARS line """

    obs = int(re.search('-O (\\d+)', vars_line).group(1))
    kind = re.search('-K ([a-zA-Z]+)', vars_line).group(1)
    rev = int(re.search('-R (\\d+)', vars_line).group(1))
    gpsstart = int(re.search('-s (\\d+)', vars_line).group(1))
    Tsft = int(re.search('-t (\\d+)', vars_line).group(1))
    window = re.search('-w ([a-zA-Z]+)', vars_line).group(1)
    channels = vars_line.split(" -N ")[1].split(" ")[0].split(",")
    sftpaths = vars_line.split(' -p ')[-1].split()[0].split(',')

    return obs, kind, rev, gpsstart, Tsft, window, channels, sftpaths


def sft_name_from_vars(obs, kind, rev, gpsstart, Tsft, window, channel):
    """ Create SFT file name from specification """

    return (
        f"{channel[0]}-1_{channel[:2]}_"
        f"{Tsft}SFT_O{obs}{kind}+R{rev}+"
        f"C{channel[3:].replace('-', '').replace('_', '')}+"
        f"W{window.upper()}-{gpsstart}-{Tsft}.sft")
