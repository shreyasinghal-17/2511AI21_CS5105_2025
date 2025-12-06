#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    void dfs(int r, int c, vector<vector<int>>& image, int oldColor, int newColor) {
        int rows = image.size(), cols = image[0].size();
        // Out of bounds or different color -> stop
        if (r < 0 || c < 0 || r >= rows || c >= cols) return;
        if (image[r][c] != oldColor) return;

        // Fill current pixel
        image[r][c] = newColor;

        // Explore 4 directions
        dfs(r+1, c, image, oldColor, newColor);
        dfs(r-1, c, image, oldColor, newColor);
        dfs(r, c+1, image, oldColor, newColor);
        dfs(r, c-1, image, oldColor, newColor);
    }

    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int newColor) {
        int oldColor = image[sr][sc];
        if (oldColor == newColor) return image; // no change needed
        dfs(sr, sc, image, oldColor, newColor);
        return image;
    }
};

// Example usage
int main() {
    int n, m;
    cin >> n >> m; // rows, cols
    vector<vector<int>> image(n, vector<int>(m));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> image[i][j];

    int sr, sc, newColor;
    cin >> sr >> sc >> newColor;

    Solution sol;
    vector<vector<int>> res = sol.floodFill(image, sr, sc, newColor);

    for (auto& row : res) {
        for (int val : row) cout << val << " ";
        cout << "\n";
    }
    return 0;
}
