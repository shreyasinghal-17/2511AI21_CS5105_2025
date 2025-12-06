#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> parent, rank;
    DSU(int n) {
        parent.resize(n);
        rank.resize(n, 0);
        for(int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if(parent[x] != x)
            parent[x] = find(parent[x]);
        return parent[x];
    }
    void unite(int x, int y) {
        int px = find(x), py = find(y);
        if(px == py) return;
        if(rank[px] < rank[py]) parent[px] = py;
        else if(rank[px] > rank[py]) parent[py] = px;
        else {
            parent[py] = px;
            rank[px]++;
        }
    }
};

int makeConnected(int n, vector<vector<int>>& connections) {
    if(connections.size() < n - 1) return -1; // not enough edges
    
    DSU dsu(n);
    for(auto &c : connections) {
        dsu.unite(c[0], c[1]);
    }
    
    unordered_set<int> components;
    for(int i = 0; i < n; i++) {
        components.insert(dsu.find(i));
    }
    
    return (int)components.size() - 1;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> connections(m, vector<int>(2));
    for(int i = 0; i < m; i++) {
        cin >> connections[i][0] >> connections[i][1];
    }
    
    cout << makeConnected(n, connections) << "\n";
    return 0;
}
