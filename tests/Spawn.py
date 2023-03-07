from qapio_python_core.qapi.Qapi import Qapi

qapi = Qapi("http://localhost:4000/graphql")

print(qapi.query("MKT_CAP_LOCAL", "run", ["-12 days", "-1 day", "A"]))

#esults = qapi.time_series("MyInfluxNode").dataset("MY_DATA", ["B02ZTY-R", "B1MKLM-R", "B4KHWT-R"], ["VOLATILITY"], "2000-01-01", "2023-03-01")

query = f'from(bucket: "EXTRACT")' \
        f'|> range(start: -1y, stop: now())' \
        f'|> filter(fn: (r) => r["_measurement"] == "EM" and r["_field"]=="VOLATILITY")' \
        f'|> keep(columns: ["FSYM_ID","_measurement"])' \
        f'|> distinct()'

members = []


results = qapi.time_series("InfluxDb").query(query)


measurements = list(results.FSYM_ID.unique())

for member in measurements:
    members.append({"measurement": member, "meta": {}})

print(members)
