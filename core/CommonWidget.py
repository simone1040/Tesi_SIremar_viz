from PyQt5.QtWidgets import QLabel, QSpacerItem, QSizePolicy, QHBoxLayout

from utils.Costants import VERSION


def footer(verticalLayoutWidget):
    footer_layout = QHBoxLayout()
    footer_layout.setContentsMargins(-1, -1, -1, 5)
    footer_layout.setSpacing(6)
    footer_layout.setObjectName("footer_layout")
    spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    footer_layout.addItem(spacerItem10)
    label_product_by = QLabel(verticalLayoutWidget)
    label_product_by.setObjectName("label_product_by")
    label_product_by.setText("Copyright Simone Condorelli")
    footer_layout.addWidget(label_product_by)
    spacerItem11 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
    footer_layout.addItem(spacerItem11)
    label_5 = QLabel(verticalLayoutWidget)
    label_5.setObjectName("label_5")
    label_5.setText("Version :")
    footer_layout.addWidget(label_5)
    spacerItem12 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
    footer_layout.addItem(spacerItem12)
    label_version = QLabel(verticalLayoutWidget)
    label_version.setObjectName("label_version")
    label_version.setText(VERSION)
    footer_layout.addWidget(label_version)
    return footer_layout