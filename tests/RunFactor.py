from qapio_python_core.qapi.Qapi import Qapi
from pandas import Timestamp
qapi = Qapi("http://localhost:4000/graphql")

results = qapi.time_series("MKT_CAP_LOCAL").dataset("MY_DATA", ["A"], ["B"], Timestamp("2020-01-01", tz="utc"), Timestamp("2023-01-01", tz="utc"))

print(results)
