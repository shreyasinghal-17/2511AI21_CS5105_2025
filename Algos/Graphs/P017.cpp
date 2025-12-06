#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    void dfs(int r, int c, vector<vector<int>>& grid, vector<vector<int>>& visited) {
        int n = grid.size(), m = grid[0].size();
        visited[r][c] = 1;
        int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};

        for (int k = 0; k < 4; ++k) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr >= 0 && nr < n && nc >= 0 && nc < m &&
                !visited[nr][nc] && grid[nr][nc] == 1) {
                dfs(nr, nc, grid, visited);
            }
        }
    }

    int numEnclaves(vector<vector<int>>& grid) {
        int n = grid.size(), m = grid[0].size();
        vector<vector<int>> visited(n, vector<int>(m, 0));

        // Start DFS from all boundary land cells
        for (int i = 0; i < n; ++i) {
            if (grid[i][0] == 1 && !visited[i][0]) dfs(i, 0, grid, visited);
            if (grid[i][m-1] == 1 && !visited[i][m-1]) dfs(i, m-1, grid, visited);
        }
        for (int j = 0; j < m; ++j) {
            if (grid[0][j] == 1 && !visited[0][j]) dfs(0, j, grid, visited);
            if (grid[n-1][j] == 1 && !visited[n-1][j]) dfs(n-1, j, grid, visited);
        }

        // Count unvisited land cells (enclaves)
        int enclaves = 0;
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                if (grid[i][j] == 1 && !visited[i][j])
                    ++enclaves;

        return enclaves;
    }
};

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> grid(n, vector<int>(m));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            cin >> grid[i][j];

    Solution sol;
    cout << sol.numEnclaves(grid) << "\n";
    return 0;
}
