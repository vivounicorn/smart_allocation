# smart_allocation

allocating customers and funders using smart algorithm.

$$
\begin{align*}
&\max\quad \sum\limits_{i=1,j=1}^{n,m} x_{i,j}\cdot m_i \cdot (e(i)-pd_i\cdot lgd_i-c_j)\\
& \begin{array}{l@{\quad}r@{}l@{\quad}l}
s.t. &\sum\limits_{i=1}^{n}x_{ij}\cdot m_i&\leq (1-e^{\frac{\sum\limits_{k\in \Gamma({t\leq v_j})}^{}x_{kj}\cdot m_k}{s_j}-1})\cdot s_j, &j=1,2,\ldots,m\\
     &\frac{\sum\limits_{i=1}^{n}x_{ij}}{\sum\limits_{i=1,j=1}^{n,m}x_{ij}}&\leq \frac{d_j\cdot(\frac{p_j}{\sum\limits_{k=1}^{m}p_k})}{\sum\limits_{j=1}^{m}d_j\cdot(\frac{p_j}{\sum\limits_{k=1}^{m}p_k})},  &j=1,2,\ldots,m  \\
     &\frac{\sum\limits_{i=1}^{n}x_{ij}\cdot m_i\cdot b(i)}{\sum\limits_{i=1,j=1}^{n,m}x_{ij}\cdot m_i}&\leq td_k,  &i=1,2,\ldots,n;j=1,2,\ldots,m;k=1,2,\ldots,q \\
     &\frac{\sum\limits_{i=1}^{n}x_{ij}\cdot pscore_i}{n}&\leq dscore_j,  &i=1,2,\ldots,n;j=1,2,\ldots,m  \\
     &pscore_i,dscore_j&\geq 0&i=1,2,\ldots,n;j=1,2,\ldots,m \\
     &\frac{\sum\limits_{i=1}^{n}x_{ij}\cdot pd_i}{n}\cdot\lambda&+\frac{\alpha}{\alpha+\beta}\cdot (1-\lambda) \leq dr_j,  &i=1,2,\ldots,n;j=1,2,\ldots,m  \\
     &\lambda&=\frac{\sum\limits_{i=1}^{n}x_{ij}}{\sum\limits_{i=1}^{n}x_{ij}+\alpha+\beta}&i=1,2,\ldots,n;j=1,2,\ldots,m\\
     &\alpha,\beta&\geq 0\\
     &\sum\limits_{k=1}^{s} td_k &\leq 1&k=1,2,\ldots,q\\
     &\sum\limits_{j=1}^{m} d_j &\leq 1&j=1,2,\ldots,m \\
     &\Gamma({t\leq v_j})&\neq \emptyset,  &j=1,2,\ldots,m  \\
     &x_{ij}&\in \{0,1\}  &i=1,2,\ldots,n;j=1,2,\ldots,m \\
     &\sum\limits_{j=1}^{m}x_{ij}&=1 &i=1,2,\ldots,n;j=1,2,\ldots,m  \\
     &v_j&\geq0,  &j=1,2,\ldots,m \\
     &s_j&\geq0,  &j=1,2,\ldots,m  \\
     &m_i&\geq0,  &i=1,2,\ldots,n  \\
     &w_i&\geq0,  &i=1,2,\ldots,n  \\
     &t(i)&\geq0,  &i=1,2,\ldots,n  \\
     &d_j&\geq0,  &j=1,2,\ldots,m   \\
     &0\leq r_i&\leq1,  &i=1,2,\ldots,n  \\
     &0\leq dr_j&\leq1,  &j=1,2,\ldots,m   \\
     &0\leq p_j&\leq1,  &j=1,2,\ldots,m   \\
     &c_j&\geq0,  &j=1,2,\ldots,m   \\
     &0\leq pd_i&\leq1,  &i=1,2,\ldots,n  \\
     &0\leq lgd_i&\leq1,  &i=1,2,\ldots,n   \\
     &i&\geq0,  &i=1,2,\ldots,n  \\
     &j&\geq0,  &j=1,2,\ldots,m \\
     &k&\geq0,  &k=1,2,\ldots,q  \\
\end{array}
\end{align*}
$$
