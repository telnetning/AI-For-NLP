### Q2
1.  How to Github and Why do we use Jupyter and Pycharm?    

    +  Github 开源协作平台，使用 Git 进行协同开发，也可以被用作很多其他的用途。简单高效易用，每一个开发者必须会用的东西。
    +  Jupyter 支持多种格式，即使是在同一个 notes 中，并且也还算比较容易共享。
    +  Jupyter 不适合大型软件开发，只适合小脚本，稍微复杂点的程序还是只能交给 IDE，比如 Pycharm。

2.  What's the Probability Model?  

    +  概率模型就是通过对概率的计算，来判断一件事情的合理性，比如一个单词。

3. Can you came up with some sceneraies at which we could use Probability Model?  

    +  依据最近几年历史战绩、当赛季常规赛战绩、相互对战战绩等判断 NBA 哪只球队今年能夺冠
    +  王者荣耀中，两方英雄选定之后，根据英雄相互胜率以及搭配胜率，计算哪一方获胜可能性更大
    +  ....

4. Why do we use probability and what's the difficult points for programming based on parsing and pattern match?  

    +  比较重要的原因可能就是基于模式匹配太难了，需要构造大量的模式，这可能需要语言学家参与；以及实现起来也比较困难。
    +  基于概率计算比较简单，并且可以很方便的用极其大量的数据作为语料处理。

5. What's the Language Model?  

    +  语言模型，就是通过概率模型来计算一个句子出现的合理性。

6. Can you came up with some sceneraies at which we could use Language Model?  

    +  语音识别，识别出一句话之后，判断识别出来的话的可能性，如果可能性低，那可能就得考虑是不是识别错了。
    +  微信公众号文章自动review，写好文章之后，review一下每句话的概率，如果有反常的极低的概率，那可能就是敲错字了。
    +  ...

7. What's the 1-gram language model?  

    +  就是通过单独计算句子里的每一个 token 出现的概率，然后连乘，不考虑 token 之间的关系

8. What's the disadvantages and advantages of 1-gram language model?  

    +  优势就是简单，很容易实现
    +  劣势就是没有考虑 token 之间的相关性，缺乏语言逻辑上的整体判断，对于常用词构造的不合逻辑的句子无法甄别

9. What't the 2-gram models?  

    +  考虑某个 token 的概率的时候，只考虑其前一个 token 出现时该 token 出现的概率，这样可以将一个 token 和其前一个 token 联系起来

10. what's the web crawler, and can you implement a simple crawler?

    +  网页请求和分析的技术，一个简单实现的爬虫小工具：[命令行有道词典](https://github.com/telnetning/script_tools/blob/master/youdao.py)

11. There may be some issues to make our crwaler programming difficult, what are these, and how do we solve them?

    +  主要是`JS`动态加载的内容可能无法爬取到，需要使用`headless`的浏览器工具进行爬虫操作

12. What't the Regular Expression and how to use?

    +  用于在大量文本中提取特定模式，各个语言都有对应的模块，python 中是`re`模块

### Q3
Step 5: If we need to solve following problems, how can language model help us?

+  Voice Recognization: 可以通过计算识别出的句子的概率判断这句话是不是识别准确了  
+  Sogou pinyin input: 当用户敲下一个词时，可以通过概率计算用户下一个输入词的概率，用来做自动联想功能  
+  Auto correction in search engine: 判断用户输入的概率，如果概率不高，可以试着将某些词尝试进行修正，计算修正后的合理性，如果概率大大提升，可以说明修正后的结果可能才是用户真正想要的输入  
+  Abnormal Detection:  指的是用户语言行为的？那么可以根据用户的语言历史作为语料，计算 token 概率，如果用户新的一段时间的语言行为也同时进行处理，如果某个之前出现概率较高的词（可能是感叹词、形容词之类比较准确）在新的语言行为中长时间没出现，或者新的语言行为中出现的某个高频词之前很少出现，那么该用户可能是异常的。简单的比如用 ”吧“、”啊“、”哈哈“ 之类的做判断

### Optional 
How did you solve this problem(OOV) in your programming task?  

+  最简单的方式，没出现的将其出现的次数 +1，即作为出现一次处理了。
