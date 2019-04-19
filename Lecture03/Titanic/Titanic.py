import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np

content = pd.read_csv("./train.csv")
content = content.dropna() # 过滤缺失数据
ages = content["Age"]
fares = content["Fare"]
plt.scatter(ages, fares) # 散点图
plt.show()

age_with_fares = content[
    (content['Age'] > 22) & (content['Fare'] < 400) & (content['Fare'] > 130)]

# sub_fare 和 sub_age 是 pandas 中的 Series 类型
sub_fare = age_with_fares['Fare']
sub_age = age_with_fares['Age']


# plt.scatter(sub_age, sub_fare)
# plt.show()

# 使用 y = kx + b 拟合，求 k b

def func(age, k, b): return age * k + b

# 定义损失函数
def loss(y, y_hat):
    '''
    :param y: 实际的值
    :param y_hat: k、b计算得到的值
    :return:
    '''
    return np.mean(abs(y - y_hat))

loop_times = 1000


#####################随机变化############################
def random_solution(ages, fares):
    '''
    random 方法，随机选取k, b迭代，始终保持最好的k, b
    :param ages:
    :param fares:
    :return:
    '''
    min_error_rate = float('inf')
    k_best = None
    b_best = None
    loop = 0
    while loop < loop_times:
        k_hat = random.randint(-10, 10)
        b_hat = random.randint(-10, 10)

        loop = loop + 1
        estimated_fares = func(sub_age, k_hat, b_hat)
        error_rate = loss(y=sub_fare, y_hat=estimated_fares)
        if error_rate < min_error_rate:
            print(error_rate)
            min_error_rate = error_rate
            k_best, b_best = k_hat, b_hat
            print("{} times:f(age)={} * age + {}, with rate error {}".format(loop,k_hat,
                                                                     b_hat, min_error_rate))

    plt.scatter(sub_age, sub_fare)
    plt.plot(sub_age, estimated_fares, c='r')

# random_solution(sub_age, sub_fare)
'''
160.98465263157894
1 times:f(age)=9 * age + -9, with rate error 160.98465263157894
110.54649473684212
2 times:f(age)=7 * age + 3, with rate error 110.54649473684212
89.12544210526316
8 times:f(age)=6 * age + 10, with rate error 89.12544210526316
63.679389473684225
9 times:f(age)=4 * age + -4, with rate error 63.679389473684225
61.525442105263174
24 times:f(age)=4 * age + 6, with rate error 61.525442105263174
61.3149157894737
43 times:f(age)=4 * age + 8, with rate error 61.3149157894737
61.26228421052633
423 times:f(age)=4 * age + 9, with rate error 61.26228421052633
61.20965263157896
485 times:f(age)=4 * age + 10, with rate error 61.20965263157896
'''


#####################监督学习############################
def change_directions_solution(sub_age, sub_fare):
    '''
    supervisor 监督学习
    随机选择方向，得到更好的结果之后，继续沿着该方向变化
    当沿着该方向结果不是更好的时候，再随机选择方向
    :param sub_age:
    :param sub_fare:
    :return:
    '''
    change_directions = [
        (1, -1),
        (1, 1),
        (-1, 1),
        (-1, -1)
    ]

    k_hat = random.random() * 20 - 10
    k_best = k_hat
    b_hat = random.random() * 20 - 10
    b_best = b_hat
    loop_times = 1000
    loop = 0
    best_directions = None
    min_error_rate = float('inf')

    while loop < loop_times:
        loop = loop + 1
        k_delta_direction, b_delta_direction = best_directions or random.choice(
            change_directions)
        k_delta = k_delta_direction * step()
        b_delta = b_delta_direction * step()

        new_k = k_best + k_delta
        new_b = b_best + b_delta

        estimated_fares = func(sub_age, new_k, new_b)
        error_rate = loss(y=sub_fare, y_hat=estimated_fares)

        if error_rate < min_error_rate:
            print(error_rate)
            k_best = new_k
            b_best = new_b
            best_directions = k_delta_direction, b_delta_direction
            min_error_rate = error_rate
            k_best, b_best = new_k, new_b
            print("{} times:f(age)={} * age + {}, with rate error {}".format(
                loop,k_best,b_best, min_error_rate))
        else:
            best_directions = None # 当前方向已经不是最优，重置

def step(): return random.random()

# change_directions_solution(sub_age, sub_fare)
'''
10 times:f(age)=2.8825859676810786 * age + 12.052664741560742, with rate error 74.22864909355253
62.316946710078426
11 times:f(age)=3.517153916672162 * age + 12.07247800078801, with rate error 62.316946710078426
60.822065156635674
12 times:f(age)=3.8139301108005768 * age + 12.439466159434623, with rate error 60.822065156635674
60.77159276250118
22 times:f(age)=3.8363231193067553 * age + 12.520265898220481, with rate error 60.77159276250118
60.56892050710403        =======22次已经下降到60=======
...
...
859 times:f(age)=3.5575646336491715 * age + 27.660536220599464, with rate error 58.850511740075156
58.720196928649436
875 times:f(age)=3.6923590035931735 * age + 27.766122700605425, with rate error 58.720196928649436
58.66845130027528
890 times:f(age)=3.635695657841037 * age + 27.98018808128547, with rate error 58.66845130027528
58.61803218561164
937 times:f(age)=3.65937970232956 * age + 28.046879332944307, with rate error 58.61803218561164
58.600040219364125
1000 times:f(age)=3.649027036772251 * age + 28.2712568851232, with rate error 58.600040219364125
'''


#####################梯度下降############################
def derivate_solution(sub_age, sub_fare):
    '''
    梯度下降法，梯度代表的是变化趋势和变量之间的关系
    梯度在二维的意思就是导数
    这里要求的就是 loss 的变化趋势和 k,b 取值的关系
        loss = np.mean(abs(y - y_hat))
    那么 loss = 1/n Sum( |y-(kx+b)| )
    那么 loss 相对 k 的导数是 :
        y > yi : 1/n * -1 * x
        y < yi : 1/n * x
    loss 相对 b 的导数就是 ：
        y > yi : 1/n * 1
        y < yi : 1/n * -1
    :param sub_age:
    :param sub_fare:
    :return:
    '''

    k_hat = random.random() * 20 - 10
    b_hat = random.random() * 20 - 10
    loop_times = 1000
    loop = 0
    learning_rate = 1e-2

    while loop < loop_times:
        loop = loop + 1

        k_delta = -1 * learning_rate * devirate_k(sub_fare, func(sub_age,
                                                                k_hat, b_hat), sub_age)
        b_delta = 1 * learning_rate * devirate_b(sub_fare, func(sub_age,
                                                                k_hat, b_hat))
        k_hat += k_delta
        b_hat += b_delta

        estimated_fares = func(sub_age, k_hat, b_hat)
        error_rate = loss(y=sub_fare, y_hat=estimated_fares)

        print("{} times:f(age)={} * age + {}, with rate error {}".format(
                loop,k_hat,b_hat, error_rate))

def devirate_k(y, y_hat, x):
    abs_value = [1 if y_i > y_hat else -1 for y_i, y_hat in zip(y, y_hat) ]
    return np.mean([ a * -x_i for a, x_i in zip(abs_value, x)])


def devirate_b(y, y_hat):
    abs_value = [1 if y_i > y_hat else -1 for y_i, y_hat in zip(y, y_hat) ]
    return np.mean([a * -1 for a in abs_value])

derivate_solution(sub_age, sub_fare)
'''
一直在下降, 监督学习的效果本身很好，但是当参数维度越高时，监督学习的方向指数增长，难以实现
而导数法，tensflow 等可以帮忙求导
1 times:f(age)=-8.962186581205303 * age + 5.813347062930788, with rate error 525.658036347208
2 times:f(age)=-8.581133949626356 * age + 5.803347062930788, with rate error 511.147925543884
3 times:f(age)=-8.200081318047408 * age + 5.793347062930788, with rate error 496.63781474055986
4 times:f(age)=-7.81902868646846 * age + 5.783347062930789, with rate error 482.12770393723576
5 times:f(age)=-7.437976054889512 * age + 5.773347062930789, with rate error 467.61759313391167
6 times:f(age)=-7.056923423310565 * age + 5.763347062930789, with rate error 453.1074823305876
...
...
940 times:f(age)=4.055708155636806 * age + 4.2791365366148515, with rate error 61.792223494974664
941 times:f(age)=4.0051818398473324 * age + 4.278610220825378, with rate error 61.78851318223206
942 times:f(age)=4.02202394511049 * age + 4.277031273456957, with rate error 61.760396838741755
943 times:f(age)=4.038866050373648 * age + 4.275452326088535, with rate error 61.73228049525144
944 times:f(age)=4.055708155636806 * age + 4.273873378720114, with rate error 61.79250050328491
945 times:f(age)=4.0051818398473324 * age + 4.2733470629306405, with rate error 61.78934420716282
...
...
999 times:f(age)=4.038866050373648 * age + 4.20176811556221, with rate error 61.74391484428193
1000 times:f(age)=4.055708155636806 * age + 4.200189168193789, with rate error 61.796378619628406
'''
