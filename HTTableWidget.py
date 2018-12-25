from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from global_data import global_data


class TableWidget(QTableWidget):
	def __init__(self, datas):
		super().__init__()

		self.datas = datas


		self.setUI()
		self.setTable()

	def setTable(self):
		self.clearContents()
		for i in range(len(self.datas)):
			data = self.datas[i]
			for j in range(len(data)):
				item = data[j]
				if j == 1:
					# qq
					qqArr, index = self.getQQ(data)
					self.setComboBox(i, j, qqArr, edit=False, index=index)

				elif j == 6:
					pass
					# 分类
					# self.data = gfunc.readJsonFile('classify')
        			# firstArr = self.data['first']

				elif j == 7:
					pass
				else:
					self.setItem(i, j, QTableWidgetItem(str(item)))



		self.setRowCount(len(self.datas))

		QTableWidget.resizeColumnsToContents(self)


	def setUI(self):
		headerArr = ['id', 'qq', 'title', 'url', 'alias', 'tags', 'first_class', 'second_class', 'platform_create_time', 'create_time', 'publish_time', 'aid', 'vid', 'pic', 'is_exist_local', 'local_path', 'fromUserId', 'platform']

		self.setColumnCount(len(headerArr))

		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.setHorizontalHeaderLabels(headerArr)

		# QTableWidget.resizeColumnsToContents(self)
		QTableWidget.resizeRowsToContents(self)

	def setComboBox(self, i, j, arr, index=0, edit=True):
		comBox = QComboBox()
		comBox.addItems(arr)
		comBox.setEditable(edit)
		comBox.setCurrentIndex(index)
		comBox.setStyleSheet('QComboBox{margin:3px}')

		self.setCellWidget(i , j, comBox)

	def getQQ(self, item):
		qq = item[1]
		finish_time = str(item[10])
		index = 0
		if len(qq) > 0 and finish_time != 'None' :
			return [qq], index
		else:
			qqArr = ['']
			for i in range(len(global_data.UploaderArray)):
				ii = global_data.UploaderArray[i][1]
				qqArr.append(ii)
				if ii == qq:
					index = i+1

			return qqArr, index



	def updateTable(self, datas):
		self.datas = datas
		# print(self.datas)
		self.setTable()




if __name__ == '__main__':
	app = QApplication(sys.argv)

	tb = TableWidget()
	tb.show()
	app.exec_()
