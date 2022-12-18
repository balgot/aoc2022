"""
DP[i][j] = "max pressure released with i minutes remaining starting at room j"
OP[i][j] = "whether j-th room's valve is open"

DP[0][j] = 0
OP[0][j] = False

DP[i][j] = max{
    valve[j] + DP[i-1][j]  # open IF NOT OPENED
    max{ DP[i-1][k] for k in neighrbours[j] }  # move - keep open status
}
"""
import sys
from typing import Dict, Tuple, List
from pprint import pprint
from tqdm import tqdm


DEBUG = True
_dbg = lambda *args, **kwargs: pprint(*args, **kwargs) if DEBUG else ()


TIME = 30  # minutes ;)
Graph = Dict[str, List[str]]  # adjacency list, both dirs
Stats = Dict[str, int]  # valve stats for each room


def load() -> Tuple[Graph, Stats]:
    g: Graph = {}
    s: Stats = {}
    for line in sys.stdin:
        _valve, name, _has, _flow, rate, _tunnels, _lead, _to, _valves, *vs = line.split()
        rate = int(rate.strip(";").split("=")[1])
        s[name] = rate
        g[name] = [v.strip(",") for v in vs]
    return g, s


def _travel(g: Graph, s: Stats):
    # exponential
    start = "AA"
    opened = { room: False for room in g }

    def _dfs(room: str, ttl: int) -> int:
        if ttl <= 0: return 0
        open_score = 0
        if not opened[room] and s[room] > 0:
            opened[room] = True
            open_score = s[room] * (ttl - 1) + _dfs(room, ttl - 1)
            # opened[room] = False
            return open_score
        travel_score = max(_dfs(nxt, ttl-1) for nxt in tqdm(g[room], leave=False))
        return max(open_score, travel_score)

    return _dfs(start, TIME)


def _dp(g: Graph, s: Stats) -> int:
    # dp[time][room] - best achievable score at any given time from any given room
    dp = [{k: 0 for k in g} for _ in range(TIME+1)]
    # op[time][room] - dictionry assigning bool to each open room when starting from room at time
    op = [{k: {j: False for j in g} for k in g} for _ in range(TIME+1)]

    for i in range(1, TIME+1):
        for j in g:
            # move away from this room
            best_move = None  # score, which room
            for k in g[j]:
                score = dp[i-1][k]
                if best_move is None or score > best_move[0]:
                    best_move = (score, k)

            # try to open this room
            if not op[i-1][j]:
                best_open = s[j]*(i-1) + dp[i-1][j]
                if best_open > best_move:
                    op[i][j] = True
                    best_move = best_open
            dp[i][j] = best_move
    return dp[TIME]["AA"]


def main():
    g, s = load()
    _dbg(g)
    _dbg(s)
    print(_travel(g, s))
    # print(_dp(g, s))


if __name__ == "__main__":
    main()
