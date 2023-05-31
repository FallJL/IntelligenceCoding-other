import queue

N=105
M=5005
INF=2**30

class edge:  #fc:startStop CLASS [edge]
	def __init__(self,to,nxt,w):  #fc:startStop FUNC [__init__]: is used to describe test cases and might in future become helpful as an experimental tutorial as well .
		self.to=to
		self.nxt=nxt
		self.w=w  #fc:startStop CLASS [edge] END  #fc:startStop FUNC [__init__]: END

a=[]
head=[-1 for i in range(N)]
cnt=0
cur=[-1 for i in range(N)]
dep=[0 for i in range(N)]

def link(u,v,w):  #fc:startStop FUNC [link]: is used to describe test cases and might in future become helpful as an experimental tutorial as well .
	global a,head,cnt
	a.append(edge(v,head[u],w))
	head[u]=cnt
	cnt+=1
	a.append(edge(u,head[v],0))
	head[v]=cnt
	cnt+=1  #fc:startStop FUNC [link]: END

def bfs():  #fc:startStop FUNC [bfs]: enable or disable layer .
	global dep
	q=queue.Queue()
	for i in range(n): #fc:forLoop LOOP 
		dep[i]=0  #fc:end LOOP END
	dep[s]=1
	q.put(s)
	while(not q.empty()): #fc:forLoop LOOP 
		u=q.get()
		e=head[u]
		while(e!=-1): #fc:forLoop LOOP 
			if(a[e].w!=0 and dep[a[e].to]==0):  #fc:ifBranch IF 
				dep[a[e].to]=dep[u]+1
				q.put(a[e].to)  #fc:end IF END
			e=a[e].nxt  #fc:end LOOP END  #fc:end LOOP END
	return dep[t]!=0  #fc:startStop FUNC [bfs]: END

def dfs(u,f):  #fc:startStop FUNC [dfs]: disables aslr .
	global a
	if(u==t):  #fc:ifBranch IF 
		return f;  #fc:end IF END
	res=0
	e=cur[u]
	while(e!=-1): #fc:forLoop LOOP 
		if(a[e].w!=0 and dep[a[e].to]==dep[u]+1):  #fc:ifBranch IF 
			d=dfs(a[e].to,min(a[e].w,f))
			a[e].w-=d
			a[e^1].w+=d
			f-=d
			res+=d
			if(f==0):  #fc:ifBranch IF 
				break  #fc:end IF END  #fc:end IF END
		cur[u]=e=a[e].nxt  #fc:end LOOP END
	if(res==0):  #fc:ifBranch IF 
		dep[u]=0  #fc:end IF END
	return res  #fc:startStop FUNC [dfs]: END

n,m,s,t=map(int,input().split())
s-=1
t-=1
for i in range(m): #fc:forLoop LOOP 
	x,y,z=map(int,input().split())
	x-=1
	y-=1
	link(x,y,z)  #fc:end LOOP END
ans=0
while(bfs()): #fc:forLoop LOOP 
	for i in range(n): #fc:forLoop LOOP 
		cur[i]=head[i]  #fc:end LOOP END
	ans+=dfs(s,INF)  #fc:end LOOP END
print(ans)