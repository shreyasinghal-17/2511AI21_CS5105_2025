#include <bits/stdc++.h>
using namespace std;

bool dfs(int node, int c, vector<int> adj[], vector<int>& color) {
    color[node] = c;
    
    for(int neighbor : adj[node]) {
        if(color[neighbor] == -1) {
            // Assign opposite color
            if(!dfs(neighbor, 1 - c, adj, color))
                return false;
        } else if(color[neighbor] == color[node]) {
            // Conflict → not bipartite
            return false;
        }
    }
    return true;
}

bool isBipartite(int V, vector<int> adj[]) {
    vector<int> color(V, -1);
    
    // Graph may be disconnected → check all components
    for(int i = 0; i < V; i++) {
        if(color[i] == -1) {
            if(!dfs(i, 0, adj, color))
                return false;
        }
    }
    return true;
}

int main() {
    int V, E;
    cin >> V >> E;
    vector<int> adj[V];
    
    for(int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u); // undirected graph
    }
    
    if(isBipartite(V, adj))
        cout << "Graph is Bipartite\n";
    else
        cout << "Graph is Not Bipartite\n";
    
    return 0;
}
