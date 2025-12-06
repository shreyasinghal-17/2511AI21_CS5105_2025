#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(3^N)
// Space Complexity: O(N) (Recursion Stack)
int getMaxPathSumBrute(int i, int j, int m, vector<vector<int>> &matrix) {
    // Boundary check
    if (j < 0 || j >= m) return -1e9; // Return very small value for invalid paths
    if (i == 0) return matrix[0][j]; // Base case: reached the first row

    int up = matrix[i][j] + getMaxPathSumBrute(i - 1, j, m, matrix);
    int leftDiag = matrix[i][j] + getMaxPathSumBrute(i - 1, j - 1, m, matrix);
    int rightDiag = matrix[i][j] + getMaxPathSumBrute(i - 1, j + 1, m, matrix);

    return max(up, max(leftDiag, rightDiag));
}

// Optimal Approach: Space Optimization (Tabulation)
// Time Complexity: O(N*M)
// Space Complexity: O(M) (Storing only the previous row)
int getMaxPathSumOptimal(vector<vector<int>> &matrix) {
    int n = matrix.size();
    int m = matrix[0].size();
    vector<int> prev(m, 0);

    // Initialize first row
    for (int j = 0; j < m; j++) {
        prev[j] = matrix[0][j];
    }

    for (int i = 1; i < n; i++) {
        vector<int> cur(m, 0);
        for (int j = 0; j < m; j++) {
            int up = matrix[i][j] + prev[j];
            
            int leftDiag = matrix[i][j];
            if (j - 1 >= 0) leftDiag += prev[j - 1];
            else leftDiag += -1e9;

            int rightDiag = matrix[i][j];
            if (j + 1 < m) rightDiag += prev[j + 1];
            else rightDiag += -1e9;

            cur[j] = max(up, max(leftDiag, rightDiag));
        }
        prev = cur;
    }

    // The answer is the maximum value in the last row
    int maxi = -1e9;
    for (int j = 0; j < m; j++) {
        maxi = max(maxi, prev[j]);
    }
    return maxi;
}

int main() {
    vector<vector<int>> matrix = {{1, 2, 10, 4}, {100, 3, 2, 1}, {1, 1, 20, 2}, {1, 2, 2, 1}};
    // Optimal call for full answer
    cout << "Maximum Path Sum: " << getMaxPathSumOptimal(matrix) << endl; 
    return 0;
}