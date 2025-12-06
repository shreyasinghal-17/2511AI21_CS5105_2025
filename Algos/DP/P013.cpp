#include <iostream>
#include <vector>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(2^N)
// Space Complexity: O(N)
bool subsetSumBrute(int ind, int target, vector<int> &arr) {
    if (target == 0) return true;
    if (ind == 0) return (arr[0] == target);
    
    bool notTake = subsetSumBrute(ind - 1, target, arr);
    bool take = false;
    if (target >= arr[ind])
        take = subsetSumBrute(ind - 1, target - arr[ind], arr);
        
    return take || notTake;
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N * K)
// Space Complexity: O(K)
bool subsetSumOptimal(int n, int k, vector<int> &arr) {
    vector<bool> prev(k + 1, 0);
    
    // Base Case: Target 0 is always true
    prev[0] = true;
    
    // Base Case: Index 0 can form target if arr[0] == target
    if (arr[0] <= k) prev[arr[0]] = true;
    
    for (int i = 1; i < n; i++) {
        vector<bool> cur(k + 1, 0);
        cur[0] = true; // Target 0 is always possible
        for (int target = 1; target <= k; target++) {
            bool notTake = prev[target];
            bool take = false;
            if (target >= arr[i]) take = prev[target - arr[i]];
            cur[target] = take || notTake;
        }
        prev = cur;
    }
    return prev[k];
}

int main() {
    vector<int> arr = {1, 2, 3, 4};
    int k = 4;
    if (subsetSumOptimal(arr.size(), k, arr)) cout << "Subset with sum " << k << " exists." << endl;
    else cout << "Subset does not exist." << endl;
    return 0;
}