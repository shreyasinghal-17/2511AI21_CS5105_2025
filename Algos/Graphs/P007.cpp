#include <bits/stdc++.h>
using namespace std;

// Function to find shortest path in a binary maze
int shortestPath(vector<vector<int>>& grid, pair<int,int> src, pair<int,int> dest) {
    int n = grid.size(), m = grid[0].size();
    
    if(grid[src.first][src.second] == 0 || grid[dest.first][dest.second] == 0)
        return -1; // blocked source or destination

    vector<vector<int>> dist(n, vector<int>(m, INT_MAX));
    dist[src.first][src.second] = 0;

    // Min-heap: {distance, {x, y}}
    priority_queue<pair<int, pair<int,int>>, 
                   vector<pair<int, pair<int,int>>>, 
                   greater<pair<int, pair<int,int>>>> pq;

    pq.push({0, {src.first, src.second}});

    // Directions: up, down, left, right
    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};

    while(!pq.empty()) {
        auto [d, cell] = pq.top();
        pq.pop();

        int x = cell.first, y = cell.second;

        // If destination reached
        if(x == dest.first && y == dest.second) 
            return d;

        for(int k = 0; k < 4; k++) {
            int nx = x + dx[k];
            int ny = y + dy[k];

            if(nx >= 0 && ny >= 0 && nx < n && ny < m && grid[nx][ny] == 1) {
                if(d + 1 < dist[nx][ny]) {
                    dist[nx][ny] = d + 1;
                    pq.push({dist[nx][ny], {nx, ny}});
                }
            }
        }
    }

    return -1; // destination not reachable
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> grid(n, vector<int>(m));

    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            cin >> grid[i][j];
        }
    }

    int sx, sy, dx, dy;
    cin >> sx >> sy >> dx >> dy;

    int ans = shortestPath(grid, {sx, sy}, {dx, dy});
    cout << ans << "\n";

    return 0;
}
