#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Brute Force Approach: Recursion
// Time Complexity: O(2^N)
// Space Complexity: O(N)
int maxNonAdjacentBrute(int index, vector<int>& arr) {
    if (index == 0) return arr[0];
    if (index < 0) return 0;
    
    int pick = arr[index] + maxNonAdjacentBrute(index - 2, arr);
    int notPick = 0 + maxNonAdjacentBrute(index - 1, arr);
    
    return max(pick, notPick);
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N)
// Space Complexity: O(1)
int maxNonAdjacentOptimal(int n, vector<int>& arr) {
    int prev = arr[0];
    int prev2 = 0;

    for (int i = 1; i < n; i++) {
        int pick = arr[i];
        if (i > 1) pick += prev2;
        
        int notPick = 0 + prev;
        
        int current = max(pick, notPick);
        prev2 = prev;
        prev = current;
    }
    return prev;
}

int main() {
    vector<int> arr = {2, 1, 4, 9}; 
    int n = arr.size();
    cout << "Maximum sum of non-adjacent elements: " << maxNonAdjacentOptimal(n, arr) << endl;
    return 0;
}