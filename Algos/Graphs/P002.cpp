#include <iostream>
#include <vector> 
#include<stack>
using namespace std;
void dfs(int node,vector<int> adj_list[],int n,vector<bool> &visited)
{
 visited[node]=true;
 for(auto it:adj_list[node])
 {
     if(!visited[it])
     dfs(it,adj_list,n,visited);
 }
}
int provinces(int node, vector<int> adj_list[],int n)
{
   vector<bool> visited(n+1, false);
   int ans=0;
   for(int i=1;i<=n;i++)
   {
       if(!visited[i])
       {
           ans++;
           dfs(i,adj_list,n,visited);
       }
   }
  return ans;  
}
   
int main() {
    int n,m,u,v,node;
    cout<<"enter no of nodes,edges,node to start with";
    cin>>n>>m>>node;
    vector<int> adj_lis[n+1];
    vector<bool> visited(n+1, false);
    int ans=0;
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
    ans=provinces(node, adj_lis,n);
    cout<<"no of provinces are :\n";
    cout<<ans;
    

    
    return 0;
}