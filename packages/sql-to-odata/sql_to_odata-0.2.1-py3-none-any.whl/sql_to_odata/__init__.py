import os
import sqlite3

import ujson


__version__ = '0.2.1'


class ODataInterface():
    """OData interface to a SQL database."""

    @staticmethod
    def datatype_to_odata(type_name):
        """
        Convert a SQLite datatype to an OData type.

        :param type_name: SQLite datatype
        :return: OData type name
        """
        if type_name == 'INTEGER':
            return 'Edm.Int64'
        elif type_name == 'REAL':
            return 'Edm.Double'
        elif type_name.startswith('NUMERIC'):
            return 'Edm.Decimal'
        elif type_name == 'TEXT':
            return 'Edm.String'
        elif type_name.startswith('NVARCHAR'):
            return 'Edm.String'
        elif type_name == 'BLOB':
            return 'Edm.Binary'
        elif type_name == 'DATETIME':
            return 'Edm.DateTimeOffset'
        else:
            raise ValueError(f'Unknown data type: {type_name}')

    def get_table_names(self):
        """
        Fetch the names of all tables in the database.

        :return: List of table names in sorted order
        """
        query = '''SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';'''
        rows = self._connection.execute(query)
        return sorted(r[0] for r in rows)

    def get_table_schema(self, table_name):
        """
        Fetch a single table's schema.

        :param table_name: Name of the table whose schema should be fetched
        :return: List of tuples of schema info: (name, odata_type, is_nullable, default_value, is_primary_key)
        """
        query = '''SELECT * FROM pragma_table_info(?);'''
        rows = self._connection.execute(query, [table_name])
        return [(r[1], ODataInterface.datatype_to_odata(r[2]), r[3] == 1, r[4], r[5] == 1) for r in rows]

    def get_table_schema_xml(self, table_name):
        """
        Create an OData metadata fragment for the given table in XML format.

        :param table_name: Name of the table whose schema should be fetched
        :return: OData metadata fragment as an XML string
        """
        schema = self.get_table_schema(table_name)
        xml_lines = []
        xml_lines.append(f'<EntityType Name="{table_name}">')
        for field in schema:
            xml_lines.append(f'<Property Name="{field[0]}" Type="{field[1]}" />')
        xml_lines.append('</EntityType>')
        return '\n'.join(xml_lines)

    def get_database_schema(self):
        """
        Fetch the schemas for all tables in the database.

        :return: Dictionary of schemas, where the keys are the table names and the
                 values are schema tuples as defined in the get_table_schema function.
        """
        return {t: self.get_table_schema(t) for t in self.get_table_names()}

    def get_database_schema_xml(self):
        """
        Create an OData metadata file for the database in XML format.

        :return: OData metadata as an XML string
        """
        table_names = self.get_table_names()
        xml_lines = []
        xml_lines.append('<?xml version="1.0" encoding="utf-8"?>')
        xml_lines.append('<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">')
        xml_lines.append('<edmx:DataServices>')
        xml_lines.append('<Schema Namespace="DCT" xmlns="http://docs.oasis-open.org/odata/ns/edm">')
        for table_name in table_names:
            xml_lines.append(self.get_table_schema_xml(table_name))
        xml_lines.append('</Schema>')
        xml_lines.append('</edmx:DataServices>')
        xml_lines.append('</edmx:Edmx>')
        return '\n'.join(xml_lines)

    def get_table_rows(self, table_name):
        """
        Fetch all rows of a single table.

        :param table_name: Name of the table to be fetched
        :return: List of rows each of which is a dictionary of field name / value pairs
        """
        table_names = self.get_table_names()
        # Prevents SQL injection by validating parameter against list of table names
        if table_name not in table_names:
            raise ValueError(f'Table not found: {table_name}')
        query = f'''SELECT * FROM {table_name}'''  # nosec - this is safe because of the prior check
        rows = self._connection.execute(query)
        schema = self.get_table_schema(table_name)
        field_names = [f[0] for f in schema]
        return [dict(zip(field_names, r)) for r in rows]

    def get_table_json(self, table_name, formatted=False):
        """
        Fetch all rows of a single table in OData-compatible JSON format.

        :param table_name: Name of the table to be fetched
        :param formatted: JSON output is formatted with indentation, defaults to false
        :return: JSON-formatted rows and an OData context header pointing to metadata
        """
        odata_context_url = f'$metadata#{table_name}'
        table_rows = self.get_table_rows(table_name)
        table_json = {'@odata.context': odata_context_url, 'value': table_rows}
        if formatted:
            return ujson.dumps(table_json, indent=4)
        else:
            return ujson.dumps(table_json, separators=(',', ':'))

    def dump_database(self, folder, formatted=False):
        """
        Create a metadata file for the database schemas and a JSON file for
        each table, suitable for creating an OData-compatible API endpoint.

        :param folder: Location to store output files
        :param formatted: JSON output is formatted with indentation, defaults to false
        """
        os.makedirs(folder, exist_ok=True)
        schema_filename = os.path.join(folder, '$metadata')
        schema_xml = self.get_database_schema_xml()
        with open(schema_filename, 'w') as schema_file:
            schema_file.write(schema_xml)
        table_names = self.get_table_names()
        for table_name in table_names:
            table_filename = os.path.join(folder, table_name)
            table_json = self.get_table_json(table_name, formatted)
            with open(table_filename, 'w') as table_file:
                table_file.write(table_json)

    def __init__(self, *args, **kwargs):
        """Construct an instance of the class."""
        sqlite_filename = kwargs['sqlite_filename']
        sqlite_uri = f'file:{sqlite_filename}?mode=ro'
        self._connection = sqlite3.connect(sqlite_uri, uri=True)
