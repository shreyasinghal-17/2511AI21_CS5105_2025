#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    bool dfsCycle(int node, int parent, vector<int> adj[], vector<int>& visited) {
        visited[node] = 1;

        for (int nei : adj[node]) {
            if (!visited[nei]) {
                if (dfsCycle(nei, node, adj, visited)) return true;
            } 
            else if (nei != parent) {
                // Already visited and not the parent -> cycle found
                return true;
            }
        }
        return false;
    }

    bool isCycle(int V, vector<int> adj[]) {
        vector<int> visited(V, 0);
        for (int i = 0; i < V; i++) {
            if (!visited[i]) {
                if (dfsCycle(i, -1, adj, visited)) return true;
            }
        }
        return false;
    }
};

// Example usage
int main() {
    int V, E;
    cin >> V >> E;
    vector<int> adj[V];
    for (int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u); // undirected graph
    }

    Solution sol;
    if (sol.isCycle(V, adj)) cout << "Cycle detected\n";
    else cout << "No cycle\n";
    return 0;
}
