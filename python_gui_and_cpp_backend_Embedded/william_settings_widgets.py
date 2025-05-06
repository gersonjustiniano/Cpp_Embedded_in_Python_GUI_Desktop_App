import PyQt6.QtWidgets as qt
from PyQt6.QtGui import QColor
import css_styles


def set_label_config(combo_settings,settings,label_config,william_settings):
    if combo_settings.currentText()==settings[0]:
        gator=william_settings['alligator']
        label_config.setText(f"({gator['lips'][0]},{gator['teeths'][0]},{gator['jaw'][0]})")
    elif combo_settings.currentText()==settings[1]:
        frac=william_settings['fractals']
        label_config.setText(f"({frac['fractal']})")
    elif combo_settings.currentText()==settings[2]:
        awe=william_settings['awesome']
        label_config.setText(f"({awe['slow']},{awe['fast']})")

#----------------------------------------------------------------------------------------------------------------------------------------------

def set_lips_color(lips_color,color_vals):
    color=qt.QColorDialog.getColor()
    if color.isValid():
        lips_color.setStyleSheet(f"""QPushButton {{background-color:{color.name()};}} QPushButton:pressed {{border: 2px solid black;}}""")
        color_vals[0]=color.name()

def set_teeths_color(teeths_color,color_vals):
    color=qt.QColorDialog.getColor()
    if color.isValid():
        teeths_color.setStyleSheet(f"""QPushButton {{background-color:{color.name()};}} QPushButton:pressed {{border: 2px solid black;}}""")
        color_vals[1]=color.name()

def set_jaw_color(jaw_color,color_vals):
    color=qt.QColorDialog.getColor()
    if color.isValid():
        jaw_color.setStyleSheet(f"""QPushButton {{background-color:{color.name()};}} QPushButton:pressed {{border: 2px solid black;}}""")
        color_vals[2]=color.name()

def get_will_vals(spin_vals,color_vals,william_settings,label_config,win):
    gator=william_settings['alligator']
    gator['lips']=[spin_vals[0].value(),color_vals[0]]
    gator['teeths']=[spin_vals[1].value(),color_vals[1]]
    gator['jaw']=[spin_vals[2].value(),color_vals[2]]
    label_config.setText(f"({spin_vals[0].value()},{spin_vals[1].value()},{spin_vals[2].value()})")
    win.close()

def alligator_window(william_settings,label_config,will_windows):
    
    win=qt.QWidget()
    win.setGeometry(300,300,190,140)
    win.setFixedSize(190,140)
    win.setWindowTitle('Alligator Settings')
    win.setStyleSheet('background-color:#1c1c1c;')

    labels=['Lips','Teeths','Jaw']
    spin_vals=[]
    will=william_settings['alligator']
    color_vals=[will['lips'][1],will['teeths'][1],will['jaw'][1]]

    for i in range(len(william_settings['alligator'])):
        will_vals=william_settings['alligator'][labels[i].lower()]

        label=qt.QLabel(labels[i],win)
        label.setGeometry(5,30*i+10,50,20)
        label.setStyleSheet(css_styles.label_symbol_style)
        
        spin=qt.QSpinBox(win)
        spin.setMinimum(1)
        spin.setMaximum(1000)
        spin.setValue(will_vals[0])
        spin.setGeometry(70,30*i+10,80,20)
        spin.setStyleSheet(css_styles.spin_style)
        spin_vals.append(spin)


    lips_color=qt.QPushButton('',win)
    lips_color.setGeometry(160,10,20,20)
    lips_color.setStyleSheet(f"""QPushButton {{background-color:{color_vals[0]};}} QPushButton:pressed {{border: 2px solid black;}}""")
    lips_color.clicked.connect(lambda:set_lips_color(lips_color,color_vals))

    teeths_color=qt.QPushButton('',win)
    teeths_color.setGeometry(160,40,20,20)
    teeths_color.setStyleSheet(f"""QPushButton {{background-color:{color_vals[1]};}} QPushButton:pressed {{border: 2px solid black;}}""")
    teeths_color.clicked.connect(lambda:set_teeths_color(teeths_color,color_vals))

    jaw_color=qt.QPushButton('',win)
    jaw_color.setGeometry(160,70,20,20)
    jaw_color.setStyleSheet(f"""QPushButton {{background-color:{color_vals[2]};}} QPushButton:pressed {{border: 2px solid black;}}""")
    jaw_color.clicked.connect(lambda:set_jaw_color(jaw_color,color_vals))

    button_accept=qt.QPushButton('Accept',win)
    button_accept.setGeometry(20,110,70,20)
    button_accept.setStyleSheet(css_styles.accept_cancel_style)
    button_accept.clicked.connect(lambda:get_will_vals(spin_vals,color_vals,william_settings,label_config,win))

    button_cancel=qt.QPushButton('Cancel',win)
    button_cancel.setGeometry(100,110,70,20)
    button_cancel.setStyleSheet(css_styles.accept_cancel_style)
    button_cancel.clicked.connect(win.close)

    will_windows.append(win)
    win.show()

#----------------------------------------------------------------------------------------------------------------------------------------------

def set_up_color(color_up,color_vals):
    color=qt.QColorDialog.getColor()
    if color.isValid():
        color_up.setStyleSheet(f"""QPushButton {{background-color:{color.name()};}} QPushButton:pressed {{border: 2px solid black;}}""")
        color_vals[0]=color.name()

def set_down_color(color_down,color_vals):
    color=qt.QColorDialog.getColor()
    if color.isValid():
        color_down.setStyleSheet(f"""QPushButton {{background-color:{color.name()};}} QPushButton:pressed {{border: 2px solid black;}}""")
        color_vals[1]=color.name()

def get_frac_vals(william_settings,label_config,spin,color_vals,win):

    frac=william_settings['fractals']
    frac['fractal']=spin.value()
    frac['up']=color_vals[0]
    frac['down']=color_vals[1]
    label_config.setText(f'({spin.value()})')
    win.close()

def fractal_window(william_settings,label_config,will_windows):

    win=qt.QWidget()
    win.setGeometry(300,300,190,120)
    win.setFixedSize(190,120)
    win.setWindowTitle('Fractal Settings')
    win.setStyleSheet('background-color:#1c1c1c;')

    frac=william_settings['fractals']
    color_vals=[frac['up'],frac['down']]

    label=qt.QLabel('Fractal',win)
    label.setGeometry(35,20,50,20)
    label.setStyleSheet(css_styles.label_symbol_style)

    spin=qt.QSpinBox(win)
    spin.setMinimum(2)
    spin.setMaximum(100)
    spin.setValue(frac['fractal'])
    spin.setGeometry(95,20,50,20)
    spin.setStyleSheet(css_styles.spin_style)

    label_up=qt.QLabel('Up',win)
    label_up.setGeometry(15,45,50,30)
    label_up.setStyleSheet(css_styles.label_symbol_style)

    color_up=qt.QPushButton('',win)
    color_up.setGeometry(50,50,20,20)
    color_up.setStyleSheet(f"""QPushButton {{background-color:{color_vals[0]};}} QPushButton:pressed {{border: 2px solid black;}}""")
    color_up.clicked.connect(lambda:set_up_color(color_up,color_vals))

    label_down=qt.QLabel('Down',win)
    label_down.setGeometry(95,45,50,30)
    label_down.setStyleSheet(css_styles.label_symbol_style)

    color_down=qt.QPushButton('',win)
    color_down.setGeometry(150,50,20,20)
    color_down.setStyleSheet(f"""QPushButton {{background-color:{color_vals[1]};}} QPushButton:pressed {{border: 2px solid black;}}""")
    color_down.clicked.connect(lambda:set_down_color(color_down,color_vals))

    button_accept=qt.QPushButton('Accept',win)
    button_accept.setGeometry(20,90,70,20)
    button_accept.setStyleSheet(css_styles.accept_cancel_style)
    button_accept.clicked.connect(lambda:get_frac_vals(william_settings,label_config,spin,color_vals,win))

    button_cancel=qt.QPushButton('Cancel',win)
    button_cancel.setGeometry(100,90,70,20)
    button_cancel.setStyleSheet(css_styles.accept_cancel_style)
    button_cancel.clicked.connect(win.close)

    will_windows.append(win)
    win.show()


#----------------------------------------------------------------------------------------------------------------------------------------------

def set_up_awesome_color(color_up_awe,color_vals):
    color=qt.QColorDialog.getColor()
    if color.isValid():
        color_up_awe.setStyleSheet(f"""QPushButton {{background-color:{color.name()};}} QPushButton:pressed {{border: 2px solid black;}}""")
        color_vals[0]=color.name()

def set_down_awesome_color(color_down_awe,color_vals):
    color=qt.QColorDialog.getColor()
    if color.isValid():
        color_down_awe.setStyleSheet(f"""QPushButton {{background-color:{color.name()};}} QPushButton:pressed {{border: 2px solid black;}}""")
        color_vals[1]=color.name()

def get_awesome_vals(spin_slow,spin_fast,color_vals,william_settings,label_config,win):
    awe=william_settings['awesome']
    awe['slow']=spin_slow.value()
    awe['fast']=spin_fast.value()
    awe['up']=color_vals[0]
    awe['down']=color_vals[1]
    label_config.setText(f'({spin_slow.value()},{spin_fast.value()})')
    win.close()

def awesome_window(william_settings,label_config,will_windows):
    
    win=qt.QWidget()
    win.setGeometry(300,300,190,190)
    win.setFixedSize(190,190)
    win.setWindowTitle('Awesome O. Settings')
    win.setStyleSheet('background-color:#1c1c1c;')

    awe=william_settings['awesome']
    color_vals=[awe['up'],awe['down']]

    label_slow=qt.QLabel('Slow',win)
    label_slow.setGeometry(35,20,50,30)
    label_slow.setStyleSheet(css_styles.label_symbol_style)

    spin_slow=qt.QSpinBox(win)
    spin_slow.setMinimum(2)
    spin_slow.setMaximum(1000)
    spin_slow.setValue(awe['slow'])
    spin_slow.setGeometry(95,25,50,20)
    spin_slow.setStyleSheet(css_styles.spin_style)

    label_fast=qt.QLabel('Fast',win)
    label_fast.setGeometry(35,50,50,30)
    label_fast.setStyleSheet(css_styles.label_symbol_style)

    spin_fast=qt.QSpinBox(win)
    spin_fast.setMinimum(2)
    spin_fast.setMaximum(1000)
    spin_fast.setValue(awe['fast'])
    spin_fast.setGeometry(95,55,50,20)
    spin_fast.setStyleSheet(css_styles.spin_style)

    label_color_up=qt.QLabel('Up Color',win)
    label_color_up.setGeometry(30,80,70,30)
    label_color_up.setStyleSheet(css_styles.label_symbol_style)

    color_up_awe=qt.QPushButton('',win)
    color_up_awe.setGeometry(130,85,20,20)
    color_up_awe.setStyleSheet(f"""QPushButton {{background-color:{color_vals[0]};}} QPushButton:pressed {{border: 2px solid black;}}""")
    color_up_awe.clicked.connect(lambda:set_up_awesome_color(color_up_awe,color_vals))

    label_color_down=qt.QLabel('Down Color',win)
    label_color_down.setGeometry(30,110,90,30)
    label_color_down.setStyleSheet(css_styles.label_symbol_style)

    color_down_awe=qt.QPushButton('',win)
    color_down_awe.setGeometry(130,115,20,20)
    color_down_awe.setStyleSheet(f"""QPushButton {{background-color:{color_vals[1]};}} QPushButton:pressed {{border: 2px solid black;}}""")
    color_down_awe.clicked.connect(lambda:set_down_awesome_color(color_down_awe,color_vals))

    button_accept=qt.QPushButton('Accept',win)
    button_accept.setGeometry(20,155,70,20)
    button_accept.setStyleSheet(css_styles.accept_cancel_style)
    button_accept.clicked.connect(lambda:get_awesome_vals(spin_slow,spin_fast,color_vals,william_settings,label_config,win))

    button_cancel=qt.QPushButton('Cancel',win)
    button_cancel.setGeometry(100,155,70,20)
    button_cancel.setStyleSheet(css_styles.accept_cancel_style)
    button_cancel.clicked.connect(win.close)

    will_windows.append(win)
    win.show()

