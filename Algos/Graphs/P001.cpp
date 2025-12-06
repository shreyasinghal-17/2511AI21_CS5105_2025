#include <iostream>
#include <vector> 
#include<queue>
using namespace std;
vector<int> bfs(int node, vector<int> adj_list[],int n)
{
   vector<bool> visited(n+1, false);
   queue<int> q;
   visited[node]=1;
   q.push(node);
   vector<int>ans;
   while(!q.empty())
   {
       int temp = q.front();
       q.pop();
       ans.push_back(temp);
       for(auto it: adj_list[temp])
       {
           if(!visited[it])
           {
               visited[it]=1;
               q.push(it);
           }
       }
       
   }
   
  return ans; 
}
int main() {
    int n,m,u,v,node;
    cout<<"enter no of nodes,edges,node to start with";
    cin>>n>>m>>node;
    vector<int> adj_lis[n+1];
    vector <int>ans;
    for(int i=0;i<m;i++)
    {
        cin>>u>>v;
        adj_lis[u].push_back(v);
        adj_lis[v].push_back(u);
        
    }
    cout << "\nAdjacency List:\n";
    for (int i = 1; i <= n; i++) {
        cout << "Node " << i << ": ";
        for (int neighbor : adj_lis[i]) {
            cout << neighbor << " ";
        }
        cout << endl;
    }
    ans=bfs(node, adj_lis,n);
    cout<<"bfs is:\n";
    for(int i=0;i<ans.size();i++)
    {
        cout<<ans[i];
        
    }
    

    
    return 0;
}