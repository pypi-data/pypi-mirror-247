#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Any, Union, Optional, List, Tuple
from epyk.core.py import primitives, types
from epyk.core.js.packages import JsPackage
from epyk.core.js import JsUtils
from epyk.core.js.primitives import JsObjects


class ColumnComponent(JsPackage):
  lib_alias = {"js": "ag-grid-community", "css": "ag-grid-community"}
  lib_selector = "column"

  @property
  def field(self):
    return JsObjects.JsObject.JsObject("%s.colDef.field" % self.varId)

  def getId(self):
    return JsObjects.JsString.JsString("%s.getId()" % self.varId)

  def cellStyle(self, js_funcs: types.JS_FUNCS_TYPES, profile: types.PROFILE_TYPE = None, func_ref: bool = False):
    """This sub function will use p as sub parameter to not corrupt the main event.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/column-definitions/#default-column-definitions>`_

    :param js_funcs: The Javascript functions
    :param profile: Optional. A flag to set the component performance storage
    :param func_ref: Optional. Specify if js_funcs point to an external function
    """
    if not isinstance(js_funcs, list):
      js_funcs = [js_funcs]
    str_func = JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)
    if not str_func.startswith("function(p)") and not func_ref:
      str_func = "function(p){%s}" % str_func
    return JsUtils.jsWrap(str_func)


class DataComponent(JsPackage):
  lib_alias = {"js": "ag-grid-community", "css": "ag-grid-community"}
  lib_selector = "data"


class NodeComponent(JsPackage):
  lib_alias = {"js": "ag-grid-community", "css": "ag-grid-community"}
  lib_selector = "node"

  @property
  def id(self):
    return JsObjects.JsString.JsString("%s.id" % self.varId)


class _Export:

  @property
  def column(self):
    return ColumnComponent(selector="param.column")

  @property
  def data(self):
    return DataComponent(selector="param.data")

  @property
  def node(self):
    return NodeComponent(selector="param.node")

  @property
  def param(self):
    """ Variable received in the aggrid methods. """
    return JsObjects.JsObject.JsObject("param")

  @property
  def newValue(self):
    """  """
    return JsObjects.JsObject.JsObject("param.newValue")

  @property
  def oldValue(self):
    """ """
    return JsObjects.JsObject.JsObject("param.oldValue")

  def rowIndex(self, js_code: str = "param"):
    return JsObjects.JsNumber.JsNumber("%s.rowIndex" % js_code)


class ColumnApi:

  def __init__(self, page: primitives.PageModel, js_code: str):
    self.varId = js_code
    self.page = page

  def sizeColumnsToFit(self, width):
    """Gets the grid to size the columns to the specified width in pixels, e.g. sizeColumnsToFix(900).
    To have the grid fit the columns to the grid's width, use the Grid API gridApi.sizeColumnsToFit() instead.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param width:
    """
    return JsObjects.JsVoid("%s.sizeColumnsToFit(%s)" % (self.varId, JsUtils.jsConvertData(width, None)))

  def getColumnGroup(self, name: str):
    """Returns the column group with the given name.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param name:
    """
    return JsObjects.JsVoid("%s.getColumnGroup(%s)" % (self.varId, JsUtils.jsConvertData(name, None)))

  def getColumn(self, name: str):
    """Returns the column with the given colKey, which can either be the colId (a string) or the colDef (an object).

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param name:
    """
    return JsObjects.JsVoid("%s.getColumn(%s)" % (self.varId, JsUtils.jsConvertData(name, None)))

  def getColumnState(self):
    """Gets the state of the columns. It is used when saving column state.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.getColumnState()" % self.varId)

  def setColumnState(self, column_state):
    """Sets the state of the columns from a previous state. Returns false if one or more columns could not be found.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.setColumnState(%s)" % (self.varId, JsUtils.jsConvertData(column_state, None)))

  def resetColumnState(self):
    """Sets the state back to match the originally provided column definitions.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.resetColumnState()" % self.varId)

  def isPinning(self):
    """Returns true if pinning left or right, otherwise false.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.isPinning()" % self.varId)

  def isPinningLeft(self):
    """Returns true if pinning left, otherwise false.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.isPinningLeft()" % self.varId)

  def isPinningRight(self):
    """Returns true if pinning right, otherwise false.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.isPinningRight()" % self.varId)

  def setColumnVisible(self, col_name: str, visible: bool):
    """
    Sets the visibility of a column. Key can be the column ID or Column object.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param col_name: The column name
    :param visible:
    """
    col_name = JsUtils.jsConvertData(col_name, None)
    visible = JsUtils.jsConvertData(visible, None)
    return JsObjects.JsVoid("%s.setColumnVisible(%s. %s)" % (self.varId, col_name, visible))

  def setColumnsVisible(self, col_names, visible):
    """Same as setColumnVisible, but provide a list of column keys.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    col_names = JsUtils.jsConvertData(col_names, None)
    visible = JsUtils.jsConvertData(visible, None)
    return JsObjects.JsVoid("%s.setColumnsVisible(%s. %s)" % (self.varId, col_names, visible))

  def setColumnPinned(self, col_name: str, pinned: bool):
    """Sets the column pinned / unpinned. Key can be the column ID, field, ColDef object or Column object.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    col_name = JsUtils.jsConvertData(col_name, None)
    pinned = JsUtils.jsConvertData(pinned, None)
    return JsObjects.JsVoid("%s.setColumnPinned(%s. %s)" % (self.varId, col_name, pinned))

  def setColumnsPinned(self, col_names, pinned):
    """Sets the column pinned / unpinned. Key can be the column ID, field, ColDef object or Column object.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    col_names = JsUtils.jsConvertData(col_names, None)
    pinned = JsUtils.jsConvertData(pinned, None)
    return JsObjects.JsVoid("%s.setColumnsPinned(%s. %s)" % (self.varId, col_names, pinned))

  def getColumnGroupState(self):
    """Gets the state of the column groups. Typically used when saving column group state.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.getColumnGroupState()" % self.varId)

  def autoSizeColumn(self, col_name: str):
    """Auto-sizes a column based on its contents.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.autoSizeColumn(%s)" % (self.varId, JsUtils.jsConvertData(col_name, None)))

  def autoSizeColumns(self, col_names: list):
    """Same as autoSizeColumn, but provide a list of column keys.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.autoSizeColumns(%s)" % (self.varId, JsUtils.jsConvertData(col_names, None)))

  def getDisplayNameForColumn(self, name: str):
    """Returns the display name for a column.
    Useful if you are doing your own header rendering and want the grid to work out if headerValueGetter is used, or
    if you are doing your own column management GUI, to know what to show as the column name.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param name:
    """
    return JsObjects.JsVoid("%s.getDisplayNameForColumn(%s)" % (self.varId, JsUtils.jsConvertData(name, None)))

  def getAllColumns(self):
    """Returns all the columns, regardless of visible or not.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.getAllColumns()" % self.varId)

  def getAllGridColumns(self):
    """Returns all the grid columns, same as getAllColumns(), except a) it has the order of the columns that are presented
    in the grid and b) it's after the 'pivot' step, so if pivoting, has the value columns for the pivot.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.getAllGridColumns()" % self.varId)

  def getPrimaryColumns(self):
    """Returns the grid's primary columns.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.getPrimaryColumns()" % self.varId)

  def getSecondaryColumns(self):
    """Returns the grid's secondary columns.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.getSecondaryColumns()" % self.varId)

  def getAllDisplayedVirtualColumns(self):
    """Same as getAllGridColumns(), except only returns rendered columns, i.e. columns that are not within the viewport
    and therefore not rendered, due to column virtualisation, are not displayed.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.getAllDisplayedVirtualColumns()" % self.varId)

  def moveColumn(self, col_name, to_index):
    """Moves a column to toIndex. The column is first removed, then added at the toIndex location, thus index locations
    will change to the right of the column after the removal.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param col_name:
    :param to_index:
    """
    col_name = JsUtils.jsConvertData(col_name, None)
    to_index = JsUtils.jsConvertData(to_index, None)
    return JsObjects.JsVoid("%s.moveColumn(%s, %s)" % (self.varId, col_name, to_index))

  def moveColumns(self, col_names, to_index):
    """Moves a column to toIndex. The column is first removed, then added at the toIndex location, thus index locations
    will change to the right of the column after the removal.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param col_names:
    :param to_index:
    """
    col_names = JsUtils.jsConvertData(col_names, None)
    to_index = JsUtils.jsConvertData(to_index, None)
    return JsObjects.JsVoid("%s.moveColumns(%s, %s)" % (self.varId, col_names, to_index))

  def setColumnAggFunc(self, column, agg_func):
    """Sets the agg function for a column. aggFunc can be one of 'min' | 'max' | 'sum'.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param column:
    :param agg_func:
    """
    column = JsUtils.jsConvertData(column, None)
    agg_func = JsUtils.jsConvertData(agg_func, None)
    return JsObjects.JsVoid("%s.setColumnAggFunc(%s, %s)" % (self.varId, column, agg_func))

  def setColumnWidth(self, col_name, new_width, finished=True):
    """Sets the column width on a single column. The finished flag gets included in the resulting event and not used
    internally by the grid.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param col_name:
    :param new_width:
    :param finished:
    """
    col_name = JsUtils.jsConvertData(col_name, None)
    new_width = JsUtils.jsConvertData(new_width, None)
    finished = JsUtils.jsConvertData(finished, None)
    return JsObjects.JsVoid("%s.setColumnWidth(%s, %s, %s)" % (self.varId, col_name, new_width, finished))

  def setColumnWidths(self, column_widths, finished=True):
    """Sets the column width on a single column. The finished flag gets included in the resulting event and not used
    internally by the grid.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param column_widths:
    :param finished:
    """
    column_widths = JsUtils.jsConvertData(column_widths, None)
    finished = JsUtils.jsConvertData(finished, None)
    return JsObjects.JsVoid("%s.setColumnWidth(%s, %s)" % (self.varId, column_widths, finished))

  def custom(self, func_nam: str, *argv):
    """Generic function to call any missing function form a package.
    This will automatically convert the object to JavaScript and also put the right object reference.

    :param func_nam: The function name
    :param argv: Objects. Optional. The function arguments on the JavasScript side
    """
    js_args = []
    for arg in argv:
      js_args.append(str(JsUtils.jsConvertData(arg, None)))
    return JsObjects.JsObject.JsObject.get("%s.%s(%s)" % (self.varId, func_nam, ", ".join(js_args)))


class AgGrid(JsPackage):
  lib_alias = {"js": "ag-grid-community", "css": "ag-grid-community"}

  #  -----------------------------------------
  #  Common table javascript interface
  #  -----------------------------------------
  def empty(self):
    """ Empty the table """
    return self.setRowData([])

  def download(self, filename: str = None, options: dict = None, *args, **kwargs):
    """Common download feature for tables.

    `Related Pages <http://tabulator.info/docs/4.0/download>`_

    :param filename: Filename
    :param options: Download option
    """
    filename = filename or "%s.csv" % self.component.html_code
    if not options:
      options = {}
    options["fileName"] = filename
    return self.exportDataAsCsv(options)

  def add_row(self, data, flag: Union[types.JS_DATA_TYPES, bool] = False, dataflows: List[dict] = None):
    row = JsUtils.dataFlows(data, dataflows, self.page)
    return JsObjects.JsVoid(
      "%(tableId)s.gridOptions.rowData.push(%(row)s); %(tableId)s.gridApi.setRowData(this.gridOptions.rowData)" % {
        "tableId": self.varId, "row": row})

  def show_column(self, column: str):
    return self.columnApi.setColumnVisible(column, False)

  def hide_column(self, column: str):
    return self.columnApi.setColumnVisible(column, True)

  def redraw(self, flag: bool = False):
    return ""

  #  -----------------------------------------
  #  Specific table javascript interface
  #  -----------------------------------------
  def setDomLayout(self, data: types.JS_DATA_TYPES):
    """Gets columns to adjust in size to fit the grid horizontally

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_

    :param data: The layout properties
    """
    data = JsUtils.jsConvertData(data, None)
    return JsObjects.JsVoid("%s.api.setDomLayout(%s)" % (self.varId, data))

  def setAutoHeight(self):
    """Gets columns to adjust automatically height.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.api.setDomLayout('autoHeight')" % self.varId)

  def sizeColumnsToFit(self):
    """Gets columns to adjust in size to fit the grid horizontally

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.api.sizeColumnsToFit()" % self.varId)

  def stopEditing(self):
    """The callback stopEditing (from the params above) gets called by the editor.
    This is how your cell editor informs the grid to stop editing.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/cell-editing-start-stop/>`_
    """
    return JsObjects.JsVoid("%s.api.stopEditing()" % self.varId)

  @property
  def columnApi(self):
    """
    `Related Pages <https://www.ag-grid.com/javascript-grid-column-definitions/>`_
    """
    return ColumnApi(self.page, "%s.columnApi" % self.varId)

  def collapseAll(self):
    """
    `Related Pages <https://www.ag-grid.com/javascript-data-grid/grouping-opening-groups/#opening-group-levels-by-default>`_
    """
    return ColumnApi(self.page, "%s.api.collapseAll" % self.varId)

  def expandAll(self):
    """   

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/grouping-opening-groups/#opening-group-levels-by-default>`_
    """
    return ColumnApi(self.page, "%s.api.expandAll" % self.varId)

  def setColumnDefs(self, col_defs: Any):
    """Call to set new column definitions. The grid will redraw all the column headers, and then redraw all of the rows.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_

    :param col_defs: The new table definition. If None update the existing ones.
    """
    if col_defs is None:
      return JsObjects.JsVoid("%s.api.setColumnDefs(%s)" % (
        self.varId, JsUtils.jsConvertData(self.getColumnDefs(), None)))

    return JsObjects.JsVoid("%s.api.setColumnDefs(%s)" % (self.varId, JsUtils.jsConvertData(col_defs, None)))

  def getColumnDefs(self):
    """Call to set new column definitions. The grid will redraw all the column headers, and then redraw all of the rows.

    `Related Pages <https://www.ag-grid.com/documentation/javascript/column-updating-definitions/>`_
    """
    return JsObjects.JsObject.JsObject("%s.api.getColumnDefs()" % self.varId)

  def setRowData(self, rows: types.JS_DATA_TYPES, dataflows: List[dict] = None):
    """Set rows.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_

    :param rows:
    :param dataflows: Chain of data transformations
    """
    if self.component.options.rowTotal:
      return JsObjects.JsVoid("%s.api.setRowData(%s); %s" % (
        self.varId, JsUtils.dataFlows(rows, dataflows, self.page),
        self.setTotalRow(rows, self.component.options.rowTotal).toStr()))

    return JsObjects.JsVoid("%s.api.setRowData(%s)" % (
      self.varId, JsUtils.dataFlows(rows, dataflows, self.page)))

  def applyTransaction(self, transaction):
    """Update row data. Pass a transaction object with lists for add, remove and update.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_

    :param transaction:
    """
    return JsObjects.JsVoid("%s.api.applyTransaction(%s)" % (self.varId, JsUtils.jsConvertData(transaction, None)))

  def applyTransactionAsync(self, transaction, callback):
    """Same as applyTransaction except executes asynchronous for efficiency.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_

    :param transaction:
    :param callback:
    """
    return JsObjects.JsVoid("%s.api.applyTransaction(%s, %s)" % (
      self.varId, JsUtils.jsConvertData(transaction, None), callback))

  def exportDataAsCsv(self, csv_export_params: dict = None):
    """The grid data can be exported to CSV with an API call, or using the right-click context menu
    (Enterprise only) on the Grid.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/csv-export/>`_
    `Related Pages <https://www.ag-grid.com/javascript-data-grid/csv-export/#csvexportparams>`_

    :param csv_export_params: CSV export options
    """
    if csv_export_params is not None:
      return JsObjects.JsVoid("%s.api.exportDataAsCsv(%s)" % (self.varId, JsUtils.jsConvertData(csv_export_params, None)))

    return JsObjects.JsVoid("%s.api.exportDataAsCsv()" % self.varId)

  def getDisplayedRowCount(self):
    """Returns the total number of displayed rows.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.getDisplayedRowCount()" % self.varId)

  def getFirstDisplayedRow(self):
    """Get the index of the first displayed row due to scrolling (includes invisible rendered rows in the buffer).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.getFirstDisplayedRow()" % self.varId)

  def getLastDisplayedRow(self):
    """Get the index of the last displayed row due to scrolling (includes invisible rendered rows in the buffer).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.getLastDisplayedRow()" % self.varId)

  def hideColumns(self, columns):
    """

    :param columns:
    """
    return JsObjects.JsVoid("%(varId)s.columnApi.setColumnsVisible(%(cols)s, false)" % {
      'varId': self.varId, 'cols': JsUtils.jsConvertData(columns, None)})

  def purgeServerSideCache(self, route):
    """

    `Related Pages <http://54.222.217.254/javascript-grid-server-side-model-tree-data/>`_

    :param route:
    """
    return JsObjects.JsVoid("%s.api.purgeServerSideCache(%s)" % (self.varId, JsUtils.jsConvertData(route, None)))

  def showColumns(self, columns):
    """

    :param columns:
    """
    return JsObjects.JsVoid("%(varId)s.columnApi.setColumnsVisible(%(cols)s, true)" % {
      'varId': self.varId, 'cols': JsUtils.jsConvertData(columns, None)})

  def hideColumn(self, column):
    """

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-definitions/>`_

    :param column:
    """
    return JsObjects.JsVoid("%(varId)s.columnApi.setColumnVisible(%(cols)s, false)" % {
      'varId': self.varId, 'cols': JsUtils.jsConvertData(column, None)})

  def showColumn(self, column):
    """
    `Related Pages <https://www.ag-grid.com/javascript-grid-column-definitions/>`_

    :param column:
    """
    return JsObjects.JsVoid("%(varId)s.columnApi.setColumnVisible(%(cols)s, true)" % {
      'varId': self.varId, 'cols': JsUtils.jsConvertData(column, None)})

  def getRowNode(self, row_id):
    """Returns the row node with the given ID.
    The row node ID is the one you provide with the callback getRowNodeId(data),
    otherwise the ID is a number auto generated by the grid when the row data is set.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_

    :param row_id:
    """
    row_id = JsUtils.jsConvertData(row_id, None)
    return JsObjects.JsVoid("%s.api.getRowNode(%s)" % (self.varId, row_id))

  def getDisplayedRowAtIndex(self, index):
    """Returns the displayed rowNode at the given index.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_

    :param index:
    """
    index = JsUtils.jsConvertData(index, None)
    return JsObjects.JsVoid("%s.api.getRowNode(%s)" % (self.varId, index))

  def selectAll(self):
    """Select all rows (even rows that are not visible due to grouping being enabled and their groups not expanded).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.selectAll()" % self.varId)

  def deselectAll(self):
    """Clear all row selections.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.deselectAll()" % self.varId)

  def selectAllFiltered(self):
    """Select all filtered rows.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.selectAllFiltered()" % self.varId)

  def deselectAllFiltered(self):
    """Clear all filtered selections.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.deselectAllFiltered()" % self.varId)

  def getSelectedNodes(self):
    """Returns a list of selected nodes. Getting the underlying node (rather than the data) is useful when
    working with tree / aggregated data, as the node can be traversed.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.getSelectedNodes()" % self.varId)

  def getFocusedCell(self):
    """Returns the focused cell (or the last focused cell if the grid lost focus).

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/grid-api/
    """
    return JsObjects.JsVoid("%s.api.getFocusedCell()" % self.varId)

  def getFilterModel(self):
    """It is possible to get the state of all filters using the grid API method getFilterModel(), and to set the state
    using setFilterModel().
    These methods manage the filters states via the getModel() and setModel() methods of the individual filters.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/filter-api/#get--set-all-filter-models>`_
    """
    return JsObjects.JsObject.JsObject("%s.api.getFilterModel()" % self.varId)

  def setFilterModel(self, data: types.JS_DATA_TYPES):
    """Sets the state of all the advanced filters.
    Provide it with what you get from getFilterModel() to restore filter state.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/filter-api/#get--set-all-filter-models>`_
    """
    data = JsUtils.jsConvertData(data, None)
    return JsObjects.JsObject.JsObject("%s.api.setFilterModel(%s)" % (self.varId, data))

  def destroyFilter(self):
    """Sets the state of all the advanced filters.
    Provide it with what you get from getFilterModel() to restore filter state.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/filter-api/#get--set-all-filter-models>`_
    """
    return JsObjects.JsObject.JsObject("%s.api.destroyFilter()" % self.varId)

  def getFilterInstance(self, data: types.JS_DATA_TYPES):
    """
    `Related Pages <https://www.ag-grid.com/javascript-data-grid/filter-api/#get--set-all-filter-models>`_

    :param data:
    """
    raise NotImplementedError("Not yet available")

  def getModel(self):
    """Get table model.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/filter-api/#get--set-all-filter-models>`_
    """
    return JsObjects.JsObject.JsObject("%s.api.getModel()" % self.varId)

  def getRowsData(self) -> JsObjects.JsArray.JsArray:
    """Get all the data in the table.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/accessing-data/>`_
    """
    return JsObjects.JsArray.JsArray.get('''
(function(table) {let rowData = []; table.api.forEachNode(node => rowData.push(node.data)); return rowData})(%s)''' % self.varId)

  def getSelectedRows(self):
    """Returns a list of selected rows (i.e. row data that you provided).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsArray.JsArray.get("%s.api.getSelectedRows()" % self.varId)

  def getCellRanges(self):
    """Returns the list of selected cell ranges.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.getCellRanges()" % self.varId)

  def clearRangeSelection(self):
    """Clears the selected range.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.clearRangeSelection()" % self.varId)

  def refreshCells(self, params):
    """Performs change detection on all cells, refreshing cells where required.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    params = JsUtils.jsConvertData(params, None)
    return JsObjects.JsVoid("%s.api.refreshCells(%s)" % (self.varId, params))

  def redrawRows(self, params):
    """Remove a row from the DOM and recreate it again from scratch.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    params = JsUtils.jsConvertData(params, None)
    return JsObjects.JsVoid("%s.api.redrawRows(%s)" % (self.varId, params))

  def refreshHeader(self):
    """Redraws the header. Useful if a column name changes, or something else that changes how the column header is
    displayed.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.refreshHeader()" % self.varId)

  def flashCells(self, params):
    """Flash rows, columns or individual cells. See Flashing Cells.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    `Related Pages <https://www.ag-grid.com/angular-data-grid/flashing-cells/>`_
    """
    params = JsUtils.jsConvertData(params, None)
    return JsObjects.JsVoid("%s.api.flashCells(%s)" % (self.varId, params))

  def clearFocusedCell(self):
    """Clears the focused cell.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.clearFocusedCell()" % self.varId)

  def tabToNextCell(self):
    """Navigates the grid focus to the next cell, as if tabbing.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.tabToNextCell()" % self.varId)

  def tabToPreviousCell(self):
    """Navigates the grid focus to the previous cell, as if shift-tabbing.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.tabToPreviousCell()" % self.varId)

  def overlayLoadingTemplate(self, js_data: types.JS_DATA_TYPES) -> JsObjects.JsVoid:
    """Set the template for loading overlay.

    :param js_data: String or HTML string
    """
    js_data = JsUtils.jsConvertData(js_data, None)
    return JsObjects.JsVoid("%s.overlayLoadingTemplate = %s" % (self.varId, js_data))

  def overlayNoRowsTemplate(self, js_data: types.JS_DATA_TYPES) -> JsObjects.JsVoid:
    """Set the template for No Rows overlay

    :param js_data: String or HTML string
    """
    js_data = JsUtils.jsConvertData(js_data, None)
    return JsObjects.JsVoid("%s.overlayNoRowsTemplate = %s" % (self.varId, js_data))

  def showLoadingOverlay(self) -> JsObjects.JsVoid:
    """Show the 'loading' overlay.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.showLoadingOverlay()" % self.varId)

  def showNoRowsOverlay(self):
    """Show the 'no rows' overlay.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.showNoRowsOverlay()" % self.varId)

  def hideOverlay(self) -> JsObjects.JsVoid:
    """Hides the overlay if showing.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.hideOverlay()" % self.varId)

  def destroy(self) -> JsObjects.JsVoid:
    """Will destroy the grid and release resources.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.destroy()" % self.varId)

  def resetRowHeights(self) -> JsObjects.JsVoid:
    """Tells the grid to recalculate the row heights.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.resetRowHeights()" % self.varId)

  def paginationIsLastPageFound(self) -> JsObjects.JsVoid:
    """Returns true when the last page is known; this will always be the case if you are using the Client-Side
    Row Model for pagination.
    Returns false when the last page is not known; this only happens when using Infinite Scrolling Row Model.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationIsLastPageFound()" % self.varId)

  def copySelectedRangeToClipboard(self, include_headers) -> JsObjects.JsVoid:
    """Copies the selected ranges to the clipboard.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    include_headers = JsUtils.jsConvertData(include_headers, None)
    return JsObjects.JsVoid("%s.api.copySelectedRangeToClipboard(%s)" % (self.varId, include_headers))

  def copySelectedRangeDown(self) -> JsObjects.JsVoid:
    """Copies the selected range down, similar to Ctrl + D in Excel.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.copySelectedRangeDown()" % self.varId)

  def paginationGetPageSize(self) -> JsObjects.JsVoid:
    """Returns how many rows are being shown per page.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGetPageSize()" % self.varId)

  def paginationSetPageSize(self, new_page_size) -> JsObjects.JsVoid:
    """Sets the paginationPageSize to newPageSize, then re-paginates the grid so the changes are applied immediately.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    new_page_size = JsUtils.jsConvertData(new_page_size, None)
    return JsObjects.JsVoid("%s.api.paginationSetPageSize(%s)" % (self.varId, new_page_size))

  def paginationGetCurrentPage(self) -> JsObjects.JsVoid:
    """Returns the 0-based index of the page which is showing.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGetCurrentPage()" % self.varId)

  def paginationGetTotalPages(self) -> JsObjects.JsVoid:
    """Returns the total number of pages. Returns null if paginationIsLastPageFound() == false.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGetTotalPages()" % self.varId)

  def paginationGetRowCount(self) -> JsObjects.JsVoid:
    """The total number of rows. Returns null if paginationIsLastPageFound() == false.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGetRowCount()" % self.varId)

  def paginationGoToPage(self, page_number: types.JS_DATA_TYPES) -> JsObjects.JsVoid:
    """Goes to the specified page. If the page requested doesn't exist, it will go to the last page.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_

    :param page_number: Page index
    """
    page_number = JsUtils.jsConvertData(page_number, None)
    return JsObjects.JsVoid("%s.api.paginationGoToPage(%s)" % (self.varId, page_number))

  def paginationGoToNextPage(self) -> JsObjects.JsVoid:
    """Shorthands for goToPage(relevantPageNumber).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGoToNextPage()" % self.varId)

  def paginationGoToPreviousPage(self) -> JsObjects.JsVoid:
    """Shorthands for goToPage(relevantPageNumber).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGoToPreviousPage()" % self.varId)

  def paginationGoToFirstPage(self) -> JsObjects.JsVoid:
    """Shorthands for goToPage(relevantPageNumber).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGoToFirstPage()" % self.varId)

  def paginationGoToLastPage(self) -> JsObjects.JsVoid:
    """Shorthands for goToPage(relevantPageNumber).

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    return JsObjects.JsVoid("%s.api.paginationGoToLastPage()" % self.varId)

  def setSideBarVisible(self, show) -> JsObjects.JsVoid:
    """Tells the grid to recalculate the row heights.

    `Related Pages <https://www.ag-grid.com/javascript-grid-api/>`_
    """
    show = JsUtils.jsConvertData(show, None)
    return JsObjects.JsVoid("%s.api.setSideBarVisible(%s)" % (self.varId, show))

  def getSortModel(self) -> JsObjects.JsVoid:
    """Returns the sort state.

    `Related Pages <https://www.ag-grid.com/javascript-grid-column-api/>`_
    """
    return JsObjects.JsVoid("%s.api.getSortModel()" % self.varId)

  def setPinnedBottomRowData(self, rowData) -> JsObjects.JsVoid:
    """
    `Related Pages <https://www.ag-grid.com/javascript-data-grid/row-pinning/>`_

    :param rowData:
    """
    return JsObjects.JsVoid("%s.api.setPinnedBottomRowData(%s)" % (self.varId, JsUtils.jsConvertData(rowData, None)))

  def setPinnedTopRowData(self, rowData) -> JsObjects.JsVoid:
    """
    `Related Pages <https://www.ag-grid.com/javascript-data-grid/row-pinning/>`_

    :param rowData:
    """
    return JsObjects.JsVoid("%s.api.setPinnedTopRowData(%s)" % (self.varId, JsUtils.jsConvertData(rowData, None)))

  def setTotalRow(self, rowData, cols: types.JS_DATA_TYPES = None) -> JsObjects.JsVoid:
    """
    
    :param rowData: 
    :param cols: 
    :return: 
    """
    return JsObjects.JsVoid('''
const calcTotalCols = %s;
const totalRow = function(api) {
      let result = [{}];
      calcTotalCols.forEach(function (params){result[0][params] = 0});
      calcTotalCols.forEach(function (params){%s.forEach(function (line) {result[0][params] += line[params];})});
      api.setPinnedBottomRowData(result);
  }; totalRow(%s.api)''' % (JsUtils.jsConvertData(cols, None), JsUtils.jsConvertData(rowData, None), self.varId))

  def setServerSideDatasource(self, data) -> JsObjects.JsVoid:
    """Set new datasource for Server-Side Row Model.

    `Related Pages <https://www.ag-grid.com/javascript-data-grid/grid-api/#reference-serverSideRowModel>`_

    :param data:
    """
    return JsObjects.JsVoid("%s.api.setServerSideDatasource(%s)" % (self.varId, JsUtils.jsConvertData(data, None)))

  def fetch(self, url: Union[str, primitives.JsDataModel], data: Optional[dict] = None, js_code: str = "response",
            is_json: bool = True,
            components: Optional[List[Union[Tuple[primitives.HtmlModel, str], primitives.HtmlModel]]] = None,
            profile: Optional[Union[dict, bool]] = None, headers: Optional[dict] = None,
            asynchronous: bool = False, stringify: bool = True, method: str = "GET") -> JsObjects.XMLHttpRequest:
      rest_call = self.page.js.rest(
        method, url, data, js_code, is_json=is_json, components=components, profile=profile, headers=headers,
        asynchronous=asynchronous, stringify=stringify)
      rest_call.onSuccess(['''
var fakeServer = {
    getData: (request) => {
      const requestedRows = %s.response.slice(request.startRow, request.endRow);
      return {success: true, rows: requestedRows};},
};
%s.api.setServerSideDatasource({
  getRows: (params) => {
    const response = fakeServer.getData(params.request);
    setTimeout(function () {
      if (response.success) {params.success({ rowData: response.rows })} else {params.fail();}
    }, 500);
  }});''' % (js_code, self.varId)])
      return rest_call

  @property
  def _(self):
    """Aggrid standard components (mainly for events).

    Usage::

      table.js._
    """
    return _Export()
