# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AttributeTransferToSchema
                                 A QGIS plugin
 Attribute Transfer to Schema is a QGIS plugin that enables seamless transfer of attribute data from a source vector layer to a template layer with a predefined schema
                             -------------------
        begin                : 2025-06-22
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AttributeTransferToSchema class from file AttributeTransferToSchema.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .attribute_transfer_to_schema import AttributeTransferToSchema
    return AttributeTransferToSchema(iface)
