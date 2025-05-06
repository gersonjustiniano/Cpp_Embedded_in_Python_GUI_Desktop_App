

accept_cancel_style="""
    QPushButton{
        background-color:#9c9c9c;
        color:black;
        font-size:16px;
        border-radius:10px;
    }
    QPushButton:pressed{
        background-color: #7c7c7c;
        color: black;
        border: 2px solid black;
    }
"""

stop_style="""
    QPushButton{
        background-color: darkred;
        color:black;
        font-size:16px;
        border-radius:10px;
    }
    QPushButton:pressed{
        background-color: darkred;
        color: black;
        border: 2px solid black;
    }
"""

start_style="""
    QPushButton{
        background-color: darkgreen;
        color:black;
        font-size:16px;
        border-radius:10px;
    }
    QPushButton:pressed{
        background-color: darkgreen;
        color: black;
        border: 2px solid black;
    }
"""

label_symbol_style="""
    background-color:#1c1c1c;
    color:white;
    font-size:16px;
    border-radius:10px;
    text-align:center;
    padding:1px;
"""

combo_symbol_style="""
    QComboBox {
        background-color: gray;     /* Fondo del combo box */
        color: black;               /* Color del texto */
        border: 1px solid black;    /* Borde gris */
        border-radius: 5px;         /* Bordes redondeados */
        font-size: 16px;            /* Tamano de la fuente */
        padding: 1px;
    }
    QComboBox QAbstractItemView {
        background-color: gray;                 /* Fondo de los ├¡tems desplegados */
        color: black;                           /* Color de los textos en la lista */
        border: 1px solid #555555;              /* Borde de la lista */
        selection-background-color: #0078d7;    /* Fondo cuando un ├¡tem est├í seleccionado */
        selection-color: white;                 /* Color de texto cuando un ├¡tem est├í seleccionado */
    }
"""

label_interval_style="""
    background-color:#1c1c1c;
    color:white;
    font-size:16px;
    border-radius:10px;
    text-align:center;
    padding:1px;
"""

combo_interval_style="""
    QComboBox {
        background-color: gray;     /* Fondo del combo box */
        color: black;               /* Color del texto */
        border: 1px solid black;    /* Borde gris */
        border-radius: 5px;         /* Bordes redondeados */
        font-size: 16px;            /* Tamano de la fuente */
        padding: 1px;
    }
    QComboBox QAbstractItemView {
        background-color: gray;                 /* Fondo de los ├¡tems desplegados */
        color: black;                           /* Color de los textos en la lista */
        border: 1px solid #555555;              /* Borde de la lista */
        selection-background-color: #0078d7;    /* Fondo cuando un ├¡tem est├í seleccionado */
        selection-color: white;                 /* Color de texto cuando un ├¡tem est├í seleccionado */
    }
"""

label_settings_style="""
    background-color:#1c1c1c;
    color:white;
    font-size:16px;
    border-radius:10px;
    text-align:center;
    padding:1px;
"""

combo_settings_style="""
    QComboBox {
        background-color: gray;     /* Fondo del combo box */
        color: black;               /* Color del texto */
        border: 1px solid black;    /* Borde gris */
        border-radius: 5px;         /* Bordes redondeados */
        font-size: 16px;            /* Tamano de la fuente */
        padding: 1px;
    }
    QComboBox QAbstractItemView {
        background-color: gray;                 /* Fondo de los ├¡tems desplegados */
        color: black;                           /* Color de los textos en la lista */
        border: 1px solid #555555;              /* Borde de la lista */
        selection-background-color: #0078d7;    /* Fondo cuando un ├¡tem est├í seleccionado */
        selection-color: white;                 /* Color de texto cuando un ├¡tem est├í seleccionado */
    }
"""

button_settings_style="""
    QPushButton{
        background-color: darkblue;
        color:gray;
        font-size:16px;
        font-weight: bold;
        border-radius:10px;
        padding-bottom: 8px;
    }
    QPushButton:pressed{
        background-color: darkblue;
        color: black;
        font-size:16px;
        font-weight: bold;
        border: 2px solid black;
    }
"""

label_config_style="""
    background-color: black;
    color:white;
    font-size:16px;
    border-radius:10px;
    text-align:center;
    padding:1px;
"""

table_style="""
    QTableWidget {
        background-color:black;
        color:white;
        font-size:14px;
    }
    QHeaderView::section {
        background-color: #2c2c2c;
        color: white;
        font-size: 14px;
        height:15px;
        padding: 1px;
        font-weight: bold;
        border: 1px solid black;
    }
    QTableWidget::item {
        selection-background-color: black;
        selection-color: white;
    }
    QTableWidget::item:selected {
        background-color: #3c3c3c;
        border: 1px solid black;
    }

    QScrollBar:vertical {
        background: #f0f0f0;
        width: 10px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #c0c0c0;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover {
        background: #a0a0a0;
    }
    QScrollBar::add-line:vertical {
        height: 16px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
        background: #d0d0d0;
        border: none;
    }
    QScrollBar::sub-line:vertical {
        height: 16px;
        subcontrol-position: top;
        subcontrol-origin: margin;
        background: #d0d0d0;
        border: none;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        width: 10px;
        height: 10px;
        background: black;
    }

    QScrollBar:horizontal {
        background: #f0f0f0;
        height: 10px;
        margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background: #c0c0c0;
        min-width: 20px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #a0a0a0;
    }
    QScrollBar::add-line:horizontal {
        width: 16px;
        subcontrol-position: right;
        subcontrol-origin: margin;
        background: #d0d0d0;
        border: none;
    }
    QScrollBar::sub-line:horizontal {
        width: 16px;
        subcontrol-position: left;
        subcontrol-origin: margin;
        background: #d0d0d0;
        border: none;
    }
    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
        width: 10px;
        height: 10px;
        background: black;
    }
"""

spin_style="""
    QSpinBox {
        background-color: black;
        color: white;
        border: 2px solid black;
        border-radius: 5px;
        font-size: 16px;
    }
"""

messageBoxInformation_style="""
    QMessageBox {
        background-color: #1c1c1c;
    }

    QLabel {
        color: white;
        font-size: 14px;
    }

    QPushButton {
        background-color: #3a3a3a;
        color: white;
        border: 1px solid #5a5a5a;
        padding: 5px 12px;
        min-width: 80px;
    }

    QPushButton:hover {
        background-color: #505050;
    }"""

