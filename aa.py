from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QFormLayout,
    QLineEdit, QLabel, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestão de Produtos")
        self.setGeometry(100, 100, 600, 400)

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Add tabs
        self.tab_widget.addTab(self.create_product_source_tab(), "Produto Fonte")
        self.tab_widget.addTab(self.create_original_product_tab(), "Produto Original")

        # Storage for product source data
        self.product_source_data = {}

    def create_product_source_tab(self):
        """Create the 'Produto Fonte' tab."""
        tab = QWidget()
        layout = QFormLayout()

        # Input fields
        self.description_input = QLineEdit()
        self.width_input = QLineEdit()
        self.thickness_input = QLineEdit()
        self.wood_type_input = QLineEdit()  # Changed to QLineEdit for custom wood type
        self.cubic_meter_price_input = QLineEdit()

        # Add fields to layout
        layout.addRow("Descrição:", self.description_input)
        layout.addRow("Largura (cm):", self.width_input)
        layout.addRow("Espessura (cm):", self.thickness_input)
        layout.addRow("Tipo de Madeira:", self.wood_type_input)
        layout.addRow("Valor por m³ (R$):", self.cubic_meter_price_input)

        # Save button
        self.save_button = QLabel("Pressione Enter para salvar produto fonte")
        self.cubic_meter_price_input.returnPressed.connect(self.save_product_source)
        layout.addRow(self.save_button)

        # Set layout
        tab.setLayout(layout)
        return tab

    def create_original_product_tab(self):
        """Create the 'Produto Original' tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # Input fields
        self.source_product_selector = QComboBox()
        self.linear_meter_price_input = QLineEdit()
        self.calculated_linear_price_label = QLabel("Preço calculado por metro linear: R$ 0.00")
        self.profit_label = QLabel("Lucro: 0% (R$ 0.00)")

        # Connect events
        self.source_product_selector.currentIndexChanged.connect(self.load_source_product_data)
        self.linear_meter_price_input.textChanged.connect(self.update_profit)

        # Add fields to form layout
        form_layout.addRow("Produto Fonte:", self.source_product_selector)
        form_layout.addRow("Preço calculado por metro linear (R$):", self.calculated_linear_price_label)
        form_layout.addRow("Valor por metro linear (R$):", self.linear_meter_price_input)
        form_layout.addRow("Lucro:", self.profit_label)

        layout.addLayout(form_layout)
        tab.setLayout(layout)
        return tab

    def save_product_source(self):
        """Save product source data."""
        description = self.description_input.text()
        width = self.width_input.text()
        thickness = self.thickness_input.text()
        wood_type = self.wood_type_input.text()
        cubic_meter_price = self.cubic_meter_price_input.text()

        if description and cubic_meter_price:
            display_name = f"{description} - {width}x{thickness} - {wood_type}"
            self.product_source_data[display_name] = {
                "width": float(width) / 100 if width else 0,
                "thickness": float(thickness) / 100 if thickness else 0,
                "wood_type": wood_type,
                "cubic_meter_price": float(cubic_meter_price)
            }
            self.source_product_selector.addItem(display_name)
            self.save_button.setText("Produto salvo com sucesso!")
        else:
            self.save_button.setText("Por favor, preencha todos os campos obrigatórios!")

    def load_source_product_data(self):
        """Load data from the selected source product."""
        product_name = self.source_product_selector.currentText()
        if product_name in self.product_source_data:
            data = self.product_source_data[product_name]
            self.cubic_meter_price = data["cubic_meter_price"]
            width = data["width"]
            thickness = data["thickness"]
            if width > 0 and thickness > 0:
                volume_per_linear_meter = width * thickness * 1  # 1 meter linear
                linear_price = self.cubic_meter_price * volume_per_linear_meter
                self.calculated_linear_price_label.setText(f"Preço calculado por metro linear: R$ {linear_price:.2f}")
            else:
                self.calculated_linear_price_label.setText("Preço calculado por metro linear: R$ 0.00")
        else:
            self.cubic_meter_price = 0.0
            self.calculated_linear_price_label.setText("Preço calculado por metro linear: R$ 0.00")

    def update_profit(self):
        """Update the profit label based on input values."""
        try:
            linear_price = float(self.linear_meter_price_input.text())
            cubic_price = self.cubic_meter_price

            if cubic_price > 0:
                profit = ((linear_price - cubic_price) / cubic_price) * 100
                profit_value = linear_price - cubic_price
                self.profit_label.setText(f"Lucro: {profit:.2f}% (R$ {profit_value:.2f})")
            else:
                self.profit_label.setText("Lucro: 0% (R$ 0.00)")
        except ValueError:
            self.profit_label.setText("Lucro: 0% (R$ 0.00)")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())