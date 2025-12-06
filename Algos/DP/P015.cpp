#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>
#include <algorithm>

using namespace std;

// This problem relies on the tabulation table of Subset Sum.
// Optimal Approach using Subset Sum Logic
// Time Complexity: O(N * TotalSum)
// Space Complexity: O(TotalSum)
int minSubsetSumDifference(vector<int> &arr) {
    int n = arr.size();
    int totalSum = 0;
    for(int i : arr) totalSum += i;

    int k = totalSum;
    vector<bool> prev(k + 1, 0);

    // Initialization (Subset Sum Logic)
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

    // The 'prev' array now contains true for all subset sums possible using elements 0 to n-1.
    // We iterate from 0 to totalSum/2 to find the largest possible sum s1.
    int minDiff = 1e9;
    for (int s1 = 0; s1 <= totalSum / 2; s1++) {
        if (prev[s1] == true) {
            int s2 = totalSum - s1;
            minDiff = min(minDiff, abs(s2 - s1));
        }
    }
    return minDiff;
}

// Brute Force: Recursive Summation
int solveBrute(int ind, int currentSum, int totalSum, vector<int> &arr) {
    if (ind == 0) {
        int s2 = totalSum - currentSum;
        // Case: Pick 0th element
        int diff1 = abs((currentSum + arr[0]) - (totalSum - (currentSum + arr[0])));
        // Case: Don't pick 0th element
        int diff2 = abs(currentSum - s2);
        return min(diff1, diff2);
    }
    
    int pick = solveBrute(ind - 1, currentSum + arr[ind], totalSum, arr);
    int notPick = solveBrute(ind - 1, currentSum, totalSum, arr);
    return min(pick, notPick);
}


int main() {
    vector<int> arr = {8, 6, 5}; // Example from doc [cite: 462, 463]
    cout << "Minimum Absolute Difference: " << minSubsetSumDifference(arr) << endl;
    return 0;
}