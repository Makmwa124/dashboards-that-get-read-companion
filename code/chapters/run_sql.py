# Run every statement in a .sql file against coastline.sqlite and print the results
import sqlite3, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import coastline as cl

con = sqlite3.connect(cl.DATA / "coastline.sqlite")
sql = open(sys.argv[1]).read()
for stmt in [s for s in sql.split(";") if "SELECT" in s.upper()]:
    cur = con.execute(stmt)
    cols = [d[0] for d in cur.description]
    rows = [[str(v) for v in r] for r in cur.fetchall()]
    w = [max(len(c), *(len(r[i]) for r in rows)) for i, c in enumerate(cols)]
    print("  ".join(c.ljust(w[i]) for i, c in enumerate(cols)).rstrip())
    print("  ".join("-" * w[i] for i in range(len(cols))))
    for r in rows:
        print("  ".join(v.ljust(w[i]) for i, v in enumerate(r)).rstrip())
    print()
