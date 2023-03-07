from qapio_python_core.qapi.Qapi import Qapi

qapi = Qapi("http://localhost:4000/graphql")

qapi.mutate("Screen", "run", ["-12 days", "-1 day"])

