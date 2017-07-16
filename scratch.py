import pandas as pd
import censusbatchgeocoder

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

df = pd.read_excel(
    "~/Code/python-censusbatchgeocoder-example/privateschools1617.xls",
    skiprows=3
)

result = censusbatchgeocoder.geocode(
    df.to_dict("records")[770:775],
    id="Affidavit ID",
    address="Street",
    city="City",
    state="State",
    zipcode="Zip",
)
