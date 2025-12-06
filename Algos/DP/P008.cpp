#include <iostream>
#include <vector>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(2^(M+N))
// Space Complexity: O(M+N)
int uniquePathsObstaclesBrute(int i, int j, vector<vector<int>>& maze) {
    if (i >= 0 && j >= 0 && maze[i][j] == -1) return 0;
    if (i == 0 && j == 0) return 1;
    if (i < 0 || j < 0) return 0;

    int up = uniquePathsObstaclesBrute(i - 1, j, maze);
    int left = uniquePathsObstaclesBrute(i, j - 1, maze);
    return up + left;
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N*M)
// Space Complexity: O(M)
int uniquePathsObstaclesOptimal(int n, int m, vector<vector<int>>& maze) {
    vector<int> prev(m, 0);

    for (int i = 0; i < n; i++) {
        vector<int> temp(m, 0);
        for (int j = 0; j < m; j++) {
            if (maze[i][j] == -1) {
                temp[j] = 0;
                continue;
            }
            if (i == 0 && j == 0) {
                temp[j] = 1;
                continue;
            }
            
            int up = 0;
            int left = 0;
            if (i > 0) up = prev[j];
            if (j > 0) left = temp[j - 1];
            
            temp[j] = up + left;
        }
        prev = temp;
    }
    return prev[m - 1];
}

int main() {
    vector<vector<int>> maze = {{0, 0, 0}, {0, -1, 0}, {0, 0, 0}};
    int n = maze.size();
    int m = maze[0].size();
    cout << "Unique paths with obstacles: " << uniquePathsObstaclesOptimal(n, m, maze) << endl;
    return 0;
}