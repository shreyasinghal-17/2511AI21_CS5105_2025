#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(2^(N+M))
// Space Complexity: O(N+M)
int minPathSumBrute(int i, int j, vector<vector<int>>& grid) {
    if (i == 0 && j == 0) return grid[0][0];
    if (i < 0 || j < 0) return 1e9; // Return large value for invalid paths

    int up = grid[i][j] + minPathSumBrute(i - 1, j, grid);
    int left = grid[i][j] + minPathSumBrute(i, j - 1, grid);

    return min(up, left);
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N*M)
// Space Complexity: O(M)
int minPathSumOptimal(int n, int m, vector<vector<int>>& grid) {
    vector<int> prev(m, 0);

    for (int i = 0; i < n; i++) {
        vector<int> temp(m, 0);
        for (int j = 0; j < m; j++) {
            if (i == 0 && j == 0) {
                temp[j] = grid[i][j];
                continue;
            }
            
            int up = grid[i][j];
            if (i > 0) up += prev[j];
            else up = 1e9;
            
            int left = grid[i][j];
            if (j > 0) left += temp[j - 1];
            else left = 1e9;
            
            temp[j] = min(up, left);
        }
        prev = temp;
    }
    return prev[m - 1];
}

int main() {
    vector<vector<int>> grid = {{5, 9, 6}, {11, 5, 2}};
    int n = grid.size();
    int m = grid[0].size();
    cout << "Minimum Path Sum: " << minPathSumOptimal(n, m, grid) << endl;
    return 0;
}