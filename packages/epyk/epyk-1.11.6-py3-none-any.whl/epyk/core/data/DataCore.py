#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from typing import Union, Any, List
from epyk.core.py import primitives
from epyk.core.js import JsUtils
from epyk.core.py import OrderedSet

from epyk.core.js.primitives import JsObjects


class DataAggregators:

  def __init__(self,  js_code: str, page: primitives.PageModel = None):
    self.varName = js_code
    self.page = page

  def max(self, column: str) -> JsObjects.JsArray.JsArray:
    """ Returns the maximum value in list.
    If an iterator function is provided, it will be used on each value to generate the criterion by which the value is
    ranked.
    -Infinity is returned if list is empty, so an isEmpty guard may be required.
    Non-numerical values in list will be ignored.

    Related Pages:

      https://underscorejs.org/#max

    :param column: The column name. The key in the list of dictionary.
    """
    self.page.jsImports.add('underscore')
    return JsObjects.JsArray.JsArray("[_.max(%s, function(rec){return rec['%s']; })]" % (
      self.varName, column), page=self.page)

  def min(self, column: str) -> JsObjects.JsArray.JsArray:
    """ Returns the minimum value in list.
    If an iterator function is provided, it will be used on each value to generate the criterion by which the value is
    ranked.
    Infinity is returned if list is empty, so an isEmpty guard may be required.
    Non-numerical values in list will be ignored.

    Related Pages:

      https://underscorejs.org/#min

    :param column: The column name. The key in the list of dictionary.
    """
    self.page.jsImports.add('underscore')
    return JsObjects.JsArray.JsArray("[_.min(%s, function(rec){ return rec['%s']; })]" % (
      self.varName, column), page=self.page)

  def sortBy(self, column: str) -> JsObjects.JsArray.JsArray:
    """ Returns a (stably) sorted copy of list, ranked in ascending order by the results of running each value through
    iterator. iterator may also be the string name of the property to sort by (eg. length).

    :param column: The column name. The key in the list of dictionary.
    """
    self.page.jsImports.add('underscore')
    column = JsUtils.jsConvertData(column, None)
    return JsObjects.JsArray.JsArray("_.sortBy(%s, %s)" % (self.varName, column), page=self.page)

  def sum(self, columns: list, attrs: dict = None) -> JsObjects.JsArray.JsArray:
    """ Reduce the record set by adding all the columns.

    :param list columns: The columns in the records to be counted.
    :param dict attrs: Optional. The static values to be added to the final records.
    """
    return JsObjects.JsArray.JsArray('''
       (function(r, cs){var result = {}; cs.forEach(function(c){result[c] = 0});
        r.forEach(function(v){cs.forEach(function(c){ if(typeof v[c] !== 'undefined'){ result[c] += v[c]}})
        }); var attrs = %s; if(attrs){for(var attr in attrs){result[attr] = attrs[attr]}}; return [result]})(%s, %s)
        ''' % (json.dumps(attrs), self.varName, json.dumps(columns)), is_py_data=False, page=self.page)

  def count(self, columns: list, attrs: dict = None) -> JsObjects.JsArray.JsArray:
    """   Reduce the record set by counting all the columns.

    :param columns: The columns in the records to be counted.
    :param attrs: Optional. The static values to be added to the final records.
    """
    return JsObjects.JsArray.JsArray('''
       (function(r, cs){ var result = {}; cs.forEach(function(c){result[c] = 0});
        r.forEach(function(v){cs.forEach(function(c){ if(typeof v[c] !== 'undefined'){ result[c] += 1}})
        }); var attrs = %s; if(attrs){for(var attr in attrs){result[attr] = attrs[attr]}}; return [result]})(%s, %s)
        ''' % (json.dumps(attrs), self.varName, json.dumps(columns)), is_py_data=False, page=self.page)

  def countBy(self, column: list) -> JsObjects.JsArray.JsArray:
    """   Reduce the record set by counting all the columns.

    :param column: The columns in the records to be counted.
    """
    return JsObjects.JsArray.JsArray('''
 (function(r, c){var tempDict = {};
  r.forEach(function(v){if(typeof v[c] !== 'undefined'){
    if(typeof tempDict[v[c]] === 'undefined'){tempDict[v[c]] = 0}; tempDict[v[c]] += 1} }); 
  result = []; for(var key in tempDict){result.push({[c]: key, count: tempDict[key]})}; return result})(%s, %s)
        ''' % (self.varName, json.dumps(column)), is_py_data=False, page=self.page)

  def sumBy(self, columns: list, keys, dst_key: dict = None, cast_vals: bool = False) -> JsObjects.JsArray.JsRecordSet:
    """   

    :param columns: The list of columns / attributes in the JavaScript object
    :param keys: The list of keys
    :param dst_key: Optional.
    :param cast_vals: Optional.
    """
    keys = JsUtils.jsConvertData(keys, None)
    dst_key = JsUtils.jsConvertData(dst_key, None)
    columns = JsUtils.jsConvertData(columns, None)
    name = "AggSumBy"
    self.page.properties.js.add_constructor(name, '''
function %s(rs, cs, sks, dk){var result = []; var tmpResults = {}; if(sks == ''){return rs}; 
  var rdk = dk === null ? sks :  dk;
  if (!Array.isArray(sks)) {sks = [sks]}
  rs.forEach(function(r){
    var sk = []; sks.forEach(function(s){sk.push(r[s])}); var skKey = sk.join('#');
    if (!(skKey in tmpResults)){tmpResults[skKey] = {}; sks.forEach(function(s){tmpResults[skKey][s] = r[s]})
       cs.forEach(function(c){tmpResults[skKey][c] = 0})}
    cs.forEach(function(c){tmpResults[skKey][c] += %s})
  }); for(var v in tmpResults){result.push(tmpResults[v])}; return result}''' % (
      name, "parseFloat(r[c])" if cast_vals else 'r[c]'))
    return JsObjects.JsArray.JsRecordSet('%s(%s, %s, %s, %s)' % (
      name, self.varName, columns, keys, dst_key), page=self.page)

  def pluck(self, column: Union[str, primitives.JsDataModel]) -> JsObjects.JsArray.JsArray:
    """ A convenient version of what is perhaps the most common use-case for map: extracting a list of property values.

    Related Pages:

      https://underscorejs.org/#pluck

    :param column: The column / attribute in the JavaScript object
    """
    self.page.jsImports.add('underscore')
    column = JsUtils.jsConvertData(column, None)
    return JsObjects.JsArray.JsArray("_.pluck(%s, %s)" % (self.varName, column), page=self.page)


class DataFilters:

  def __init__(self,  js_code: str, filter_map, page: primitives.PageModel = None):
    self.varName, self.__filters = js_code, OrderedSet()
    self.page, self.filter_map = page, filter_map

  def setFilter(self, name: str) -> JsObjects.JsVoid:
    """   

    :param name: The filter reference on the JavaScript side
    """
    self.filter_map[name] = self.toStr()
    return JsObjects.JsVoid("const %s = %s" % (name, self.filter_map[name]))

  def match(self, data: Union[dict, primitives.JsDataModel], case_sensitive: bool = True):
    """
    Filtering rule based on a Dictionary of lists.

    :param data: The keys, values to be filtered
    :param case_sensitive: Optional. To make sure algorithm case-sensitive
    """
    data = JsUtils.jsConvertData(data, None)
    name = "filterMatch"
    self.page.properties.js.add_constructor(name, '''
function %s(r, v){if(typeof r === 'undefined'){return []}; 
if(v.length == 0){return r}; var n=[];r.forEach(function(e){var isValid = true;
for(var a in v){if(!v[a].includes(e[a])){isValid = false; break}}; if(isValid){n.push(e)}}); return n}''' % name)
    self.__filters.add("%s(%%s, %s)" % (name, data))
    return self

  def any(self, value: Any, keys: list = None):
    """
    Check if any value in the record match the value. This is not case sensitive.

    TODO: improve the performances by filtering on a list of keys if passed

    :param value: The value to keep
    :param keys: Optional. The list of keys to check
    """
    value = JsUtils.jsConvertData(value, None)
    keys = JsUtils.jsConvertData(keys, None)
    name = "AnyMatch"
    self.page.properties.js.add_constructor(name, '''
function %s(r, v, ks){if (v == ''){return r}; 
v = v.toUpperCase(); var n=[];r.forEach(function(e){for(const k in e){
  if(String(e[k]).toUpperCase().includes(v)){n.push(e); break;} } });return n}''' % name)
    self.__filters.add("%s(%%s, %s, %s)" % (name, value, keys))
    return self

  def equal(self, key: str, value: Any, case_sensitive: bool = True):
    """
    Filtering rule based on a key, value.

    Usage::

      select = page.ui.select(components.select.from_records(languages, column=filter_column))
      table = page.ui.tables.aggrid(languages)
      filter_data = DataJs(page).record(js_code="myData", data=languages)
      filt_grp = filter_data.filterGroup("test")
      select.change([table.js.setRowData(filt_grp.equal(filter_column, select.dom.content))])

    :param key: The key in the various records
    :param value: Object. The value to keep
    :param case_sensitive: Optional. To make sure algorithm case-sensitive
    """
    key = JsUtils.jsConvertData(key, None)
    value = JsUtils.jsConvertData(value, None)
    if not case_sensitive:
      name = "filterEqualUpper"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){if (v == ''){return r}; var n=[];
v = v.toUpperCase(); r.forEach(function(e){if(e[k].toUpperCase()==v){n.push(e)}});return n}''' % name)
    else:
      name = "filterEqual"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){if (v == ''){return r}; var n=[];
r.forEach(function(e){if(e[k]==v){n.push(e)}});return n}''' % name)
    self.__filters.add("%s(%%s, %s, %s)" % (name, key, value))
    return self

  def includes(self, key: str, values: list, case_sensitive: bool = True, empty_all: bool = True):
    """
    Filtering rule based on a key, list of values.

    :param key: The key in the various records
    :param values: The list of values to keep
    :param case_sensitive: Optional. To make sure algorithm case-sensitive
    :param empty_all: Optional. To specify how to consider the empty case
    """
    key = JsUtils.jsConvertData(key, None)
    value = JsUtils.jsConvertData(values, None)
    if not case_sensitive:
      name = "filterContainUpper"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){if (v.length == 0){if(%s){return r} 
else {return []}}; var vUp = []; v.forEach(function(t){vUp.push(t.toUpperCase())}); var n=[];
r.forEach(function(e){if(vUp.includes(e[k].toUpperCase())){n.push(e)}});return n}''' % (name, json.dumps(empty_all)))
    else:
      name = "filterContain"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){
if (v.length == 0){if(%s){return r} else {return []}}; var n=[];
r.forEach(function(e){if(v.includes(e[k])){n.push(e)}});return n}''' % (name, json.dumps(empty_all)))
    self.__filters.add("%s(%%s, %s, %s)" % (name, key, value))
    return self

  def startswith(self, key: str, value: str):
    """
    Filtering rule based on a key, and a value starting with a specific format.

    :param key: The key in the various records
    :param value: The list of values to keep
    """
    name = "filterStartsWith"
    key = JsUtils.jsConvertData(key, None)
    value = JsUtils.jsConvertData(value, None)
    self.page.properties.js.add_constructor(name, '''function %s(r, k, v){var n=[];
r.forEach(function(e){if(e[k].startsWith(v)){n.push(e)}});return n}''' % name)
    self.__filters.add("%s(%%s, %s, %s)" % (name, key, value))
    return self

  def sup(self, key: Union[str, primitives.JsDataModel], value: Union[float, primitives.JsDataModel],
          strict: bool = True):
    """
    Filter values below a certain value.

    :param key: The key in the various records
    :param value: The threshold
    :param strict: Optional. Include threshold
    """
    key = JsUtils.jsConvertData(key, None)
    value = JsUtils.jsConvertData(value, None)
    if strict:
      name = "filterSup"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){var n=[];
r.forEach(function(e){if(e[k] > v){n.push(e)}});return n}''' % name)
    else:
      name = "filterSupEq"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){var n=[];
r.forEach(function(e){if(e[k] >= v){n.push(e)}});return n}''' % name)
    self.__filters.add("%s(%%s, %s, %s)" % (name, key, value))
    return self

  def inf(self, key: Union[str, primitives.JsDataModel], value: Union[float, primitives.JsDataModel],
          strict: bool = True):
    """
    Filter values above a certain value.

    :param key: The key in the various records
    :param value: The threshold
    :param strict: Optional. Include threshold
    """
    key = JsUtils.jsConvertData(key, None)
    value = JsUtils.jsConvertData(value, None)
    if strict:
      name = "filterInf"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){var n=[];
r.forEach(function(e){if(e[k] < v){n.push(e)}});return n}''' % name)
    else:
      name = "filterInfEq"
      self.page.properties.js.add_constructor(name, '''function %s(r, k, v){var n=[];
r.forEach(function(e){if(e[k] <= v){n.push(e)}});return n}''' % name)
    self.__filters.add("%s(%%s, %s, %s)" % (name, key, value))
    return self

  def group(self) -> DataAggregators:
    """
    Group a group for the data transformation.
    This will be defined in the Python but processed on the JavaScript side.

    Usage::

      js_data = page.data.js.record(js_code="myData", data=randoms.languages) # Create JavaScript data
      filter1 = js_data.filterGroup("filter1") # Add a filter object

      select.change([
          bar.build(filter1.group().sumBy(['rating', 'change'], select.dom.content), options={"x_axis": select.dom.content}),
          ...
      ])
    """
    return DataAggregators(self.toStr(), self.page)

  def sortBy(self, column: Union[str, primitives.JsDataModel]):
    """ Returns a (stably) sorted copy of list, ranked in ascending order by the results of running each value
    through iterator. iterator may also be the string name of the property to sort by (eg: length).

    Related Pages:

      https://underscorejs.org/#sortBy

    :param column: The key in the record to be used as key for sorting
    """
    self.page.jsImports.add('underscore')
    column = JsUtils.jsConvertData(column, None)
    self.__filters.add("_.sortBy(%%s, %s)" % column)
    return self

  def pivot(self, column: str, value: str, p: str, type: Union[str, tuple] = None):
    """ Pivot the data from rows (keys) to columns in the records.
    This should reduce the size of the record and it will make it usable in charts.

    Usages::

      page.js.fetch(data_urls.C02_DATA).csvtoRecords().get([
        page.js.console.log(page.data.js.record("data").filterGroup("test").pivot("country", "co2", "year"))
      ])

    :param column: The key in the record to be used as key for sorting
    :param value: The key in the record to be used as key for sorting
    :param p: The key used as pivot
    :param type: Optional int, or float or (fnc, alias)
    """
    value = JsUtils.jsConvertData(value, None)
    column = JsUtils.jsConvertData(column, None)
    p = JsUtils.jsConvertData(p, None)
    if type is not None:
      groups = {"int": ["parseInt", "Integer"], "float": ["parseFloat", "Float"]}.get(type, type)
      fnc_name = "SimplePivot%s" % groups[1]
      val_fmt = "%s(t[v])" % groups[0]
    else:
      fnc_name, val_fmt = "SimplePivot", "t[v]"
    self.page.properties.js.add_constructor(fnc_name, '''
function %(fnc_name)s(r, k, v, p){
var s = {}; r.forEach(function(t){if (t[p] in s){s[t[p]][t[k]] = %(vFmt)s} else {s[t[p]] = {[t[k]]: %(vFmt)s}}});
var result = []; for (const [key, values] of Object.entries(s)) {result.push(Object.assign(values, {[p]: key}))}
return result}''' % {"fnc_name": fnc_name, "vFmt": val_fmt})
    self.__filters.add("%s(%%s, %s, %s, %s)" % (fnc_name, column, value, p))
    return self

  def toStr(self) -> str:
    result = "%s"
    for rec in self.__filters[::-1]:
      result %= rec
    return result % self.varName


class DataGlobal:

  def __init__(self, js_code: str, data, page: primitives.PageModel = None):
    if data is not None:
      page._props["js"]["datasets"][js_code] = "var %s = %s" % (js_code, json.dumps(data))
    self._data, self.__filters_groups, self.page, self.varName = data, {}, page, js_code
    self.__filter_saved = {}

  def getFilter(self, name: str, group_name: str = None) -> DataFilters:
    """   

    :param name: The filter alias name
    :param group_name: Optional. The filter group name
    """
    if group_name is None:
      saved_filter = None
      for k, v in self.__filter_saved.items():
        if name in v:
          saved_filter = v
          break

    else:
      if name not in self.__filter_saved[group_name]:
        raise NotImplementedError()

      saved_filter = self.__filter_saved[group_name]
    return DataFilters(name, saved_filter, self.page)

  def clearFilter(self, name: str, group_name: str = None):
    """   

    :param name:
    :param group_name: Optional.
    """
    if group_name is None:
      for k, v in self.__filter_saved.items():
        if name in v:
          del v[name]

    else:
      del self.__filter_saved[group_name][name]

    return self

  def filterGroup(self, group_name: str) -> DataFilters:
    """
    Create a JavaScript filtering group.

    Usage::

      js_data = page.data.js.record(js_code="myData", data=randoms.languages) # Create JavaScript data
      filter1 = js_data.filterGroup("filter1") # Add a filter object

    :param group_name: The filter name.
    """
    if group_name not in self.__filters_groups:
      self.__filter_saved[group_name] = {}
      self.__filters_groups[group_name] = DataFilters(self.varName, self.__filter_saved[group_name], self.page)
    return self.__filters_groups[group_name]

  def cleafFilterGroup(self, group_name: str):
    """   

    :param group_name: The filter name.
    """
    if group_name not in self.__filters_groups:
      del self.__filters_groups[group_name]

    return self

  def clearFilters(self):
    """ Remove all the filters. """
    self.__filters_groups = {}
    return self


class ServerConfig:

  def __init__(self, hostname: str, port: int, page: primitives.PageModel = None):
    self.js_code = "server_config_%s" % id(self)
    page._props["js"]["configs"][self.js_code] = self
    self.__namespaces, self.__end_points, self.host, self.port = {}, {}, hostname, port

  def getNamespace(self, alias: str):
    """ Get the name space from its alias.

    :param alias: The name space alias.
    """
    return self.__namespaces[alias]

  def addNamespace(self, name: str, alias: str = None, end_points: list = None):
    """
    Add a JavaScript name space and its full end points and assigned it to a dedicated alias on the Python side.
    This will allow the Python to get the name space from its alias.

    :param name: The url name space.
    :param alias: Optional. The alias for the entry point.
    :param end_points: Optional. The endpoint routes.
    """
    if alias is None:
      alias = name
    self.__namespaces[alias] = ServerNameSpaceConfig(self, name, alias, end_points)
    return self

  def endPoint(self, name: str):
    """
    Set the end point.

    :param name: The endpoint name.
    """
    self.__end_points[name] = "http://%s:%s/%s" % (self.host, self.port, name)
    return self

  def endPoints(self, names: List[str]):
    """
    Set multiple end points.

    :param names: The end points names
    """
    for name in names:
      self.__end_points[name] = "http://%s:%s/%s" % (self.host, self.port, name)
    return self

  def get(self, name: str) -> JsObjects.JsObject.JsObject:
    """ Get the end point from its name.

    :param name: The end point name
    """
    if name not in self.__end_points:
      raise ValueError("Missing end point in the server configuration - %s" % name)

    return JsObjects.JsObject.JsObject.get(self.js_code)[name]

  def toStr(self) -> str:
    """

    """
    for np, np_val in self.__namespaces.items():
      self.__end_points[np] = {'e': np_val.end_points, 'n': np_val.name, 'u': "http://%s:%s/%s" % (
        self.host, self.port, np_val.name)}
    return "var %s = %s" % (self.js_code, JsUtils.jsConvertData(self.__end_points, None))

  def __str__(self):
    return self.toStr()


class ServerNameSpaceConfig:
  def __init__(self, config: ServerConfig, name: str, alias: str, end_points: list):
    self.__config, self.end_points, self.name, self.alias = config, {}, name, alias
    if end_points is not None:
      self.endPoints(end_points)

  @property
  def address(self):
    """


    """
    return JsObjects.JsObject.JsObject.get(self.__config.js_code)[self.alias]['u']

  def endPoint(self, name: str):
    """

    :param name:
    """
    self.end_points[name] = "http://%s:%s/%s/%s" % (self.__config.host, self.name, self.__config.port, name)
    return self

  def endPoints(self, names: list):
    """

    :param names:
    """
    for name in names:
      self.endPoint(name)
    return self
