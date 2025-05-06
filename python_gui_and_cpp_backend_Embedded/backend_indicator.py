import PyQt6.QtWidgets as qt
import PyQt6.QtCore as qcore
import PyQt6.QtGui as qgui
import pyqtgraph as pg
from datetime import datetime, timedelta
import time,random
import numpy as np
import indicator as indi

def update_buttons(button_start,button_stop,start_enable,stop_enable):
    button_start.setEnabled(start_enable)
    button_stop.setEnabled(stop_enable)

def r_price(symbol,price):
    r={'EURUSD':5,'BTCUSD':2,'XAUUSD':3,'US500':2}[symbol]
    return round(price,r)

def print_data(symbol,var,val):
    print(len(var['tick_time']),'/',len(var['time']),var['tick_time'][-1],'|',f"Bid: {r_price(symbol,var['bid'][-1])}",f"Ask: {r_price(symbol,var['ask'][-1])}",
          f"O: {r_price(symbol,var['open'][-1])}",f"H: {r_price(symbol,var['high'][-1])}",f"L: {r_price(symbol,var['low'][-1])}",f"C: {r_price(symbol,var['close'][-1])}",val)

def n_candles(interval):
    n={'M1':1,'M5':5,'M30':30,'H1':60,'H4':240,'D1':1440}[interval]
    return n

def line_style(color,width,style):
    lstyles={
        'line':qcore.Qt.PenStyle.SolidLine,
        'dash':qcore.Qt.PenStyle.DashLine,
        'dot':qcore.Qt.PenStyle.DotLine,
        'dash-dot':qcore.Qt.PenStyle.DashDotLine,
        'dash-dot-dot':qcore.Qt.PenStyle.DashDotDotLine}
    pen_style=pg.mkPen(color=color,width=width,style=lstyles[style])
    return pen_style

def plot_data(var,var_prices,get_settings,get_widgets,fr,val):

    plot_price=get_widgets['plot_price']
    
    plot_price.setXRange(0 if len(var['time'])<fr else len(var['time'])-fr,fr if len(var['time'])<fr else len(var['time']))
    plot_price.setYRange(0 if len(var['time'])<2 else min(var['low'][-fr:]), 0.1 if len(var['time'])<2 else max(var['high'][-fr:]))
    
    if 'candle' not in var_prices:
        var_prices['candle']=[]
        for i in range(len(var['time'])):
            if var['close'][i]>var['open'][i]:
                ccolor='#3ba3bc'
            elif var['close'][i]<var['open'][i]:
                ccolor='#264f5a'
            else:
                ccolor='gray'
            oc_price=plot_price.plot([var['time'].index(var['time'][i])]*2,[var['open'][i],var['close'][i]],pen=line_style(ccolor,3,'line'))
            hl_price=plot_price.plot([var['time'].index(var['time'][i])]*2,[var['high'][i],var['low'][i]],pen=line_style(ccolor,0.5,'line'))

            var_prices['candle'].append([oc_price,hl_price])
    else:
        ccolor='#3ba3bc' if var['close'][-1]>var['open'][-1] else '#264f5a' if var['close'][-1]<var['open'][-1] else 'gray'

        if val=='nc':
            oc_price=plot_price.plot([len(var['time'])-1]*2,[var['open'][-1],var['close'][-1]],pen=line_style(ccolor, 3, 'line'))
            hl_price=plot_price.plot([len(var['time'])-1]*2,[var['high'][-1],var['low'][-1]],pen=line_style(ccolor,0.5,'line'))
            var_prices['candle'].append([oc_price,hl_price])
        else:
            var_prices['candle'][-1][0].setData([len(var['time'])-2]*2,[var['open'][-1],var['close'][-1]])
            var_prices['candle'][-1][0].setPen(line_style(ccolor, 3, 'line'))
            var_prices['candle'][-1][1].setData([len(var['time'])-2]*2,[var['high'][-1],var['low'][-1]])
            var_prices['candle'][-1][1].setPen(line_style(ccolor,0.5,'line'))
    
    if 'BidAsk' not in var_prices:
        bid_price=pg.InfiniteLine(pos=var['bid'][-1],angle=0,pen=line_style('darkblue',0.5,'line'))
        ask_price=pg.InfiniteLine(pos=var['ask'][-1],angle=0,pen=line_style('darkred',0.5,'line'))
        plot_price.addItem(bid_price)
        plot_price.addItem(ask_price)
        var_prices['BidAsk']=[bid_price,ask_price]
    else:
        var_prices['BidAsk'][0].setPos(var['bid'][-1])
        var_prices['BidAsk'][1].setPos(var['ask'][-1])

    if 'alligator' not in var_prices:
        lips_price=plot_price.plot(list(range(len(var['time'][0:-1]))),var['lips'][0:-1],pen=line_style(get_settings['william_settings']['alligator']['lips'][1],0.7,'line'))
        teeth_price=plot_price.plot(list(range(len(var['time'][0:-1]))),var['teeth'][0:-1],pen=line_style(get_settings['william_settings']['alligator']['teeths'][1],0.7,'line'))
        jaw_price=plot_price.plot(list(range(len(var['time'][0:-1]))),var['jaw'][0:-1],pen=line_style(get_settings['william_settings']['alligator']['jaw'][1],0.7,'line'))
        var_prices['alligator']=[lips_price,teeth_price,jaw_price]
    else:
        var_prices['alligator'][0].setData(list(range(len(var['time'][0:-1]))), var['lips'][0:-1])
        var_prices['alligator'][1].setData(list(range(len(var['time'][0:-1]))), var['teeth'][0:-1])
        var_prices['alligator'][2].setData(list(range(len(var['time'][0:-1]))), var['jaw'][0:-1])

    up_frac_dates=[var['time'].index(i[0]) for i in var['up'] if i[0] in var['time']]
    up_frac_prices=[i[1]*(1+2e-5) for i in var['up'] if i[0] in var['time']]
    down_frac_dates=[var['time'].index(i[0]) for i in var['down'] if i[0] in var['time']]
    down_frac_prices=[i[1]*(1-2e-5) for i in var['down'] if i[0] in var['time']]
    up_color,down_color=get_settings['william_settings']['fractals']['up'],get_settings['william_settings']['fractals']['down']
    if 'fractal' not in var_prices:
        up_prices=plot_price.plot(up_frac_dates,up_frac_prices,pen=None,symbol='t1',symbolSize=5,symbolBrush=up_color,symbolPen=pg.mkPen(up_color,width=1))
        down_prices=plot_price.plot(down_frac_dates,down_frac_prices,pen=None,symbol='t',symbolSize=5,symbolBrush=down_color,symbolPen=pg.mkPen(down_color,width=1))
        var_prices['fractal']=[up_prices,down_prices]
    else:
        var_prices['fractal'][0].setData(up_frac_dates,up_frac_prices)
        var_prices['fractal'][0].setSymbolBrush(up_color)
        var_prices['fractal'][0].setSymbolPen(pg.mkPen(up_color, width=1))
        var_prices['fractal'][1].setData(down_frac_dates,down_frac_prices)
        var_prices['fractal'][1].setSymbolBrush(down_color)
        var_prices['fractal'][1].setSymbolPen(pg.mkPen(down_color, width=1))
                
def plot_AO(var,var_prices,get_settings,get_widgets,fr,val):

    plot_awesome=get_widgets['plot_awesome']

    if 'awesome' not in var_prices:
        plot_awesome.clear()
        var_prices['awesome']=[]
        for i in range(len(var['time'])):
            if var['ao'][i]>0:
                ccolor=get_settings['william_settings']['awesome']['up']
            elif var['ao'][i]<0:
                ccolor=get_settings['william_settings']['awesome']['down']
            else:
                ccolor='gray'
            ao_bar=plot_awesome.plot([var['time'].index(var['time'][i])]*2,[0,var['ao'][i]],pen=line_style(ccolor,5,'line'))
            var_prices['awesome'].append(ao_bar)
    else:
        ccolor=get_settings['william_settings']['awesome']['up']  if var['ao'][-1]>0 else get_settings['william_settings']['awesome']['down'] if var['ao'][-1]<0 else 'gray'
        if val=='nc':
            ao_bar=plot_awesome.plot([len(var['time'])-2]*2,[0,var['ao'][-1]],pen=line_style(ccolor,5,'line'))
            var_prices['awesome'].append(ao_bar)
        else:
            var_prices['awesome'][-1].setData([len(var['time'])-2]*2,[0,var['ao'][-1]])
            var_prices['awesome'][-1].setPen(line_style(ccolor, 5, 'line'))
        

def update_table(var,table):
    row_index=table.rowCount()
    table.insertRow(row_index)

    columns=['tick_time','bid']
    for col in range(len(columns)):
        item = qt.QTableWidgetItem(str(var['tick_time'][-1].split(' ')[1]) if columns[col]=='tick_time' else str(round(var['bid'][-1],5)))
        item.setTextAlignment(qcore.Qt.AlignmentFlag.AlignLeft)
        table.setItem(row_index, col, item)

    table.scrollToItem(table.item(row_index, 0))

#--------------------------------------------------------------------------------------------------------------------------------------------------

def run_live(get_settings,get_widgets):

    candle_variables=['id','tick_time','bid','ask','time','open','high','low','close']
    william_variables=['lips','teeth','jaw','up','down','fast_ao','slow_ao','ao']
    variables=candle_variables+william_variables
    var={i:[] for i in variables}
    for v in variables:
        var[v].clear()

    table=get_widgets['table']
    table.setRowCount(0)

    fr=80
    var_prices={}
    var_prices.clear()

    symbol=get_settings['symbol']
    interval=get_settings['interval']
    alligator_values=[v[0] for v in get_settings['william_settings']['alligator'].values()]
    fractal_value=get_settings['william_settings']['fractals']['fractal']
    awesome_values=[get_settings['william_settings']['awesome']['fast'],get_settings['william_settings']['awesome']['slow']]

    initial_time=datetime.now()-timedelta(minutes=fr*n_candles(interval))
    
    while get_settings['active_live'][0]:
        
        indi.get_data(symbol,var,initial_time,fr)
        val=indi.order_data(var,interval)
        indi.candles(var,val)
        indi.alligator(alligator_values,'high','low',var,val)
        indi.fractals(fractal_value,var,val)
        indi.awesome(awesome_values,'high','low',var,val)
        print_data(symbol,var,val)
        
        if len(var['time'])>fr:
            get_widgets['widgetSignals'].updatePlot.emit(var,var_prices,get_settings,get_widgets,fr,val)
            get_widgets['widgetSignals'].updateAwesome.emit(var,var_prices,get_settings,get_widgets,fr,val)
            time.sleep(0.5)

        get_widgets['widgetSignals'].updateTable.emit(var,table)

    get_settings['active_live'][0]=False
    button_start=get_widgets['start_button']
    button_stop=get_widgets['stop_button']
    get_widgets['widgetSignals'].enable_buttons.emit(button_start,button_stop,True,False)
        
