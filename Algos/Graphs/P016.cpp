#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    void dfs(int r, int c, vector<vector<char>>& mat, vector<vector<int>>& visited) {
        int n = mat.size(), m = mat[0].size();
        visited[r][c] = 1;

        // Directions: up, down, left, right
        int dr[4] = {-1, 1, 0, 0};
        int dc[4] = {0, 0, -1, 1};

        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k];
            int nc = c + dc[k];
            if (nr >= 0 && nc >= 0 && nr < n && nc < m &&
                !visited[nr][nc] && mat[nr][nc] == 'O') {
                dfs(nr, nc, mat, visited);
            }
        }
    }

    void replaceSurrounded(vector<vector<char>>& mat) {
        int n = mat.size(), m = mat[0].size();
        vector<vector<int>> visited(n, vector<int>(m, 0));

        // Step 1: Mark all 'O's connected to boundary
        for (int i = 0; i < n; i++) {
            // first col, last col
            if (mat[i][0] == 'O' && !visited[i][0]) dfs(i, 0, mat, visited);
            if (mat[i][m-1] == 'O' && !visited[i][m-1]) dfs(i, m-1, mat, visited);
        }
        for (int j = 0; j < m; j++) {
            // first row, last row
            if (mat[0][j] == 'O' && !visited[0][j]) dfs(0, j, mat, visited);
            if (mat[n-1][j] == 'O' && !visited[n-1][j]) dfs(n-1, j, mat, visited);
        }

        // Step 2: Convert unvisited 'O's to 'X'
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (mat[i][j] == 'O' && !visited[i][j]) {
                    mat[i][j] = 'X';
                }
            }
        }
    }
};

// Example usage
int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<char>> mat(n, vector<char>(m));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> mat[i][j];

    Solution sol;
    sol.replaceSurrounded(mat);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) cout << mat[i][j] << " ";
        cout << "\n";
    }
    return 0;
}
