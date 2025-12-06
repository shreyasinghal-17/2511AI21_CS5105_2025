#include <iostream>
#include <vector>
#include <cmath>
#include <climits>
#include <algorithm>

using namespace std;

// Brute Force Approach: Recursion
// Time Complexity: O(K^N)
// Space Complexity: O(N)
int frogJumpKBrute(int index, int k, vector<int>& heights) {
    if (index == 0) return 0;
    
    int minEnergy = INT_MAX;
    
    for (int j = 1; j <= k; j++) {
        if (index - j >= 0) {
            int jumpEnergy = frogJumpKBrute(index - j, k, heights) + abs(heights[index] - heights[index - j]);
            minEnergy = min(minEnergy, jumpEnergy);
        }
    }
    return minEnergy;
}

// Optimal Approach: Tabulation
// Time Complexity: O(N * K)
// Space Complexity: O(N) (Can be optimized to O(K) but O(N) is standard for 1D DP array)
int frogJumpKOptimal(int n, int k, vector<int>& heights) {
    vector<int> dp(n, 0);
    dp[0] = 0;

    for (int i = 1; i < n; i++) {
        int minEnergy = INT_MAX;
        
        for (int j = 1; j <= k; j++) {
            if (i - j >= 0) {
                int jumpEnergy = dp[i - j] + abs(heights[i] - heights[i - j]);
                minEnergy = min(minEnergy, jumpEnergy);
            }
        }
        dp[i] = minEnergy;
    }
    return dp[n - 1];
}

int main() {
    vector<int> heights = {10, 20, 30, 10}; 
    int n = heights.size();
    int k = 2; 
    cout << "Minimum energy with K jumps: " << frogJumpKOptimal(n, k, heights) << endl;
    return 0;
}