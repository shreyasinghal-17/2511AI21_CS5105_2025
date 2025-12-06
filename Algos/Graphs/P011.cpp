// C++17
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    int n;
    vector<int> parent, rank;
    DSU(int n): n(n), parent(n), rank(n,0) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] == x) return x;
        return parent[x] = find(parent[x]);
    }
    bool unite(int a, int b) {
        int pa = find(a), pb = find(b);
        if (pa == pb) return false;
        if (rank[pa] < rank[pb]) swap(pa, pb);
        parent[pb] = pa;
        if (rank[pa] == rank[pb]) ++rank[pa];
        return true;
    }
};

class Solution {
public:
    // stones: vector of {row, col}
    int removeStones(vector<vector<int>>& stones) {
        int n = stones.size();
        DSU dsu(n);
        unordered_map<int,int> row_to_index;
        unordered_map<int,int> col_to_index;

        for (int i = 0; i < n; ++i) {
            int r = stones[i][0];
            int c = stones[i][1];
            // If row seen before, union this stone with that representative
            if (row_to_index.count(r)) dsu.unite(i, row_to_index[r]);
            else row_to_index[r] = i;

            // If column seen before, union this stone with that representative
            if (col_to_index.count(c)) dsu.unite(i, col_to_index[c]);
            else col_to_index[c] = i;
        }

        // Count number of distinct components
        unordered_set<int> comps;
        for (int i = 0; i < n; ++i) comps.insert(dsu.find(i));
        int components = (int)comps.size();

        // Max stones removable = total stones - number of connected components
        return n - components;
    }
};

// Optional main for quick testing
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Input format:
    // first line: n (number of stones)
    // next n lines: r c
    int n;
    if (!(cin >> n)) return 0;
    vector<vector<int>> stones(n, vector<int>(2));
    for (int i = 0; i < n; ++i) cin >> stones[i][0] >> stones[i][1];

    Solution sol;
    cout << sol.removeStones(stones) << "\n";
    return 0;
}
// C++17
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    int n;
    vector<int> parent, rank;
    DSU(int n): n(n), parent(n), rank(n,0) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] == x) return x;
        return parent[x] = find(parent[x]);
    }
    bool unite(int a, int b) {
        int pa = find(a), pb = find(b);
        if (pa == pb) return false;
        if (rank[pa] < rank[pb]) swap(pa, pb);
        parent[pb] = pa;
        if (rank[pa] == rank[pb]) ++rank[pa];
        return true;
    }
};

class Solution {
public:
    // stones: vector of {row, col}
    int removeStones(vector<vector<int>>& stones) {
        int n = stones.size();
        DSU dsu(n);
        unordered_map<int,int> row_to_index;
        unordered_map<int,int> col_to_index;

        for (int i = 0; i < n; ++i) {
            int r = stones[i][0];
            int c = stones[i][1];
            // If row seen before, union this stone with that representative
            if (row_to_index.count(r)) dsu.unite(i, row_to_index[r]);
            else row_to_index[r] = i;

            // If column seen before, union this stone with that representative
            if (col_to_index.count(c)) dsu.unite(i, col_to_index[c]);
            else col_to_index[c] = i;
        }

        // Count number of distinct components
        unordered_set<int> comps;
        for (int i = 0; i < n; ++i) comps.insert(dsu.find(i));
        int components = (int)comps.size();

        // Max stones removable = total stones - number of connected components
        return n - components;
    }
};

// Optional main for quick testing
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Input format:
    // first line: n (number of stones)
    // next n lines: r c
    int n;
    if (!(cin >> n)) return 0;
    vector<vector<int>> stones(n, vector<int>(2));
    for (int i = 0; i < n; ++i) cin >> stones[i][0] >> stones[i][1];

    Solution sol;
    cout << sol.removeStones(stones) << "\n";
    return 0;
}
