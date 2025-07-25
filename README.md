# Attribute Transfer to Schema QGIS Plugin
![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/icon.png?raw=true)

## Overview
The **Attribute Transfer to Schema** plugin for QGIS enables seamless transfer of attribute data from a source vector layer to a template layer with a predefined schema. It provides a user-friendly interface with dropdown menus to manually map fields between the source and template layers, ensuring accurate and efficient data transfer.

## Features
- **Layer Selection**: Select source and template vector layers from the current QGIS project using dropdown menus.
- **Field Mapping**: Map fields from the source layer to the template layer's fields, with automatic suggestions for similar field names (case-insensitive partial matches).
- **Data Transfer**: Transfer features from the source layer to the template layer, preserving geometry and applying the mapped attributes. Unmapped fields are set to `NULL`.
- **Geometry Validation**: Ensures compatibility between source and template layer geometry types before transfer.
- **Editable Template Layer**: Automatically clears the template layer and commits changes after successful transfer.
- **Error Handling**: Provides clear error messages for invalid layer selections, geometry mismatches, or editing failures.
- **Logging**: Detailed debug and error logs are available in the QGIS Python Console for troubleshooting.

## Installation
1. **From QGIS Plugin Repository**:
   - In QGIS, go to `Plugins > Manage and Install Plugins`.
  
     ![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/doc/1st.png?raw=true)
   - Search for "Attribute Transfer to Schema" in the `All` tab.

     ![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/doc/2nd.png?raw=true)
   - Click `Install Plugin`.

1. **From ZIP File**:
   - Download the plugin ZIP file from the [GitHub Releases](https://github.com/AnustupJana/AttributeTransferToSchema-plugin.git) page.
   - In QGIS, go to `Plugins > Manage and Install Plugins > Install from ZIP`.
   - Select the downloaded ZIP file and click `Install Plugin`.

1. **Download the Plugin**:
   - Clone or download the plugin repository to your local machine.
   - Alternatively, obtain the zipped plugin folder.

2. **Install in QGIS**:
   - Alternatively, copy the plugin folder to the QGIS plugins directory:
     - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
     - Windows: `C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
     - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

3. **Enable the Plugin**:
   - In QGIS, go to **Plugins > Manage and Install Plugins**.
   - Find **Attribute Transfer to Schema** in the list and ensure it is enabled.

## Usage
1. **Load Vector Layers**:
   - Add at least two vector layers to your QGIS project (e.g., a template layer with fields like `ID, Name, Address, UID, Area, Length, Date` and a source layer with fields like `ID, Nme, Addr, UUID, Shape_Area, Shape_Length, Remark, Others, Date`).

2. **Open the Plugin**:
   - Click the plugin icon in the QGIS toolbar or select **Attribute Transfer to Schema** from the **Plugins** menu.

   ![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/doc/3rd.png?raw=true)

3. **Configure the Dialog**:
   - In the dialog, select the **Template Layer** and **Source Layer** from the dropdown menus.
   - The **Field Selection** section will display dropdowns for each template layer field, allowing you to map corresponding source layer fields. Fields with similar names are pre-selected where possible.
   - Choose `<None>` for any template fields that should remain unmapped (set to `NULL`).

   ![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/doc/4th.png?raw=true)

4. **Run the Transfer**:
   - Click **OK** to start the transfer process.

   ![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/doc/5th.png?raw=true)
   - The plugin will:
     - Validate that both layers have compatible geometry types.
     - Clear existing features in the template layer.
     - Copy features from the source layer, applying the mapped attributes.
     - Commit changes to the template layer.
   - A success message ("Features transferred successfully") will appear in the QGIS message bar, or an error message will indicate any issues.
  
   ![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/doc/6th.png?raw=true)
   
   ![Diagram of the System](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/doc/7th.png?raw=true)

6. **Cancel or Close**:
   - Click **Cancel** to close the dialog without performing the transfer.

## Requirements
- **QGIS Version**: 3.0 or higher (tested up to QGIS 3.34).
- **Layer Types**: Both source and template layers must be vector layers with compatible geometry types (e.g., both must be points, lines, or polygons).
- **Editable Template Layer**: The template layer must support editing (e.g., not read-only).

## Troubleshooting
- **QGIS Crashes or Errors**:
  - Check the QGIS Python Console (Ctrl+Alt+P) for `DEBUG` or `ERROR` messages from `AttributeTransferToSchema`.
  - Ensure both layers are valid vector layers and listed in the QGIS Layers panel.
  - Verify that layer names in the dropdowns match those in the project exactly.
- **"Invalid layer selection" Error**:
  - Confirm that both template and source layers are selected and valid.
  - Ensure no layers were removed or renamed during the dialog session.
- **No Vector Layers Available**:
  - Add at least one vector layer to the QGIS project before running the plugin.
- **Log Output**:
  - Logs are available in the QGIS Python Console, including layer lists, selected layers, and error details. Share these with developers for support.

- **Contributing**:
  - Fork the repository and submit pull requests with improvements or bug fixes.
  - Report issues or feature requests via the repository's [issue](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/issues) tracker.

## License
This plugin is licensed under the **GNU General Public License v2.0 or later**. See the [LICENSE](https://github.com/AnustupJana/AttributeTransferToSchema-plugin/blob/main/LICENSE) file for details.

## Author
- **Name**: Anustup Jana
- **Email**: anustupjana21@gmail.com
- **Copyright**: © 2025 Anustup Jana

