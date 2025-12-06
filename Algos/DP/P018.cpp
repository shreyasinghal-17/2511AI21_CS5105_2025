#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Using the same Space Optimization logic as Problem 017
int findTargetSumWays(vector<int>& arr, int target) {
    int n = arr.size();
    int totalSum = 0;
    for(int x : arr) totalSum += x;

    // Check if partition is possible
    if (totalSum - target < 0 || (totalSum - target) % 2 != 0) return 0;
    
    int s2 = (totalSum - target) / 2;
    
    vector<int> prev(s2 + 1, 0);

    // Handling zeros correctly at index 0
    if (arr[0] == 0) prev[0] = 2;
    else prev[0] = 1;
    
    if (arr[0] != 0 && arr[0] <= s2) prev[arr[0]] = 1;

    for (int i = 1; i < n; i++) {
        vector<int> cur(s2 + 1, 0);
        for (int sum = 0; sum <= s2; sum++) {
            int notPick = prev[sum];
            int pick = 0;
            if (arr[i] <= sum) pick = prev[sum - arr[i]];
            
            cur[sum] = pick + notPick;
        }
        prev = cur;
    }
    return prev[s2];
}

int main() {
    vector<int> arr = {1, 1, 1, 1, 1};
    int target = 3;
    cout << "Target Sum Ways: " << findTargetSumWays(arr, target) << endl;
    return 0;
}