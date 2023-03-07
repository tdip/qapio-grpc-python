from qapio_python_core.qapi.Qapi import Qapi

qapi = Qapi("http://localhost:4000/graphql")

results = qapi.query("MKT_CAP_LOCAL", "run", ["-120 days", "-1 day", "A"])

print(results)
