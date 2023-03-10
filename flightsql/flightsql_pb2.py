# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flightsql/flightsql.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x66lightsql/flightsql.proto\x12\x19\x61rrow.flight.protocol.sql\x1a google/protobuf/descriptor.proto\"&\n\x11\x43ommandGetSqlInfo\x12\x0c\n\x04info\x18\x01 \x03(\r:\x03\xc0>\x01\"C\n\x16\x43ommandGetXdbcTypeInfo\x12\x16\n\tdata_type\x18\x01 \x01(\x05H\x00\x88\x01\x01:\x03\xc0>\x01\x42\x0c\n\n_data_type\"\x19\n\x12\x43ommandGetCatalogs:\x03\xc0>\x01\"\x80\x01\n\x13\x43ommandGetDbSchemas\x12\x14\n\x07\x63\x61talog\x18\x01 \x01(\tH\x00\x88\x01\x01\x12%\n\x18\x64\x62_schema_filter_pattern\x18\x02 \x01(\tH\x01\x88\x01\x01:\x03\xc0>\x01\x42\n\n\x08_catalogB\x1b\n\x19_db_schema_filter_pattern\"\xf0\x01\n\x10\x43ommandGetTables\x12\x14\n\x07\x63\x61talog\x18\x01 \x01(\tH\x00\x88\x01\x01\x12%\n\x18\x64\x62_schema_filter_pattern\x18\x02 \x01(\tH\x01\x88\x01\x01\x12&\n\x19table_name_filter_pattern\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x13\n\x0btable_types\x18\x04 \x03(\t\x12\x16\n\x0einclude_schema\x18\x05 \x01(\x08:\x03\xc0>\x01\x42\n\n\x08_catalogB\x1b\n\x19_db_schema_filter_patternB\x1c\n\x1a_table_name_filter_pattern\"\x1b\n\x14\x43ommandGetTableTypes:\x03\xc0>\x01\"s\n\x15\x43ommandGetPrimaryKeys\x12\x14\n\x07\x63\x61talog\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tdb_schema\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\r\n\x05table\x18\x03 \x01(\t:\x03\xc0>\x01\x42\n\n\x08_catalogB\x0c\n\n_db_schema\"t\n\x16\x43ommandGetExportedKeys\x12\x14\n\x07\x63\x61talog\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tdb_schema\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\r\n\x05table\x18\x03 \x01(\t:\x03\xc0>\x01\x42\n\n\x08_catalogB\x0c\n\n_db_schema\"t\n\x16\x43ommandGetImportedKeys\x12\x14\n\x07\x63\x61talog\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tdb_schema\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\r\n\x05table\x18\x03 \x01(\t:\x03\xc0>\x01\x42\n\n\x08_catalogB\x0c\n\n_db_schema\"\xeb\x01\n\x18\x43ommandGetCrossReference\x12\x17\n\npk_catalog\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x19\n\x0cpk_db_schema\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x10\n\x08pk_table\x18\x03 \x01(\t\x12\x17\n\nfk_catalog\x18\x04 \x01(\tH\x02\x88\x01\x01\x12\x19\n\x0c\x66k_db_schema\x18\x05 \x01(\tH\x03\x88\x01\x01\x12\x10\n\x08\x66k_table\x18\x06 \x01(\t:\x03\xc0>\x01\x42\r\n\x0b_pk_catalogB\x0f\n\r_pk_db_schemaB\r\n\x0b_fk_catalogB\x0f\n\r_fk_db_schema\"j\n$ActionCreatePreparedStatementRequest\x12\r\n\x05query\x18\x01 \x01(\t\x12\x1b\n\x0etransaction_id\x18\x02 \x01(\x0cH\x00\x88\x01\x01:\x03\xc0>\x01\x42\x11\n\x0f_transaction_id\"3\n\rSubstraitPlan\x12\x0c\n\x04plan\x18\x01 \x01(\x0c\x12\x0f\n\x07version\x18\x02 \x01(\t:\x03\xc0>\x01\"\x97\x01\n(ActionCreatePreparedSubstraitPlanRequest\x12\x36\n\x04plan\x18\x01 \x01(\x0b\x32(.arrow.flight.protocol.sql.SubstraitPlan\x12\x1b\n\x0etransaction_id\x18\x02 \x01(\x0cH\x00\x88\x01\x01:\x03\xc0>\x01\x42\x11\n\x0f_transaction_id\"\x7f\n#ActionCreatePreparedStatementResult\x12!\n\x19prepared_statement_handle\x18\x01 \x01(\x0c\x12\x16\n\x0e\x64\x61taset_schema\x18\x02 \x01(\x0c\x12\x18\n\x10parameter_schema\x18\x03 \x01(\x0c:\x03\xc0>\x01\"M\n#ActionClosePreparedStatementRequest\x12!\n\x19prepared_statement_handle\x18\x01 \x01(\x0c:\x03\xc0>\x01\"$\n\x1d\x41\x63tionBeginTransactionRequest:\x03\xc0>\x01\"H\n\x1b\x41\x63tionBeginSavepointRequest\x12\x16\n\x0etransaction_id\x18\x01 \x01(\x0c\x12\x0c\n\x04name\x18\x02 \x01(\t:\x03\xc0>\x01\";\n\x1c\x41\x63tionBeginTransactionResult\x12\x16\n\x0etransaction_id\x18\x01 \x01(\x0c:\x03\xc0>\x01\"7\n\x1a\x41\x63tionBeginSavepointResult\x12\x14\n\x0csavepoint_id\x18\x01 \x01(\x0c:\x03\xc0>\x01\"\xfe\x01\n\x1b\x41\x63tionEndTransactionRequest\x12\x16\n\x0etransaction_id\x18\x01 \x01(\x0c\x12U\n\x06\x61\x63tion\x18\x02 \x01(\x0e\x32\x45.arrow.flight.protocol.sql.ActionEndTransactionRequest.EndTransaction\"k\n\x0e\x45ndTransaction\x12\x1f\n\x1b\x45ND_TRANSACTION_UNSPECIFIED\x10\x00\x12\x1a\n\x16\x45ND_TRANSACTION_COMMIT\x10\x01\x12\x1c\n\x18\x45ND_TRANSACTION_ROLLBACK\x10\x02:\x03\xc0>\x01\"\xef\x01\n\x19\x41\x63tionEndSavepointRequest\x12\x14\n\x0csavepoint_id\x18\x01 \x01(\x0c\x12Q\n\x06\x61\x63tion\x18\x02 \x01(\x0e\x32\x41.arrow.flight.protocol.sql.ActionEndSavepointRequest.EndSavepoint\"d\n\x0c\x45ndSavepoint\x12\x1d\n\x19\x45ND_SAVEPOINT_UNSPECIFIED\x10\x00\x12\x19\n\x15\x45ND_SAVEPOINT_RELEASE\x10\x01\x12\x1a\n\x16\x45ND_SAVEPOINT_ROLLBACK\x10\x02:\x03\xc0>\x01\"[\n\x15\x43ommandStatementQuery\x12\r\n\x05query\x18\x01 \x01(\t\x12\x1b\n\x0etransaction_id\x18\x02 \x01(\x0cH\x00\x88\x01\x01:\x03\xc0>\x01\x42\x11\n\x0f_transaction_id\"\x8c\x01\n\x1d\x43ommandStatementSubstraitPlan\x12\x36\n\x04plan\x18\x01 \x01(\x0b\x32(.arrow.flight.protocol.sql.SubstraitPlan\x12\x1b\n\x0etransaction_id\x18\x02 \x01(\x0cH\x00\x88\x01\x01:\x03\xc0>\x01\x42\x11\n\x0f_transaction_id\"5\n\x14TicketStatementQuery\x12\x18\n\x10statement_handle\x18\x01 \x01(\x0c:\x03\xc0>\x01\"G\n\x1d\x43ommandPreparedStatementQuery\x12!\n\x19prepared_statement_handle\x18\x01 \x01(\x0c:\x03\xc0>\x01\"\\\n\x16\x43ommandStatementUpdate\x12\r\n\x05query\x18\x01 \x01(\t\x12\x1b\n\x0etransaction_id\x18\x02 \x01(\x0cH\x00\x88\x01\x01:\x03\xc0>\x01\x42\x11\n\x0f_transaction_id\"H\n\x1e\x43ommandPreparedStatementUpdate\x12!\n\x19prepared_statement_handle\x18\x01 \x01(\x0c:\x03\xc0>\x01\".\n\x11\x44oPutUpdateResult\x12\x14\n\x0crecord_count\x18\x01 \x01(\x03:\x03\xc0>\x01\"-\n\x18\x41\x63tionCancelQueryRequest\x12\x0c\n\x04info\x18\x01 \x01(\x0c:\x03\xc0>\x01\"\xfd\x01\n\x17\x41\x63tionCancelQueryResult\x12O\n\x06result\x18\x01 \x01(\x0e\x32?.arrow.flight.protocol.sql.ActionCancelQueryResult.CancelResult\"\x8b\x01\n\x0c\x43\x61ncelResult\x12\x1d\n\x19\x43\x41NCEL_RESULT_UNSPECIFIED\x10\x00\x12\x1b\n\x17\x43\x41NCEL_RESULT_CANCELLED\x10\x01\x12\x1c\n\x18\x43\x41NCEL_RESULT_CANCELLING\x10\x02\x12!\n\x1d\x43\x41NCEL_RESULT_NOT_CANCELLABLE\x10\x03:\x03\xc0>\x01*\xb7\x18\n\x07SqlInfo\x12\x1a\n\x16\x46LIGHT_SQL_SERVER_NAME\x10\x00\x12\x1d\n\x19\x46LIGHT_SQL_SERVER_VERSION\x10\x01\x12#\n\x1f\x46LIGHT_SQL_SERVER_ARROW_VERSION\x10\x02\x12\x1f\n\x1b\x46LIGHT_SQL_SERVER_READ_ONLY\x10\x03\x12\x19\n\x15\x46LIGHT_SQL_SERVER_SQL\x10\x04\x12\x1f\n\x1b\x46LIGHT_SQL_SERVER_SUBSTRAIT\x10\x05\x12+\n\'FLIGHT_SQL_SERVER_SUBSTRAIT_MIN_VERSION\x10\x06\x12+\n\'FLIGHT_SQL_SERVER_SUBSTRAIT_MAX_VERSION\x10\x07\x12!\n\x1d\x46LIGHT_SQL_SERVER_TRANSACTION\x10\x08\x12\x1c\n\x18\x46LIGHT_SQL_SERVER_CANCEL\x10\t\x12\'\n#FLIGHT_SQL_SERVER_STATEMENT_TIMEOUT\x10\x64\x12)\n%FLIGHT_SQL_SERVER_TRANSACTION_TIMEOUT\x10\x65\x12\x14\n\x0fSQL_DDL_CATALOG\x10\xf4\x03\x12\x13\n\x0eSQL_DDL_SCHEMA\x10\xf5\x03\x12\x12\n\rSQL_DDL_TABLE\x10\xf6\x03\x12\x18\n\x13SQL_IDENTIFIER_CASE\x10\xf7\x03\x12\x1e\n\x19SQL_IDENTIFIER_QUOTE_CHAR\x10\xf8\x03\x12\x1f\n\x1aSQL_QUOTED_IDENTIFIER_CASE\x10\xf9\x03\x12\"\n\x1dSQL_ALL_TABLES_ARE_SELECTABLE\x10\xfa\x03\x12\x16\n\x11SQL_NULL_ORDERING\x10\xfb\x03\x12\x11\n\x0cSQL_KEYWORDS\x10\xfc\x03\x12\x1a\n\x15SQL_NUMERIC_FUNCTIONS\x10\xfd\x03\x12\x19\n\x14SQL_STRING_FUNCTIONS\x10\xfe\x03\x12\x19\n\x14SQL_SYSTEM_FUNCTIONS\x10\xff\x03\x12\x1b\n\x16SQL_DATETIME_FUNCTIONS\x10\x80\x04\x12\x1d\n\x18SQL_SEARCH_STRING_ESCAPE\x10\x81\x04\x12\x1e\n\x19SQL_EXTRA_NAME_CHARACTERS\x10\x82\x04\x12!\n\x1cSQL_SUPPORTS_COLUMN_ALIASING\x10\x83\x04\x12\x1f\n\x1aSQL_NULL_PLUS_NULL_IS_NULL\x10\x84\x04\x12\x19\n\x14SQL_SUPPORTS_CONVERT\x10\x85\x04\x12)\n$SQL_SUPPORTS_TABLE_CORRELATION_NAMES\x10\x86\x04\x12\x33\n.SQL_SUPPORTS_DIFFERENT_TABLE_CORRELATION_NAMES\x10\x87\x04\x12)\n$SQL_SUPPORTS_EXPRESSIONS_IN_ORDER_BY\x10\x88\x04\x12$\n\x1fSQL_SUPPORTS_ORDER_BY_UNRELATED\x10\x89\x04\x12\x1b\n\x16SQL_SUPPORTED_GROUP_BY\x10\x8a\x04\x12$\n\x1fSQL_SUPPORTS_LIKE_ESCAPE_CLAUSE\x10\x8b\x04\x12&\n!SQL_SUPPORTS_NON_NULLABLE_COLUMNS\x10\x8c\x04\x12\x1a\n\x15SQL_SUPPORTED_GRAMMAR\x10\x8d\x04\x12\x1f\n\x1aSQL_ANSI92_SUPPORTED_LEVEL\x10\x8e\x04\x12\x30\n+SQL_SUPPORTS_INTEGRITY_ENHANCEMENT_FACILITY\x10\x8f\x04\x12\"\n\x1dSQL_OUTER_JOINS_SUPPORT_LEVEL\x10\x90\x04\x12\x14\n\x0fSQL_SCHEMA_TERM\x10\x91\x04\x12\x17\n\x12SQL_PROCEDURE_TERM\x10\x92\x04\x12\x15\n\x10SQL_CATALOG_TERM\x10\x93\x04\x12\x19\n\x14SQL_CATALOG_AT_START\x10\x94\x04\x12\"\n\x1dSQL_SCHEMAS_SUPPORTED_ACTIONS\x10\x95\x04\x12#\n\x1eSQL_CATALOGS_SUPPORTED_ACTIONS\x10\x96\x04\x12&\n!SQL_SUPPORTED_POSITIONED_COMMANDS\x10\x97\x04\x12$\n\x1fSQL_SELECT_FOR_UPDATE_SUPPORTED\x10\x98\x04\x12$\n\x1fSQL_STORED_PROCEDURES_SUPPORTED\x10\x99\x04\x12\x1d\n\x18SQL_SUPPORTED_SUBQUERIES\x10\x9a\x04\x12(\n#SQL_CORRELATED_SUBQUERIES_SUPPORTED\x10\x9b\x04\x12\x19\n\x14SQL_SUPPORTED_UNIONS\x10\x9c\x04\x12\"\n\x1dSQL_MAX_BINARY_LITERAL_LENGTH\x10\x9d\x04\x12 \n\x1bSQL_MAX_CHAR_LITERAL_LENGTH\x10\x9e\x04\x12\x1f\n\x1aSQL_MAX_COLUMN_NAME_LENGTH\x10\x9f\x04\x12 \n\x1bSQL_MAX_COLUMNS_IN_GROUP_BY\x10\xa0\x04\x12\x1d\n\x18SQL_MAX_COLUMNS_IN_INDEX\x10\xa1\x04\x12 \n\x1bSQL_MAX_COLUMNS_IN_ORDER_BY\x10\xa2\x04\x12\x1e\n\x19SQL_MAX_COLUMNS_IN_SELECT\x10\xa3\x04\x12\x1d\n\x18SQL_MAX_COLUMNS_IN_TABLE\x10\xa4\x04\x12\x18\n\x13SQL_MAX_CONNECTIONS\x10\xa5\x04\x12\x1f\n\x1aSQL_MAX_CURSOR_NAME_LENGTH\x10\xa6\x04\x12\x19\n\x14SQL_MAX_INDEX_LENGTH\x10\xa7\x04\x12\x1e\n\x19SQL_DB_SCHEMA_NAME_LENGTH\x10\xa8\x04\x12\"\n\x1dSQL_MAX_PROCEDURE_NAME_LENGTH\x10\xa9\x04\x12 \n\x1bSQL_MAX_CATALOG_NAME_LENGTH\x10\xaa\x04\x12\x15\n\x10SQL_MAX_ROW_SIZE\x10\xab\x04\x12$\n\x1fSQL_MAX_ROW_SIZE_INCLUDES_BLOBS\x10\xac\x04\x12\x1d\n\x18SQL_MAX_STATEMENT_LENGTH\x10\xad\x04\x12\x17\n\x12SQL_MAX_STATEMENTS\x10\xae\x04\x12\x1e\n\x19SQL_MAX_TABLE_NAME_LENGTH\x10\xaf\x04\x12\x1d\n\x18SQL_MAX_TABLES_IN_SELECT\x10\xb0\x04\x12\x1c\n\x17SQL_MAX_USERNAME_LENGTH\x10\xb1\x04\x12&\n!SQL_DEFAULT_TRANSACTION_ISOLATION\x10\xb2\x04\x12\x1f\n\x1aSQL_TRANSACTIONS_SUPPORTED\x10\xb3\x04\x12\x30\n+SQL_SUPPORTED_TRANSACTIONS_ISOLATION_LEVELS\x10\xb4\x04\x12\x32\n-SQL_DATA_DEFINITION_CAUSES_TRANSACTION_COMMIT\x10\xb5\x04\x12\x31\n,SQL_DATA_DEFINITIONS_IN_TRANSACTIONS_IGNORED\x10\xb6\x04\x12#\n\x1eSQL_SUPPORTED_RESULT_SET_TYPES\x10\xb7\x04\x12;\n6SQL_SUPPORTED_CONCURRENCIES_FOR_RESULT_SET_UNSPECIFIED\x10\xb8\x04\x12<\n7SQL_SUPPORTED_CONCURRENCIES_FOR_RESULT_SET_FORWARD_ONLY\x10\xb9\x04\x12@\n;SQL_SUPPORTED_CONCURRENCIES_FOR_RESULT_SET_SCROLL_SENSITIVE\x10\xba\x04\x12\x42\n=SQL_SUPPORTED_CONCURRENCIES_FOR_RESULT_SET_SCROLL_INSENSITIVE\x10\xbb\x04\x12 \n\x1bSQL_BATCH_UPDATES_SUPPORTED\x10\xbc\x04\x12\x1d\n\x18SQL_SAVEPOINTS_SUPPORTED\x10\xbd\x04\x12#\n\x1eSQL_NAMED_PARAMETERS_SUPPORTED\x10\xbe\x04\x12\x1d\n\x18SQL_LOCATORS_UPDATE_COPY\x10\xbf\x04\x12\x35\n0SQL_STORED_FUNCTIONS_USING_CALL_SYNTAX_SUPPORTED\x10\xc0\x04*\x91\x01\n\x17SqlSupportedTransaction\x12\"\n\x1eSQL_SUPPORTED_TRANSACTION_NONE\x10\x00\x12)\n%SQL_SUPPORTED_TRANSACTION_TRANSACTION\x10\x01\x12\'\n#SQL_SUPPORTED_TRANSACTION_SAVEPOINT\x10\x02*\xb2\x01\n\x1bSqlSupportedCaseSensitivity\x12 \n\x1cSQL_CASE_SENSITIVITY_UNKNOWN\x10\x00\x12)\n%SQL_CASE_SENSITIVITY_CASE_INSENSITIVE\x10\x01\x12\"\n\x1eSQL_CASE_SENSITIVITY_UPPERCASE\x10\x02\x12\"\n\x1eSQL_CASE_SENSITIVITY_LOWERCASE\x10\x03*\x82\x01\n\x0fSqlNullOrdering\x12\x19\n\x15SQL_NULLS_SORTED_HIGH\x10\x00\x12\x18\n\x14SQL_NULLS_SORTED_LOW\x10\x01\x12\x1d\n\x19SQL_NULLS_SORTED_AT_START\x10\x02\x12\x1b\n\x17SQL_NULLS_SORTED_AT_END\x10\x03*^\n\x13SupportedSqlGrammar\x12\x17\n\x13SQL_MINIMUM_GRAMMAR\x10\x00\x12\x14\n\x10SQL_CORE_GRAMMAR\x10\x01\x12\x18\n\x14SQL_EXTENDED_GRAMMAR\x10\x02*h\n\x1eSupportedAnsi92SqlGrammarLevel\x12\x14\n\x10\x41NSI92_ENTRY_SQL\x10\x00\x12\x1b\n\x17\x41NSI92_INTERMEDIATE_SQL\x10\x01\x12\x13\n\x0f\x41NSI92_FULL_SQL\x10\x02*m\n\x19SqlOuterJoinsSupportLevel\x12\x19\n\x15SQL_JOINS_UNSUPPORTED\x10\x00\x12\x1b\n\x17SQL_LIMITED_OUTER_JOINS\x10\x01\x12\x18\n\x14SQL_FULL_OUTER_JOINS\x10\x02*Q\n\x13SqlSupportedGroupBy\x12\x1a\n\x16SQL_GROUP_BY_UNRELATED\x10\x00\x12\x1e\n\x1aSQL_GROUP_BY_BEYOND_SELECT\x10\x01*\x90\x01\n\x1aSqlSupportedElementActions\x12\"\n\x1eSQL_ELEMENT_IN_PROCEDURE_CALLS\x10\x00\x12$\n SQL_ELEMENT_IN_INDEX_DEFINITIONS\x10\x01\x12(\n$SQL_ELEMENT_IN_PRIVILEGE_DEFINITIONS\x10\x02*V\n\x1eSqlSupportedPositionedCommands\x12\x19\n\x15SQL_POSITIONED_DELETE\x10\x00\x12\x19\n\x15SQL_POSITIONED_UPDATE\x10\x01*\x97\x01\n\x16SqlSupportedSubqueries\x12!\n\x1dSQL_SUBQUERIES_IN_COMPARISONS\x10\x00\x12\x1c\n\x18SQL_SUBQUERIES_IN_EXISTS\x10\x01\x12\x19\n\x15SQL_SUBQUERIES_IN_INS\x10\x02\x12!\n\x1dSQL_SUBQUERIES_IN_QUANTIFIEDS\x10\x03*6\n\x12SqlSupportedUnions\x12\r\n\tSQL_UNION\x10\x00\x12\x11\n\rSQL_UNION_ALL\x10\x01*\xc9\x01\n\x1cSqlTransactionIsolationLevel\x12\x18\n\x14SQL_TRANSACTION_NONE\x10\x00\x12$\n SQL_TRANSACTION_READ_UNCOMMITTED\x10\x01\x12\"\n\x1eSQL_TRANSACTION_READ_COMMITTED\x10\x02\x12#\n\x1fSQL_TRANSACTION_REPEATABLE_READ\x10\x03\x12 \n\x1cSQL_TRANSACTION_SERIALIZABLE\x10\x04*\x89\x01\n\x18SqlSupportedTransactions\x12\x1f\n\x1bSQL_TRANSACTION_UNSPECIFIED\x10\x00\x12$\n SQL_DATA_DEFINITION_TRANSACTIONS\x10\x01\x12&\n\"SQL_DATA_MANIPULATION_TRANSACTIONS\x10\x02*\xbc\x01\n\x19SqlSupportedResultSetType\x12#\n\x1fSQL_RESULT_SET_TYPE_UNSPECIFIED\x10\x00\x12$\n SQL_RESULT_SET_TYPE_FORWARD_ONLY\x10\x01\x12*\n&SQL_RESULT_SET_TYPE_SCROLL_INSENSITIVE\x10\x02\x12(\n$SQL_RESULT_SET_TYPE_SCROLL_SENSITIVE\x10\x03*\xa2\x01\n SqlSupportedResultSetConcurrency\x12*\n&SQL_RESULT_SET_CONCURRENCY_UNSPECIFIED\x10\x00\x12(\n$SQL_RESULT_SET_CONCURRENCY_READ_ONLY\x10\x01\x12(\n$SQL_RESULT_SET_CONCURRENCY_UPDATABLE\x10\x02*\x99\x04\n\x12SqlSupportsConvert\x12\x16\n\x12SQL_CONVERT_BIGINT\x10\x00\x12\x16\n\x12SQL_CONVERT_BINARY\x10\x01\x12\x13\n\x0fSQL_CONVERT_BIT\x10\x02\x12\x14\n\x10SQL_CONVERT_CHAR\x10\x03\x12\x14\n\x10SQL_CONVERT_DATE\x10\x04\x12\x17\n\x13SQL_CONVERT_DECIMAL\x10\x05\x12\x15\n\x11SQL_CONVERT_FLOAT\x10\x06\x12\x17\n\x13SQL_CONVERT_INTEGER\x10\x07\x12!\n\x1dSQL_CONVERT_INTERVAL_DAY_TIME\x10\x08\x12#\n\x1fSQL_CONVERT_INTERVAL_YEAR_MONTH\x10\t\x12\x1d\n\x19SQL_CONVERT_LONGVARBINARY\x10\n\x12\x1b\n\x17SQL_CONVERT_LONGVARCHAR\x10\x0b\x12\x17\n\x13SQL_CONVERT_NUMERIC\x10\x0c\x12\x14\n\x10SQL_CONVERT_REAL\x10\r\x12\x18\n\x14SQL_CONVERT_SMALLINT\x10\x0e\x12\x14\n\x10SQL_CONVERT_TIME\x10\x0f\x12\x19\n\x15SQL_CONVERT_TIMESTAMP\x10\x10\x12\x17\n\x13SQL_CONVERT_TINYINT\x10\x11\x12\x19\n\x15SQL_CONVERT_VARBINARY\x10\x12\x12\x17\n\x13SQL_CONVERT_VARCHAR\x10\x13*\x8f\x04\n\x0cXdbcDataType\x12\x15\n\x11XDBC_UNKNOWN_TYPE\x10\x00\x12\r\n\tXDBC_CHAR\x10\x01\x12\x10\n\x0cXDBC_NUMERIC\x10\x02\x12\x10\n\x0cXDBC_DECIMAL\x10\x03\x12\x10\n\x0cXDBC_INTEGER\x10\x04\x12\x11\n\rXDBC_SMALLINT\x10\x05\x12\x0e\n\nXDBC_FLOAT\x10\x06\x12\r\n\tXDBC_REAL\x10\x07\x12\x0f\n\x0bXDBC_DOUBLE\x10\x08\x12\x11\n\rXDBC_DATETIME\x10\t\x12\x11\n\rXDBC_INTERVAL\x10\n\x12\x10\n\x0cXDBC_VARCHAR\x10\x0c\x12\r\n\tXDBC_DATE\x10[\x12\r\n\tXDBC_TIME\x10\\\x12\x12\n\x0eXDBC_TIMESTAMP\x10]\x12\x1d\n\x10XDBC_LONGVARCHAR\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x18\n\x0bXDBC_BINARY\x10\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x1b\n\x0eXDBC_VARBINARY\x10\xfd\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x1f\n\x12XDBC_LONGVARBINARY\x10\xfc\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x18\n\x0bXDBC_BIGINT\x10\xfb\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x19\n\x0cXDBC_TINYINT\x10\xfa\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x15\n\x08XDBC_BIT\x10\xf9\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x17\n\nXDBC_WCHAR\x10\xf8\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x1a\n\rXDBC_WVARCHAR\x10\xf7\xff\xff\xff\xff\xff\xff\xff\xff\x01*\xa3\x08\n\x13XdbcDatetimeSubcode\x12\x18\n\x14XDBC_SUBCODE_UNKNOWN\x10\x00\x12\x15\n\x11XDBC_SUBCODE_YEAR\x10\x01\x12\x15\n\x11XDBC_SUBCODE_DATE\x10\x01\x12\x15\n\x11XDBC_SUBCODE_TIME\x10\x02\x12\x16\n\x12XDBC_SUBCODE_MONTH\x10\x02\x12\x1a\n\x16XDBC_SUBCODE_TIMESTAMP\x10\x03\x12\x14\n\x10XDBC_SUBCODE_DAY\x10\x03\x12#\n\x1fXDBC_SUBCODE_TIME_WITH_TIMEZONE\x10\x04\x12\x15\n\x11XDBC_SUBCODE_HOUR\x10\x04\x12(\n$XDBC_SUBCODE_TIMESTAMP_WITH_TIMEZONE\x10\x05\x12\x17\n\x13XDBC_SUBCODE_MINUTE\x10\x05\x12\x17\n\x13XDBC_SUBCODE_SECOND\x10\x06\x12\x1e\n\x1aXDBC_SUBCODE_YEAR_TO_MONTH\x10\x07\x12\x1c\n\x18XDBC_SUBCODE_DAY_TO_HOUR\x10\x08\x12\x1e\n\x1aXDBC_SUBCODE_DAY_TO_MINUTE\x10\t\x12\x1e\n\x1aXDBC_SUBCODE_DAY_TO_SECOND\x10\n\x12\x1f\n\x1bXDBC_SUBCODE_HOUR_TO_MINUTE\x10\x0b\x12\x1f\n\x1bXDBC_SUBCODE_HOUR_TO_SECOND\x10\x0c\x12!\n\x1dXDBC_SUBCODE_MINUTE_TO_SECOND\x10\r\x12\x1e\n\x1aXDBC_SUBCODE_INTERVAL_YEAR\x10\x65\x12\x1f\n\x1bXDBC_SUBCODE_INTERVAL_MONTH\x10\x66\x12\x1d\n\x19XDBC_SUBCODE_INTERVAL_DAY\x10g\x12\x1e\n\x1aXDBC_SUBCODE_INTERVAL_HOUR\x10h\x12 \n\x1cXDBC_SUBCODE_INTERVAL_MINUTE\x10i\x12 \n\x1cXDBC_SUBCODE_INTERVAL_SECOND\x10j\x12\'\n#XDBC_SUBCODE_INTERVAL_YEAR_TO_MONTH\x10k\x12%\n!XDBC_SUBCODE_INTERVAL_DAY_TO_HOUR\x10l\x12\'\n#XDBC_SUBCODE_INTERVAL_DAY_TO_MINUTE\x10m\x12\'\n#XDBC_SUBCODE_INTERVAL_DAY_TO_SECOND\x10n\x12(\n$XDBC_SUBCODE_INTERVAL_HOUR_TO_MINUTE\x10o\x12(\n$XDBC_SUBCODE_INTERVAL_HOUR_TO_SECOND\x10p\x12*\n&XDBC_SUBCODE_INTERVAL_MINUTE_TO_SECOND\x10q\x1a\x02\x10\x01*W\n\x08Nullable\x12\x18\n\x14NULLABILITY_NO_NULLS\x10\x00\x12\x18\n\x14NULLABILITY_NULLABLE\x10\x01\x12\x17\n\x13NULLABILITY_UNKNOWN\x10\x02*a\n\nSearchable\x12\x13\n\x0fSEARCHABLE_NONE\x10\x00\x12\x13\n\x0fSEARCHABLE_CHAR\x10\x01\x12\x14\n\x10SEARCHABLE_BASIC\x10\x02\x12\x13\n\x0fSEARCHABLE_FULL\x10\x03*\\\n\x11UpdateDeleteRules\x12\x0b\n\x07\x43\x41SCADE\x10\x00\x12\x0c\n\x08RESTRICT\x10\x01\x12\x0c\n\x08SET_NULL\x10\x02\x12\r\n\tNO_ACTION\x10\x03\x12\x0f\n\x0bSET_DEFAULT\x10\x04:6\n\x0c\x65xperimental\x12\x1f.google.protobuf.MessageOptions\x18\xe8\x07 \x01(\x08\x42[\n org.apache.arrow.flight.sql.implZ7github.com/apache/arrow/go/arrow/flight/internal/flightb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flightsql.flightsql_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(experimental)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n org.apache.arrow.flight.sql.implZ7github.com/apache/arrow/go/arrow/flight/internal/flight'
  _XDBCDATETIMESUBCODE._options = None
  _XDBCDATETIMESUBCODE._serialized_options = b'\020\001'
  _COMMANDGETSQLINFO._options = None
  _COMMANDGETSQLINFO._serialized_options = b'\300>\001'
  _COMMANDGETXDBCTYPEINFO._options = None
  _COMMANDGETXDBCTYPEINFO._serialized_options = b'\300>\001'
  _COMMANDGETCATALOGS._options = None
  _COMMANDGETCATALOGS._serialized_options = b'\300>\001'
  _COMMANDGETDBSCHEMAS._options = None
  _COMMANDGETDBSCHEMAS._serialized_options = b'\300>\001'
  _COMMANDGETTABLES._options = None
  _COMMANDGETTABLES._serialized_options = b'\300>\001'
  _COMMANDGETTABLETYPES._options = None
  _COMMANDGETTABLETYPES._serialized_options = b'\300>\001'
  _COMMANDGETPRIMARYKEYS._options = None
  _COMMANDGETPRIMARYKEYS._serialized_options = b'\300>\001'
  _COMMANDGETEXPORTEDKEYS._options = None
  _COMMANDGETEXPORTEDKEYS._serialized_options = b'\300>\001'
  _COMMANDGETIMPORTEDKEYS._options = None
  _COMMANDGETIMPORTEDKEYS._serialized_options = b'\300>\001'
  _COMMANDGETCROSSREFERENCE._options = None
  _COMMANDGETCROSSREFERENCE._serialized_options = b'\300>\001'
  _ACTIONCREATEPREPAREDSTATEMENTREQUEST._options = None
  _ACTIONCREATEPREPAREDSTATEMENTREQUEST._serialized_options = b'\300>\001'
  _SUBSTRAITPLAN._options = None
  _SUBSTRAITPLAN._serialized_options = b'\300>\001'
  _ACTIONCREATEPREPAREDSUBSTRAITPLANREQUEST._options = None
  _ACTIONCREATEPREPAREDSUBSTRAITPLANREQUEST._serialized_options = b'\300>\001'
  _ACTIONCREATEPREPAREDSTATEMENTRESULT._options = None
  _ACTIONCREATEPREPAREDSTATEMENTRESULT._serialized_options = b'\300>\001'
  _ACTIONCLOSEPREPAREDSTATEMENTREQUEST._options = None
  _ACTIONCLOSEPREPAREDSTATEMENTREQUEST._serialized_options = b'\300>\001'
  _ACTIONBEGINTRANSACTIONREQUEST._options = None
  _ACTIONBEGINTRANSACTIONREQUEST._serialized_options = b'\300>\001'
  _ACTIONBEGINSAVEPOINTREQUEST._options = None
  _ACTIONBEGINSAVEPOINTREQUEST._serialized_options = b'\300>\001'
  _ACTIONBEGINTRANSACTIONRESULT._options = None
  _ACTIONBEGINTRANSACTIONRESULT._serialized_options = b'\300>\001'
  _ACTIONBEGINSAVEPOINTRESULT._options = None
  _ACTIONBEGINSAVEPOINTRESULT._serialized_options = b'\300>\001'
  _ACTIONENDTRANSACTIONREQUEST._options = None
  _ACTIONENDTRANSACTIONREQUEST._serialized_options = b'\300>\001'
  _ACTIONENDSAVEPOINTREQUEST._options = None
  _ACTIONENDSAVEPOINTREQUEST._serialized_options = b'\300>\001'
  _COMMANDSTATEMENTQUERY._options = None
  _COMMANDSTATEMENTQUERY._serialized_options = b'\300>\001'
  _COMMANDSTATEMENTSUBSTRAITPLAN._options = None
  _COMMANDSTATEMENTSUBSTRAITPLAN._serialized_options = b'\300>\001'
  _TICKETSTATEMENTQUERY._options = None
  _TICKETSTATEMENTQUERY._serialized_options = b'\300>\001'
  _COMMANDPREPAREDSTATEMENTQUERY._options = None
  _COMMANDPREPAREDSTATEMENTQUERY._serialized_options = b'\300>\001'
  _COMMANDSTATEMENTUPDATE._options = None
  _COMMANDSTATEMENTUPDATE._serialized_options = b'\300>\001'
  _COMMANDPREPAREDSTATEMENTUPDATE._options = None
  _COMMANDPREPAREDSTATEMENTUPDATE._serialized_options = b'\300>\001'
  _DOPUTUPDATERESULT._options = None
  _DOPUTUPDATERESULT._serialized_options = b'\300>\001'
  _ACTIONCANCELQUERYREQUEST._options = None
  _ACTIONCANCELQUERYREQUEST._serialized_options = b'\300>\001'
  _ACTIONCANCELQUERYRESULT._options = None
  _ACTIONCANCELQUERYRESULT._serialized_options = b'\300>\001'
  _SQLINFO._serialized_start=3356
  _SQLINFO._serialized_end=6483
  _SQLSUPPORTEDTRANSACTION._serialized_start=6486
  _SQLSUPPORTEDTRANSACTION._serialized_end=6631
  _SQLSUPPORTEDCASESENSITIVITY._serialized_start=6634
  _SQLSUPPORTEDCASESENSITIVITY._serialized_end=6812
  _SQLNULLORDERING._serialized_start=6815
  _SQLNULLORDERING._serialized_end=6945
  _SUPPORTEDSQLGRAMMAR._serialized_start=6947
  _SUPPORTEDSQLGRAMMAR._serialized_end=7041
  _SUPPORTEDANSI92SQLGRAMMARLEVEL._serialized_start=7043
  _SUPPORTEDANSI92SQLGRAMMARLEVEL._serialized_end=7147
  _SQLOUTERJOINSSUPPORTLEVEL._serialized_start=7149
  _SQLOUTERJOINSSUPPORTLEVEL._serialized_end=7258
  _SQLSUPPORTEDGROUPBY._serialized_start=7260
  _SQLSUPPORTEDGROUPBY._serialized_end=7341
  _SQLSUPPORTEDELEMENTACTIONS._serialized_start=7344
  _SQLSUPPORTEDELEMENTACTIONS._serialized_end=7488
  _SQLSUPPORTEDPOSITIONEDCOMMANDS._serialized_start=7490
  _SQLSUPPORTEDPOSITIONEDCOMMANDS._serialized_end=7576
  _SQLSUPPORTEDSUBQUERIES._serialized_start=7579
  _SQLSUPPORTEDSUBQUERIES._serialized_end=7730
  _SQLSUPPORTEDUNIONS._serialized_start=7732
  _SQLSUPPORTEDUNIONS._serialized_end=7786
  _SQLTRANSACTIONISOLATIONLEVEL._serialized_start=7789
  _SQLTRANSACTIONISOLATIONLEVEL._serialized_end=7990
  _SQLSUPPORTEDTRANSACTIONS._serialized_start=7993
  _SQLSUPPORTEDTRANSACTIONS._serialized_end=8130
  _SQLSUPPORTEDRESULTSETTYPE._serialized_start=8133
  _SQLSUPPORTEDRESULTSETTYPE._serialized_end=8321
  _SQLSUPPORTEDRESULTSETCONCURRENCY._serialized_start=8324
  _SQLSUPPORTEDRESULTSETCONCURRENCY._serialized_end=8486
  _SQLSUPPORTSCONVERT._serialized_start=8489
  _SQLSUPPORTSCONVERT._serialized_end=9026
  _XDBCDATATYPE._serialized_start=9029
  _XDBCDATATYPE._serialized_end=9556
  _XDBCDATETIMESUBCODE._serialized_start=9559
  _XDBCDATETIMESUBCODE._serialized_end=10618
  _NULLABLE._serialized_start=10620
  _NULLABLE._serialized_end=10707
  _SEARCHABLE._serialized_start=10709
  _SEARCHABLE._serialized_end=10806
  _UPDATEDELETERULES._serialized_start=10808
  _UPDATEDELETERULES._serialized_end=10900
  _COMMANDGETSQLINFO._serialized_start=90
  _COMMANDGETSQLINFO._serialized_end=128
  _COMMANDGETXDBCTYPEINFO._serialized_start=130
  _COMMANDGETXDBCTYPEINFO._serialized_end=197
  _COMMANDGETCATALOGS._serialized_start=199
  _COMMANDGETCATALOGS._serialized_end=224
  _COMMANDGETDBSCHEMAS._serialized_start=227
  _COMMANDGETDBSCHEMAS._serialized_end=355
  _COMMANDGETTABLES._serialized_start=358
  _COMMANDGETTABLES._serialized_end=598
  _COMMANDGETTABLETYPES._serialized_start=600
  _COMMANDGETTABLETYPES._serialized_end=627
  _COMMANDGETPRIMARYKEYS._serialized_start=629
  _COMMANDGETPRIMARYKEYS._serialized_end=744
  _COMMANDGETEXPORTEDKEYS._serialized_start=746
  _COMMANDGETEXPORTEDKEYS._serialized_end=862
  _COMMANDGETIMPORTEDKEYS._serialized_start=864
  _COMMANDGETIMPORTEDKEYS._serialized_end=980
  _COMMANDGETCROSSREFERENCE._serialized_start=983
  _COMMANDGETCROSSREFERENCE._serialized_end=1218
  _ACTIONCREATEPREPAREDSTATEMENTREQUEST._serialized_start=1220
  _ACTIONCREATEPREPAREDSTATEMENTREQUEST._serialized_end=1326
  _SUBSTRAITPLAN._serialized_start=1328
  _SUBSTRAITPLAN._serialized_end=1379
  _ACTIONCREATEPREPAREDSUBSTRAITPLANREQUEST._serialized_start=1382
  _ACTIONCREATEPREPAREDSUBSTRAITPLANREQUEST._serialized_end=1533
  _ACTIONCREATEPREPAREDSTATEMENTRESULT._serialized_start=1535
  _ACTIONCREATEPREPAREDSTATEMENTRESULT._serialized_end=1662
  _ACTIONCLOSEPREPAREDSTATEMENTREQUEST._serialized_start=1664
  _ACTIONCLOSEPREPAREDSTATEMENTREQUEST._serialized_end=1741
  _ACTIONBEGINTRANSACTIONREQUEST._serialized_start=1743
  _ACTIONBEGINTRANSACTIONREQUEST._serialized_end=1779
  _ACTIONBEGINSAVEPOINTREQUEST._serialized_start=1781
  _ACTIONBEGINSAVEPOINTREQUEST._serialized_end=1853
  _ACTIONBEGINTRANSACTIONRESULT._serialized_start=1855
  _ACTIONBEGINTRANSACTIONRESULT._serialized_end=1914
  _ACTIONBEGINSAVEPOINTRESULT._serialized_start=1916
  _ACTIONBEGINSAVEPOINTRESULT._serialized_end=1971
  _ACTIONENDTRANSACTIONREQUEST._serialized_start=1974
  _ACTIONENDTRANSACTIONREQUEST._serialized_end=2228
  _ACTIONENDTRANSACTIONREQUEST_ENDTRANSACTION._serialized_start=2116
  _ACTIONENDTRANSACTIONREQUEST_ENDTRANSACTION._serialized_end=2223
  _ACTIONENDSAVEPOINTREQUEST._serialized_start=2231
  _ACTIONENDSAVEPOINTREQUEST._serialized_end=2470
  _ACTIONENDSAVEPOINTREQUEST_ENDSAVEPOINT._serialized_start=2365
  _ACTIONENDSAVEPOINTREQUEST_ENDSAVEPOINT._serialized_end=2465
  _COMMANDSTATEMENTQUERY._serialized_start=2472
  _COMMANDSTATEMENTQUERY._serialized_end=2563
  _COMMANDSTATEMENTSUBSTRAITPLAN._serialized_start=2566
  _COMMANDSTATEMENTSUBSTRAITPLAN._serialized_end=2706
  _TICKETSTATEMENTQUERY._serialized_start=2708
  _TICKETSTATEMENTQUERY._serialized_end=2761
  _COMMANDPREPAREDSTATEMENTQUERY._serialized_start=2763
  _COMMANDPREPAREDSTATEMENTQUERY._serialized_end=2834
  _COMMANDSTATEMENTUPDATE._serialized_start=2836
  _COMMANDSTATEMENTUPDATE._serialized_end=2928
  _COMMANDPREPAREDSTATEMENTUPDATE._serialized_start=2930
  _COMMANDPREPAREDSTATEMENTUPDATE._serialized_end=3002
  _DOPUTUPDATERESULT._serialized_start=3004
  _DOPUTUPDATERESULT._serialized_end=3050
  _ACTIONCANCELQUERYREQUEST._serialized_start=3052
  _ACTIONCANCELQUERYREQUEST._serialized_end=3097
  _ACTIONCANCELQUERYRESULT._serialized_start=3100
  _ACTIONCANCELQUERYRESULT._serialized_end=3353
  _ACTIONCANCELQUERYRESULT_CANCELRESULT._serialized_start=3209
  _ACTIONCANCELQUERYRESULT_CANCELRESULT._serialized_end=3348
# @@protoc_insertion_point(module_scope)
