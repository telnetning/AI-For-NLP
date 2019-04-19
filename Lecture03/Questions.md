### Q2
1. Why we need machine learning methods instead of creating a complicated formula?

	+	机器学习相对不断构建模板的方式，实现上简单高效地多。

2. Wha't's the disadvantages of the 1st Random Choosen methods in our course?

	+	随机取参数的方法，最大的问题是收敛太慢。

3. Is the 2nd method supervised direction better than 1st one? What's the disadvantages of the 2nd supversied directin method?

	+	监督学习的方式比随机取参的方法好，收敛速度快了很多。
	+  监督学习的缺点在于参数过多时，需要维护的方向空间以指数级方式增加。
	
4. Why do we use Derivative / Gredient to fit a target function?

	+	可以保证 loss 是持续下降的，更加准确，并且更加符合机器学习框架的现状，比起监督学习容易实现。

5. In the words 'Gredient Descent', what's the Gredient and what's the Descent?

	+	梯度是指 loss 随着参数的变化的变化趋势，下降指的是 loss 减小，即拟合更准确。
	+ 	梯度下降是指通过梯度计算，变化参数，保证梯度持续下降，loss 持续减小。

6. What's the advantages of the 3rd gradient descent method compared to the previous methods?

	+	loss 下降快，下降方向更加准确。
	+ 	便于实现，尤其是在当前的计算框架下。

7. Using the simple words to describe: What's the machine leanring.

	+	通过一定的算法，从已知的大量数据中自主学习拟合函数，拟合得到的函数可以用来预测新的数据集。

