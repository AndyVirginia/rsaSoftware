import sys

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMessageBox, QPushButton,
                             QTextEdit, QVBoxLayout, QWidget)


def ModExp(x, n, m):
    '''模指运算，计算b^n(mod m)'''
    a = 1   
    b = x   
    while True:
        temp = n
        if n % 2 == 1 :
            a = a * b % m
        b = b * b % m
        n = n//2
        if temp < 1 :
            return a

def ExtGCD(a, b):
    '''扩展欧几里得算法'''
    #a*xi + b*yi = ri
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = ExtGCD(b, a % b) # q = gcd(a, b) = gcd(b, a%b)
        x, y = y, (x - (a // b) * y)
        return x, y, q


def isPrime(n):
    '''判断一个数是否为素数'''
    if n < 2:
        return False
    for i in range(2, int(n**0.5+1)):
        if n%i == 0:
            return False
    return True


def gcd(a, b):
    '''
    a较大，b较小
    求两个数的最大公约数
    辗转相除法：
    用较小数除较大数，再用余数去除除数，直到余数是0为止
    '''
    if a < b:
        a, b = b, a
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def prime_list(e):
    '''生成1~e间的素数序列'''
    eulers = []
    for x in range(e):
        if isPrime(x) and gcd(x, e) == 1:
            eulers.append(str(x))
    return eulers


class UI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        '''创建控件'''
        # 标记控件的生成
        self.lab1 = QLabel('素数p')
        self.lab2 = QLabel('素数q')
        self.lab3 = QLabel('n')
        self.lab4 = QLabel('eluer')
        self.lab5 = QLabel('e')
        self.lab6 = QLabel('d')
        self.lab7 = QLabel('明文')
        self.lab8 = QLabel('密文')

        # 单行文本输入框组件的生成
        self.edit1 = QLineEdit()
        self.edit1.setValidator(QIntValidator())  # 限制只能输入整数
        self.edit2 = QLineEdit()
        self.edit2.setValidator(QIntValidator())
        self.edit2.textChanged.connect(self.textchanged)
        self.edit3 = QLineEdit()
        self.edit3.setEnabled(False)
        self.edit4 = QLineEdit()
        self.edit4.setEnabled(False)
        self.edit5 = QComboBox()
        self.edit5.activated[str].connect(self.combo_changed)
        self.edit6 = QLineEdit()
        self.edit6.setEnabled(False)

        # 多行文本输入框组件的生成
        self.text1 = QTextEdit()
        self.text2 = QTextEdit()

        # 按钮组件的生成
        self.button1 = QPushButton('加密')
        self.button1.clicked.connect(self.encrypt)
        self.button2 = QPushButton('解密')
        self.button2.clicked.connect(self.decrypt)

        #  
        self.layout1 = QFormLayout()
        self.layout1.setWidget(0, QFormLayout.LabelRole, self.lab1)
        self.layout1.setWidget(0, QFormLayout.FieldRole, self.edit1)
        self.layout1.setWidget(1, QFormLayout.LabelRole, self.lab2)
        self.layout1.setWidget(1, QFormLayout.FieldRole, self.edit2)
        self.layout1.setWidget(2, QFormLayout.LabelRole, self.lab3)
        self.layout1.setWidget(2, QFormLayout.FieldRole, self.edit3)
        self.layout1.setWidget(3, QFormLayout.LabelRole, self.lab4)
        self.layout1.setWidget(3, QFormLayout.FieldRole, self.edit4)
        self.layout1.setWidget(4, QFormLayout.LabelRole, self.lab6)
        self.layout1.setWidget(4, QFormLayout.FieldRole, self.edit6)

        self.layout2 = QHBoxLayout()
        self.layout2.addLayout(self.layout1)
        self.layout2.addWidget(self.lab5)
        self.layout2.addWidget(self.edit5)

        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.button1)
        self.layout3.addWidget(self.button2)

        self.layout4 = QHBoxLayout()
        self.layout4.addWidget(self.lab7)
        self.layout4.addWidget(self.text1)
        self.layout4.addWidget(self.lab8)
        self.layout4.addWidget(self.text2)

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addLayout(self.layout2)
        self.mainlayout.addLayout(self.layout4)
        self.mainlayout.addLayout(self.layout3)
        self.setLayout(self.mainlayout)

    def textchanged(self):
        if self.edit1.text() == '' or self.edit2.text() == '':
            pass
        elif not isPrime(int(self.edit1.text())):
            self.edit3.setText('p非素数')
        elif not isPrime(int(self.edit2.text())):
            self.edit4.setText('q非素数')
        else:
            p = int(self.edit1.text())
            q = int(self.edit2.text())
            n = p * q
            e = (p-1)*(q-1)
            self.edit3.setText(str(n))
            self.edit4.setText(str(e))
            self.edit5.clear()
            eulers = prime_list(e)
            for x in range(len(eulers)):
                self.edit5.addItem(eulers[x])
            self.combo_changed(self.edit5.currentText())

    def combo_changed(self, text):
        e = int(text)
        d, d1, d2 = ExtGCD(e, int(self.edit4.text()))
        self.edit6.setText(str(d))

    def encrypt(self):
        '''实现加密'''
        mingwen = int(self.text1.toPlainText())
        self.e = int(self.edit5.currentText())
        self.n = int(self.edit1.text()) * int(self.edit2.text())
        miwen = ModExp(mingwen, self.e, self.n)
        self.text2.setText(str(miwen))
        self.edit6.setEnabled(True)

    def decrypt(self):
        '''实现解密'''
        miwen = int(self.text2.toPlainText())
        d = int(self.edit6.text())
        mingwen = ModExp(miwen, d, self.n)
        self.text1.setText(str(mingwen))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    ex.show()
    sys.exit(app.exec_())
