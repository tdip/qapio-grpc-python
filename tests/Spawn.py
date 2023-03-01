from qapio_python_core.qapi.Qapi import Qapi
qapi = Qapi("http://localhost:4000/graphql")


results = qapi.query("Factor1", "run", ["-12 days", "-1 day", "APL"])

print(results)
