1.	Why do we need dynamic programming? What's the difference of dynamic programming and previous talked search problme?

	+	动态规划对于求解重叠子问题十分有效，相比之前的搜索方法，动态规划将问题分解成重叠的子问题，存储子问题的解，从而大大减少搜索空间

2.	Why do we still need dynamic programming? Why not we train a machine learning to fit a function which could get the right answer based on inputs?

	+	有时候可能训练数据是缺乏的，这种情况下缺少数据训练，无法用机器学习的方式拟合
	+  某些场景下使用机器学习训练可能是没必要的，训练的修改迭代耗时可能远远超过动态规划
	+  动态规划是确切解，机器学习的不是

3.	Can you catch up at least 3 problems which could solved by Dynamic Programming?
	
	+	一维切割问题、二维切割问题
	+  矩形覆盖问题
	+  路线规划问题

4.	Can you catch up at least 3 problems wich could sloved by Edit Distance?
	
	+	拼写检查
	+	diff、patch 命令等实现
	+  生物领域 DNA 分析 


5.	Please summarize the three main features of Dynamic Programming, and make a concise explain for each feature.
	
	1.	分析子问题重复（动态规划的核心在于将一个问题分解成很多子问题，子问题存在大量的重叠，保重程序运行的效率）
	2. 子问题存储（程序效率提高的根本原因是，重复的子问题的解保存下来，下一次求解同一个子问题时，直接查询就可得到结果）
	3. solution 解析（解析问题处理过程，得到最终的处理解）

6.	What's the disadvantages of Dynamic Programming? (You may need search by yourself in Internet)

	+  缺乏统一通用的算法模型，每一个问题都需要具体分析
	+  问题拆解及结果存储对内存耗费较多
