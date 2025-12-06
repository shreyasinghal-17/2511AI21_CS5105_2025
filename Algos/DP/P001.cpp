#include <iostream>
#include <vector>

using namespace std;

// Brute Force Approach: Recursion
// Time Complexity: O(2^N)
// Space Complexity: O(N) (recursion stack)
int climbStairsBrute(int n) {
    if (n == 0 || n == 1) return 1;
    return climbStairsBrute(n - 1) + climbStairsBrute(n - 2);
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N)
// Space Complexity: O(1)
int climbStairsOptimal(int n) {
    if (n == 0 || n == 1) return 1;

    int prev2 = 1; // Represents ways(i-2)
    int prev = 1;  // Represents ways(i-1)
    
    for (int i = 2; i <= n; i++) {
        int current = prev + prev2;
        prev2 = prev;
        prev = current;
    }
    return prev;
}

int main() {
    int n = 3; 
    cout << "Ways to reach stair " << n << ": " << climbStairsOptimal(n) << endl;
    return 0;
}