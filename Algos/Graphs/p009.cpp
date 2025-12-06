#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int countPaths(int n, vector<vector<int>>& roads) {
    vector<vector<pair<int,long long>>> adj(n);

    for(auto &r : roads) {
        int u = r[0], v = r[1], t = r[2];
        adj[u].push_back({v, t});
        adj[v].push_back({u, t});
    }

    vector<long long> dist(n, LLONG_MAX);
    vector<long long> ways(n, 0);

    // Min-heap {dist, node}
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;

    dist[0] = 0;
    ways[0] = 1;
    pq.push({0, 0});

    while(!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if(d > dist[u]) continue;

        for(auto [v, w] : adj[u]) {
            long long newDist = d + w;

            if(newDist < dist[v]) {
                dist[v] = newDist;
                ways[v] = ways[u];
                pq.push({newDist, v});
            } else if(newDist == dist[v]) {
                ways[v] = (ways[v] + ways[u]) % MOD;
            }
        }
    }

    return ways[n-1] % MOD;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> roads(m, vector<int>(3));

    for(int i = 0; i < m; i++) {
        cin >> roads[i][0] >> roads[i][1] >> roads[i][2];
    }

    cout << countPaths(n, roads) << "\n";
    return 0;
}
