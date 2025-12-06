#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    int wordLadderLength(string startWord, string targetWord, vector<string>& wordList) {
        unordered_set<string> wordSet(wordList.begin(), wordList.end());
        if (!wordSet.count(targetWord)) return 0; // targetWord must be in the list

        queue<pair<string,int>> q;  // {word, steps}
        q.push({startWord, 1});

        while (!q.empty()) {
            auto [word, steps] = q.front(); 
            q.pop();

            if (word == targetWord) return steps;

            for (int i = 0; i < word.size(); i++) {
                char orig = word[i];
                for (char c = 'a'; c <= 'z'; c++) {
                    word[i] = c;
                    if (wordSet.count(word)) {
                        q.push({word, steps + 1});
                        wordSet.erase(word); // mark as visited
                    }
                }
                word[i] = orig; // restore
            }
        }
        return 0; // no transformation sequence found
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string startWord, targetWord;
    int n;
    cin >> startWord >> targetWord >> n;

    vector<string> wordList(n);
    for (int i = 0; i < n; i++) cin >> wordList[i];

    Solution sol;
    cout << sol.wordLadderLength(startWord, targetWord, wordList) << "\n";
    return 0;
}
