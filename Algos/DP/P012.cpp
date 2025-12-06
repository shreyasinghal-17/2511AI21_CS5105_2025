#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(3^N * 3^N)
// Space Complexity: O(N)
int solveBrute(int i, int j1, int j2, int n, int m, vector<vector<int>> &grid) {
    if (j1 < 0 || j1 >= m || j2 < 0 || j2 >= m) return -1e8;
    if (i == n - 1) {
        if (j1 == j2) return grid[i][j1];
        else return grid[i][j1] + grid[i][j2];
    }

    int maxi = -1e8;
    // Explore all 9 combinations of moves (Alice's 3 moves * Bob's 3 moves)
    for (int di = -1; di <= 1; di++) {
        for (int dj = -1; dj <= 1; dj++) {
            int value = 0;
            if (j1 == j2) value = grid[i][j1];
            else value = grid[i][j1] + grid[i][j2];
            
            value += solveBrute(i + 1, j1 + di, j2 + dj, n, m, grid);
            maxi = max(maxi, value);
        }
    }
    return maxi;
}

// Optimal Approach: Space Optimization (Tabulation)
// Time Complexity: O(N * M * M)
// Space Complexity: O(M * M)
int solveOptimal(int n, int m, vector<vector<int>> &grid) {
    vector<vector<int>> prev(m, vector<int>(m, 0));

    // Base Case: Last row
    for (int j1 = 0; j1 < m; j1++) {
        for (int j2 = 0; j2 < m; j2++) {
            if (j1 == j2) prev[j1][j2] = grid[n - 1][j1];
            else prev[j1][j2] = grid[n - 1][j1] + grid[n - 1][j2];
        }
    }

    // Move upwards from second last row
    for (int i = n - 2; i >= 0; i--) {
        vector<vector<int>> cur(m, vector<int>(m, 0));
        for (int j1 = 0; j1 < m; j1++) {
            for (int j2 = 0; j2 < m; j2++) {
                int maxi = -1e8;
                // 9 transitions
                for (int di = -1; di <= 1; di++) {
                    for (int dj = -1; dj <= 1; dj++) {
                        int ans;
                        if (j1 == j2) ans = grid[i][j1];
                        else ans = grid[i][j1] + grid[i][j2];
                        
                        // Check boundary for next state
                        if (j1 + di >= 0 && j1 + di < m && j2 + dj >= 0 && j2 + dj < m)
                            ans += prev[j1 + di][j2 + dj];
                        else
                            ans += -1e8;
                        
                        maxi = max(maxi, ans);
                    }
                }
                cur[j1][j2] = maxi;
            }
        }
        prev = cur;
    }
    return prev[0][m - 1]; // Alice start (0), Bob start (m-1)
}

int main() {
    vector<vector<int>> grid = {{2, 3, 1, 2}, {3, 4, 2, 2}, {5, 6, 3, 5}};
    int n = grid.size();
    int m = grid[0].size();
    cout << "Max Chocolates: " << solveOptimal(n, m, grid) << endl;
    return 0;
}