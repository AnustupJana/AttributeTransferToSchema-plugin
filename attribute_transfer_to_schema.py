# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AttributeTransferToSchema
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import QgsProject, QgsFeature, QgsFeatureSink
from qgis.utils import iface
from .attribute_transfer_to_schema_dialog import AttributeTransferToSchemaDialog
import os.path
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AttributeTransferToSchema:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor."""
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AttributeTransferToSchema_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&Attribute Transfer to Schema')
        self.dlg = None

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QCoreApplication.translate('AttributeTransferToSchema', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'Attribute Transfer to Schema'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&Attribute Transfer to Schema'), action)
            self.iface.removeToolBarIcon(action)
        if self.dlg:
            self.dlg.close()
            self.dlg = None

    def transfer_features_with_mapping(self, dialog):
        """Execute the feature transfer with attribute mapping."""
        try:
            field_mapping, template_layer, source_layer = dialog.get_mapping()
            logger.debug(f"Field mapping: {field_mapping}")
            logger.debug(f"Template layer: {template_layer.name() if template_layer else 'None'}")
            logger.debug(f"Source layer: {source_layer.name() if source_layer else 'None'}")

            if not template_layer or not source_layer:
                QMessageBox.critical(None, "Error", "Invalid layer selection. Ensure both template and source layers are valid.")
                return

            # Validate geometry compatibility
            if template_layer.wkbType() != source_layer.wkbType():
                QMessageBox.critical(None, "Error", "Template and Source layers have incompatible geometry types.")
                return

            # Start editing template layer
            if not template_layer.isEditable():
                if not template_layer.startEditing():
                    QMessageBox.critical(None, "Error", "Cannot edit Template layer.")
                    return

            # Clear existing features in template layer
            if not template_layer.dataProvider().truncate():
                template_layer.rollBack()
                QMessageBox.critical(None, "Error", "Failed to clear Template layer.")
                return

            # Copy features with mapped attributes
            template_fields = [field.name() for field in template_layer.fields()]
            for feature in source_layer.getFeatures():
                new_feature = QgsFeature(template_layer.fields())
                new_feature.setGeometry(feature.geometry())
                for template_field in template_fields:
                    if template_field in field_mapping:
                        source_field = field_mapping[template_field]
                        source_value = feature[source_field]
                        new_feature.setAttribute(template_field, source_value)
                    else:
                        new_feature.setAttribute(template_field, None)
                if not template_layer.dataProvider().addFeature(new_feature):
                    template_layer.rollBack()
                    QMessageBox.critical(None, "Error", "Failed to add feature to Template layer.")
                    return

            # Commit changes
            if template_layer.commitChanges():
                self.iface.messageBar().pushMessage("Success", "Features transferred successfully.", level=3, duration=5)
            else:
                template_layer.rollBack()
                QMessageBox.critical(None, "Error", "Failed to commit changes to Template layer.")

        except Exception as e:
            logger.error(f"Error in transfer_features_with_mapping: {str(e)}")
            QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")

    def run(self):
        """Run method that performs all the real work."""
        try:
            # Always create a new dialog to avoid deleted object errors
            self.dlg = AttributeTransferToSchemaDialog(self.iface.mainWindow())
            logger.debug("Dialog initialized")

            self.dlg.show()
            result = self.dlg.exec_()
            if result:
                self.transfer_features_with_mapping(self.dlg)
            else:
                QMessageBox.information(None, "Info", "Operation cancelled.")
            self.dlg = None  # Clear dialog reference after use
        except Exception as e:
            logger.error(f"Error in run method: {str(e)}")
            QMessageBox.critical(None, "Error", f"Failed to open dialog: {str(e)}")
            self.dlg = None