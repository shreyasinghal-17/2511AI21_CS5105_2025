#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    void dfs(int node, vector<int> adj[], vector<int>& visited, vector<int>& result) {
        visited[node] = 1;
        result.push_back(node);
        for (int nei : adj[node]) {
            if (!visited[nei]) dfs(nei, adj, visited, result);
        }
    }

    vector<int> dfsOfGraph(int V, vector<int> adj[]) {
        vector<int> result;
        vector<int> visited(V, 0);
        // Assuming graph may be disconnected
        for (int i = 0; i < V; i++) {
            if (!visited[i]) dfs(i, adj, visited, result);
        }
        return result;
    }
};

// Example usage
int main() {
    int V, E;
    cin >> V >> E;  // number of vertices, edges
    vector<int> adj[V];
    for (int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u); // undirected graph
    }

    Solution sol;
    vector<int> dfs_traversal = sol.dfsOfGraph(V, adj);

    for (int x : dfs_traversal) cout << x << " ";
    cout << "\n";
    return 0;
}
