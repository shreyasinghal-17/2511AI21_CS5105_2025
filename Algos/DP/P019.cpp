#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Brute Force: Recursion
// Time Complexity: Exponential
bool isMatchBrute(int i, int j, string &s1, string &s2) {
    // Base Cases
    if (i < 0 && j < 0) return true;
    if (i < 0 && j >= 0) return false; // S1 exhausted, S2 remains
    if (j < 0 && i >= 0) {
        // S2 exhausted, S1 must be all '*' to match
        for (int k = 0; k <= i; k++) {
            if (s1[k] != '*') return false;
        }
        return true;
    }

    if (s1[i] == s2[j] || s1[i] == '?') {
        return isMatchBrute(i - 1, j - 1, s1, s2);
    }
    if (s1[i] == '*') {
        // Two choices: match '*' with nothing (i-1, j) OR match '*' with one char (i, j-1)
        return isMatchBrute(i - 1, j, s1, s2) || isMatchBrute(i, j - 1, s1, s2);
    }
    return false;
}

// Optimal Approach: Tabulation (Space Optimized)
// Time Complexity: O(N*M)
// Space Complexity: O(M)
bool isMatchOptimal(string s1, string s2) {
    int n = s1.size();
    int m = s2.size();
    vector<bool> prev(m + 1, false);
    vector<bool> cur(m + 1, false);

    // Base Case 1: i=0, j=0 (both empty) -> True
    prev[0] = true;

    // Base Case 2: i=0 (S1 empty), j>0 (S2 not empty) -> False (Initialized to false)
    
    for (int i = 1; i <= n; i++) {
        // Base Case 3: j=0 (S2 empty), S1 must be all '*'
        bool flag = true;
        for (int k = 1; k <= i; k++) {
            if (s1[k - 1] != '*') {
                flag = false;
                break;
            }
        }
        cur[0] = flag;

        for (int j = 1; j <= m; j++) {
            if (s1[i - 1] == s2[j - 1] || s1[i - 1] == '?') {
                cur[j] = prev[j - 1];
            } else if (s1[i - 1] == '*') {
                cur[j] = prev[j] || cur[j - 1];
            } else {
                cur[j] = false;
            }
        }
        prev = cur;
    }
    return prev[m];
}

int main() {
    string s1 = "ab*cd";
    string s2 = "abdefcd";
    
    // Note: The logic usually assumes 1-based indexing for DP table, 
    // so input strings map to i-1 and j-1.
    if (isMatchOptimal(s1, s2)) cout << "Strings Match" << endl;
    else cout << "Strings Do Not Match" << endl;
    return 0;
}