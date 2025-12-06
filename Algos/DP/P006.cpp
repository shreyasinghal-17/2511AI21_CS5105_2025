#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Brute Force: Recursion
// Time Complexity: O(3^N)
// Space Complexity: O(N)
int ninjaTrainingBrute(int day, int lastTask, vector<vector<int>>& points) {
    if (day == 0) {
        int maxi = 0;
        for (int task = 0; task < 3; task++) {
            if (task != lastTask) {
                maxi = max(maxi, points[0][task]);
            }
        }
        return maxi;
    }

    int maxi = 0;
    for (int task = 0; task < 3; task++) {
        if (task != lastTask) {
            int point = points[day][task] + ninjaTrainingBrute(day - 1, task, points);
            maxi = max(maxi, point);
        }
    }
    return maxi;
}

// Optimal Approach: Space Optimization
// Time Complexity: O(N*4*3)
// Space Complexity: O(4) ~ O(1)
int ninjaTrainingOptimal(int n, vector<vector<int>>& points) {
    vector<int> prev(4, 0);

    // Base Case: Day 0
    prev[0] = max(points[0][1], points[0][2]);
    prev[1] = max(points[0][0], points[0][2]);
    prev[2] = max(points[0][0], points[0][1]);
    prev[3] = max(points[0][0], max(points[0][1], points[0][2]));

    for (int day = 1; day < n; day++) {
        vector<int> temp(4, 0);
        for (int last = 0; last < 4; last++) {
            temp[last] = 0;
            for (int task = 0; task < 3; task++) {
                if (task != last) {
                    temp[last] = max(temp[last], points[day][task] + prev[task]);
                }
            }
        }
        prev = temp;
    }
    return prev[3];
}

int main() {
    vector<vector<int>> points = {{10, 40, 70}, {20, 50, 80}, {30, 60, 90}};
    int n = points.size();
    cout << "Maximum merit points: " << ninjaTrainingOptimal(n, points) << endl;
    return 0;
}