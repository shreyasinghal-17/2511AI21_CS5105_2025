#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Modified Optimal Approach to handle Zeros
// Time Complexity: O(N * Target)
// Space Complexity: O(Target)
int countPartitionsOptimal(int n, int d, vector<int>& arr) {
    int totalSum = 0;
    for(int x : arr) totalSum += x;
    
    // If (TotalSum + D) is odd or negative, we can't split it evenly
    if (totalSum - d < 0 || (totalSum - d) % 2 != 0) return 0;
    
    int target = (totalSum - d) / 2;
    vector<int> prev(target + 1, 0);

    // Base case logic for index 0 handling zeros
    if (arr[0] == 0) prev[0] = 2; // Two ways: pick or not pick 0
    else prev[0] = 1; // One way: not pick
    
    // If arr[0] is not 0 and <= target, set that index to 1
    if (arr[0] != 0 && arr[0] <= target) prev[arr[0]] = 1;

    for (int i = 1; i < n; i++) {
        vector<int> cur(target + 1, 0);
        for (int sum = 0; sum <= target; sum++) {
            int notPick = prev[sum];
            int pick = 0;
            if (arr[i] <= sum) pick = prev[sum - arr[i]];
            
            cur[sum] = (pick + notPick); 
            // Modulo arithmetic % 1e9+7 usually required here for large inputs
        }
        prev = cur;
    }
    return prev[target];
}

int main() {
    vector<int> arr = {5, 2, 6, 4};
    int d = 3;
    cout << "Count of Partitions: " << countPartitionsOptimal(arr.size(), d, arr) << endl;
    return 0;
}