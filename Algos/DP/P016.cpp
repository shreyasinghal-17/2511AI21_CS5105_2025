#include <iostream>
#include <vector>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(2^N)
// Space Complexity: O(N)
int countSubsetsBrute(int ind, int target, vector<int>& arr) {
    if (target == 0) return 1;
    if (ind == 0) return (arr[0] == target) ? 1 : 0;

    int notPick = countSubsetsBrute(ind - 1, target, arr);
    int pick = 0;
    if (arr[ind] <= target) 
        pick = countSubsetsBrute(ind - 1, target - arr[ind], arr);

    return pick + notPick;
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N * K)
// Space Complexity: O(K)
int countSubsetsOptimal(vector<int>& arr, int k) {
    int n = arr.size();
    vector<int> prev(k + 1, 0);

    // Base Case: target 0
    prev[0] = 1;
    
    // Base Case: index 0
    if (arr[0] <= k) prev[arr[0]] = 1;

    for (int i = 1; i < n; i++) {
        vector<int> cur(k + 1, 0);
        cur[0] = 1; // Target 0 is always possible (empty subset)
        
        for (int target = 1; target <= k; target++) {
            int notPick = prev[target];
            int pick = 0;
            if (arr[i] <= target) pick = prev[target - arr[i]];
            
            cur[target] = pick + notPick;
        }
        prev = cur;
    }
    return prev[k];
}

int main() {
    vector<int> arr = {1, 2, 2, 3};
    int k = 3;
    cout << "Count of subsets: " << countSubsetsOptimal(arr, k) << endl;
    return 0;
}