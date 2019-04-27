#!/usr/bin/env python3

from functools import lru_cache
"""
增加和删除的距离定义为 4
替换的距离定义为 5
空字符串和非空字符串的距离定义为 长度差 * 2

原因：
1. 替换距离要 大于 增加和删除的距离
2. 替换距离要 小于 (删除 + 删除）的距离
2. 替换距离要 小于 (删除 + 空与非空距离) 

主要是为了避免以下情况： 
"a" 和 "b" 的比较，拿到非替换方案，而是 (删除 + 删除）的方案
"""

solution = {}

@lru_cache(maxsize=2**10)
def edit_distance(string1, string2):
    if len(string1) == 0:
        solution[(string1, string2)] = (len(string2) * 2, 'ADD {}'.format(string2))
        return len(string2) * 2
    if len(string2) == 0:
        solution[(string1, string2)] = (len(string1) * 2, 'ADD {}'.format(string1))
        return len(string1) * 2

    tail_s1 = string1[-1]
    tail_s2 = string2[-1]

    candidates = [
        (edit_distance(string1[:-1], string2) + 4, 'DEL {}'.format(tail_s1)), # string1 delete tail
        (edit_distance(string1, string2[:-1]) + 4, 'ADD {}'.format(tail_s2)),# string1 add string2's tail
    ]

    if tail_s1 == tail_s2:
        candidates.append((edit_distance(string1[:-1], string2[:-1]), 'BOTH DEL {}'.format(tail_s1)))
    else:
        candidates.append(((edit_distance(string1[:-1], string2[:-1]) + 5), 'SUB {} TO {}'.format(tail_s1, tail_s2)))

    solution[(string1, string2)] = min(candidates, key=lambda x : x[0])
    return solution[(string1, string2)][0]
    #return min(candidates, key=lambda x : x[0])[0]

### test

print(edit_distance("rbcd", "abcde")) # 3
print(edit_distance("我不想上班", "我不像吃饭"))

# 手动 parse 流程
print(solution[("rbcd", "abcde")]) # (9, 'ADD e')
print(solution[("rbcd", "abcd")]) #(5, 'Both DEL d')
print(solution[("rbc", "abc")]) # (5, 'Both DEL c')
print(solution[("rb", "ab")]) # (5, 'Both DEL b')
print(solution[("r", "a")]) # (5, 'SUB r TO a')

print(edit_distance("r", ""))
print(solution[("r", "")])


"""
如果是 ADD,那么 solution(str1, str2[:-1])
如果是 DEL,那么 solution(str[:-1], str2)
如果是 SUB,那么 solution(str1[:-1], str2[:-1]) 
如果是 BOTH,那么 solution(str1[:-1], str2[:-1]) 
如果 str1="" 或者 str2=""  结束
"""
def parse_solution(string1, string2, solution):
    if (string1, string2) not in solution.keys():
        edit_distance(string1, string2)

    # 递归退出条件
    if(len(string1) == 0 and len(string2) != 0): return ["ADD {}".format(string2)]
    if(len(string2) == 0 and len(string1) != 0): return ["DEL {}".format(string1)]
    if(len(string1) == 0 and len(string2) == 0): return ["END"]

    # 递归
    operate = solution[(string1, string2)][1]
    if operate.startswith("ADD"):
        return [operate] + parse_solution(string1, string2[:-1], solution)
    elif operate.startswith("DEL"):
        return [operate] + parse_solution(string1[:-1], string2, solution)
    else:
        return [operate] + parse_solution(string1[:-1], string2[:-1], solution)

print(parse_solution("rbcd", "abcde", solution)) # ['ADD e', 'BOTH DEL d', 'BOTH DEL c', 'BOTH DEL b', 'SUB r TO a', 'END']
print(parse_solution("abcde", "rbcd", solution)) # ['DEL e', 'BOTH DEL d', 'BOTH DEL c', 'BOTH DEL b', 'SUB a TO r', 'END']
