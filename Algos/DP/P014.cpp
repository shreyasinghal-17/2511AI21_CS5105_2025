#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// We reuse the logic from Subset Sum (Problem 013) here.
// Optimal Approach: Space Optimization
// Time Complexity: O(N * TotalSum)
// Space Complexity: O(TotalSum)
bool canPartitionOptimal(vector<int> &arr) {
    int n = arr.size();
    int totalSum = 0;
    for(int i : arr) totalSum += i;

    // If total sum is odd, we cannot divide it into two equal integer halves
    if (totalSum % 2 != 0) return false;

    int k = totalSum / 2;
    vector<bool> prev(k + 1, 0);
    
    prev[0] = true;
    if (arr[0] <= k) prev[arr[0]] = true;
    
    for (int i = 1; i < n; i++) {
        vector<bool> cur(k + 1, 0);
        cur[0] = true;
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

// Brute Force: Recursion Wrapper
bool canPartitionBrute(int ind, int target, vector<int> &arr) {
    if(target == 0) return true;
    if(ind == 0) return (arr[0] == target);
    bool notTake = canPartitionBrute(ind - 1, target, arr);
    bool take = false;
    if(target >= arr[ind]) take = canPartitionBrute(ind - 1, target - arr[ind], arr);
    return take || notTake;
}

int main() {
    vector<int> arr = {2, 3, 3, 3, 4, 5};
    int sum = 0;
    for(int x : arr) sum += x;
    
    // Check parity for Brute force call
    if(sum % 2 != 0) cout << "Cannot Partition (Odd Sum)" << endl;
    else {
        // Calling Optimal directly for output
        if (canPartitionOptimal(arr)) cout << "Partition Possible" << endl;
        else cout << "Partition Not Possible" << endl;
    }
    return 0;
}