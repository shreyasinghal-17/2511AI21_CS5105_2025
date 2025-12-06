#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Helper function from Problem 004 (solving linear non-adjacent sum)
long long solveMaxNonAdjacent(vector<int>& arr) {
    int n = arr.size();
    long long prev = arr[0];
    long long prev2 = 0;

    for (int i = 1; i < n; i++) {
        long long pick = arr[i];
        if (i > 1) pick += prev2;
        long long notPick = 0 + prev;
        long long current = max(pick, notPick);
        prev2 = prev;
        prev = current;
    }
    return prev;
}

// Optimal Approach: Breaking Circle into Two Linear Problems
// Time Complexity: O(N)
// Space Complexity: O(1) (excluding input vector construction)
long long houseRobberCircular(vector<int>& money) {
    int n = money.size();
    if (n == 1) return money[0];

    vector<int> temp1, temp2;
    for (int i = 0; i < n; i++) {
        if (i != 0) temp1.push_back(money[i]); // Case 1: Exclude first element
        if (i != n - 1) temp2.push_back(money[i]); // Case 2: Exclude last element
    }

    return max(solveMaxNonAdjacent(temp1), solveMaxNonAdjacent(temp2));
}

int main() {
    vector<int> money = {2, 3, 2}; 
    cout << "Maximum money robbed: " << houseRobberCircular(money) << endl;
    return 0;
}