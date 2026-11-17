import sys
B=list("rnbqkbnr"+"pppppppp"+"."*32+"PPPPPPPP"+"RNBQKBNR")
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0,'.':0}
N=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
K=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
G={'n':N,'b':[(-1,-1),(-1,1),(1,-1),(1,1)],'r':[(0,1),(0,-1),(1,0),(-1,0)],'q':K,'k':K}
def pc(i):return B[i]
def side(p):return p.isupper()
def idx(s):return (8-int(s[1]))*8+ord(s[0])-97
def nm(i):return "abcdefgh"[i%8]+str(8-i//8)
def gen(w):
    out=[]
    for i,p in enumerate(B):
        if p=='.' or side(p)!=w:continue
        t=p.lower();r,c=divmod(i,8);d=-1 if w else 1
        if t=='p':
            j=i+8*d
            if 0<=j<64 and B[j]=='.':
                out.append((i,j,'q' if r+d in(0,7) else ''))
                j2=i+16*d
                if r in(1,6)and B[j2]=='.':out.append((i,j2,''))
            for dc in(-1,1):
                c2=c+dc;r2=r+d
                if 0<=c2<8 and 0<=r2<8:
                    j=r2*8+c2
                    if B[j]!='.' and side(B[j])!=w:out.append((i,j,'q' if r2 in(0,7) else ''))
        elif t=='n' or t=='k':
            for dr,dc in G[t]:
                r2,c2=r+dr,c+dc
                if 0<=r2<8 and 0<=c2<8:
                    j=r2*8+c2
                    if B[j]=='.' or side(B[j])!=w:out.append((i,j,''))
        else:
            for dr,dc in G[t]:
                r2,c2=r+dr,c+dc
                while 0<=r2<8 and 0<=c2<8:
                    j=r2*8+c2
                    if B[j]!='.':
                        if side(B[j])!=w:out.append((i,j,''))
                        break
                    out.append((i,j,''))
                    r2+=dr;c2+=dc
    return out
def put(b,i,j,pr=''):
    b[j]=b[i].lower() if pr else b[i];b[i]='.'
    if pr:b[j]=pr.upper() if side(b[j]) else pr
def king(b,w):
    t='K' if w else 'k'
    return b.index(t)
def att(b,sq,w):
    for i,p in enumerate(b):
        if p=='.' or side(p)!=w:continue
        r,c=divmod(i,8);t=p.lower()
        if t=='p':
            d=-1 if w else 1
            if sq//8==r+d and abs(sq%8-c)==1:return 1
        elif t in G:
            for dr,dc in G[t]:
                r2,c2=r+dr,c+dc
                while 0<=r2<8 and 0<=c2<8:
                    if r2*8+c2==sq:return 1
                    if b[r2*8+c2]!='.':break
                    r2+=dr;c2+=dc
                    if t in'nk':break
    return 0
def legal(w):
    out=[]
    for m in gen(w):
        b=B[:]
        put(b,m[0],m[1],m[2])
        e=-1
        if att(b,king(b,w),not w):continue
        out.append(m)
    return out
def perft(w,d):
    if d==0:return 1
    n=0
    for m in legal(w):
        global B
        old=B;B=B[:];put(B,m[0],m[1],m[2])
        n+=perft(not w,d-1)
        B=old
    return n
def ev():
    s=0
    for p in B:
        if p=='.':continue
        v=V[p.lower()]
        s+= v if side(p) else -v
    return s
def search(w,d,a,b):
    if d==0:return ev() if w else -ev(),None
    best=None;sc=-99999 if w else 99999
    for m in legal(w):
        global B
        old=B;B=B[:];put(B,m[0],m[1],m[2])
        v,_=search(not w,d-1,a,b)
        B=old
        if w and v>sc:sc,best=v,m
        if not w and v<sc:sc,best=v,m
    return sc,best
def mv(s):
    a=idx(s[:2]);c=idx(s[2:4]);pr=s[4:5] if len(s)>4 else ''
    put(B,a,c,pr)
w=True
for line in sys.stdin:
    t=line.split()
    if not t:continue
    if t[0]=='uci':print('id name tiny4k');print('id author gn-buffy-swarm');print('uciok')
    elif t[0]=='isready':print('readyok')
    elif t[0]=='position':
        B=list("rnbqkbnr"+"pppppppp"+"."*32+"PPPPPPPP"+"RNBQKBNR");w=True
        if 'moves' in t:
            for s in t[t.index('moves')+1:]:mv(s);w=not w
    elif t[0]=='go' and 'perft' in t:
        print('nodes',perft(w,int(t[t.index('perft')+1])))
    elif t[0]=='go':
        d=4
        if 'depth' in t:d=int(t[t.index('depth')+1])
        sc,m=search(w,d,-99999,99999)
        print('info depth',d,'score cp',sc)
        print('bestmove',nm(m[0])+nm(m[1]) if m else '0000')
    elif t[0]=='quit':break
    sys.stdout.flush()
