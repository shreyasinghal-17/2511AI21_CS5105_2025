#include <bits/stdc++.h>
using namespace std;

vector<int> dijkstra(int V, vector<vector<pair<int,int>>>& adj, int src) {
    // Distance array
    vector<int> dist(V, INT_MAX);
    dist[src] = 0;

    // Min-heap: {distance, node}
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    pq.push({0, src});

    while(!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        // Skip if we already found a better path
        if(d > dist[u]) continue;

        for(auto [v, wt] : adj[u]) {
            if(dist[u] + wt < dist[v]) {
                dist[v] = dist[u] + wt;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    int V, E;
    cin >> V >> E;

    // Adjacency list: adj[u] = {{v, weight}, ...}
    vector<vector<pair<int,int>>> adj(V);

    for(int i = 0; i < E; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w}); // remove this if graph is directed
    }

    int src;
    cin >> src;

    vector<int> dist = dijkstra(V, adj, src);

    cout << "Shortest distances from source " << src << ":\n";
    for(int i = 0; i < V; i++) {
        cout << "Node " << i << " : " << dist[i] << "\n";
    }

    return 0;
}
