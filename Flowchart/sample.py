import queue

N=105
M=5005
INF=2**30

class edge:
	def __init__(self,to,nxt,w):
		self.to=to
		self.nxt=nxt
		self.w=w

a=[]
head=[-1 for i in range(N)]
cnt=0
cur=[-1 for i in range(N)]
dep=[0 for i in range(N)]

def link(u,v,w):
	global a,head,cnt
	a.append(edge(v,head[u],w))
	head[u]=cnt
	cnt+=1
	a.append(edge(u,head[v],0))
	head[v]=cnt
	cnt+=1

def bfs():
	global dep
	q=queue.Queue()
	for i in range(n):
		dep[i]=0
	dep[s]=1
	q.put(s)
	while(not q.empty()):
		u=q.get()
		e=head[u]
		while(e!=-1):
			if(a[e].w!=0 and dep[a[e].to]==0):
				dep[a[e].to]=dep[u]+1
				q.put(a[e].to)
			e=a[e].nxt
	return dep[t]!=0

def dfs(u,f):
	global a
	if(u==t):
		return f;
	res=0
	e=cur[u]
	while(e!=-1):
		if(a[e].w!=0 and dep[a[e].to]==dep[u]+1):
			d=dfs(a[e].to,min(a[e].w,f))
			a[e].w-=d
			a[e^1].w+=d
			f-=d
			res+=d
			if(f==0):
				break
		cur[u]=e=a[e].nxt
	if(res==0):
		dep[u]=0
	return res

n,m,s,t=map(int,input().split())
s-=1
t-=1
for i in range(m):
	x,y,z=map(int,input().split())
	x-=1
	y-=1
	link(x,y,z)
ans=0
while(bfs()):
	for i in range(n):
		cur[i]=head[i]
	ans+=dfs(s,INF)
print(ans)