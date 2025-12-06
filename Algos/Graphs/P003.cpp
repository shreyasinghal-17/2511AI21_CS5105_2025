#include <iostream>
#include <vector> 
#include<stack>
#include<bits/stdc++.h>
using namespace std;
int rottenoranges(vector<vector<int>>& mat)
{
 if(mat.size()==0)
 {
     return 0;
     
 }
 int r=mat.size();
 int c=mat[0].size();
 queue<pair<pair<int,int>,int>> q;
 int visited[r][c];
 int cntfresh=0;
 
 for(int i=0;i<r;i++)
 {
     for(int j=0;j<c;j++)
     {
         if(mat[i][j]==2)
         {
             q.push({{i,j},0});
             visited[i][j]=2;
         }
        else
        {
            visited[i][j]=0;
            
        }
        if(mat[i][j]==1)
        cntfresh ++;
        
     }
 }
 int tm=0;
 int drow[]={-1,1,0,0};
 int dcol[]={0,0,1,-1};
 int cnt=0;
 while(!q.empty())
 {
     int n=q.front().first.first;
     int m=q.front().first.second;
     int t = q.front().second;
     tm=max(tm,t);
     q.pop();
     for(int i=0;i<4;i++)
     {
         int nrow=n+drow[i];
         int ncol=m+dcol[i];
         if(nrow>=0 && nrow < r &&ncol >=0 && ncol< c && visited[nrow][ncol]!=2 && mat[nrow][ncol] ==1)
         {
             q.push({{nrow,ncol},t+1});
             visited[nrow][ncol]=2;
             cnt++;
             
         }
     }
     
 }
 if(cnt!=cntfresh) return -1;
 return tm;
}
int main() {
    int n,m,u,v,node;
    cout<<"enter no of nodes,edges,node to start with";
    cin>>n>>m;
    vector<vector<int>> mat(n, vector<int>(m));
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            cin>>mat[i][j];
        }
    }
int count = rottenoranges(mat);
cout<<"no of minutes req:"<<count;
    
    return 0;
}