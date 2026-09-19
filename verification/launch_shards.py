"""Start N independent `sage -python census_shard.sage.py` processes (no shell job control, no fork of Sage state),
wait for all, report exit codes. Usage: python3 launch_shards.py N <snappy site-packages>"""
import glob, json, subprocess, sys
n, sp = int(sys.argv[1]), sys.argv[2]
done = set(json.load(open("census_done.json")))
for f in glob.glob("census_shard*.jsonl") + glob.glob("census_mp.jsonl"):
    for l in open(f):
        try: done.add(json.loads(l)["name"])
        except Exception: pass
json.dump(sorted(done), open("census_done.json", "w"))
print(len(done), "done before start", flush=True)
sage = "/opt/homebrew/Caskroom/miniforge/base/envs/sage/bin/sage"
procs = [subprocess.Popen([sage, "-python", "census_shard.sage.py", sp, str(i), str(n), f"census_p{i}.jsonl", "census_done.json"],
                          stdout=open(f"census_p{i}.log", "w"), stderr=subprocess.STDOUT, start_new_session=True) for i in range(n)]
codes = [p.wait() for p in procs]
print("exit codes", codes, flush=True)
