#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    void dfs(int r, int c, vector<vector<int>>& grid, vector<vector<int>>& visited) {
        int n = grid.size(), m = grid[0].size();
        visited[r][c] = 1;

        // 8 directions
        int dr[8] = {-1,-1,-1,0,0,1,1,1};
        int dc[8] = {-1,0,1,-1,1,-1,0,1};

        for (int k = 0; k < 8; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr >= 0 && nr < n && nc >= 0 && nc < m &&
                !visited[nr][nc] && grid[nr][nc] == 1) {
                dfs(nr, nc, grid, visited);
            }
        }
    }

    int numIslands(vector<vector<int>>& grid) {
        int n = grid.size(), m = grid[0].size();
        vector<vector<int>> visited(n, vector<int>(m, 0));
        int count = 0;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (!visited[i][j] && grid[i][j] == 1) {
                    count++;
                    dfs(i, j, grid, visited);
                }
            }
        }
        return count;
    }
};

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> grid(n, vector<int>(m));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> grid[i][j];

    Solution sol;
    cout << sol.numIslands(grid) << "\n";
    return 0;
}
