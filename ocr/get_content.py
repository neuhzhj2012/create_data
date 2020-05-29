#encoding: utf-8
import random
class CONT():
    def __init__(self):
        self.num = [str(i) for i in range(9)]
        self.alpha = [chr(i) for i in range(65,91)]
        with open('data/content/400.txt', 'r', encoding='utf-8') as fp:
            buffs = fp.readlines()

        self.chinese = [k.strip() for k in buffs]
    def __getRandomContent__(self, conts, num): #从字库中随机获得指定num的内容
        step = int(num / len(conts)) #步长数，因为无法sample大于候选集数量的结果
        remainder = num % len(conts) #余数
        rst = ''
        for i in list(range(step)):
            rst += ''.join(random.sample(conts, len(conts)))
        if remainder > 0:
            rst += ''.join(random.sample(conts, remainder))
        return rst
    def getChinese(self, num): #指定类型的数据
        return self.__getRandomContent__(self.chinese, num)
    def getNum(self, num):
        return self.__getRandomContent__(self.num, num)
    def getAlpha(self, num):
        return self.__getRandomContent__(self.alpha, num)
    def getContent(self, num, *args):  #随机获得num个数据
        num_chinese = args[0] #汉字数量
        num_alpha = args[1]
        num_num = args[2] #数字数量
        flag_shuffle = args[3] #是否打乱顺序
        conts = self.getChinese(num_chinese) + self.getAlpha(num_alpha) + self.getNum(num_num)
        if flag_shuffle:
            ''.join(random.sample(conts, len(conts)))
        return conts

