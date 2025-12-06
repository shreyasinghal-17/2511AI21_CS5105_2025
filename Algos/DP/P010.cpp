#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(2^N)
// Space Complexity: O(N)
int minimumTotalBrute(int i, int j, int n, vector<vector<int>>& triangle) {
    if (i == n - 1) return triangle[i][j];

    int down = triangle[i][j] + minimumTotalBrute(i + 1, j, n, triangle);
    int diagonal = triangle[i][j] + minimumTotalBrute(i + 1, j + 1, n, triangle);

    return min(down, diagonal);
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N*N)
// Space Complexity: O(N)
// Note: We start tabulation from the bottom row up to the top.
int minimumTotalOptimal(int n, vector<vector<int>>& triangle) {
    vector<int> front(n, 0); // Represents the next row (i+1)

    // Base Case: Fill the last row
    for (int j = 0; j < n; j++) {
        front[j] = triangle[n - 1][j];
    }

    // Move upwards from second last row
    for (int i = n - 2; i >= 0; i--) {
        vector<int> cur(n, 0);
        for (int j = i; j >= 0; j--) {
            int down = triangle[i][j] + front[j];
            int diagonal = triangle[i][j] + front[j + 1];
            cur[j] = min(down, diagonal);
        }
        front = cur;
    }
    return front[0];
}

int main() {
    vector<vector<int>> triangle = {{1}, {2, 3}, {3, 6, 7}, {8, 9, 6, 10}};
    int n = triangle.size();
    cout << "Minimum Path Sum in Triangle: " << minimumTotalOptimal(n, triangle) << endl;
    return 0;
}