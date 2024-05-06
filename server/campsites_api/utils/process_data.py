import codecs
import csv
from typing import List

from fastapi import HTTPException, UploadFile

import campsites_api.utils.process_data_utils as ut
from campsites_api.dto import CampsiteDTO


def process_data(file: UploadFile) -> List[CampsiteDTO]:

    raw_rows = []

    reader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))
    for row in reader:
        raw_rows.append(row)

    if len(raw_rows) == 0:
        raise HTTPException(status_code=422, detail="Empty file uploaded.")


    processed_campsites: List[CampsiteDTO] = []

    for row in raw_rows:

        row = {k: v.strip() if v.strip() != "" else None for (k, v) in row.items()}


        row["num_campsites"] = (
            row["num_campsites"]
            if row["num_campsites"] is not None and row["num_campsites"].isdigit()
            else None
        )

        row["campsite_type"] = row["type"]

        row["phone"] = ut.process_phone_number(row["phone"])

        dates = ut.process_dates(row["dates_open"])
        row = row | dates

        row["country"] = ut.process_country(row["state"])

        amenities = ut.process_amenities(row["amenities"])
        row = row | amenities
        try:
            processed_campsites.append(CampsiteDTO(**row))
        except Exception:
            raise HTTPException(status_code=422, detail="CSV file in incorrect format.")

    file.file.close()
    return processed_campsites
