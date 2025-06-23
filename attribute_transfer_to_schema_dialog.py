# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AttributeTransferToSchemaDialog
                                 A QGIS plugin
 Attribute Transfer to Schema is a QGIS plugin that enables seamless transfer of attribute data from a source vector layer to a template layer with a predefined schema. It features a user-friendly interface with dropdown lists to manually map fields
                             -------------------
        begin                : 2025-06-22
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QGroupBox
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AttributeTransferToSchemaDialog(QDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)
        self.template_layer = None
        self.source_layer = None
        self.mapping = {}
        self.combos = {}
        self.attribute_layout = None
        self.init_ui()

    def init_ui(self):
        """Set up the dialog UI programmatically."""
        try:
            logger.debug("Starting to set up the dialog UI")
            self.setWindowTitle("Attribute Transfer to Schema")
            self.setMinimumWidth(500)

            main_layout = QVBoxLayout()

            # Initialize layers and layer names
            self.layers = [layer for layer in QgsProject.instance().mapLayers().values() if layer.type() == 0]  # Vector layers only
            self.layer_names = [layer.name() for layer in self.layers]
            logger.debug(f"Initial layer list: {self.layer_names}")

            # Check if layers are available
            if not self.layer_names:
                QMessageBox.critical(None, "Error", "No vector layers found in the project.")
                self.reject()
                return

            # Group Box 1: Input Layers
            input_layers_group = QGroupBox("Input Layers")
            input_layers_layout = QVBoxLayout()

            template_layout = QHBoxLayout()
            template_label = QLabel("Template Layer:")
            self.template_combo = QComboBox()
            self.template_combo.addItems(self.layer_names)
            if "Template" in self.layer_names:
                self.template_combo.setCurrentText("Template")
            template_layout.addWidget(template_label)
            template_layout.addWidget(self.template_combo)
            input_layers_layout.addLayout(template_layout)

            source_layout = QHBoxLayout()
            source_label = QLabel("Source Layer:")
            self.source_combo = QComboBox()
            self.source_combo.addItems(self.layer_names)
            if "Source" in self.layer_names:
                self.source_combo.setCurrentText("Source")
            source_layout.addWidget(source_label)
            source_layout.addWidget(self.source_combo)
            input_layers_layout.addLayout(source_layout)

            input_layers_group.setLayout(input_layers_layout)
            main_layout.addWidget(input_layers_group)

            # Group Box 2: Field Selection
            field_selection_group = QGroupBox("Field Selection")
            self.attribute_layout = QVBoxLayout()
            self.combos = {}
            self.update_attribute_mapping()
            field_selection_group.setLayout(self.attribute_layout)
            main_layout.addWidget(field_selection_group)

            # Connect layer changes to update attribute mapping
            self.template_combo.currentIndexChanged.connect(self.update_attribute_mapping)
            self.source_combo.currentIndexChanged.connect(self.update_attribute_mapping)

            # Buttons
            button_layout = QHBoxLayout()
            ok_button = QPushButton("OK")
            cancel_button = QPushButton("Cancel")
            ok_button.clicked.connect(self.accept)
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            main_layout.addLayout(button_layout)

            self.setLayout(main_layout)
            logger.debug("Dialog UI setup completed")
        except Exception as e:
            logger.error(f"Error in init_ui: {str(e)}")
            QMessageBox.critical(None, "Error", f"Failed to initialize dialog: {str(e)}")
            self.reject()

    def update_attribute_mapping(self):
        """Update the attribute mapping dropdowns based on selected layers."""
        try:
            logger.debug("Updating attribute mapping")
            # Disconnect signals to prevent multiple calls
            try:
                self.template_combo.currentIndexChanged.disconnect()
                self.source_combo.currentIndexChanged.disconnect()
            except TypeError:
                pass  # Signals may not be connected yet

            # Refresh layer list
            self.layers = [layer for layer in QgsProject.instance().mapLayers().values() if layer.type() == 0]
            self.layer_names = [layer.name() for layer in self.layers]
            logger.debug(f"Updated layer list: {self.layer_names}")

            # Update dropdowns
            current_template = self.template_combo.currentText()
            current_source = self.source_combo.currentText()
            self.template_combo.clear()
            self.source_combo.clear()
            self.template_combo.addItems(self.layer_names)
            self.source_combo.addItems(self.layer_names)
            if current_template in self.layer_names:
                self.template_combo.setCurrentText(current_template)
            if current_source in self.layer_names:
                self.source_combo.setCurrentText(current_source)

            # Reconnect signals
            self.template_combo.currentIndexChanged.connect(self.update_attribute_mapping)
            self.source_combo.currentIndexChanged.connect(self.update_attribute_mapping)

            # Clear existing attribute mapping widgets safely
            if self.attribute_layout:
                while self.attribute_layout.count():
                    item = self.attribute_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                    elif item.layout():
                        layout = item.layout()
                        while layout.count():
                            sub_item = layout.takeAt(0)
                            if sub_item.widget():
                                sub_item.widget().deleteLater()
                        layout.deleteLater()
            self.combos = {}

            # Get selected layer names
            template_name = self.template_combo.currentText()
            source_name = self.source_combo.currentText()
            logger.debug(f"Selected template: {template_name}")
            logger.debug(f"Selected source: {source_name}")

            # Fetch layers
            self.template_layer = None
            self.source_layer = None
            for layer in self.layers:
                if layer.name() == template_name:
                    self.template_layer = layer
                if layer.name() == source_name:
                    self.source_layer = layer

            # Validate layers before accessing fields
            if not self.template_layer or not self.source_layer:
                logger.debug("No valid layers selected")
                return

            # Ensure layers are valid QGIS layers
            if not self.template_layer.isValid() or not self.source_layer.isValid():
                logger.error(f"Invalid layers: Template valid={self.template_layer.isValid() if self.template_layer else False}, Source valid={self.source_layer.isValid() if self.source_layer else False}")
                return

            template_fields = [field.name() for field in self.template_layer.fields()]
            source_fields = [field.name() for field in self.source_layer.fields()]
            source_fields.insert(0, "<None>")

            for template_field in template_fields:
                h_layout = QHBoxLayout()
                label = QLabel(f"Template: {template_field}")
                combo = QComboBox()
                combo.addItems(source_fields)
                combo.setMinimumWidth(200)
                for src_field in source_fields[1:]:
                    if template_field.lower() == src_field.lower() or \
                       template_field.lower() in src_field.lower() or \
                       src_field.lower() in template_field.lower():
                        combo.setCurrentText(src_field)
                        break
                h_layout.addWidget(label)
                h_layout.addWidget(combo)
                self.attribute_layout.addLayout(h_layout)
                self.combos[template_field] = combo
            logger.debug("Attribute mapping updated")
        except Exception as e:
            logger.error(f"Error in update_attribute_mapping: {str(e)}")
            QMessageBox.critical(None, "Error", f"Error updating field mappings: {str(e)}")

    def get_mapping(self):
        """Return the field mapping and selected layers."""
        try:
            # Refresh layer list
            self.layers = [layer for layer in QgsProject.instance().mapLayers().values() if layer.type() == 0]
            self.layer_names = [layer.name() for layer in self.layers]
            logger.debug(f"Layer list in get_mapping: {self.layer_names}")

            # Get selected layer names
            template_name = self.template_combo.currentText()
            source_name = self.source_combo.currentText()
            logger.debug(f"Template name in get_mapping: {template_name}")
            logger.debug(f"Source name in get_mapping: {source_name}")

            # Fetch layers
            self.template_layer = None
            self.source_layer = None
            for layer in self.layers:
                if layer.name() == template_name:
                    self.template_layer = layer
                if layer.name() == source_name:
                    self.source_layer = layer

            if not self.template_layer or not self.source_layer:
                logger.error(f"Invalid layers: Template={template_name}, Source={source_name}")
                return {}, None, None

            # Validate layer integrity
            if not self.template_layer.isValid() or not self.source_layer.isValid():
                logger.error(f"Invalid layers: Template valid={self.template_layer.isValid()}, Source valid={self.source_layer.isValid()}")
                return {}, None, None

            for template_field, combo in self.combos.items():
                source_field = combo.currentText()
                if source_field != "<None>":
                    self.mapping[template_field] = source_field
            logger.debug(f"Mapping retrieved: {self.mapping}")
            return self.mapping, self.template_layer, self.source_layer
        except Exception as e:
            logger.error(f"Error in get_mapping: {str(e)}")
            return {}, None, None