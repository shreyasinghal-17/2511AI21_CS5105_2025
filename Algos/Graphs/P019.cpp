#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    vector<vector<string>> findLadders(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> dict(wordList.begin(), wordList.end());
        vector<vector<string>> ans;
        if (!dict.count(endWord)) return ans;

        // Step 1: BFS to build adjacency map
        unordered_map<string, vector<string>> adj;
        unordered_map<string, int> level;
        queue<string> q;

        q.push(beginWord);
        level[beginWord] = 0;

        while (!q.empty()) {
            string word = q.front(); q.pop();
            int currLevel = level[word];

            string temp = word;
            for (int i = 0; i < word.size(); i++) {
                char orig = temp[i];
                for (char c = 'a'; c <= 'z'; c++) {
                    temp[i] = c;
                    if (dict.count(temp)) {
                        if (!level.count(temp)) {
                            level[temp] = currLevel + 1;
                            q.push(temp);
                        }
                        if (level[temp] == currLevel + 1) {
                            adj[word].push_back(temp);
                        }
                    }
                }
                temp[i] = orig;
            }
        }

        // Step 2: DFS backtracking to find all paths
        vector<string> path;
        function<void(string)> dfs = [&](string word) {
            path.push_back(word);
            if (word == endWord) {
                ans.push_back(path);
            } else {
                for (auto next : adj[word]) {
                    dfs(next);
                }
            }
            path.pop_back();
        };

        dfs(beginWord);
        return ans;
    }
};

// Example usage
int main() {
    string startWord, targetWord;
    int n;
    cin >> startWord >> targetWord >> n;

    vector<string> wordList(n);
    for (int i = 0; i < n; i++) cin >> wordList[i];

    Solution sol;
    vector<vector<string>> res = sol.findLadders(startWord, targetWord, wordList);

    for (auto& seq : res) {
        for (auto& word : seq) cout << word << " ";
        cout << "\n";
    }
    return 0;
}
