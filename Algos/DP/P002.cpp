#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <climits>

using namespace std;

// Brute Force Approach: Recursion
// Time Complexity: O(2^N)
// Space Complexity: O(N)
int frogJumpBrute(int index, vector<int>& heights) {
    if (index == 0) return 0;
    
    int left = frogJumpBrute(index - 1, heights) + abs(heights[index] - heights[index - 1]);
    int right = INT_MAX;
    if (index > 1) {
        right = frogJumpBrute(index - 2, heights) + abs(heights[index] - heights[index - 2]);
    }
    
    return min(left, right);
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N)
// Space Complexity: O(1)
int frogJumpOptimal(int n, vector<int>& heights) {
    int prev = 0;
    int prev2 = 0;

    for (int i = 1; i < n; i++) {
        int left = prev + abs(heights[i] - heights[i - 1]);
        int right = INT_MAX;
        if (i > 1) {
            right = prev2 + abs(heights[i] - heights[i - 2]);
        }
        
        int current = min(left, right);
        prev2 = prev;
        prev = current;
    }
    return prev;
}

int main() {
    vector<int> heights = {10, 20, 30, 10}; 
    int n = heights.size();
    cout << "Minimum energy required: " << frogJumpOptimal(n, heights) << endl;
    return 0;
}