#include <bits/stdc++.h>
using namespace std;

int minimumEffortPath(vector<vector<int>>& heights) {
    int n = heights.size(), m = heights[0].size();
    vector<vector<int>> dist(n, vector<int>(m, INT_MAX));
    dist[0][0] = 0;

    // Min-heap: {effort, {x, y}}
    priority_queue<pair<int, pair<int,int>>, 
                   vector<pair<int, pair<int,int>>>, 
                   greater<pair<int, pair<int,int>>>> pq;

    pq.push({0, {0, 0}});

    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};

    while(!pq.empty()) {
        auto [effort, cell] = pq.top();
        pq.pop();

        int x = cell.first, y = cell.second;

        // If we reached the destination
        if(x == n-1 && y == m-1) return effort;

        for(int k = 0; k < 4; k++) {
            int nx = x + dx[k];
            int ny = y + dy[k];

            if(nx >= 0 && ny >= 0 && nx < n && ny < m) {
                int newEffort = max(effort, abs(heights[x][y] - heights[nx][ny]));
                if(newEffort < dist[nx][ny]) {
                    dist[nx][ny] = newEffort;
                    pq.push({newEffort, {nx, ny}});
                }
            }
        }
    }

    return 0; // fallback, though we always reach (n-1,m-1)
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> heights(n, vector<int>(m));

    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> heights[i][j];
        }
    }

    cout << minimumEffortPath(heights) << "\n";
    return 0;
}
