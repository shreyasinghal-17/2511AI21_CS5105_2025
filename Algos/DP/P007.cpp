#include <iostream>
#include <vector>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(2^(M+N))
// Space Complexity: O(path length) ~ O(M+N)
int uniquePathsBrute(int i, int j) {
    if (i == 0 && j == 0) return 1;
    if (i < 0 || j < 0) return 0;
    
    int up = uniquePathsBrute(i - 1, j);
    int left = uniquePathsBrute(i, j - 1);
    
    return up + left;
}

// Optimal Approach: Combinatorics (Math) is strictly O(M-1) or O(N-1) time,
// but DP Space Optimization is standard interview expectation.
// Time Complexity: O(M*N)
// Space Complexity: O(N) (Using 1D array)
int uniquePathsOptimal(int m, int n) {
    vector<int> prev(n, 0);

    for (int i = 0; i < m; i++) {
        vector<int> temp(n, 0);
        for (int j = 0; j < n; j++) {
            if (i == 0 && j == 0) {
                temp[j] = 1;
                continue;
            }
            int up = 0;
            int left = 0;
            if (i > 0) up = prev[j];
            if (j > 0) left = temp[j - 1];
            
            temp[j] = up + left;
        }
        prev = temp;
    }
    return prev[n - 1];
}

int main() {
    int m = 3, n = 2;
    cout << "Unique Paths: " << uniquePathsOptimal(m, n) << endl;
    return 0;
}