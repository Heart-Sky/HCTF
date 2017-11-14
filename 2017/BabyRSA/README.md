### BabyRSA

先看下题目的逻辑
``` py
M = r * bytes_to_long('hctf{' + sha256(open('./flag').read()).hexdigest() + '}')
S = pow(M, d, n)
```
程序接收 r，然后同 flag 相乘后计算出它的数字签名
先说下本来的思路，flag 为 m，单纯 flag 的签名为 S，返回的签名为 S',如果我们构造 `r=R^e`
因为
\begin{matrix} 
M = R^e*m \pmod {n}
\end{matrix}
所以

\begin{matrix} 
m = M / R^e = M^{ed}/R^e = S'^e/R^e = (S'/R)^e \pmod {n}
\end{matrix} 
e 的值未知，通过爆破 e 的值遍历提交 R^e，再根据上式得出 flag

但是题目忘记对 r 进行限制，导致也可以通过传入 `r=2` 来做出
\begin{matrix} 
m = M / 2 = M^{ed}/2 = S'^e/2 \pmod {n}
\end{matrix}
因为 `2m < n`，所以直接对 S'^e 除以 2 就是 m

另外分享下 Blue-Whale 队师傅的解法
\begin{matrix} 
r1*r2 \equiv 1 \pmod n \\
(r1*m)^{d}*(r2*m)^{d} = (r1*r2*m*m)^{de} = m^2 \pmod n
\end{matrix} 
然后对 m^2 开方就是 flag 了
