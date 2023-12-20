# -*- coding: utf-8 -*-
"""Data-readers for Maccor"""

import pandas as pd
import datetime
from scibatt.config import COLUMN_NAMES, CURRENT_ZERO_TOLERANCE


def read_txt(filepath):
    """
    Reads a maccor datafile and returns a dict of of dataframes;
    The key being the standard filename, and the dataframe being the data for each step in the programme
    """
    # This reads the csv file with some extra options
    with open(filepath, "r") as f:
        header_line_num = None
        for i, line in enumerate(f.readlines()):
            if line.startswith("Rec\tCycle"):
                header_line_num = i
                break
        if not header_line_num:
            raise Exception(
                f"Could not find headerline in Maccor datafile: {filepath}"
            )  # TODO: Convert to custom exception

    df = pd.read_csv(
        filepath,
        usecols=["Cycle", "DPT Time", "Current", "Voltage", "Capacity", "Step", "MD"],
        encoding="UTF-8",
        header=header_line_num,
        delimiter="\t",
    )

    # Modifying time
    def convert_timestamp_to_unix_epoch(timestamp_str):
        timestamp_format = "%m/%d/%Y %H:%M:%S"
        datetime_obj = datetime.datetime.strptime(timestamp_str, timestamp_format)

        return datetime_obj.timestamp()  # Returns unix epoch float

    df[COLUMN_NAMES["TIME"]] = df["DPT Time"].apply(
        lambda x: convert_timestamp_to_unix_epoch(x)
    )

    # Making sure negative currents are negative
    df.loc[df["MD"] == "D", "Current"] *= -1

    # Rename columns to match spec
    df.rename(
        columns={
            "Current": COLUMN_NAMES["CURRENT"],
            "Voltage": COLUMN_NAMES["VOLTAGE1"],
            "Cycle": "Cycle",
        },
        inplace=True,
    )

    # Group by step to separate steps
    groups_step = df.groupby("Step")

    # Scan groups and add to return dict
    data = {}
    tol = CURRENT_ZERO_TOLERANCE
    for num, group_df in groups_step:
        mean_current = group_df[COLUMN_NAMES["CURRENT"]].mean()
        timestamp = group_df[COLUMN_NAMES["TIME"]].iloc[0]

        # Remove columns we don't want
        required_columns = [
            COLUMN_NAMES["TIME"],
            COLUMN_NAMES["CURRENT"],
            COLUMN_NAMES["VOLTAGE1"],
        ]
        group_df = group_df.drop(
            columns=[col for col in df if col not in required_columns]
        )

        if -tol < mean_current < tol:
            data[f"{timestamp}_cycling_p000.000A"] = group_df
        elif mean_current > tol:
            data[f"{timestamp}_cycling_p{mean_current:08.4f}A"] = group_df
        elif mean_current < tol:
            data[f"{timestamp}_cycling_n{mean_current:08.4f}A"] = group_df

    return data
