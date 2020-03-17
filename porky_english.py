import sys, re
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("porky_english.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    progress = 1
    widgets = []
    lines = []
    layout = None
    textEdits = []

    # 본문 문장단위로 분리해서 띄울 때 상수
    textEdit_width = 500
    textEdit_height = 60
    deleteButton_width = 60

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.layout = self.children()[0]
        self.nextButton.clicked.connect(self.nextFunction)

    # 다음 progress로 넘어감
    def nextFunction(self):
        if (self.progress == 1):
            self.splitMainText(self.mainTextEdit.toPlainText())
        print("--------remove widgets--------")
        self.removeWidgets()
        print("------------------------------")
        print("--------create widgets--------")
        self.createWidgets()
        print("------------------------------")
        print("--------change label--------")
        self.changeLabel()
        print("------------------------------")
        
    def changeLabel(self):
        self.progress = self.progress + 1
        if self.progress == 4:
            self.nextButton.setText("처음으로")
            self.showProgressLabel.setText(str(self.progress))
        elif self.progress == 5:
            self.nextButton.setText("다음")
            self.progress = 1
            self.showProgressLabel.setText(str(self.progress))
        else:
            self.showProgressLabel.setText(str(self.progress))

    def splitMainText(self, mainText):
        self.lines = re.split(r'\n|[.]', mainText)

    # widget들을 초기화해줌
    def removeWidgets(self):
        if self.progress == 1:
            self.mainTextEdit.deleteLater()
        elif self.progress == 2:
            for i in range(len(self.widgets)):
                self.widgets[i].deleteLater()
        self.widgets = []
    
    # 각 progress에 맞춰서 widget들을 생성해줌
    def createWidgets(self):
        if self.progress == 1:
            scrollArea = QScrollArea(self)
            scrollArea.setWidgetResizable(True)
            l = len(self.lines)
            scrollArea.resize(650, 400)
            scrollArea.move(40, 70)
            scrollAreaContents = QWidget()
            layout = QVBoxLayout(scrollAreaContents)
            for i in range(l):
                self.addTextEdit(self.lines[i], layout)
            scrollAreaContents.setLayout(layout)
            scrollArea.setWidget(scrollAreaContents)
            self.layout.addWidget(scrollArea)
            pushButton = QPushButton(self)
            pushButton.setObjectName("addTextEdit")
            pushButton.resize(75, 30)
            pushButton.move(40, 550)
            pushButton.setText("Add")
            pushButton.clicked.connect(lambda:self.addTextEdit("", layout))
            self.layout.addWidget(pushButton)
            self.widgets.append(scrollArea)
            self.widgets.append(pushButton)
    
    def addTextEdit(self, line, layout):
        groupBox = QGroupBox()
        contentLayout = QBoxLayout(QBoxLayout.LeftToRight, parent=groupBox)
        textEdit = QTextEdit()
        textEdit.resize(self.textEdit_width, self.textEdit_height)
        textEdit.setText(line)
        deleteButton = QPushButton()
        deleteButton.setText("delete")
        deleteButton.resize(self.deleteButton_width, self.textEdit_height)
        deleteButton.clicked.connect(lambda:deleteButton.parent().deleteLater())
        contentLayout.addWidget(textEdit)
        contentLayout.addWidget(deleteButton)
        layout.addWidget(groupBox)

    
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()