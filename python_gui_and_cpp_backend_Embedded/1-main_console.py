import PyQt6.QtWidgets as qt
import PyQt6.QtCore as qcore
import PyQt6.QtGui as qgui
#from PyQt6.QtCore import Qt,QThread,pyqtSignal,QObject
#from PyQt6.QtGui import QBrush, QColor
import pyqtgraph as pg
import css_styles
import random,time
from datetime import datetime,timedelta
import pandas as pd
import william_settings_widgets as will_config
import backend_indicator as back_indi

import threading

app=qt.QApplication([])

win=qt.QWidget()
win.setGeometry(300,200,300,300)
win.setFixedSize(700,300)
win.setWindowTitle('Live')
win.setStyleSheet('background-color:#1c1c1c;')

#-------------------------------------------------------------------------------------------

plot_price=pg.PlotWidget(parent=win)
plot_price.setBackground('black')
plot_price.setStyleSheet('border: 1px solid dimgray;')
plot_price.setGeometry(175,1,523,240)
plot_price.showAxis('bottom',False)
plot_price.showAxis('left',False)
#plot_price.setMouseEnabled(x=False, y=False)
#plot_price.getViewBox().setMenuEnabled(False)
#plot_price.getViewBox().setWheelEnabled(False)

plot_awesome=pg.PlotWidget(parent=win)
plot_awesome.setBackground('black')
plot_awesome.setStyleSheet('border: 1px solid dimgray;')
plot_awesome.setGeometry(175,240,523,60)
plot_awesome.showAxis('bottom',False)
plot_awesome.showAxis('left',False)
plot_awesome.setXLink(plot_price)
#plot_awesome.setMouseEnabled(x=False, y=False)
#plot_awesome.getViewBox().setMenuEnabled(False)
#plot_awesome.getViewBox().setWheelEnabled(False)

#-------------------------------------------------------------------------------------------

#SYMBOL:

label_symbol=qt.QLabel('Symbol',win)
label_symbol.setGeometry(5,5,65,20)
label_symbol.setStyleSheet(css_styles.label_symbol_style)

combo_symbol=qt.QComboBox(win)
combo_symbol.setGeometry(70,5,100,20)
combo_symbol.setStyleSheet(css_styles.combo_symbol_style)
combo_symbol.addItem('Select')
symbols=['EURUSD','BTCUSD','XAUUSD','SP500']
combo_symbol.addItems(symbols)

#INTERVAL:

label_interval=qt.QLabel('Interval',win)
label_interval.setGeometry(5,30,100,20)
label_interval.setStyleSheet(css_styles.label_interval_style)

combo_interval=qt.QComboBox(win)
combo_interval.setGeometry(110,30,60,20)
combo_interval.setStyleSheet(css_styles.combo_interval_style)
intervals=['M1','M5','M15','M30','H1','H4','D1']
combo_interval.addItems(intervals)

#WILLIAM INDICATORS:

william_settings={
    'alligator': {
        'lips':[5,'green'],'teeths':[8,'red'],'jaw':[13,'blue']
    },
    'fractals':{
        'fractal':2,'up':'#3ba3bc','down':'#264f5a'
    },
    'awesome':{
        'slow':34,'fast':5,'up':'#3ba3bc','down':'#264f5a'
    }
}

label_settings=qt.QLabel('Settings',win)
label_settings.setGeometry(5,55,60,20)
label_settings.setStyleSheet(css_styles.label_settings_style)

combo_settings=qt.QComboBox(win)
combo_settings.setGeometry(80,55,90,20)
combo_settings.setStyleSheet(css_styles.combo_settings_style)
settings=['Alligator','Fractals','Awesome']
combo_settings.addItems(settings)
combo_settings.activated.connect(lambda:will_config.set_label_config(combo_settings,settings,label_config,william_settings))

label_config=qt.QLabel('(5,8,13)',win)
label_config.setGeometry(5,80,135,20)
label_config.setStyleSheet(css_styles.label_config_style)

will_windows=[]

def will_configure(combo_settings,settings,william_settings,label_config,will_windows):
    if combo_settings.currentText()==settings[0]:
        will_config.alligator_window(william_settings,label_config,will_windows)
    elif combo_settings.currentText()==settings[1]:
        will_config.fractal_window(william_settings,label_config,will_windows)
    elif combo_settings.currentText()==settings[2]:
        will_config.awesome_window(william_settings,label_config,will_windows)

button_settings=qt.QPushButton('...',win)
button_settings.setGeometry(145,80,20,20)
button_settings.setStyleSheet(css_styles.button_settings_style)
button_settings.clicked.connect(lambda:will_configure(combo_settings,settings,william_settings,label_config,will_windows))

#-------------------------------------------------------------------------------------------

#TABLE:

columns=['Time','Price']
table=qt.QTableWidget(win)
table.setGeometry(5,105,165,165)
table.setColumnCount(len(columns))
table.setHorizontalHeaderLabels(columns)
table.setStyleSheet(css_styles.table_style)
table.setVerticalScrollBarPolicy(qcore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
table.verticalHeader().setVisible(False)
for col in range(len(columns)):
    table.setColumnWidth(col,76)

#-------------------------------------------------------------------------------------------

#START - STOP BUTTONS:

active_live=[False]
active_thread=None

#CONFIGURE THREAD CONECTION TO FUNCTION WHO USE WIDGETS UPDATES:

class widget_signal_thread(qcore.QObject):
    enable_buttons=qcore.pyqtSignal(object,object,bool,bool)
    updateTable=qcore.pyqtSignal(dict,object)
    updatePlot=qcore.pyqtSignal(dict,dict,dict,dict,int,str)
    updateAwesome=qcore.pyqtSignal(dict,dict,dict,dict,int,str)

widgetSignals=widget_signal_thread()
widgetSignals.enable_buttons.connect(back_indi.update_buttons)
widgetSignals.updateTable.connect(back_indi.update_table)
widgetSignals.updatePlot.connect(back_indi.plot_data)
widgetSignals.updateAwesome.connect(back_indi.plot_AO)

def start_live():
    global active_thread
    if active_live[0]==False:
        if combo_symbol.currentText()!='Select':
            active_live[0]=True
            widgetSignals.enable_buttons.emit(button_start,button_stop,False,True)

            get_settings={
                'symbol':combo_symbol.currentText(),
                'interval':combo_interval.currentText(),
                'william_settings':william_settings,
                'active_live':active_live}

            get_widgets={
                'symbol':combo_symbol,
                'interval':combo_interval,
                'settings':combo_settings,
                'table':table,
                'start_button':button_start,
                'stop_button':button_stop,
                'plot_price':plot_price,
                'plot_awesome':plot_awesome,
                'widgetSignals':widgetSignals}
            
            #ADDING THREAD TO A FUNCTION:
            #threading.Thread(target=back_indi.run_live,args=[get_settings,get_widgets],daemon=True).start()    #this can be used too

            active_thread=qcore.QThread()            
            active_thread.run=lambda:back_indi.run_live(get_settings,get_widgets)
            active_thread.start()
        else:
            msg=qt.QMessageBox(win)
            msg.setIcon(qt.QMessageBox.Icon.Information)
            msg.setWindowTitle('Symbol')
            msg.setText('Select Symbol')
            msg.setStyleSheet(css_styles.messageBoxInformation_style)
            msg.exec()

def stop_live():
    global active_thread
    if active_live[0]==True:
        active_live[0]=False
        widgetSignals.enable_buttons.emit(button_start,button_stop,True,False)
    if active_thread and active_thread.isRunning():
        active_thread.quit()

button_start=qt.QPushButton('Start',win)
button_start.setGeometry(5,275,80,20)
button_start.setStyleSheet(css_styles.start_style)
button_start.setEnabled(True)
button_start.clicked.connect(start_live)

button_stop=qt.QPushButton('Stop',win)
button_stop.setGeometry(90,275,80,20)
button_stop.setStyleSheet(css_styles.stop_style)
button_stop.setEnabled(False)
button_stop.clicked.connect(stop_live)

def close_event(event):
    for w in will_windows:
        w.close()

win.closeEvent=close_event
win.show()
app.exec()
