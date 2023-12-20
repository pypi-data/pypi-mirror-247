# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict, Any, List


class ErrorResponse(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
    ):
        self.code = code
        self.message = message
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['code'] = self.code
        if self.message is not None:
            result['message'] = self.message
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('code') is not None:
            self.code = m.get('code')
        if m.get('message') is not None:
            self.message = m.get('message')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class VariablesValueFuncValue(TeaModel):
    def __init__(
        self,
        func_class_name: str = None,
        template: str = None,
    ):
        # The class name.
        self.func_class_name = func_class_name
        # The template of the variable.
        self.template = template

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.func_class_name is not None:
            result['funcClassName'] = self.func_class_name
        if self.template is not None:
            result['template'] = self.template
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('funcClassName') is not None:
            self.func_class_name = m.get('funcClassName')
        if m.get('template') is not None:
            self.template = m.get('template')
        return self


class VariablesValue(TeaModel):
    def __init__(
        self,
        disable_modify: bool = None,
        is_modify: bool = None,
        value: str = None,
        description: str = None,
        template_value: str = None,
        type: str = None,
        func_value: VariablesValueFuncValue = None,
    ):
        # Specifies whether the variable cannot be modified.
        self.disable_modify = disable_modify
        # Specifies whether the variable is modified.
        self.is_modify = is_modify
        # The value of the variable.
        self.value = value
        # The description about the variable.
        self.description = description
        # The value of the template.
        self.template_value = template_value
        # The type of the variable. Valid values:
        # 
        # *   NORMAL: a normal variable
        # *   FUNCTION: a function variable
        self.type = type
        # The function variable.
        self.func_value = func_value

    def validate(self):
        if self.func_value:
            self.func_value.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.disable_modify is not None:
            result['disableModify'] = self.disable_modify
        if self.is_modify is not None:
            result['isModify'] = self.is_modify
        if self.value is not None:
            result['value'] = self.value
        if self.description is not None:
            result['description'] = self.description
        if self.template_value is not None:
            result['templateValue'] = self.template_value
        if self.type is not None:
            result['type'] = self.type
        if self.func_value is not None:
            result['funcValue'] = self.func_value.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('disableModify') is not None:
            self.disable_modify = m.get('disableModify')
        if m.get('isModify') is not None:
            self.is_modify = m.get('isModify')
        if m.get('value') is not None:
            self.value = m.get('value')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('templateValue') is not None:
            self.template_value = m.get('templateValue')
        if m.get('type') is not None:
            self.type = m.get('type')
        if m.get('funcValue') is not None:
            temp_model = VariablesValueFuncValue()
            self.func_value = temp_model.from_map(m['funcValue'])
        return self


class BuildIndexRequest(TeaModel):
    def __init__(
        self,
        build_mode: str = None,
        data_source_name: str = None,
        data_source_type: str = None,
        data_time_sec: int = None,
        domain: str = None,
        generation: int = None,
        partition: str = None,
    ):
        # The mode in which reindexing is performed.
        self.build_mode = build_mode
        # The name of the data source.
        self.data_source_name = data_source_name
        # The type of the data source.
        self.data_source_type = data_source_type
        # The timestamp in seconds. This parameter is required if you import data from the data source by calling API operations.
        self.data_time_sec = data_time_sec
        # The data center in which the data source resides.
        self.domain = domain
        # The ID of the generation.
        self.generation = generation
        # The data partition. This parameter is required if the dataSourceType parameter is set to odps.
        self.partition = partition

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.build_mode is not None:
            result['buildMode'] = self.build_mode
        if self.data_source_name is not None:
            result['dataSourceName'] = self.data_source_name
        if self.data_source_type is not None:
            result['dataSourceType'] = self.data_source_type
        if self.data_time_sec is not None:
            result['dataTimeSec'] = self.data_time_sec
        if self.domain is not None:
            result['domain'] = self.domain
        if self.generation is not None:
            result['generation'] = self.generation
        if self.partition is not None:
            result['partition'] = self.partition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('buildMode') is not None:
            self.build_mode = m.get('buildMode')
        if m.get('dataSourceName') is not None:
            self.data_source_name = m.get('dataSourceName')
        if m.get('dataSourceType') is not None:
            self.data_source_type = m.get('dataSourceType')
        if m.get('dataTimeSec') is not None:
            self.data_time_sec = m.get('dataTimeSec')
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('generation') is not None:
            self.generation = m.get('generation')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        return self


class BuildIndexResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The result returned.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class BuildIndexResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: BuildIndexResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = BuildIndexResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateClusterRequestDataNode(TeaModel):
    def __init__(
        self,
        number: int = None,
    ):
        # The number of Searcher workers.
        self.number = number

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.number is not None:
            result['number'] = self.number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('number') is not None:
            self.number = m.get('number')
        return self


class CreateClusterRequestQueryNode(TeaModel):
    def __init__(
        self,
        number: int = None,
    ):
        # The number of QRS workers.
        self.number = number

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.number is not None:
            result['number'] = self.number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('number') is not None:
            self.number = m.get('number')
        return self


class CreateClusterRequest(TeaModel):
    def __init__(
        self,
        auto_load: bool = None,
        data_node: CreateClusterRequestDataNode = None,
        description: str = None,
        name: str = None,
        query_node: CreateClusterRequestQueryNode = None,
    ):
        # Specifies whether to automatically balance the load between QRS workers.
        self.auto_load = auto_load
        # The information about Searcher workers.
        self.data_node = data_node
        # The description of the cluster.
        self.description = description
        # The name of the cluster.
        self.name = name
        # The information about Query Result Searcher (QRS) workers.
        self.query_node = query_node

    def validate(self):
        if self.data_node:
            self.data_node.validate()
        if self.query_node:
            self.query_node.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_load is not None:
            result['autoLoad'] = self.auto_load
        if self.data_node is not None:
            result['dataNode'] = self.data_node.to_map()
        if self.description is not None:
            result['description'] = self.description
        if self.name is not None:
            result['name'] = self.name
        if self.query_node is not None:
            result['queryNode'] = self.query_node.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoLoad') is not None:
            self.auto_load = m.get('autoLoad')
        if m.get('dataNode') is not None:
            temp_model = CreateClusterRequestDataNode()
            self.data_node = temp_model.from_map(m['dataNode'])
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('queryNode') is not None:
            temp_model = CreateClusterRequestQueryNode()
            self.query_node = temp_model.from_map(m['queryNode'])
        return self


class CreateClusterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The result returned.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class CreateClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateClusterResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateDataSourceRequestConfig(TeaModel):
    def __init__(
        self,
        access_key: str = None,
        access_secret: str = None,
        bucket: str = None,
        endpoint: str = None,
        namespace: str = None,
        oss_path: str = None,
        partition: str = None,
        path: str = None,
        project: str = None,
        table: str = None,
    ):
        self.access_key = access_key
        self.access_secret = access_secret
        self.bucket = bucket
        self.endpoint = endpoint
        self.namespace = namespace
        self.oss_path = oss_path
        self.partition = partition
        self.path = path
        self.project = project
        self.table = table

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key is not None:
            result['accessKey'] = self.access_key
        if self.access_secret is not None:
            result['accessSecret'] = self.access_secret
        if self.bucket is not None:
            result['bucket'] = self.bucket
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.namespace is not None:
            result['namespace'] = self.namespace
        if self.oss_path is not None:
            result['ossPath'] = self.oss_path
        if self.partition is not None:
            result['partition'] = self.partition
        if self.path is not None:
            result['path'] = self.path
        if self.project is not None:
            result['project'] = self.project
        if self.table is not None:
            result['table'] = self.table
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKey') is not None:
            self.access_key = m.get('accessKey')
        if m.get('accessSecret') is not None:
            self.access_secret = m.get('accessSecret')
        if m.get('bucket') is not None:
            self.bucket = m.get('bucket')
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('namespace') is not None:
            self.namespace = m.get('namespace')
        if m.get('ossPath') is not None:
            self.oss_path = m.get('ossPath')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('path') is not None:
            self.path = m.get('path')
        if m.get('project') is not None:
            self.project = m.get('project')
        if m.get('table') is not None:
            self.table = m.get('table')
        return self


class CreateDataSourceRequestSaroConfig(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        table_name: str = None,
    ):
        self.namespace = namespace
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.namespace is not None:
            result['namespace'] = self.namespace
        if self.table_name is not None:
            result['tableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('namespace') is not None:
            self.namespace = m.get('namespace')
        if m.get('tableName') is not None:
            self.table_name = m.get('tableName')
        return self


class CreateDataSourceRequest(TeaModel):
    def __init__(
        self,
        auto_build_index: bool = None,
        config: CreateDataSourceRequestConfig = None,
        domain: str = None,
        name: str = None,
        saro_config: CreateDataSourceRequestSaroConfig = None,
        type: str = None,
        dry_run: bool = None,
    ):
        self.auto_build_index = auto_build_index
        self.config = config
        self.domain = domain
        self.name = name
        self.saro_config = saro_config
        self.type = type
        # Specifies whether to perform a dry run. This parameter is only used to check whether the data source is valid. Valid values: true and false.
        self.dry_run = dry_run

    def validate(self):
        if self.config:
            self.config.validate()
        if self.saro_config:
            self.saro_config.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_build_index is not None:
            result['autoBuildIndex'] = self.auto_build_index
        if self.config is not None:
            result['config'] = self.config.to_map()
        if self.domain is not None:
            result['domain'] = self.domain
        if self.name is not None:
            result['name'] = self.name
        if self.saro_config is not None:
            result['saroConfig'] = self.saro_config.to_map()
        if self.type is not None:
            result['type'] = self.type
        if self.dry_run is not None:
            result['dryRun'] = self.dry_run
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoBuildIndex') is not None:
            self.auto_build_index = m.get('autoBuildIndex')
        if m.get('config') is not None:
            temp_model = CreateDataSourceRequestConfig()
            self.config = temp_model.from_map(m['config'])
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('saroConfig') is not None:
            temp_model = CreateDataSourceRequestSaroConfig()
            self.saro_config = temp_model.from_map(m['saroConfig'])
        if m.get('type') is not None:
            self.type = m.get('type')
        if m.get('dryRun') is not None:
            self.dry_run = m.get('dryRun')
        return self


class CreateDataSourceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        self.request_id = request_id
        # The returned results.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class CreateDataSourceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateDataSourceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateDataSourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateIndexRequestDataSourceInfoConfig(TeaModel):
    def __init__(
        self,
        access_key: str = None,
        access_secret: str = None,
        endpoint: str = None,
        partition: str = None,
        project: str = None,
        table: str = None,
    ):
        self.access_key = access_key
        self.access_secret = access_secret
        self.endpoint = endpoint
        self.partition = partition
        self.project = project
        self.table = table

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key is not None:
            result['accessKey'] = self.access_key
        if self.access_secret is not None:
            result['accessSecret'] = self.access_secret
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.partition is not None:
            result['partition'] = self.partition
        if self.project is not None:
            result['project'] = self.project
        if self.table is not None:
            result['table'] = self.table
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKey') is not None:
            self.access_key = m.get('accessKey')
        if m.get('accessSecret') is not None:
            self.access_secret = m.get('accessSecret')
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('project') is not None:
            self.project = m.get('project')
        if m.get('table') is not None:
            self.table = m.get('table')
        return self


class CreateIndexRequestDataSourceInfo(TeaModel):
    def __init__(
        self,
        auto_build_index: bool = None,
        config: CreateIndexRequestDataSourceInfoConfig = None,
        process_partition_count: int = None,
        type: str = None,
    ):
        self.auto_build_index = auto_build_index
        self.config = config
        self.process_partition_count = process_partition_count
        self.type = type

    def validate(self):
        if self.config:
            self.config.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_build_index is not None:
            result['autoBuildIndex'] = self.auto_build_index
        if self.config is not None:
            result['config'] = self.config.to_map()
        if self.process_partition_count is not None:
            result['processPartitionCount'] = self.process_partition_count
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoBuildIndex') is not None:
            self.auto_build_index = m.get('autoBuildIndex')
        if m.get('config') is not None:
            temp_model = CreateIndexRequestDataSourceInfoConfig()
            self.config = temp_model.from_map(m['config'])
        if m.get('processPartitionCount') is not None:
            self.process_partition_count = m.get('processPartitionCount')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class CreateIndexRequest(TeaModel):
    def __init__(
        self,
        content: str = None,
        data_source: str = None,
        data_source_info: CreateIndexRequestDataSourceInfo = None,
        domain: str = None,
        extend: Dict[str, Any] = None,
        name: str = None,
        partition: int = None,
        dry_run: bool = None,
    ):
        # The content of the index.
        self.content = content
        # Optional. The data source, which can be MaxCompute, Message Service (MNS), Realtime Compute for Apache Flink, or StreamCompute.
        self.data_source = data_source
        self.data_source_info = data_source_info
        # The data center in which the data source resides.
        self.domain = domain
        self.extend = extend
        # The name of the index.
        self.name = name
        # The data partition.
        self.partition = partition
        self.dry_run = dry_run

    def validate(self):
        if self.data_source_info:
            self.data_source_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.data_source is not None:
            result['dataSource'] = self.data_source
        if self.data_source_info is not None:
            result['dataSourceInfo'] = self.data_source_info.to_map()
        if self.domain is not None:
            result['domain'] = self.domain
        if self.extend is not None:
            result['extend'] = self.extend
        if self.name is not None:
            result['name'] = self.name
        if self.partition is not None:
            result['partition'] = self.partition
        if self.dry_run is not None:
            result['dryRun'] = self.dry_run
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('dataSource') is not None:
            self.data_source = m.get('dataSource')
        if m.get('dataSourceInfo') is not None:
            temp_model = CreateIndexRequestDataSourceInfo()
            self.data_source_info = temp_model.from_map(m['dataSourceInfo'])
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('extend') is not None:
            self.extend = m.get('extend')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('dryRun') is not None:
            self.dry_run = m.get('dryRun')
        return self


class CreateIndexResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The information about the index.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class CreateIndexResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateIndexResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateIndexResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateInstanceRequestComponents(TeaModel):
    def __init__(
        self,
        code: str = None,
        value: str = None,
    ):
        # The name of the specification. The value must be the same as the name of a parameter on the buy page.
        self.code = code
        # The value of the specification.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['code'] = self.code
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('code') is not None:
            self.code = m.get('code')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class CreateInstanceRequestOrder(TeaModel):
    def __init__(
        self,
        auto_renew: bool = None,
        duration: int = None,
        pricing_cycle: str = None,
    ):
        # Specifies whether to enable auto-renewal. Valid values: true and false.
        self.auto_renew = auto_renew
        # The billing cycle. Valid values: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, and 12.
        self.duration = duration
        # The unit of the billing cycle. Valid values: Month and Year.
        self.pricing_cycle = pricing_cycle

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_renew is not None:
            result['autoRenew'] = self.auto_renew
        if self.duration is not None:
            result['duration'] = self.duration
        if self.pricing_cycle is not None:
            result['pricingCycle'] = self.pricing_cycle
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoRenew') is not None:
            self.auto_renew = m.get('autoRenew')
        if m.get('duration') is not None:
            self.duration = m.get('duration')
        if m.get('pricingCycle') is not None:
            self.pricing_cycle = m.get('pricingCycle')
        return self


class CreateInstanceRequest(TeaModel):
    def __init__(
        self,
        charge_type: str = None,
        components: List[CreateInstanceRequestComponents] = None,
        order: CreateInstanceRequestOrder = None,
    ):
        # The billing method of the instance. Valid values: PREPAY and POSTPAY. PREPAY: subscription. If you set this parameter to PREPAY, make sure that your Alibaba Cloud account supports balance payment or credit payment. Otherwise, the system returns the InvalidPayMethod error message. In addition, you must specify the paymentInfo parameter. POSTPAY: pay-as-you-go. This billing method is not supported.
        self.charge_type = charge_type
        # The specifications of the instance.
        self.components = components
        # The information about billing.
        self.order = order

    def validate(self):
        if self.components:
            for k in self.components:
                if k:
                    k.validate()
        if self.order:
            self.order.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.charge_type is not None:
            result['chargeType'] = self.charge_type
        result['components'] = []
        if self.components is not None:
            for k in self.components:
                result['components'].append(k.to_map() if k else None)
        if self.order is not None:
            result['order'] = self.order.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('chargeType') is not None:
            self.charge_type = m.get('chargeType')
        self.components = []
        if m.get('components') is not None:
            for k in m.get('components'):
                temp_model = CreateInstanceRequestComponents()
                self.components.append(temp_model.from_map(k))
        if m.get('order') is not None:
            temp_model = CreateInstanceRequestOrder()
            self.order = temp_model.from_map(m['order'])
        return self


class CreateInstanceResponseBodyResult(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        # The ID of the instance.
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        return self


class CreateInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: CreateInstanceResponseBodyResult = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The result returned.
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = CreateInstanceResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class CreateInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteAdvanceConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The result.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class DeleteAdvanceConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteAdvanceConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteAdvanceConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteDataSourceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request
        self.request_id = request_id
        # The result returned
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class DeleteDataSourceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteDataSourceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteDataSourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteIndexRequest(TeaModel):
    def __init__(
        self,
        data_source: str = None,
        delete_data_source: bool = None,
    ):
        self.data_source = data_source
        self.delete_data_source = delete_data_source

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source is not None:
            result['dataSource'] = self.data_source
        if self.delete_data_source is not None:
            result['deleteDataSource'] = self.delete_data_source
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dataSource') is not None:
            self.data_source = m.get('dataSource')
        if m.get('deleteDataSource') is not None:
            self.delete_data_source = m.get('deleteDataSource')
        return self


class DeleteIndexResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class DeleteIndexResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteIndexResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteIndexResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteIndexVersionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class DeleteIndexVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteIndexVersionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteIndexVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        self.request_id = request_id
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class DeleteInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ForceSwitchResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The index information.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ForceSwitchResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ForceSwitchResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ForceSwitchResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAdvanceConfigRequest(TeaModel):
    def __init__(
        self,
        type: str = None,
    ):
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GetAdvanceConfigResponseBodyResultFiles(TeaModel):
    def __init__(
        self,
        full_path_name: str = None,
        is_dir: bool = None,
        is_template: bool = None,
        name: str = None,
    ):
        # The name of the file path.
        self.full_path_name = full_path_name
        # Indicates whether it is a directory.
        self.is_dir = is_dir
        # Indicates whether it is a template.
        self.is_template = is_template
        # The name.
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.full_path_name is not None:
            result['fullPathName'] = self.full_path_name
        if self.is_dir is not None:
            result['isDir'] = self.is_dir
        if self.is_template is not None:
            result['isTemplate'] = self.is_template
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fullPathName') is not None:
            self.full_path_name = m.get('fullPathName')
        if m.get('isDir') is not None:
            self.is_dir = m.get('isDir')
        if m.get('isTemplate') is not None:
            self.is_template = m.get('isTemplate')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class GetAdvanceConfigResponseBodyResult(TeaModel):
    def __init__(
        self,
        content: str = None,
        content_type: str = None,
        desc: str = None,
        files: List[GetAdvanceConfigResponseBodyResultFiles] = None,
        name: str = None,
        status: str = None,
        update_time: int = None,
    ):
        # The content of the configuration that is returned.
        self.content = content
        # The type of the configuration content. Valid values: FILE, GIT, HTTP, and ODPS.
        self.content_type = content_type
        # The description.
        self.desc = desc
        # The information about files.
        self.files = files
        # The name.
        self.name = name
        # The status.
        self.status = status
        # The update time.
        self.update_time = update_time

    def validate(self):
        if self.files:
            for k in self.files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.content_type is not None:
            result['contentType'] = self.content_type
        if self.desc is not None:
            result['desc'] = self.desc
        result['files'] = []
        if self.files is not None:
            for k in self.files:
                result['files'].append(k.to_map() if k else None)
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('contentType') is not None:
            self.content_type = m.get('contentType')
        if m.get('desc') is not None:
            self.desc = m.get('desc')
        self.files = []
        if m.get('files') is not None:
            for k in m.get('files'):
                temp_model = GetAdvanceConfigResponseBodyResultFiles()
                self.files.append(temp_model.from_map(k))
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class GetAdvanceConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetAdvanceConfigResponseBodyResult = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The returned results.
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetAdvanceConfigResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetAdvanceConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAdvanceConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetAdvanceConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAdvanceConfigFileRequest(TeaModel):
    def __init__(
        self,
        file_name: str = None,
    ):
        self.file_name = file_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.file_name is not None:
            result['fileName'] = self.file_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fileName') is not None:
            self.file_name = m.get('fileName')
        return self


class GetAdvanceConfigFileResponseBodyResult(TeaModel):
    def __init__(
        self,
        content: str = None,
    ):
        self.content = content

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        return self


class GetAdvanceConfigFileResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetAdvanceConfigFileResponseBodyResult = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetAdvanceConfigFileResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetAdvanceConfigFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAdvanceConfigFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetAdvanceConfigFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetClusterResponseBodyResultDataNode(TeaModel):
    def __init__(
        self,
        name: str = None,
        number: int = None,
        partition: int = None,
    ):
        # The name of the node.
        self.name = name
        # The number of replicas.
        self.number = number
        # The number of partitions.
        self.partition = partition

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.number is not None:
            result['number'] = self.number
        if self.partition is not None:
            result['partition'] = self.partition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('number') is not None:
            self.number = m.get('number')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        return self


class GetClusterResponseBodyResultQueryNode(TeaModel):
    def __init__(
        self,
        name: str = None,
        number: int = None,
        partition: int = None,
    ):
        # The name of the node.
        self.name = name
        # The number of nodes.
        self.number = number
        # The number of replicas.
        self.partition = partition

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.number is not None:
            result['number'] = self.number
        if self.partition is not None:
            result['partition'] = self.partition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('number') is not None:
            self.number = m.get('number')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        return self


class GetClusterResponseBodyResult(TeaModel):
    def __init__(
        self,
        config_update_time: str = None,
        current_advance_config_version: str = None,
        current_online_config_version: str = None,
        data_node: GetClusterResponseBodyResultDataNode = None,
        description: str = None,
        latest_advance_config_version: str = None,
        latest_online_config_version: str = None,
        name: str = None,
        query_node: GetClusterResponseBodyResultQueryNode = None,
        status: str = None,
    ):
        # The time when the cluster was updated.
        self.config_update_time = config_update_time
        # The effective advanced configuration version.
        self.current_advance_config_version = current_advance_config_version
        # The effective online configuration version.
        self.current_online_config_version = current_online_config_version
        # The specifications of the data node.
        self.data_node = data_node
        # The description of the cluster.
        self.description = description
        # The latest advanced configuration version.
        self.latest_advance_config_version = latest_advance_config_version
        # The latest online configuration version.
        self.latest_online_config_version = latest_online_config_version
        # The name of the cluster.
        self.name = name
        # The specifications of the query node.
        self.query_node = query_node
        # The creation status of the cluster. Valid values: NEW and PUBLISH. NEW indicates that the cluster is being created. PUBLISH indicates that the cluster is created.
        self.status = status

    def validate(self):
        if self.data_node:
            self.data_node.validate()
        if self.query_node:
            self.query_node.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_update_time is not None:
            result['configUpdateTime'] = self.config_update_time
        if self.current_advance_config_version is not None:
            result['currentAdvanceConfigVersion'] = self.current_advance_config_version
        if self.current_online_config_version is not None:
            result['currentOnlineConfigVersion'] = self.current_online_config_version
        if self.data_node is not None:
            result['dataNode'] = self.data_node.to_map()
        if self.description is not None:
            result['description'] = self.description
        if self.latest_advance_config_version is not None:
            result['latestAdvanceConfigVersion'] = self.latest_advance_config_version
        if self.latest_online_config_version is not None:
            result['latestOnlineConfigVersion'] = self.latest_online_config_version
        if self.name is not None:
            result['name'] = self.name
        if self.query_node is not None:
            result['queryNode'] = self.query_node.to_map()
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('configUpdateTime') is not None:
            self.config_update_time = m.get('configUpdateTime')
        if m.get('currentAdvanceConfigVersion') is not None:
            self.current_advance_config_version = m.get('currentAdvanceConfigVersion')
        if m.get('currentOnlineConfigVersion') is not None:
            self.current_online_config_version = m.get('currentOnlineConfigVersion')
        if m.get('dataNode') is not None:
            temp_model = GetClusterResponseBodyResultDataNode()
            self.data_node = temp_model.from_map(m['dataNode'])
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('latestAdvanceConfigVersion') is not None:
            self.latest_advance_config_version = m.get('latestAdvanceConfigVersion')
        if m.get('latestOnlineConfigVersion') is not None:
            self.latest_online_config_version = m.get('latestOnlineConfigVersion')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('queryNode') is not None:
            temp_model = GetClusterResponseBodyResultQueryNode()
            self.query_node = temp_model.from_map(m['queryNode'])
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class GetClusterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetClusterResponseBodyResult = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The list of the cluster details.
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetClusterResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetClusterResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetClusterRunTimeInfoResponseBodyResultDataNodesConfigStatusList(TeaModel):
    def __init__(
        self,
        config_update_time: str = None,
        done_percent: int = None,
        done_size: int = None,
        name: str = None,
        total_size: int = None,
    ):
        self.config_update_time = config_update_time
        self.done_percent = done_percent
        self.done_size = done_size
        self.name = name
        self.total_size = total_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_update_time is not None:
            result['configUpdateTime'] = self.config_update_time
        if self.done_percent is not None:
            result['donePercent'] = self.done_percent
        if self.done_size is not None:
            result['doneSize'] = self.done_size
        if self.name is not None:
            result['name'] = self.name
        if self.total_size is not None:
            result['totalSize'] = self.total_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('configUpdateTime') is not None:
            self.config_update_time = m.get('configUpdateTime')
        if m.get('donePercent') is not None:
            self.done_percent = m.get('donePercent')
        if m.get('doneSize') is not None:
            self.done_size = m.get('doneSize')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('totalSize') is not None:
            self.total_size = m.get('totalSize')
        return self


class GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusListAdvanceConfigInfo(TeaModel):
    def __init__(
        self,
        config_meta_name: str = None,
        version: int = None,
    ):
        self.config_meta_name = config_meta_name
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_meta_name is not None:
            result['configMetaName'] = self.config_meta_name
        if self.version is not None:
            result['version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('configMetaName') is not None:
            self.config_meta_name = m.get('configMetaName')
        if m.get('version') is not None:
            self.version = m.get('version')
        return self


class GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusListIndexConfigInfo(TeaModel):
    def __init__(
        self,
        config_meta_name: str = None,
        version: int = None,
    ):
        self.config_meta_name = config_meta_name
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_meta_name is not None:
            result['configMetaName'] = self.config_meta_name
        if self.version is not None:
            result['version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('configMetaName') is not None:
            self.config_meta_name = m.get('configMetaName')
        if m.get('version') is not None:
            self.version = m.get('version')
        return self


class GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusList(TeaModel):
    def __init__(
        self,
        advance_config_info: GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusListAdvanceConfigInfo = None,
        deploy_failed_worker: List[str] = None,
        doc_size: int = None,
        done_percent: int = None,
        done_size: int = None,
        error_msg: str = None,
        full_update_time: str = None,
        full_version: int = None,
        inc_update_time: str = None,
        inc_version: int = None,
        index_config_info: GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusListIndexConfigInfo = None,
        index_size: int = None,
        lack_disk_worker: List[str] = None,
        lack_mem_worker: List[str] = None,
        name: str = None,
        total_size: int = None,
    ):
        self.advance_config_info = advance_config_info
        self.deploy_failed_worker = deploy_failed_worker
        self.doc_size = doc_size
        self.done_percent = done_percent
        self.done_size = done_size
        self.error_msg = error_msg
        self.full_update_time = full_update_time
        self.full_version = full_version
        self.inc_update_time = inc_update_time
        self.inc_version = inc_version
        self.index_config_info = index_config_info
        self.index_size = index_size
        self.lack_disk_worker = lack_disk_worker
        self.lack_mem_worker = lack_mem_worker
        self.name = name
        self.total_size = total_size

    def validate(self):
        if self.advance_config_info:
            self.advance_config_info.validate()
        if self.index_config_info:
            self.index_config_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.advance_config_info is not None:
            result['advanceConfigInfo'] = self.advance_config_info.to_map()
        if self.deploy_failed_worker is not None:
            result['deployFailedWorker'] = self.deploy_failed_worker
        if self.doc_size is not None:
            result['docSize'] = self.doc_size
        if self.done_percent is not None:
            result['donePercent'] = self.done_percent
        if self.done_size is not None:
            result['doneSize'] = self.done_size
        if self.error_msg is not None:
            result['errorMsg'] = self.error_msg
        if self.full_update_time is not None:
            result['fullUpdateTime'] = self.full_update_time
        if self.full_version is not None:
            result['fullVersion'] = self.full_version
        if self.inc_update_time is not None:
            result['incUpdateTime'] = self.inc_update_time
        if self.inc_version is not None:
            result['incVersion'] = self.inc_version
        if self.index_config_info is not None:
            result['indexConfigInfo'] = self.index_config_info.to_map()
        if self.index_size is not None:
            result['indexSize'] = self.index_size
        if self.lack_disk_worker is not None:
            result['lackDiskWorker'] = self.lack_disk_worker
        if self.lack_mem_worker is not None:
            result['lackMemWorker'] = self.lack_mem_worker
        if self.name is not None:
            result['name'] = self.name
        if self.total_size is not None:
            result['totalSize'] = self.total_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('advanceConfigInfo') is not None:
            temp_model = GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusListAdvanceConfigInfo()
            self.advance_config_info = temp_model.from_map(m['advanceConfigInfo'])
        if m.get('deployFailedWorker') is not None:
            self.deploy_failed_worker = m.get('deployFailedWorker')
        if m.get('docSize') is not None:
            self.doc_size = m.get('docSize')
        if m.get('donePercent') is not None:
            self.done_percent = m.get('donePercent')
        if m.get('doneSize') is not None:
            self.done_size = m.get('doneSize')
        if m.get('errorMsg') is not None:
            self.error_msg = m.get('errorMsg')
        if m.get('fullUpdateTime') is not None:
            self.full_update_time = m.get('fullUpdateTime')
        if m.get('fullVersion') is not None:
            self.full_version = m.get('fullVersion')
        if m.get('incUpdateTime') is not None:
            self.inc_update_time = m.get('incUpdateTime')
        if m.get('incVersion') is not None:
            self.inc_version = m.get('incVersion')
        if m.get('indexConfigInfo') is not None:
            temp_model = GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusListIndexConfigInfo()
            self.index_config_info = temp_model.from_map(m['indexConfigInfo'])
        if m.get('indexSize') is not None:
            self.index_size = m.get('indexSize')
        if m.get('lackDiskWorker') is not None:
            self.lack_disk_worker = m.get('lackDiskWorker')
        if m.get('lackMemWorker') is not None:
            self.lack_mem_worker = m.get('lackMemWorker')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('totalSize') is not None:
            self.total_size = m.get('totalSize')
        return self


class GetClusterRunTimeInfoResponseBodyResultDataNodesServiceStatus(TeaModel):
    def __init__(
        self,
        done_percent: int = None,
        done_size: int = None,
        name: str = None,
        total_size: int = None,
    ):
        self.done_percent = done_percent
        self.done_size = done_size
        self.name = name
        self.total_size = total_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.done_percent is not None:
            result['donePercent'] = self.done_percent
        if self.done_size is not None:
            result['doneSize'] = self.done_size
        if self.name is not None:
            result['name'] = self.name
        if self.total_size is not None:
            result['totalSize'] = self.total_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('donePercent') is not None:
            self.done_percent = m.get('donePercent')
        if m.get('doneSize') is not None:
            self.done_size = m.get('doneSize')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('totalSize') is not None:
            self.total_size = m.get('totalSize')
        return self


class GetClusterRunTimeInfoResponseBodyResultDataNodes(TeaModel):
    def __init__(
        self,
        config_status_list: List[GetClusterRunTimeInfoResponseBodyResultDataNodesConfigStatusList] = None,
        data_status_list: List[GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusList] = None,
        service_status: GetClusterRunTimeInfoResponseBodyResultDataNodesServiceStatus = None,
    ):
        self.config_status_list = config_status_list
        self.data_status_list = data_status_list
        self.service_status = service_status

    def validate(self):
        if self.config_status_list:
            for k in self.config_status_list:
                if k:
                    k.validate()
        if self.data_status_list:
            for k in self.data_status_list:
                if k:
                    k.validate()
        if self.service_status:
            self.service_status.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['configStatusList'] = []
        if self.config_status_list is not None:
            for k in self.config_status_list:
                result['configStatusList'].append(k.to_map() if k else None)
        result['dataStatusList'] = []
        if self.data_status_list is not None:
            for k in self.data_status_list:
                result['dataStatusList'].append(k.to_map() if k else None)
        if self.service_status is not None:
            result['serviceStatus'] = self.service_status.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.config_status_list = []
        if m.get('configStatusList') is not None:
            for k in m.get('configStatusList'):
                temp_model = GetClusterRunTimeInfoResponseBodyResultDataNodesConfigStatusList()
                self.config_status_list.append(temp_model.from_map(k))
        self.data_status_list = []
        if m.get('dataStatusList') is not None:
            for k in m.get('dataStatusList'):
                temp_model = GetClusterRunTimeInfoResponseBodyResultDataNodesDataStatusList()
                self.data_status_list.append(temp_model.from_map(k))
        if m.get('serviceStatus') is not None:
            temp_model = GetClusterRunTimeInfoResponseBodyResultDataNodesServiceStatus()
            self.service_status = temp_model.from_map(m['serviceStatus'])
        return self


class GetClusterRunTimeInfoResponseBodyResultQueryNodeConfigStatusList(TeaModel):
    def __init__(
        self,
        config_update_time: str = None,
        done_percent: int = None,
        done_size: int = None,
        name: str = None,
        total_size: int = None,
    ):
        # configUpdateTime
        self.config_update_time = config_update_time
        # donePercent
        self.done_percent = done_percent
        # doneSize
        self.done_size = done_size
        # name
        self.name = name
        # totalSize
        self.total_size = total_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_update_time is not None:
            result['configUpdateTime'] = self.config_update_time
        if self.done_percent is not None:
            result['donePercent'] = self.done_percent
        if self.done_size is not None:
            result['doneSize'] = self.done_size
        if self.name is not None:
            result['name'] = self.name
        if self.total_size is not None:
            result['totalSize'] = self.total_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('configUpdateTime') is not None:
            self.config_update_time = m.get('configUpdateTime')
        if m.get('donePercent') is not None:
            self.done_percent = m.get('donePercent')
        if m.get('doneSize') is not None:
            self.done_size = m.get('doneSize')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('totalSize') is not None:
            self.total_size = m.get('totalSize')
        return self


class GetClusterRunTimeInfoResponseBodyResultQueryNodeServiceStatus(TeaModel):
    def __init__(
        self,
        done_percent: int = None,
        done_size: int = None,
        name: str = None,
        total_size: int = None,
    ):
        # donePercent
        self.done_percent = done_percent
        # doneSize
        self.done_size = done_size
        # The name of the cluster.
        self.name = name
        # totalSize
        self.total_size = total_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.done_percent is not None:
            result['donePercent'] = self.done_percent
        if self.done_size is not None:
            result['doneSize'] = self.done_size
        if self.name is not None:
            result['name'] = self.name
        if self.total_size is not None:
            result['totalSize'] = self.total_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('donePercent') is not None:
            self.done_percent = m.get('donePercent')
        if m.get('doneSize') is not None:
            self.done_size = m.get('doneSize')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('totalSize') is not None:
            self.total_size = m.get('totalSize')
        return self


class GetClusterRunTimeInfoResponseBodyResultQueryNode(TeaModel):
    def __init__(
        self,
        config_status_list: List[GetClusterRunTimeInfoResponseBodyResultQueryNodeConfigStatusList] = None,
        service_status: GetClusterRunTimeInfoResponseBodyResultQueryNodeServiceStatus = None,
    ):
        # configStatusList
        self.config_status_list = config_status_list
        # serviceStatus
        self.service_status = service_status

    def validate(self):
        if self.config_status_list:
            for k in self.config_status_list:
                if k:
                    k.validate()
        if self.service_status:
            self.service_status.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['configStatusList'] = []
        if self.config_status_list is not None:
            for k in self.config_status_list:
                result['configStatusList'].append(k.to_map() if k else None)
        if self.service_status is not None:
            result['serviceStatus'] = self.service_status.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.config_status_list = []
        if m.get('configStatusList') is not None:
            for k in m.get('configStatusList'):
                temp_model = GetClusterRunTimeInfoResponseBodyResultQueryNodeConfigStatusList()
                self.config_status_list.append(temp_model.from_map(k))
        if m.get('serviceStatus') is not None:
            temp_model = GetClusterRunTimeInfoResponseBodyResultQueryNodeServiceStatus()
            self.service_status = temp_model.from_map(m['serviceStatus'])
        return self


class GetClusterRunTimeInfoResponseBodyResult(TeaModel):
    def __init__(
        self,
        cluster_name: str = None,
        data_nodes: List[GetClusterRunTimeInfoResponseBodyResultDataNodes] = None,
        query_node: GetClusterRunTimeInfoResponseBodyResultQueryNode = None,
    ):
        # The name of the cluster
        self.cluster_name = cluster_name
        # dataNodes
        self.data_nodes = data_nodes
        # The specifications of the query node.
        self.query_node = query_node

    def validate(self):
        if self.data_nodes:
            for k in self.data_nodes:
                if k:
                    k.validate()
        if self.query_node:
            self.query_node.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cluster_name is not None:
            result['clusterName'] = self.cluster_name
        result['dataNodes'] = []
        if self.data_nodes is not None:
            for k in self.data_nodes:
                result['dataNodes'].append(k.to_map() if k else None)
        if self.query_node is not None:
            result['queryNode'] = self.query_node.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clusterName') is not None:
            self.cluster_name = m.get('clusterName')
        self.data_nodes = []
        if m.get('dataNodes') is not None:
            for k in m.get('dataNodes'):
                temp_model = GetClusterRunTimeInfoResponseBodyResultDataNodes()
                self.data_nodes.append(temp_model.from_map(k))
        if m.get('queryNode') is not None:
            temp_model = GetClusterRunTimeInfoResponseBodyResultQueryNode()
            self.query_node = temp_model.from_map(m['queryNode'])
        return self


class GetClusterRunTimeInfoResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[GetClusterRunTimeInfoResponseBodyResult] = None,
    ):
        # Id of the request
        self.request_id = request_id
        # The configuration progress. Unit: percentage.
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = GetClusterRunTimeInfoResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class GetClusterRunTimeInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetClusterRunTimeInfoResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetClusterRunTimeInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetDataSourceResponseBodyResult(TeaModel):
    def __init__(
        self,
        domain: str = None,
        indexes: List[str] = None,
        last_ful_time: int = None,
        name: str = None,
        status: str = None,
        type: str = None,
    ):
        self.domain = domain
        self.indexes = indexes
        self.last_ful_time = last_ful_time
        self.name = name
        self.status = status
        # The type of the data source.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.domain is not None:
            result['domain'] = self.domain
        if self.indexes is not None:
            result['indexes'] = self.indexes
        if self.last_ful_time is not None:
            result['lastFulTime'] = self.last_ful_time
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('indexes') is not None:
            self.indexes = m.get('indexes')
        if m.get('lastFulTime') is not None:
            self.last_ful_time = m.get('lastFulTime')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GetDataSourceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetDataSourceResponseBodyResult = None,
    ):
        # Id of the request
        self.request_id = request_id
        # The information about the data source.
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetDataSourceResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetDataSourceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetDataSourceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetDataSourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetDataSourceDeployResponseBodyResultExtendHdfs(TeaModel):
    def __init__(
        self,
        path: str = None,
    ):
        self.path = path

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.path is not None:
            result['path'] = self.path
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('path') is not None:
            self.path = m.get('path')
        return self


class GetDataSourceDeployResponseBodyResultExtendOdps(TeaModel):
    def __init__(
        self,
        partitions: Dict[str, str] = None,
    ):
        self.partitions = partitions

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.partitions is not None:
            result['partitions'] = self.partitions
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('partitions') is not None:
            self.partitions = m.get('partitions')
        return self


class GetDataSourceDeployResponseBodyResultExtendOss(TeaModel):
    def __init__(
        self,
        path: str = None,
    ):
        self.path = path

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.path is not None:
            result['path'] = self.path
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('path') is not None:
            self.path = m.get('path')
        return self


class GetDataSourceDeployResponseBodyResultExtendSaro(TeaModel):
    def __init__(
        self,
        path: str = None,
        version: str = None,
    ):
        self.path = path
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.path is not None:
            result['path'] = self.path
        if self.version is not None:
            result['version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('path') is not None:
            self.path = m.get('path')
        if m.get('version') is not None:
            self.version = m.get('version')
        return self


class GetDataSourceDeployResponseBodyResultExtend(TeaModel):
    def __init__(
        self,
        hdfs: GetDataSourceDeployResponseBodyResultExtendHdfs = None,
        odps: GetDataSourceDeployResponseBodyResultExtendOdps = None,
        oss: GetDataSourceDeployResponseBodyResultExtendOss = None,
        saro: GetDataSourceDeployResponseBodyResultExtendSaro = None,
    ):
        self.hdfs = hdfs
        self.odps = odps
        self.oss = oss
        self.saro = saro

    def validate(self):
        if self.hdfs:
            self.hdfs.validate()
        if self.odps:
            self.odps.validate()
        if self.oss:
            self.oss.validate()
        if self.saro:
            self.saro.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.hdfs is not None:
            result['hdfs'] = self.hdfs.to_map()
        if self.odps is not None:
            result['odps'] = self.odps.to_map()
        if self.oss is not None:
            result['oss'] = self.oss.to_map()
        if self.saro is not None:
            result['saro'] = self.saro.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('hdfs') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultExtendHdfs()
            self.hdfs = temp_model.from_map(m['hdfs'])
        if m.get('odps') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultExtendOdps()
            self.odps = temp_model.from_map(m['odps'])
        if m.get('oss') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultExtendOss()
            self.oss = temp_model.from_map(m['oss'])
        if m.get('saro') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultExtendSaro()
            self.saro = temp_model.from_map(m['saro'])
        return self


class GetDataSourceDeployResponseBodyResultProcessor(TeaModel):
    def __init__(
        self,
        args: str = None,
        resource: str = None,
    ):
        self.args = args
        self.resource = resource

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.args is not None:
            result['args'] = self.args
        if self.resource is not None:
            result['resource'] = self.resource
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('args') is not None:
            self.args = m.get('args')
        if m.get('resource') is not None:
            self.resource = m.get('resource')
        return self


class GetDataSourceDeployResponseBodyResultStorage(TeaModel):
    def __init__(
        self,
        access_key: str = None,
        access_secret: str = None,
        bucket: str = None,
        endpoint: str = None,
        namespace: str = None,
        oss_path: str = None,
        partition: str = None,
        path: str = None,
        project: str = None,
        table: str = None,
    ):
        self.access_key = access_key
        self.access_secret = access_secret
        self.bucket = bucket
        self.endpoint = endpoint
        self.namespace = namespace
        self.oss_path = oss_path
        self.partition = partition
        self.path = path
        self.project = project
        self.table = table

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key is not None:
            result['accessKey'] = self.access_key
        if self.access_secret is not None:
            result['accessSecret'] = self.access_secret
        if self.bucket is not None:
            result['bucket'] = self.bucket
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.namespace is not None:
            result['namespace'] = self.namespace
        if self.oss_path is not None:
            result['ossPath'] = self.oss_path
        if self.partition is not None:
            result['partition'] = self.partition
        if self.path is not None:
            result['path'] = self.path
        if self.project is not None:
            result['project'] = self.project
        if self.table is not None:
            result['table'] = self.table
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKey') is not None:
            self.access_key = m.get('accessKey')
        if m.get('accessSecret') is not None:
            self.access_secret = m.get('accessSecret')
        if m.get('bucket') is not None:
            self.bucket = m.get('bucket')
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('namespace') is not None:
            self.namespace = m.get('namespace')
        if m.get('ossPath') is not None:
            self.oss_path = m.get('ossPath')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('path') is not None:
            self.path = m.get('path')
        if m.get('project') is not None:
            self.project = m.get('project')
        if m.get('table') is not None:
            self.table = m.get('table')
        return self


class GetDataSourceDeployResponseBodyResultSwift(TeaModel):
    def __init__(
        self,
        topic: str = None,
        zk: str = None,
    ):
        self.topic = topic
        self.zk = zk

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.topic is not None:
            result['topic'] = self.topic
        if self.zk is not None:
            result['zk'] = self.zk
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('topic') is not None:
            self.topic = m.get('topic')
        if m.get('zk') is not None:
            self.zk = m.get('zk')
        return self


class GetDataSourceDeployResponseBodyResult(TeaModel):
    def __init__(
        self,
        auto_build_index: bool = None,
        extend: GetDataSourceDeployResponseBodyResultExtend = None,
        processor: GetDataSourceDeployResponseBodyResultProcessor = None,
        storage: GetDataSourceDeployResponseBodyResultStorage = None,
        swift: GetDataSourceDeployResponseBodyResultSwift = None,
    ):
        self.auto_build_index = auto_build_index
        self.extend = extend
        self.processor = processor
        self.storage = storage
        self.swift = swift

    def validate(self):
        if self.extend:
            self.extend.validate()
        if self.processor:
            self.processor.validate()
        if self.storage:
            self.storage.validate()
        if self.swift:
            self.swift.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_build_index is not None:
            result['autoBuildIndex'] = self.auto_build_index
        if self.extend is not None:
            result['extend'] = self.extend.to_map()
        if self.processor is not None:
            result['processor'] = self.processor.to_map()
        if self.storage is not None:
            result['storage'] = self.storage.to_map()
        if self.swift is not None:
            result['swift'] = self.swift.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoBuildIndex') is not None:
            self.auto_build_index = m.get('autoBuildIndex')
        if m.get('extend') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultExtend()
            self.extend = temp_model.from_map(m['extend'])
        if m.get('processor') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultProcessor()
            self.processor = temp_model.from_map(m['processor'])
        if m.get('storage') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultStorage()
            self.storage = temp_model.from_map(m['storage'])
        if m.get('swift') is not None:
            temp_model = GetDataSourceDeployResponseBodyResultSwift()
            self.swift = temp_model.from_map(m['swift'])
        return self


class GetDataSourceDeployResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetDataSourceDeployResponseBodyResult = None,
    ):
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetDataSourceDeployResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetDataSourceDeployResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetDataSourceDeployResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetDataSourceDeployResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetDeployGraphResponseBodyResultGraphIndexMetas(TeaModel):
    def __init__(
        self,
        domain_name: str = None,
        name: str = None,
        table_deploy_id: int = None,
        table_name: str = None,
        tag: str = None,
        zone_name: str = None,
    ):
        self.domain_name = domain_name
        self.name = name
        self.table_deploy_id = table_deploy_id
        self.table_name = table_name
        self.tag = tag
        self.zone_name = zone_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.domain_name is not None:
            result['domainName'] = self.domain_name
        if self.name is not None:
            result['name'] = self.name
        if self.table_deploy_id is not None:
            result['tableDeployId'] = self.table_deploy_id
        if self.table_name is not None:
            result['tableName'] = self.table_name
        if self.tag is not None:
            result['tag'] = self.tag
        if self.zone_name is not None:
            result['zoneName'] = self.zone_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('domainName') is not None:
            self.domain_name = m.get('domainName')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('tableDeployId') is not None:
            self.table_deploy_id = m.get('tableDeployId')
        if m.get('tableName') is not None:
            self.table_name = m.get('tableName')
        if m.get('tag') is not None:
            self.tag = m.get('tag')
        if m.get('zoneName') is not None:
            self.zone_name = m.get('zoneName')
        return self


class GetDeployGraphResponseBodyResultGraphOnlineMaster(TeaModel):
    def __init__(
        self,
        domain_name: str = None,
        hippo_id: str = None,
        id: int = None,
        name: str = None,
    ):
        self.domain_name = domain_name
        self.hippo_id = hippo_id
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.domain_name is not None:
            result['domainName'] = self.domain_name
        if self.hippo_id is not None:
            result['hippoId'] = self.hippo_id
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('domainName') is not None:
            self.domain_name = m.get('domainName')
        if m.get('hippoId') is not None:
            self.hippo_id = m.get('hippoId')
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class GetDeployGraphResponseBodyResultGraphTableMetas(TeaModel):
    def __init__(
        self,
        build_deploy_id: int = None,
        domain_name: str = None,
        name: str = None,
        table_deploy_id: int = None,
        tag: str = None,
        type: str = None,
    ):
        self.build_deploy_id = build_deploy_id
        self.domain_name = domain_name
        self.name = name
        self.table_deploy_id = table_deploy_id
        self.tag = tag
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.build_deploy_id is not None:
            result['buildDeployId'] = self.build_deploy_id
        if self.domain_name is not None:
            result['domainName'] = self.domain_name
        if self.name is not None:
            result['name'] = self.name
        if self.table_deploy_id is not None:
            result['tableDeployId'] = self.table_deploy_id
        if self.tag is not None:
            result['tag'] = self.tag
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('buildDeployId') is not None:
            self.build_deploy_id = m.get('buildDeployId')
        if m.get('domainName') is not None:
            self.domain_name = m.get('domainName')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('tableDeployId') is not None:
            self.table_deploy_id = m.get('tableDeployId')
        if m.get('tag') is not None:
            self.tag = m.get('tag')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GetDeployGraphResponseBodyResultGraphZoneMetas(TeaModel):
    def __init__(
        self,
        domain_info: str = None,
        name: str = None,
        suez_admin_name: str = None,
        tag: str = None,
        type: str = None,
    ):
        self.domain_info = domain_info
        self.name = name
        self.suez_admin_name = suez_admin_name
        self.tag = tag
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.domain_info is not None:
            result['domainInfo'] = self.domain_info
        if self.name is not None:
            result['name'] = self.name
        if self.suez_admin_name is not None:
            result['suezAdminName'] = self.suez_admin_name
        if self.tag is not None:
            result['tag'] = self.tag
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('domainInfo') is not None:
            self.domain_info = m.get('domainInfo')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('suezAdminName') is not None:
            self.suez_admin_name = m.get('suezAdminName')
        if m.get('tag') is not None:
            self.tag = m.get('tag')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GetDeployGraphResponseBodyResultGraph(TeaModel):
    def __init__(
        self,
        index_metas: List[GetDeployGraphResponseBodyResultGraphIndexMetas] = None,
        online_master: List[GetDeployGraphResponseBodyResultGraphOnlineMaster] = None,
        table_index_relation: Dict[str, List[str]] = None,
        table_metas: List[GetDeployGraphResponseBodyResultGraphTableMetas] = None,
        zone_index_relation: Dict[str, List[str]] = None,
        zone_metas: List[GetDeployGraphResponseBodyResultGraphZoneMetas] = None,
    ):
        self.index_metas = index_metas
        self.online_master = online_master
        self.table_index_relation = table_index_relation
        self.table_metas = table_metas
        self.zone_index_relation = zone_index_relation
        self.zone_metas = zone_metas

    def validate(self):
        if self.index_metas:
            for k in self.index_metas:
                if k:
                    k.validate()
        if self.online_master:
            for k in self.online_master:
                if k:
                    k.validate()
        if self.table_metas:
            for k in self.table_metas:
                if k:
                    k.validate()
        if self.zone_metas:
            for k in self.zone_metas:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['indexMetas'] = []
        if self.index_metas is not None:
            for k in self.index_metas:
                result['indexMetas'].append(k.to_map() if k else None)
        result['onlineMaster'] = []
        if self.online_master is not None:
            for k in self.online_master:
                result['onlineMaster'].append(k.to_map() if k else None)
        if self.table_index_relation is not None:
            result['tableIndexRelation'] = self.table_index_relation
        result['tableMetas'] = []
        if self.table_metas is not None:
            for k in self.table_metas:
                result['tableMetas'].append(k.to_map() if k else None)
        if self.zone_index_relation is not None:
            result['zoneIndexRelation'] = self.zone_index_relation
        result['zoneMetas'] = []
        if self.zone_metas is not None:
            for k in self.zone_metas:
                result['zoneMetas'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.index_metas = []
        if m.get('indexMetas') is not None:
            for k in m.get('indexMetas'):
                temp_model = GetDeployGraphResponseBodyResultGraphIndexMetas()
                self.index_metas.append(temp_model.from_map(k))
        self.online_master = []
        if m.get('onlineMaster') is not None:
            for k in m.get('onlineMaster'):
                temp_model = GetDeployGraphResponseBodyResultGraphOnlineMaster()
                self.online_master.append(temp_model.from_map(k))
        if m.get('tableIndexRelation') is not None:
            self.table_index_relation = m.get('tableIndexRelation')
        self.table_metas = []
        if m.get('tableMetas') is not None:
            for k in m.get('tableMetas'):
                temp_model = GetDeployGraphResponseBodyResultGraphTableMetas()
                self.table_metas.append(temp_model.from_map(k))
        if m.get('zoneIndexRelation') is not None:
            self.zone_index_relation = m.get('zoneIndexRelation')
        self.zone_metas = []
        if m.get('zoneMetas') is not None:
            for k in m.get('zoneMetas'):
                temp_model = GetDeployGraphResponseBodyResultGraphZoneMetas()
                self.zone_metas.append(temp_model.from_map(k))
        return self


class GetDeployGraphResponseBodyResult(TeaModel):
    def __init__(
        self,
        graph: GetDeployGraphResponseBodyResultGraph = None,
    ):
        self.graph = graph

    def validate(self):
        if self.graph:
            self.graph.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.graph is not None:
            result['graph'] = self.graph.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('graph') is not None:
            temp_model = GetDeployGraphResponseBodyResultGraph()
            self.graph = temp_model.from_map(m['graph'])
        return self


class GetDeployGraphResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetDeployGraphResponseBodyResult = None,
    ):
        # Id of the request
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetDeployGraphResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetDeployGraphResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetDeployGraphResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetDeployGraphResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetFileRequest(TeaModel):
    def __init__(
        self,
        file_name: str = None,
    ):
        self.file_name = file_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.file_name is not None:
            result['fileName'] = self.file_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fileName') is not None:
            self.file_name = m.get('fileName')
        return self


class GetFileResponseBodyResult(TeaModel):
    def __init__(
        self,
        content: str = None,
        data_source: str = None,
        full_path_name: str = None,
        is_dir: bool = None,
        name: str = None,
        partition: int = None,
    ):
        self.content = content
        self.data_source = data_source
        self.full_path_name = full_path_name
        self.is_dir = is_dir
        self.name = name
        self.partition = partition

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.data_source is not None:
            result['dataSource'] = self.data_source
        if self.full_path_name is not None:
            result['fullPathName'] = self.full_path_name
        if self.is_dir is not None:
            result['isDir'] = self.is_dir
        if self.name is not None:
            result['name'] = self.name
        if self.partition is not None:
            result['partition'] = self.partition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('dataSource') is not None:
            self.data_source = m.get('dataSource')
        if m.get('fullPathName') is not None:
            self.full_path_name = m.get('fullPathName')
        if m.get('isDir') is not None:
            self.is_dir = m.get('isDir')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        return self


class GetFileResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetFileResponseBodyResult = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetFileResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIndexResponseBodyResultDataSourceInfoConfig(TeaModel):
    def __init__(
        self,
        access_key: str = None,
        access_secret: str = None,
        bucket: str = None,
        endpoint: str = None,
        namespace: str = None,
        oss_path: str = None,
        partition: str = None,
        path: str = None,
        project: str = None,
        table: str = None,
    ):
        self.access_key = access_key
        self.access_secret = access_secret
        self.bucket = bucket
        # A parameter related to MaxCompute.
        self.endpoint = endpoint
        # A parameter related to SARO.
        self.namespace = namespace
        # A parameter related to OSS.
        self.oss_path = oss_path
        self.partition = partition
        # A parameter related to Apsara File Storage for HDFS.
        self.path = path
        self.project = project
        # A parameter related to SARO and MaxCompute.
        self.table = table

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key is not None:
            result['accessKey'] = self.access_key
        if self.access_secret is not None:
            result['accessSecret'] = self.access_secret
        if self.bucket is not None:
            result['bucket'] = self.bucket
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.namespace is not None:
            result['namespace'] = self.namespace
        if self.oss_path is not None:
            result['ossPath'] = self.oss_path
        if self.partition is not None:
            result['partition'] = self.partition
        if self.path is not None:
            result['path'] = self.path
        if self.project is not None:
            result['project'] = self.project
        if self.table is not None:
            result['table'] = self.table
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKey') is not None:
            self.access_key = m.get('accessKey')
        if m.get('accessSecret') is not None:
            self.access_secret = m.get('accessSecret')
        if m.get('bucket') is not None:
            self.bucket = m.get('bucket')
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('namespace') is not None:
            self.namespace = m.get('namespace')
        if m.get('ossPath') is not None:
            self.oss_path = m.get('ossPath')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('path') is not None:
            self.path = m.get('path')
        if m.get('project') is not None:
            self.project = m.get('project')
        if m.get('table') is not None:
            self.table = m.get('table')
        return self


class GetIndexResponseBodyResultDataSourceInfoSaroConfig(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        table_name: str = None,
    ):
        self.namespace = namespace
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.namespace is not None:
            result['namespace'] = self.namespace
        if self.table_name is not None:
            result['tableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('namespace') is not None:
            self.namespace = m.get('namespace')
        if m.get('tableName') is not None:
            self.table_name = m.get('tableName')
        return self


class GetIndexResponseBodyResultDataSourceInfo(TeaModel):
    def __init__(
        self,
        auto_build_index: bool = None,
        config: GetIndexResponseBodyResultDataSourceInfoConfig = None,
        domain: str = None,
        name: str = None,
        process_partition_count: int = None,
        saro_config: GetIndexResponseBodyResultDataSourceInfoSaroConfig = None,
        type: str = None,
    ):
        # Indicates whether the automatic full indexing feature is enabled.
        self.auto_build_index = auto_build_index
        # The configuration of MaxCompute data sources.
        self.config = config
        # The offline deployment name of the data source.
        self.domain = domain
        # The name of the data source.
        self.name = name
        # The number of resources used for data update.
        self.process_partition_count = process_partition_count
        # The configuration of SARO data sources.
        self.saro_config = saro_config
        # The type of the data source. Valid values: odps, swift, saro, oss, and unKnow.
        self.type = type

    def validate(self):
        if self.config:
            self.config.validate()
        if self.saro_config:
            self.saro_config.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_build_index is not None:
            result['autoBuildIndex'] = self.auto_build_index
        if self.config is not None:
            result['config'] = self.config.to_map()
        if self.domain is not None:
            result['domain'] = self.domain
        if self.name is not None:
            result['name'] = self.name
        if self.process_partition_count is not None:
            result['processPartitionCount'] = self.process_partition_count
        if self.saro_config is not None:
            result['saroConfig'] = self.saro_config.to_map()
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoBuildIndex') is not None:
            self.auto_build_index = m.get('autoBuildIndex')
        if m.get('config') is not None:
            temp_model = GetIndexResponseBodyResultDataSourceInfoConfig()
            self.config = temp_model.from_map(m['config'])
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('processPartitionCount') is not None:
            self.process_partition_count = m.get('processPartitionCount')
        if m.get('saroConfig') is not None:
            temp_model = GetIndexResponseBodyResultDataSourceInfoSaroConfig()
            self.saro_config = temp_model.from_map(m['saroConfig'])
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GetIndexResponseBodyResultVersionsFiles(TeaModel):
    def __init__(
        self,
        full_path_name: str = None,
        is_dir: bool = None,
        is_template: bool = None,
        name: str = None,
    ):
        # The full path of the file.
        self.full_path_name = full_path_name
        # Indicates whether the file is a directory.
        self.is_dir = is_dir
        # Indicates whether the file is a template.
        self.is_template = is_template
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.full_path_name is not None:
            result['fullPathName'] = self.full_path_name
        if self.is_dir is not None:
            result['isDir'] = self.is_dir
        if self.is_template is not None:
            result['isTemplate'] = self.is_template
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fullPathName') is not None:
            self.full_path_name = m.get('fullPathName')
        if m.get('isDir') is not None:
            self.is_dir = m.get('isDir')
        if m.get('isTemplate') is not None:
            self.is_template = m.get('isTemplate')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class GetIndexResponseBodyResultVersions(TeaModel):
    def __init__(
        self,
        desc: str = None,
        files: List[GetIndexResponseBodyResultVersionsFiles] = None,
        name: str = None,
        status: str = None,
        update_time: int = None,
        version_id: int = None,
    ):
        # The description of the version.
        self.desc = desc
        # The information about the files.
        self.files = files
        # The name of the version.
        self.name = name
        # The status of the version.
        self.status = status
        # The last time when the version was updated.
        self.update_time = update_time
        # The ID of the version.
        self.version_id = version_id

    def validate(self):
        if self.files:
            for k in self.files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.desc is not None:
            result['desc'] = self.desc
        result['files'] = []
        if self.files is not None:
            for k in self.files:
                result['files'].append(k.to_map() if k else None)
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        if self.version_id is not None:
            result['versionId'] = self.version_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('desc') is not None:
            self.desc = m.get('desc')
        self.files = []
        if m.get('files') is not None:
            for k in m.get('files'):
                temp_model = GetIndexResponseBodyResultVersionsFiles()
                self.files.append(temp_model.from_map(k))
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        if m.get('versionId') is not None:
            self.version_id = m.get('versionId')
        return self


class GetIndexResponseBodyResult(TeaModel):
    def __init__(
        self,
        content: str = None,
        data_source: str = None,
        data_source_info: GetIndexResponseBodyResultDataSourceInfo = None,
        description: str = None,
        domain: str = None,
        full_update_time: str = None,
        full_version: int = None,
        inc_update_time: str = None,
        index_size: int = None,
        index_status: str = None,
        name: str = None,
        partition: int = None,
        versions: List[GetIndexResponseBodyResultVersions] = None,
    ):
        # The content of the index.
        self.content = content
        self.data_source = data_source
        # The information about the data source.
        self.data_source_info = data_source_info
        # The remarks.
        self.description = description
        self.domain = domain
        # The last time when full data in the index was updated.
        self.full_update_time = full_update_time
        # The version of the data.
        self.full_version = full_version
        # The last time when incremental data in the index was updated.
        self.inc_update_time = inc_update_time
        # The index size.
        self.index_size = index_size
        # The status of the index. Valid values: NEW, PUBLISH, IN_USE, NOT_USE, STOP_USE, and RESTORE_USE. After a Retrieval Engine Edition instance is created, it enters the IN_USE state.
        self.index_status = index_status
        self.name = name
        # The number of shards.
        self.partition = partition
        # The information about the versions.
        self.versions = versions

    def validate(self):
        if self.data_source_info:
            self.data_source_info.validate()
        if self.versions:
            for k in self.versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.data_source is not None:
            result['dataSource'] = self.data_source
        if self.data_source_info is not None:
            result['dataSourceInfo'] = self.data_source_info.to_map()
        if self.description is not None:
            result['description'] = self.description
        if self.domain is not None:
            result['domain'] = self.domain
        if self.full_update_time is not None:
            result['fullUpdateTime'] = self.full_update_time
        if self.full_version is not None:
            result['fullVersion'] = self.full_version
        if self.inc_update_time is not None:
            result['incUpdateTime'] = self.inc_update_time
        if self.index_size is not None:
            result['indexSize'] = self.index_size
        if self.index_status is not None:
            result['indexStatus'] = self.index_status
        if self.name is not None:
            result['name'] = self.name
        if self.partition is not None:
            result['partition'] = self.partition
        result['versions'] = []
        if self.versions is not None:
            for k in self.versions:
                result['versions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('dataSource') is not None:
            self.data_source = m.get('dataSource')
        if m.get('dataSourceInfo') is not None:
            temp_model = GetIndexResponseBodyResultDataSourceInfo()
            self.data_source_info = temp_model.from_map(m['dataSourceInfo'])
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('fullUpdateTime') is not None:
            self.full_update_time = m.get('fullUpdateTime')
        if m.get('fullVersion') is not None:
            self.full_version = m.get('fullVersion')
        if m.get('incUpdateTime') is not None:
            self.inc_update_time = m.get('incUpdateTime')
        if m.get('indexSize') is not None:
            self.index_size = m.get('indexSize')
        if m.get('indexStatus') is not None:
            self.index_status = m.get('indexStatus')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        self.versions = []
        if m.get('versions') is not None:
            for k in m.get('versions'):
                temp_model = GetIndexResponseBodyResultVersions()
                self.versions.append(temp_model.from_map(k))
        return self


class GetIndexResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetIndexResponseBodyResult = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The information about the index.
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetIndexResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetIndexResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIndexResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIndexResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIndexVersionResponseBodyResultIndexVersions(TeaModel):
    def __init__(
        self,
        build_deploy_id: str = None,
        current_version: int = None,
        index_name: str = None,
        versions: List[int] = None,
    ):
        self.build_deploy_id = build_deploy_id
        self.current_version = current_version
        self.index_name = index_name
        self.versions = versions

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.build_deploy_id is not None:
            result['buildDeployId'] = self.build_deploy_id
        if self.current_version is not None:
            result['currentVersion'] = self.current_version
        if self.index_name is not None:
            result['indexName'] = self.index_name
        if self.versions is not None:
            result['versions'] = self.versions
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('buildDeployId') is not None:
            self.build_deploy_id = m.get('buildDeployId')
        if m.get('currentVersion') is not None:
            self.current_version = m.get('currentVersion')
        if m.get('indexName') is not None:
            self.index_name = m.get('indexName')
        if m.get('versions') is not None:
            self.versions = m.get('versions')
        return self


class GetIndexVersionResponseBodyResult(TeaModel):
    def __init__(
        self,
        cluster: str = None,
        index_versions: List[GetIndexVersionResponseBodyResultIndexVersions] = None,
    ):
        self.cluster = cluster
        self.index_versions = index_versions

    def validate(self):
        if self.index_versions:
            for k in self.index_versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cluster is not None:
            result['cluster'] = self.cluster
        result['indexVersions'] = []
        if self.index_versions is not None:
            for k in self.index_versions:
                result['indexVersions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('cluster') is not None:
            self.cluster = m.get('cluster')
        self.index_versions = []
        if m.get('indexVersions') is not None:
            for k in m.get('indexVersions'):
                temp_model = GetIndexVersionResponseBodyResultIndexVersions()
                self.index_versions.append(temp_model.from_map(k))
        return self


class GetIndexVersionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetIndexVersionResponseBodyResult = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetIndexVersionResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetIndexVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIndexVersionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIndexVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceResponseBodyResultTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class GetInstanceResponseBodyResult(TeaModel):
    def __init__(
        self,
        charge_type: str = None,
        commodity_code: str = None,
        create_time: str = None,
        description: str = None,
        expired_time: str = None,
        in_debt: bool = None,
        instance_id: str = None,
        lock_mode: str = None,
        resource_group_id: str = None,
        status: str = None,
        tags: List[GetInstanceResponseBodyResultTags] = None,
        update_time: str = None,
    ):
        # 付费类型
        self.charge_type = charge_type
        # 商品code
        self.commodity_code = commodity_code
        # 代表创建时间的资源属性字段
        self.create_time = create_time
        # The ID of the request.
        self.description = description
        # WB01240825
        self.expired_time = expired_time
        # 是否欠费
        self.in_debt = in_debt
        # 代表资源一级ID的资源属性字段
        self.instance_id = instance_id
        # 锁定状态
        self.lock_mode = lock_mode
        # ### Sample responses
        # 
        # **Sample success responses**\
        # 
        #     {
        #       "requestId": "90D6B8F5-FE97-4509-9AAB-367836C51818",
        #       "result": 
        #       {
        #         "instanceId":"fadsfsafs",
        #         "inDebt":true,
        #         "lockMode":"Unlock",
        #         "expiredTime":"asdfas",
        #         "updateTime":"dfasf",
        #         "createTime":"dfasf",
        #         "resourceGroupId":"resourceGroupID",
        #         "commodityCode":"commodityCode",
        #         "chargeType":"POSYPAY",
        #         "description":"this is description",
        #         "apiVersion": "tisplus/v1",
        #         "network": {
        #           "vSwitchId": "vswitch_id_xxx",
        #           "vpcId": "vpc_id_xxx",	  
        #         },
        #         "userName": "user",
        #         "spec": {
        #           "searchResource": {
        #             "disk": 50,
        #             "mem": 8,
        #             "cpu": 2,
        #             "nodeCount": 2
        #           },
        #           "qrsResource": {
        #             "disk": 50,
        #             "mem": 8,
        #             "cpu": 2,
        #             "nodeCount": 2
        #           }
        #         },
        #        "status": "INIT",
        #       }
        #     }
        # 
        # **Sample error responses**\
        # 
        #     {
        #       "requestId": "BD1EA715-DF6F-06C2-004C-C1FA0D3A9820",
        #       "httpCode": 404,
        #       "code": "App.NotFound",
        #       "message": "App not found"
        #     }
        self.resource_group_id = resource_group_id
        self.status = status
        self.tags = tags
        # 更新时间
        self.update_time = update_time

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.charge_type is not None:
            result['chargeType'] = self.charge_type
        if self.commodity_code is not None:
            result['commodityCode'] = self.commodity_code
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.expired_time is not None:
            result['expiredTime'] = self.expired_time
        if self.in_debt is not None:
            result['inDebt'] = self.in_debt
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.lock_mode is not None:
            result['lockMode'] = self.lock_mode
        if self.resource_group_id is not None:
            result['resourceGroupId'] = self.resource_group_id
        if self.status is not None:
            result['status'] = self.status
        result['tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['tags'].append(k.to_map() if k else None)
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('chargeType') is not None:
            self.charge_type = m.get('chargeType')
        if m.get('commodityCode') is not None:
            self.commodity_code = m.get('commodityCode')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('expiredTime') is not None:
            self.expired_time = m.get('expiredTime')
        if m.get('inDebt') is not None:
            self.in_debt = m.get('inDebt')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('lockMode') is not None:
            self.lock_mode = m.get('lockMode')
        if m.get('resourceGroupId') is not None:
            self.resource_group_id = m.get('resourceGroupId')
        if m.get('status') is not None:
            self.status = m.get('status')
        self.tags = []
        if m.get('tags') is not None:
            for k in m.get('tags'):
                temp_model = GetInstanceResponseBodyResultTags()
                self.tags.append(temp_model.from_map(k))
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class GetInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetInstanceResponseBodyResult = None,
    ):
        self.request_id = request_id
        # The description of the instance.
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetInstanceResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetNodeConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_name: str = None,
        name: str = None,
        type: str = None,
    ):
        self.cluster_name = cluster_name
        self.name = name
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cluster_name is not None:
            result['clusterName'] = self.cluster_name
        if self.name is not None:
            result['name'] = self.name
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clusterName') is not None:
            self.cluster_name = m.get('clusterName')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GetNodeConfigResponseBodyResult(TeaModel):
    def __init__(
        self,
        active: bool = None,
        data_duplicate_number: int = None,
        data_fragment_number: int = None,
        min_service_percent: int = None,
        published: bool = None,
    ):
        self.active = active
        self.data_duplicate_number = data_duplicate_number
        self.data_fragment_number = data_fragment_number
        self.min_service_percent = min_service_percent
        self.published = published

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.active is not None:
            result['active'] = self.active
        if self.data_duplicate_number is not None:
            result['dataDuplicateNumber'] = self.data_duplicate_number
        if self.data_fragment_number is not None:
            result['dataFragmentNumber'] = self.data_fragment_number
        if self.min_service_percent is not None:
            result['minServicePercent'] = self.min_service_percent
        if self.published is not None:
            result['published'] = self.published
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('active') is not None:
            self.active = m.get('active')
        if m.get('dataDuplicateNumber') is not None:
            self.data_duplicate_number = m.get('dataDuplicateNumber')
        if m.get('dataFragmentNumber') is not None:
            self.data_fragment_number = m.get('dataFragmentNumber')
        if m.get('minServicePercent') is not None:
            self.min_service_percent = m.get('minServicePercent')
        if m.get('published') is not None:
            self.published = m.get('published')
        return self


class GetNodeConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: GetNodeConfigResponseBodyResult = None,
    ):
        # Id of the request
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = GetNodeConfigResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class GetNodeConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetNodeConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetNodeConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAdvanceConfigDirRequest(TeaModel):
    def __init__(
        self,
        dir_name: str = None,
    ):
        self.dir_name = dir_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dir_name is not None:
            result['dirName'] = self.dir_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dirName') is not None:
            self.dir_name = m.get('dirName')
        return self


class ListAdvanceConfigDirResponseBodyResult(TeaModel):
    def __init__(
        self,
        full_path_name: str = None,
        is_dir: bool = None,
        is_template: bool = None,
        name: str = None,
    ):
        self.full_path_name = full_path_name
        self.is_dir = is_dir
        self.is_template = is_template
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.full_path_name is not None:
            result['fullPathName'] = self.full_path_name
        if self.is_dir is not None:
            result['isDir'] = self.is_dir
        if self.is_template is not None:
            result['isTemplate'] = self.is_template
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fullPathName') is not None:
            self.full_path_name = m.get('fullPathName')
        if m.get('isDir') is not None:
            self.is_dir = m.get('isDir')
        if m.get('isTemplate') is not None:
            self.is_template = m.get('isTemplate')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListAdvanceConfigDirResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListAdvanceConfigDirResponseBodyResult] = None,
    ):
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListAdvanceConfigDirResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListAdvanceConfigDirResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAdvanceConfigDirResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListAdvanceConfigDirResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAdvanceConfigsRequest(TeaModel):
    def __init__(
        self,
        data_source_name: str = None,
        index_name: str = None,
        type: str = None,
    ):
        self.data_source_name = data_source_name
        self.index_name = index_name
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_name is not None:
            result['dataSourceName'] = self.data_source_name
        if self.index_name is not None:
            result['indexName'] = self.index_name
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dataSourceName') is not None:
            self.data_source_name = m.get('dataSourceName')
        if m.get('indexName') is not None:
            self.index_name = m.get('indexName')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class ListAdvanceConfigsResponseBodyResultFiles(TeaModel):
    def __init__(
        self,
        full_path_name: str = None,
        is_dir: bool = None,
        is_template: bool = None,
        name: str = None,
    ):
        self.full_path_name = full_path_name
        self.is_dir = is_dir
        self.is_template = is_template
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.full_path_name is not None:
            result['fullPathName'] = self.full_path_name
        if self.is_dir is not None:
            result['isDir'] = self.is_dir
        if self.is_template is not None:
            result['isTemplate'] = self.is_template
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fullPathName') is not None:
            self.full_path_name = m.get('fullPathName')
        if m.get('isDir') is not None:
            self.is_dir = m.get('isDir')
        if m.get('isTemplate') is not None:
            self.is_template = m.get('isTemplate')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListAdvanceConfigsResponseBodyResult(TeaModel):
    def __init__(
        self,
        content: str = None,
        content_type: str = None,
        desc: str = None,
        files: List[ListAdvanceConfigsResponseBodyResultFiles] = None,
        name: str = None,
        status: str = None,
        update_time: int = None,
    ):
        # 配置内容 http，git 请求时不为空
        self.content = content
        # 配置内容的类型 (FILE, GIT, HTTP, ODPS)
        self.content_type = content_type
        self.desc = desc
        self.files = files
        self.name = name
        self.status = status
        self.update_time = update_time

    def validate(self):
        if self.files:
            for k in self.files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.content_type is not None:
            result['contentType'] = self.content_type
        if self.desc is not None:
            result['desc'] = self.desc
        result['files'] = []
        if self.files is not None:
            for k in self.files:
                result['files'].append(k.to_map() if k else None)
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('contentType') is not None:
            self.content_type = m.get('contentType')
        if m.get('desc') is not None:
            self.desc = m.get('desc')
        self.files = []
        if m.get('files') is not None:
            for k in m.get('files'):
                temp_model = ListAdvanceConfigsResponseBodyResultFiles()
                self.files.append(temp_model.from_map(k))
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class ListAdvanceConfigsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListAdvanceConfigsResponseBodyResult] = None,
    ):
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListAdvanceConfigsResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListAdvanceConfigsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAdvanceConfigsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListAdvanceConfigsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListClusterNamesResponseBodyResult(TeaModel):
    def __init__(
        self,
        description: str = None,
        id: int = None,
        name: str = None,
    ):
        self.description = description
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['description'] = self.description
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListClusterNamesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: ListClusterNamesResponseBodyResult = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = ListClusterNamesResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class ListClusterNamesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListClusterNamesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListClusterNamesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListClusterTasksResponseBodyResultTags(TeaModel):
    def __init__(
        self,
        msg: str = None,
        tag_level: str = None,
    ):
        self.msg = msg
        self.tag_level = tag_level

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.msg is not None:
            result['msg'] = self.msg
        if self.tag_level is not None:
            result['tagLevel'] = self.tag_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('msg') is not None:
            self.msg = m.get('msg')
        if m.get('tagLevel') is not None:
            self.tag_level = m.get('tagLevel')
        return self


class ListClusterTasksResponseBodyResultTaskNodes(TeaModel):
    def __init__(
        self,
        finish_date: str = None,
        index: int = None,
        name: str = None,
        status: str = None,
    ):
        self.finish_date = finish_date
        self.index = index
        self.name = name
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.finish_date is not None:
            result['finishDate'] = self.finish_date
        if self.index is not None:
            result['index'] = self.index
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('finishDate') is not None:
            self.finish_date = m.get('finishDate')
        if m.get('index') is not None:
            self.index = m.get('index')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListClusterTasksResponseBodyResult(TeaModel):
    def __init__(
        self,
        extra_attribute: str = None,
        field_3: str = None,
        fsm_id: str = None,
        group_type: str = None,
        name: str = None,
        status: str = None,
        tags: List[ListClusterTasksResponseBodyResultTags] = None,
        task_nodes: List[ListClusterTasksResponseBodyResultTaskNodes] = None,
        time: str = None,
        type: str = None,
        user: str = None,
    ):
        self.extra_attribute = extra_attribute
        self.field_3 = field_3
        # fsmId
        self.fsm_id = fsm_id
        # ### Method
        # 
        # ```java
        # GET
        # ```
        # 
        # ### URI
        # 
        # ```java
        # /openapi/ha3/instances/{instanceId}/cluster-tasks
        # ```
        self.group_type = group_type
        # Displays cluster tasks .
        self.name = name
        self.status = status
        self.tags = tags
        self.task_nodes = task_nodes
        self.time = time
        self.type = type
        self.user = user

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()
        if self.task_nodes:
            for k in self.task_nodes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.extra_attribute is not None:
            result['extraAttribute'] = self.extra_attribute
        if self.field_3 is not None:
            result['field3'] = self.field_3
        if self.fsm_id is not None:
            result['fsmId'] = self.fsm_id
        if self.group_type is not None:
            result['groupType'] = self.group_type
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        result['tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['tags'].append(k.to_map() if k else None)
        result['taskNodes'] = []
        if self.task_nodes is not None:
            for k in self.task_nodes:
                result['taskNodes'].append(k.to_map() if k else None)
        if self.time is not None:
            result['time'] = self.time
        if self.type is not None:
            result['type'] = self.type
        if self.user is not None:
            result['user'] = self.user
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('extraAttribute') is not None:
            self.extra_attribute = m.get('extraAttribute')
        if m.get('field3') is not None:
            self.field_3 = m.get('field3')
        if m.get('fsmId') is not None:
            self.fsm_id = m.get('fsmId')
        if m.get('groupType') is not None:
            self.group_type = m.get('groupType')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        self.tags = []
        if m.get('tags') is not None:
            for k in m.get('tags'):
                temp_model = ListClusterTasksResponseBodyResultTags()
                self.tags.append(temp_model.from_map(k))
        self.task_nodes = []
        if m.get('taskNodes') is not None:
            for k in m.get('taskNodes'):
                temp_model = ListClusterTasksResponseBodyResultTaskNodes()
                self.task_nodes.append(temp_model.from_map(k))
        if m.get('time') is not None:
            self.time = m.get('time')
        if m.get('type') is not None:
            self.type = m.get('type')
        if m.get('user') is not None:
            self.user = m.get('user')
        return self


class ListClusterTasksResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListClusterTasksResponseBodyResult] = None,
    ):
        # id of request
        self.request_id = request_id
        # The date when the task was completed.
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListClusterTasksResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListClusterTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListClusterTasksResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListClusterTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListClustersResponseBodyResultDataNode(TeaModel):
    def __init__(
        self,
        name: str = None,
        number: int = None,
        partition: int = None,
    ):
        self.name = name
        self.number = number
        self.partition = partition

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.number is not None:
            result['number'] = self.number
        if self.partition is not None:
            result['partition'] = self.partition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('number') is not None:
            self.number = m.get('number')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        return self


class ListClustersResponseBodyResultQueryNode(TeaModel):
    def __init__(
        self,
        name: str = None,
        number: int = None,
        partition: int = None,
    ):
        self.name = name
        self.number = number
        self.partition = partition

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.number is not None:
            result['number'] = self.number
        if self.partition is not None:
            result['partition'] = self.partition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('number') is not None:
            self.number = m.get('number')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        return self


class ListClustersResponseBodyResult(TeaModel):
    def __init__(
        self,
        config_update_time: str = None,
        current_advance_config_version: str = None,
        current_offline_dict_config_version: str = None,
        current_online_config_version: str = None,
        current_online_query_config_version: str = None,
        data_node: ListClustersResponseBodyResultDataNode = None,
        description: str = None,
        latest_advance_config_version: str = None,
        latest_offline_dict_config_version: str = None,
        latest_online_config_version: str = None,
        latest_online_query_config_version: str = None,
        name: str = None,
        query_node: ListClustersResponseBodyResultQueryNode = None,
        status: str = None,
    ):
        self.config_update_time = config_update_time
        self.current_advance_config_version = current_advance_config_version
        # 词典配置生效版本
        self.current_offline_dict_config_version = current_offline_dict_config_version
        self.current_online_config_version = current_online_config_version
        # 查询配置生效版本
        self.current_online_query_config_version = current_online_query_config_version
        self.data_node = data_node
        self.description = description
        self.latest_advance_config_version = latest_advance_config_version
        # 词典配置最新版本
        self.latest_offline_dict_config_version = latest_offline_dict_config_version
        self.latest_online_config_version = latest_online_config_version
        # 查询配置最新版本
        self.latest_online_query_config_version = latest_online_query_config_version
        self.name = name
        self.query_node = query_node
        self.status = status

    def validate(self):
        if self.data_node:
            self.data_node.validate()
        if self.query_node:
            self.query_node.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_update_time is not None:
            result['configUpdateTime'] = self.config_update_time
        if self.current_advance_config_version is not None:
            result['currentAdvanceConfigVersion'] = self.current_advance_config_version
        if self.current_offline_dict_config_version is not None:
            result['currentOfflineDictConfigVersion'] = self.current_offline_dict_config_version
        if self.current_online_config_version is not None:
            result['currentOnlineConfigVersion'] = self.current_online_config_version
        if self.current_online_query_config_version is not None:
            result['currentOnlineQueryConfigVersion'] = self.current_online_query_config_version
        if self.data_node is not None:
            result['dataNode'] = self.data_node.to_map()
        if self.description is not None:
            result['description'] = self.description
        if self.latest_advance_config_version is not None:
            result['latestAdvanceConfigVersion'] = self.latest_advance_config_version
        if self.latest_offline_dict_config_version is not None:
            result['latestOfflineDictConfigVersion'] = self.latest_offline_dict_config_version
        if self.latest_online_config_version is not None:
            result['latestOnlineConfigVersion'] = self.latest_online_config_version
        if self.latest_online_query_config_version is not None:
            result['latestOnlineQueryConfigVersion'] = self.latest_online_query_config_version
        if self.name is not None:
            result['name'] = self.name
        if self.query_node is not None:
            result['queryNode'] = self.query_node.to_map()
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('configUpdateTime') is not None:
            self.config_update_time = m.get('configUpdateTime')
        if m.get('currentAdvanceConfigVersion') is not None:
            self.current_advance_config_version = m.get('currentAdvanceConfigVersion')
        if m.get('currentOfflineDictConfigVersion') is not None:
            self.current_offline_dict_config_version = m.get('currentOfflineDictConfigVersion')
        if m.get('currentOnlineConfigVersion') is not None:
            self.current_online_config_version = m.get('currentOnlineConfigVersion')
        if m.get('currentOnlineQueryConfigVersion') is not None:
            self.current_online_query_config_version = m.get('currentOnlineQueryConfigVersion')
        if m.get('dataNode') is not None:
            temp_model = ListClustersResponseBodyResultDataNode()
            self.data_node = temp_model.from_map(m['dataNode'])
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('latestAdvanceConfigVersion') is not None:
            self.latest_advance_config_version = m.get('latestAdvanceConfigVersion')
        if m.get('latestOfflineDictConfigVersion') is not None:
            self.latest_offline_dict_config_version = m.get('latestOfflineDictConfigVersion')
        if m.get('latestOnlineConfigVersion') is not None:
            self.latest_online_config_version = m.get('latestOnlineConfigVersion')
        if m.get('latestOnlineQueryConfigVersion') is not None:
            self.latest_online_query_config_version = m.get('latestOnlineQueryConfigVersion')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('queryNode') is not None:
            temp_model = ListClustersResponseBodyResultQueryNode()
            self.query_node = temp_model.from_map(m['queryNode'])
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListClustersResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListClustersResponseBodyResult] = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListClustersResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListClustersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListClustersResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListClustersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDataSourceSchemasResponseBodyResultPrimaryKey(TeaModel):
    def __init__(
        self,
        has_primary_key_attribute: bool = None,
        is_primary_key: bool = None,
        is_primary_key_sorted: bool = None,
    ):
        self.has_primary_key_attribute = has_primary_key_attribute
        self.is_primary_key = is_primary_key
        self.is_primary_key_sorted = is_primary_key_sorted

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.has_primary_key_attribute is not None:
            result['hasPrimaryKeyAttribute'] = self.has_primary_key_attribute
        if self.is_primary_key is not None:
            result['isPrimaryKey'] = self.is_primary_key
        if self.is_primary_key_sorted is not None:
            result['isPrimaryKeySorted'] = self.is_primary_key_sorted
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('hasPrimaryKeyAttribute') is not None:
            self.has_primary_key_attribute = m.get('hasPrimaryKeyAttribute')
        if m.get('isPrimaryKey') is not None:
            self.is_primary_key = m.get('isPrimaryKey')
        if m.get('isPrimaryKeySorted') is not None:
            self.is_primary_key_sorted = m.get('isPrimaryKeySorted')
        return self


class ListDataSourceSchemasResponseBodyResult(TeaModel):
    def __init__(
        self,
        add_index: bool = None,
        attribute: bool = None,
        custom: bool = None,
        name: str = None,
        primary_key: ListDataSourceSchemasResponseBodyResultPrimaryKey = None,
        summary: bool = None,
        type: str = None,
    ):
        self.add_index = add_index
        self.attribute = attribute
        self.custom = custom
        self.name = name
        self.primary_key = primary_key
        self.summary = summary
        self.type = type

    def validate(self):
        if self.primary_key:
            self.primary_key.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.add_index is not None:
            result['addIndex'] = self.add_index
        if self.attribute is not None:
            result['attribute'] = self.attribute
        if self.custom is not None:
            result['custom'] = self.custom
        if self.name is not None:
            result['name'] = self.name
        if self.primary_key is not None:
            result['primaryKey'] = self.primary_key.to_map()
        if self.summary is not None:
            result['summary'] = self.summary
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('addIndex') is not None:
            self.add_index = m.get('addIndex')
        if m.get('attribute') is not None:
            self.attribute = m.get('attribute')
        if m.get('custom') is not None:
            self.custom = m.get('custom')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('primaryKey') is not None:
            temp_model = ListDataSourceSchemasResponseBodyResultPrimaryKey()
            self.primary_key = temp_model.from_map(m['primaryKey'])
        if m.get('summary') is not None:
            self.summary = m.get('summary')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class ListDataSourceSchemasResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListDataSourceSchemasResponseBodyResult] = None,
    ):
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListDataSourceSchemasResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListDataSourceSchemasResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDataSourceSchemasResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDataSourceSchemasResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDataSourceTasksResponseBodyResultTags(TeaModel):
    def __init__(
        self,
        msg: str = None,
        tag_level: str = None,
    ):
        self.msg = msg
        self.tag_level = tag_level

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.msg is not None:
            result['msg'] = self.msg
        if self.tag_level is not None:
            result['tagLevel'] = self.tag_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('msg') is not None:
            self.msg = m.get('msg')
        if m.get('tagLevel') is not None:
            self.tag_level = m.get('tagLevel')
        return self


class ListDataSourceTasksResponseBodyResultTaskNodes(TeaModel):
    def __init__(
        self,
        finish_date: str = None,
        index: int = None,
        name: str = None,
        status: str = None,
    ):
        self.finish_date = finish_date
        self.index = index
        self.name = name
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.finish_date is not None:
            result['finishDate'] = self.finish_date
        if self.index is not None:
            result['index'] = self.index
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('finishDate') is not None:
            self.finish_date = m.get('finishDate')
        if m.get('index') is not None:
            self.index = m.get('index')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListDataSourceTasksResponseBodyResult(TeaModel):
    def __init__(
        self,
        extra_attribute: str = None,
        field_3: str = None,
        fsm_id: str = None,
        group_type: str = None,
        name: str = None,
        status: str = None,
        tags: List[ListDataSourceTasksResponseBodyResultTags] = None,
        task_nodes: List[ListDataSourceTasksResponseBodyResultTaskNodes] = None,
        time: str = None,
        type: str = None,
        user: str = None,
    ):
        self.extra_attribute = extra_attribute
        self.field_3 = field_3
        # fsmId
        self.fsm_id = fsm_id
        # ### Method
        # 
        # ```java
        # GET
        # ```
        # 
        # ### URI
        # 
        # ```java
        # /openapi/ha3/instances/{instanceId}/data-source-tasks
        # ```
        self.group_type = group_type
        # Displays data source tasks.
        self.name = name
        self.status = status
        self.tags = tags
        self.task_nodes = task_nodes
        self.time = time
        self.type = type
        self.user = user

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()
        if self.task_nodes:
            for k in self.task_nodes:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.extra_attribute is not None:
            result['extraAttribute'] = self.extra_attribute
        if self.field_3 is not None:
            result['field3'] = self.field_3
        if self.fsm_id is not None:
            result['fsmId'] = self.fsm_id
        if self.group_type is not None:
            result['groupType'] = self.group_type
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        result['tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['tags'].append(k.to_map() if k else None)
        result['taskNodes'] = []
        if self.task_nodes is not None:
            for k in self.task_nodes:
                result['taskNodes'].append(k.to_map() if k else None)
        if self.time is not None:
            result['time'] = self.time
        if self.type is not None:
            result['type'] = self.type
        if self.user is not None:
            result['user'] = self.user
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('extraAttribute') is not None:
            self.extra_attribute = m.get('extraAttribute')
        if m.get('field3') is not None:
            self.field_3 = m.get('field3')
        if m.get('fsmId') is not None:
            self.fsm_id = m.get('fsmId')
        if m.get('groupType') is not None:
            self.group_type = m.get('groupType')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        self.tags = []
        if m.get('tags') is not None:
            for k in m.get('tags'):
                temp_model = ListDataSourceTasksResponseBodyResultTags()
                self.tags.append(temp_model.from_map(k))
        self.task_nodes = []
        if m.get('taskNodes') is not None:
            for k in m.get('taskNodes'):
                temp_model = ListDataSourceTasksResponseBodyResultTaskNodes()
                self.task_nodes.append(temp_model.from_map(k))
        if m.get('time') is not None:
            self.time = m.get('time')
        if m.get('type') is not None:
            self.type = m.get('type')
        if m.get('user') is not None:
            self.user = m.get('user')
        return self


class ListDataSourceTasksResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListDataSourceTasksResponseBodyResult] = None,
    ):
        # id of request
        self.request_id = request_id
        # The date when the task was completed.
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListDataSourceTasksResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListDataSourceTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDataSourceTasksResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDataSourceTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDataSourcesResponseBodyResult(TeaModel):
    def __init__(
        self,
        domain: str = None,
        indexes: List[str] = None,
        last_ful_time: int = None,
        name: str = None,
        status: str = None,
        type: str = None,
    ):
        # The data sources deployed in offline mode.
        self.domain = domain
        # The indexes.
        self.indexes = indexes
        # The time when the full data of the data source was last queried.
        self.last_ful_time = last_ful_time
        # The name of the data source.
        self.name = name
        # The status of the data source.
        self.status = status
        # The type of the data source.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.domain is not None:
            result['domain'] = self.domain
        if self.indexes is not None:
            result['indexes'] = self.indexes
        if self.last_ful_time is not None:
            result['lastFulTime'] = self.last_ful_time
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('indexes') is not None:
            self.indexes = m.get('indexes')
        if m.get('lastFulTime') is not None:
            self.last_ful_time = m.get('lastFulTime')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class ListDataSourcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListDataSourcesResponseBodyResult] = None,
    ):
        # ## Method
        # 
        # `GET`
        # 
        # ## URI
        # 
        # `/openapi/ha3/instances/{instanceId}/data-sources`
        self.request_id = request_id
        # The returned results.
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListDataSourcesResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListDataSourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDataSourcesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDataSourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDateSourceGenerationsRequest(TeaModel):
    def __init__(
        self,
        domain_name: str = None,
        valid_status: bool = None,
    ):
        # The data center where the data source is deployed.
        self.domain_name = domain_name
        # The valid state of the data source. Valid values: true and false. The default value of this parameter is true.
        # 
        # 1.  true indicates that the generations that have not expired and of which the tasks have been executed are returned.
        # 2.  false indicates that all generations are returned.
        self.valid_status = valid_status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.domain_name is not None:
            result['domainName'] = self.domain_name
        if self.valid_status is not None:
            result['validStatus'] = self.valid_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('domainName') is not None:
            self.domain_name = m.get('domainName')
        if m.get('validStatus') is not None:
            self.valid_status = m.get('validStatus')
        return self


class ListDateSourceGenerationsResponseBodyResult(TeaModel):
    def __init__(
        self,
        build_deploy_id: int = None,
        create_time: int = None,
        data_dump_root: str = None,
        generation: int = None,
        partition: Dict[str, int] = None,
        status: str = None,
        timestamp: int = None,
    ):
        # buildDeployId
        self.build_deploy_id = build_deploy_id
        # The time to start index building.
        self.create_time = create_time
        # The directory where the index file created by using the dump table is saved.
        self.data_dump_root = data_dump_root
        # The primary key of the generation.
        self.generation = generation
        # Key indicates the name of the index. value indicates the number of shards.
        self.partition = partition
        # The status.
        self.status = status
        # The timestamp when the offline indexing was initiated.
        self.timestamp = timestamp

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.build_deploy_id is not None:
            result['buildDeployId'] = self.build_deploy_id
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.data_dump_root is not None:
            result['dataDumpRoot'] = self.data_dump_root
        if self.generation is not None:
            result['generation'] = self.generation
        if self.partition is not None:
            result['partition'] = self.partition
        if self.status is not None:
            result['status'] = self.status
        if self.timestamp is not None:
            result['timestamp'] = self.timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('buildDeployId') is not None:
            self.build_deploy_id = m.get('buildDeployId')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('dataDumpRoot') is not None:
            self.data_dump_root = m.get('dataDumpRoot')
        if m.get('generation') is not None:
            self.generation = m.get('generation')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('timestamp') is not None:
            self.timestamp = m.get('timestamp')
        return self


class ListDateSourceGenerationsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListDateSourceGenerationsResponseBodyResult] = None,
    ):
        # id of request
        self.request_id = request_id
        # List
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListDateSourceGenerationsResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListDateSourceGenerationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDateSourceGenerationsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDateSourceGenerationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIndexesRequest(TeaModel):
    def __init__(
        self,
        new_mode: bool = None,
    ):
        self.new_mode = new_mode

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.new_mode is not None:
            result['newMode'] = self.new_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('newMode') is not None:
            self.new_mode = m.get('newMode')
        return self


class ListIndexesResponseBodyResultDataSourceInfoConfig(TeaModel):
    def __init__(
        self,
        access_key: str = None,
        access_secret: str = None,
        bucket: str = None,
        endpoint: str = None,
        namespace: str = None,
        oss_path: str = None,
        partition: str = None,
        path: str = None,
        project: str = None,
        table: str = None,
    ):
        self.access_key = access_key
        self.access_secret = access_secret
        self.bucket = bucket
        # A parameter related to MaxCompute.
        self.endpoint = endpoint
        # A parameter related to SARO.
        self.namespace = namespace
        # A parameter related to OSS.
        self.oss_path = oss_path
        self.partition = partition
        # A parameter related to Apsara File Storage for HDFS.
        self.path = path
        self.project = project
        # A parameter related to SARO and MaxCompute.
        self.table = table

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key is not None:
            result['accessKey'] = self.access_key
        if self.access_secret is not None:
            result['accessSecret'] = self.access_secret
        if self.bucket is not None:
            result['bucket'] = self.bucket
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.namespace is not None:
            result['namespace'] = self.namespace
        if self.oss_path is not None:
            result['ossPath'] = self.oss_path
        if self.partition is not None:
            result['partition'] = self.partition
        if self.path is not None:
            result['path'] = self.path
        if self.project is not None:
            result['project'] = self.project
        if self.table is not None:
            result['table'] = self.table
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKey') is not None:
            self.access_key = m.get('accessKey')
        if m.get('accessSecret') is not None:
            self.access_secret = m.get('accessSecret')
        if m.get('bucket') is not None:
            self.bucket = m.get('bucket')
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('namespace') is not None:
            self.namespace = m.get('namespace')
        if m.get('ossPath') is not None:
            self.oss_path = m.get('ossPath')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('path') is not None:
            self.path = m.get('path')
        if m.get('project') is not None:
            self.project = m.get('project')
        if m.get('table') is not None:
            self.table = m.get('table')
        return self


class ListIndexesResponseBodyResultDataSourceInfoSaroConfig(TeaModel):
    def __init__(
        self,
        namespace: str = None,
        table_name: str = None,
    ):
        self.namespace = namespace
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.namespace is not None:
            result['namespace'] = self.namespace
        if self.table_name is not None:
            result['tableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('namespace') is not None:
            self.namespace = m.get('namespace')
        if m.get('tableName') is not None:
            self.table_name = m.get('tableName')
        return self


class ListIndexesResponseBodyResultDataSourceInfo(TeaModel):
    def __init__(
        self,
        auto_build_index: bool = None,
        config: ListIndexesResponseBodyResultDataSourceInfoConfig = None,
        domain: str = None,
        name: str = None,
        process_partition_count: int = None,
        saro_config: ListIndexesResponseBodyResultDataSourceInfoSaroConfig = None,
        type: str = None,
    ):
        # Indicates whether the automatic full indexing feature is enabled.
        self.auto_build_index = auto_build_index
        # The configuration of MaxCompute data sources.
        self.config = config
        # The offline deployment name of the data source.
        self.domain = domain
        # The name of the data source.
        self.name = name
        # The number of resources used for data update.
        self.process_partition_count = process_partition_count
        # The configuration of SARO data sources.
        self.saro_config = saro_config
        # The type of the data source. Valid values: odps, swift, saro, oss, and unKnow.
        self.type = type

    def validate(self):
        if self.config:
            self.config.validate()
        if self.saro_config:
            self.saro_config.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_build_index is not None:
            result['autoBuildIndex'] = self.auto_build_index
        if self.config is not None:
            result['config'] = self.config.to_map()
        if self.domain is not None:
            result['domain'] = self.domain
        if self.name is not None:
            result['name'] = self.name
        if self.process_partition_count is not None:
            result['processPartitionCount'] = self.process_partition_count
        if self.saro_config is not None:
            result['saroConfig'] = self.saro_config.to_map()
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('autoBuildIndex') is not None:
            self.auto_build_index = m.get('autoBuildIndex')
        if m.get('config') is not None:
            temp_model = ListIndexesResponseBodyResultDataSourceInfoConfig()
            self.config = temp_model.from_map(m['config'])
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('processPartitionCount') is not None:
            self.process_partition_count = m.get('processPartitionCount')
        if m.get('saroConfig') is not None:
            temp_model = ListIndexesResponseBodyResultDataSourceInfoSaroConfig()
            self.saro_config = temp_model.from_map(m['saroConfig'])
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class ListIndexesResponseBodyResultVersionsFiles(TeaModel):
    def __init__(
        self,
        full_path_name: str = None,
        is_dir: bool = None,
        is_template: bool = None,
        name: str = None,
    ):
        # The full path of the file.
        self.full_path_name = full_path_name
        # Indicates whether the file is a directory.
        self.is_dir = is_dir
        # Indicates whether the file is a template.
        self.is_template = is_template
        # The name of the file.
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.full_path_name is not None:
            result['fullPathName'] = self.full_path_name
        if self.is_dir is not None:
            result['isDir'] = self.is_dir
        if self.is_template is not None:
            result['isTemplate'] = self.is_template
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fullPathName') is not None:
            self.full_path_name = m.get('fullPathName')
        if m.get('isDir') is not None:
            self.is_dir = m.get('isDir')
        if m.get('isTemplate') is not None:
            self.is_template = m.get('isTemplate')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListIndexesResponseBodyResultVersions(TeaModel):
    def __init__(
        self,
        desc: str = None,
        files: List[ListIndexesResponseBodyResultVersionsFiles] = None,
        name: str = None,
        status: str = None,
        update_time: int = None,
        version_id: int = None,
    ):
        # The description of the version.
        self.desc = desc
        # The information about the files.
        self.files = files
        # The name of the version.
        self.name = name
        # The status of the version. Valid values: drafting, used, unused, and trash.
        self.status = status
        # The last time when the version was updated.
        self.update_time = update_time
        # The ID of the version. The value is null for an edit version.
        self.version_id = version_id

    def validate(self):
        if self.files:
            for k in self.files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.desc is not None:
            result['desc'] = self.desc
        result['files'] = []
        if self.files is not None:
            for k in self.files:
                result['files'].append(k.to_map() if k else None)
        if self.name is not None:
            result['name'] = self.name
        if self.status is not None:
            result['status'] = self.status
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        if self.version_id is not None:
            result['versionId'] = self.version_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('desc') is not None:
            self.desc = m.get('desc')
        self.files = []
        if m.get('files') is not None:
            for k in m.get('files'):
                temp_model = ListIndexesResponseBodyResultVersionsFiles()
                self.files.append(temp_model.from_map(k))
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        if m.get('versionId') is not None:
            self.version_id = m.get('versionId')
        return self


class ListIndexesResponseBodyResult(TeaModel):
    def __init__(
        self,
        content: str = None,
        data_source: str = None,
        data_source_info: ListIndexesResponseBodyResultDataSourceInfo = None,
        description: str = None,
        domain: str = None,
        full_update_time: str = None,
        full_version: int = None,
        inc_update_time: str = None,
        index_size: int = None,
        index_status: str = None,
        name: str = None,
        partition: int = None,
        versions: List[ListIndexesResponseBodyResultVersions] = None,
    ):
        # The content of the index.
        self.content = content
        # The data source.
        self.data_source = data_source
        # The information about the data source.
        self.data_source_info = data_source_info
        # The remarks.
        self.description = description
        # The deployment name of the index.
        self.domain = domain
        # The last time when full data in the index was updated.
        self.full_update_time = full_update_time
        # The version of the data.
        self.full_version = full_version
        # The last time when incremental data in the index was updated.
        self.inc_update_time = inc_update_time
        # The index size.
        self.index_size = index_size
        # The status of the index. Valid values: NEW and PUBLISH.
        self.index_status = index_status
        # The name of the index.
        self.name = name
        # The number of shards.
        self.partition = partition
        # The information about the versions.
        self.versions = versions

    def validate(self):
        if self.data_source_info:
            self.data_source_info.validate()
        if self.versions:
            for k in self.versions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.data_source is not None:
            result['dataSource'] = self.data_source
        if self.data_source_info is not None:
            result['dataSourceInfo'] = self.data_source_info.to_map()
        if self.description is not None:
            result['description'] = self.description
        if self.domain is not None:
            result['domain'] = self.domain
        if self.full_update_time is not None:
            result['fullUpdateTime'] = self.full_update_time
        if self.full_version is not None:
            result['fullVersion'] = self.full_version
        if self.inc_update_time is not None:
            result['incUpdateTime'] = self.inc_update_time
        if self.index_size is not None:
            result['indexSize'] = self.index_size
        if self.index_status is not None:
            result['indexStatus'] = self.index_status
        if self.name is not None:
            result['name'] = self.name
        if self.partition is not None:
            result['partition'] = self.partition
        result['versions'] = []
        if self.versions is not None:
            for k in self.versions:
                result['versions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('dataSource') is not None:
            self.data_source = m.get('dataSource')
        if m.get('dataSourceInfo') is not None:
            temp_model = ListIndexesResponseBodyResultDataSourceInfo()
            self.data_source_info = temp_model.from_map(m['dataSourceInfo'])
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('fullUpdateTime') is not None:
            self.full_update_time = m.get('fullUpdateTime')
        if m.get('fullVersion') is not None:
            self.full_version = m.get('fullVersion')
        if m.get('incUpdateTime') is not None:
            self.inc_update_time = m.get('incUpdateTime')
        if m.get('indexSize') is not None:
            self.index_size = m.get('indexSize')
        if m.get('indexStatus') is not None:
            self.index_status = m.get('indexStatus')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        self.versions = []
        if m.get('versions') is not None:
            for k in m.get('versions'):
                temp_model = ListIndexesResponseBodyResultVersions()
                self.versions.append(temp_model.from_map(k))
        return self


class ListIndexesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListIndexesResponseBodyResult] = None,
    ):
        # id of request
        self.request_id = request_id
        # The information about the indexes.
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListIndexesResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListIndexesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIndexesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIndexesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstanceSpecsRequest(TeaModel):
    def __init__(
        self,
        type: str = None,
    ):
        # The node type. Valid values: qrs, search, index, and cluster. qrs specifies an Query Result Searcher (QRS) worker, search specifies a searcher worker, index specifies an index node, and cluster specifies a cluster.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class ListInstanceSpecsResponseBodyResult(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        max_disk: int = None,
        mem: int = None,
        min_disk: int = None,
    ):
        # The number of CPU cores.
        self.cpu = cpu
        # The maximum storage space of a searcher worker.
        self.max_disk = max_disk
        # The memory size. Unit: GB.
        self.mem = mem
        # The minimum storage space of a searcher worker.
        self.min_disk = min_disk

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cpu is not None:
            result['cpu'] = self.cpu
        if self.max_disk is not None:
            result['maxDisk'] = self.max_disk
        if self.mem is not None:
            result['mem'] = self.mem
        if self.min_disk is not None:
            result['minDisk'] = self.min_disk
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('cpu') is not None:
            self.cpu = m.get('cpu')
        if m.get('maxDisk') is not None:
            self.max_disk = m.get('maxDisk')
        if m.get('mem') is not None:
            self.mem = m.get('mem')
        if m.get('minDisk') is not None:
            self.min_disk = m.get('minDisk')
        return self


class ListInstanceSpecsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListInstanceSpecsResponseBodyResult] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The specifications of the instances.
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListInstanceSpecsResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListInstanceSpecsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListInstanceSpecsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListInstanceSpecsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstancesRequestTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class ListInstancesRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        edition: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        resource_group_id: str = None,
        tags: List[ListInstancesRequestTags] = None,
    ):
        # The description of the instance
        self.description = description
        # 实例类型，vector(向量索引版)，engine(召回引擎版)
        self.edition = edition
        # The time when the instance was created
        self.instance_id = instance_id
        # The status of the instance
        self.page_number = page_number
        # The description of the instance. You can use this description to filter instances. Fuzzy match is supported.
        self.page_size = page_size
        # The number of the page to return. Default value: 1.
        self.resource_group_id = resource_group_id
        self.tags = tags

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['description'] = self.description
        if self.edition is not None:
            result['edition'] = self.edition
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.resource_group_id is not None:
            result['resourceGroupId'] = self.resource_group_id
        result['tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['tags'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('edition') is not None:
            self.edition = m.get('edition')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('resourceGroupId') is not None:
            self.resource_group_id = m.get('resourceGroupId')
        self.tags = []
        if m.get('tags') is not None:
            for k in m.get('tags'):
                temp_model = ListInstancesRequestTags()
                self.tags.append(temp_model.from_map(k))
        return self


class ListInstancesShrinkRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        edition: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        resource_group_id: str = None,
        tags_shrink: str = None,
    ):
        # The description of the instance
        self.description = description
        # 实例类型，vector(向量索引版)，engine(召回引擎版)
        self.edition = edition
        # The time when the instance was created
        self.instance_id = instance_id
        # The status of the instance
        self.page_number = page_number
        # The description of the instance. You can use this description to filter instances. Fuzzy match is supported.
        self.page_size = page_size
        # The number of the page to return. Default value: 1.
        self.resource_group_id = resource_group_id
        self.tags_shrink = tags_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['description'] = self.description
        if self.edition is not None:
            result['edition'] = self.edition
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.resource_group_id is not None:
            result['resourceGroupId'] = self.resource_group_id
        if self.tags_shrink is not None:
            result['tags'] = self.tags_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('edition') is not None:
            self.edition = m.get('edition')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('resourceGroupId') is not None:
            self.resource_group_id = m.get('resourceGroupId')
        if m.get('tags') is not None:
            self.tags_shrink = m.get('tags')
        return self


class ListInstancesResponseBodyResultNetwork(TeaModel):
    def __init__(
        self,
        endpoint: str = None,
        v_switch_id: str = None,
        vpc_id: str = None,
    ):
        # 353490
        self.endpoint = endpoint
        # ### Sample responses
        # 
        # **Sample success responses**\
        # 
        #     {
        #         "requestId": "90D6B8F5-FE97-4509-9AAB-367836C51818",
        #         "result": [
        #             {
        #                 "instanceId": "igraph-cn-xxxxxx1",
        #                 "spec": {
        #                     "password": "passwd",
        #                     "searchResource": {
        #                         "disk": 50,
        #                         "mem": 8,
        #                         "cpu": 2,
        #                         "nodeCount": 2
        #                     },
        #                     "instanceName": "testInstance",
        #                     "vSwitchId": "vswitch_id_xxx",
        #                     "vpcId": "vpc_id_xxx",
        #                     "qrsResource": {
        #                         "disk": 50,
        #                         "mem": 8,
        #                         "cpu": 2,
        #                         "nodeCount": 2
        #                     },
        #                     "region": "cn-hangzhou",
        #                     "userName": "user"
        #                 },
        #                 "status": {
        #                     "phase": "PENDING",
        #                     "instancePhase": "INIT",
        #                     "createSuccess": false
        #                 }
        #             },
        #             {
        #                 "instanceId": "igraph-cn-xxxxxx2",
        #                 "spec": {
        #                     "password": "passwd",
        #                     "searchResource": {
        #                         "disk": 50,
        #                         "mem": 8,
        #                         "cpu": 2,
        #                         "nodeCount": 2
        #                     },
        #                     "instanceName": "testInstance",
        #                     "vSwitchId": "vswitch_id_xxx",
        #                     "vpcId": "vpc_id_xxx",
        #                     "qrsResource": {
        #                         "disk": 50,
        #                         "mem": 8,
        #                         "cpu": 2,
        #                         "nodeCount": 2
        #                     },
        #                     "region": "cn-hangzhou",
        #                     "userName": "user"
        #                 },
        #                 "status": {
        #                     "phase": "PENDING",
        #                     "instancePhase": "INIT",
        #                     "createSuccess": false
        #                 }
        #             }
        #         ],
        #         "totalCount": 20
        #     }
        # 
        # **Sample error responses**\
        # 
        #     {
        #       "requestId": "BD1EA715-DF6F-06C2-004C-C1FA0D3A9820",
        #       "httpCode": 404,
        #       "code": "App.NotFound",
        #       "message": "App not found"
        #     }
        self.v_switch_id = v_switch_id
        # Queries instances.
        self.vpc_id = vpc_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.v_switch_id is not None:
            result['vSwitchId'] = self.v_switch_id
        if self.vpc_id is not None:
            result['vpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('vSwitchId') is not None:
            self.v_switch_id = m.get('vSwitchId')
        if m.get('vpcId') is not None:
            self.vpc_id = m.get('vpcId')
        return self


class ListInstancesResponseBodyResultTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class ListInstancesResponseBodyResult(TeaModel):
    def __init__(
        self,
        charge_type: str = None,
        commodity_code: str = None,
        create_time: str = None,
        description: str = None,
        expired_time: str = None,
        in_debt: bool = None,
        instance_id: str = None,
        lock_mode: str = None,
        network: ListInstancesResponseBodyResultNetwork = None,
        resource_group_id: str = None,
        status: str = None,
        tags: List[ListInstancesResponseBodyResultTags] = None,
        update_time: str = None,
    ):
        # The ID of the resource group to which the instance belongs.
        self.charge_type = charge_type
        # The total number of entries returned
        self.commodity_code = commodity_code
        # Havenask instance
        self.create_time = create_time
        # The ID of the virtual switch
        self.description = description
        # The ID of the Virtual Private Cloud (VPC) network
        self.expired_time = expired_time
        # The ID of the request
        self.in_debt = in_debt
        # The access point of the gateway
        self.instance_id = instance_id
        # Emergency test
        self.lock_mode = lock_mode
        # The lock status
        self.network = network
        # The number of entries to return on each page. Valid values: 1 to 50. Default value: 10.
        self.resource_group_id = resource_group_id
        # The expiration time
        self.status = status
        self.tags = tags
        # The time when the instance was last updated
        self.update_time = update_time

    def validate(self):
        if self.network:
            self.network.validate()
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.charge_type is not None:
            result['chargeType'] = self.charge_type
        if self.commodity_code is not None:
            result['commodityCode'] = self.commodity_code
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.expired_time is not None:
            result['expiredTime'] = self.expired_time
        if self.in_debt is not None:
            result['inDebt'] = self.in_debt
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.lock_mode is not None:
            result['lockMode'] = self.lock_mode
        if self.network is not None:
            result['network'] = self.network.to_map()
        if self.resource_group_id is not None:
            result['resourceGroupId'] = self.resource_group_id
        if self.status is not None:
            result['status'] = self.status
        result['tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['tags'].append(k.to_map() if k else None)
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('chargeType') is not None:
            self.charge_type = m.get('chargeType')
        if m.get('commodityCode') is not None:
            self.commodity_code = m.get('commodityCode')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('expiredTime') is not None:
            self.expired_time = m.get('expiredTime')
        if m.get('inDebt') is not None:
            self.in_debt = m.get('inDebt')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('lockMode') is not None:
            self.lock_mode = m.get('lockMode')
        if m.get('network') is not None:
            temp_model = ListInstancesResponseBodyResultNetwork()
            self.network = temp_model.from_map(m['network'])
        if m.get('resourceGroupId') is not None:
            self.resource_group_id = m.get('resourceGroupId')
        if m.get('status') is not None:
            self.status = m.get('status')
        self.tags = []
        if m.get('tags') is not None:
            for k in m.get('tags'):
                temp_model = ListInstancesResponseBodyResultTags()
                self.tags.append(temp_model.from_map(k))
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class ListInstancesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListInstancesResponseBodyResult] = None,
        total_count: int = None,
    ):
        self.request_id = request_id
        # The result returned
        self.result = result
        self.total_count = total_count

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListInstancesResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListInstancesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListOnlineConfigsRequest(TeaModel):
    def __init__(
        self,
        domain: str = None,
    ):
        self.domain = domain

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.domain is not None:
            result['domain'] = self.domain
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        return self


class ListOnlineConfigsResponseBodyResult(TeaModel):
    def __init__(
        self,
        config: str = None,
        index_name: str = None,
    ):
        self.config = config
        self.index_name = index_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config is not None:
            result['config'] = self.config
        if self.index_name is not None:
            result['indexName'] = self.index_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('config') is not None:
            self.config = m.get('config')
        if m.get('indexName') is not None:
            self.index_name = m.get('indexName')
        return self


class ListOnlineConfigsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: List[ListOnlineConfigsResponseBodyResult] = None,
    ):
        # id of request
        self.request_id = request_id
        # List
        self.result = result

    def validate(self):
        if self.result:
            for k in self.result:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['result'] = []
        if self.result is not None:
            for k in self.result:
                result['result'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.result = []
        if m.get('result') is not None:
            for k in m.get('result'):
                temp_model = ListOnlineConfigsResponseBodyResult()
                self.result.append(temp_model.from_map(k))
        return self


class ListOnlineConfigsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListOnlineConfigsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListOnlineConfigsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListQueryResultRequest(TeaModel):
    def __init__(
        self,
        query: str = None,
        sql: str = None,
    ):
        # 353490
        self.query = query
        self.sql = sql

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.query is not None:
            result['query'] = self.query
        if self.sql is not None:
            result['sql'] = self.sql
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('query') is not None:
            self.query = m.get('query')
        if m.get('sql') is not None:
            self.sql = m.get('sql')
        return self


class ListQueryResultResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListQueryResultResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListQueryResultResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListQueryResultResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyAdvanceConfigFileRequest(TeaModel):
    def __init__(
        self,
        content: str = None,
        variables: Dict[str, VariablesValue] = None,
        file_name: str = None,
    ):
        # The content of the file.
        self.content = content
        # The variable.
        self.variables = variables
        # The name of the file.
        self.file_name = file_name

    def validate(self):
        if self.variables:
            for v in self.variables.values():
                if v:
                    v.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        result['variables'] = {}
        if self.variables is not None:
            for k, v in self.variables.items():
                result['variables'][k] = v.to_map()
        if self.file_name is not None:
            result['fileName'] = self.file_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        self.variables = {}
        if m.get('variables') is not None:
            for k, v in m.get('variables').items():
                temp_model = VariablesValue()
                self.variables[k] = temp_model.from_map(v)
        if m.get('fileName') is not None:
            self.file_name = m.get('fileName')
        return self


class ModifyAdvanceConfigFileResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # The result.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyAdvanceConfigFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyAdvanceConfigFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyAdvanceConfigFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyClusterDescRequest(TeaModel):
    def __init__(
        self,
        body: Dict[str, Any] = None,
    ):
        # The parameters in the request body
        self.body = body

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body is not None:
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class ModifyClusterDescResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request
        self.request_id = request_id
        # Map
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyClusterDescResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyClusterDescResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyClusterDescResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyClusterOfflineConfigRequest(TeaModel):
    def __init__(
        self,
        build_mode: str = None,
        config: Dict[str, int] = None,
        data_source_name: str = None,
        data_source_type: str = None,
        data_time_sec: int = None,
        domain: str = None,
        generation: int = None,
        partition: str = None,
        push_mode: str = None,
    ):
        # The reindexing method. Valid values: api: API data source. indexRecover: data recovery through indexing.
        self.build_mode = build_mode
        # The configuration name, which is stored as a key.
        self.config = config
        self.data_source_name = data_source_name
        # The type of the data source. Valid values: odps: MaxCompute. swift: Swift. unKnow: unknown type.
        self.data_source_type = data_source_type
        # This parameter is required if the API data source experiences full indexing.
        self.data_time_sec = data_time_sec
        # The domain in which the data source is deployed.
        self.domain = domain
        # The ID of the backward data delivery.
        self.generation = generation
        # This parameter is required if the MaxCompute data source experiences full indexing.
        self.partition = partition
        self.push_mode = push_mode

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.build_mode is not None:
            result['buildMode'] = self.build_mode
        if self.config is not None:
            result['config'] = self.config
        if self.data_source_name is not None:
            result['dataSourceName'] = self.data_source_name
        if self.data_source_type is not None:
            result['dataSourceType'] = self.data_source_type
        if self.data_time_sec is not None:
            result['dataTimeSec'] = self.data_time_sec
        if self.domain is not None:
            result['domain'] = self.domain
        if self.generation is not None:
            result['generation'] = self.generation
        if self.partition is not None:
            result['partition'] = self.partition
        if self.push_mode is not None:
            result['pushMode'] = self.push_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('buildMode') is not None:
            self.build_mode = m.get('buildMode')
        if m.get('config') is not None:
            self.config = m.get('config')
        if m.get('dataSourceName') is not None:
            self.data_source_name = m.get('dataSourceName')
        if m.get('dataSourceType') is not None:
            self.data_source_type = m.get('dataSourceType')
        if m.get('dataTimeSec') is not None:
            self.data_time_sec = m.get('dataTimeSec')
        if m.get('domain') is not None:
            self.domain = m.get('domain')
        if m.get('generation') is not None:
            self.generation = m.get('generation')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('pushMode') is not None:
            self.push_mode = m.get('pushMode')
        return self


class ModifyClusterOfflineConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The result of the request.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyClusterOfflineConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyClusterOfflineConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyClusterOfflineConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyClusterOnlineConfigRequest(TeaModel):
    def __init__(
        self,
        clusters: List[str] = None,
        config: Dict[str, int] = None,
    ):
        # The information about the cluster
        self.clusters = clusters
        # 配置信息
        self.config = config

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.clusters is not None:
            result['clusters'] = self.clusters
        if self.config is not None:
            result['config'] = self.config
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clusters') is not None:
            self.clusters = m.get('clusters')
        if m.get('config') is not None:
            self.config = m.get('config')
        return self


class ModifyClusterOnlineConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request
        self.request_id = request_id
        # Map
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyClusterOnlineConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyClusterOnlineConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyClusterOnlineConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyDataSourceRequest(TeaModel):
    def __init__(
        self,
        body: Dict[str, Any] = None,
        dry_run: bool = None,
    ):
        # The information about the index
        self.body = body
        # The ID of the request
        self.dry_run = dry_run

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body is not None:
            result['body'] = self.body
        if self.dry_run is not None:
            result['dryRun'] = self.dry_run
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('body') is not None:
            self.body = m.get('body')
        if m.get('dryRun') is not None:
            self.dry_run = m.get('dryRun')
        return self


class ModifyDataSourceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # The schema information.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyDataSourceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyDataSourceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyDataSourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyFileRequest(TeaModel):
    def __init__(
        self,
        content: str = None,
        partition: int = None,
        file_name: str = None,
    ):
        # The parameters in the request body
        self.content = content
        # auditing
        self.partition = partition
        # ha-cn-tl32m2c4u01@ha-cn-tl32m2c4u01_00@bj_vpc_domain_1@automobile_vector@index_config_edit
        self.file_name = file_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.partition is not None:
            result['partition'] = self.partition
        if self.file_name is not None:
            result['fileName'] = self.file_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('partition') is not None:
            self.partition = m.get('partition')
        if m.get('fileName') is not None:
            self.file_name = m.get('fileName')
        return self


class ModifyFileResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # The information about the index
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyFileResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyIndexPartitionRequestIndexInfos(TeaModel):
    def __init__(
        self,
        index_name: str = None,
        parallel_num: int = None,
        partition_count: int = None,
    ):
        # auditing
        self.index_name = index_name
        # The parameters in the request body.
        self.parallel_num = parallel_num
        # The number of shards of the index.
        self.partition_count = partition_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.index_name is not None:
            result['indexName'] = self.index_name
        if self.parallel_num is not None:
            result['parallelNum'] = self.parallel_num
        if self.partition_count is not None:
            result['partitionCount'] = self.partition_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('indexName') is not None:
            self.index_name = m.get('indexName')
        if m.get('parallelNum') is not None:
            self.parallel_num = m.get('parallelNum')
        if m.get('partitionCount') is not None:
            self.partition_count = m.get('partitionCount')
        return self


class ModifyIndexPartitionRequest(TeaModel):
    def __init__(
        self,
        data_source_name: str = None,
        domain_name: str = None,
        generation: int = None,
        index_infos: List[ModifyIndexPartitionRequestIndexInfos] = None,
    ):
        # The name of the data source.
        self.data_source_name = data_source_name
        # The information about each index.
        self.domain_name = domain_name
        # The name of the data center.
        self.generation = generation
        # The number of shards of the index.
        self.index_infos = index_infos

    def validate(self):
        if self.index_infos:
            for k in self.index_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_name is not None:
            result['dataSourceName'] = self.data_source_name
        if self.domain_name is not None:
            result['domainName'] = self.domain_name
        if self.generation is not None:
            result['generation'] = self.generation
        result['indexInfos'] = []
        if self.index_infos is not None:
            for k in self.index_infos:
                result['indexInfos'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dataSourceName') is not None:
            self.data_source_name = m.get('dataSourceName')
        if m.get('domainName') is not None:
            self.domain_name = m.get('domainName')
        if m.get('generation') is not None:
            self.generation = m.get('generation')
        self.index_infos = []
        if m.get('indexInfos') is not None:
            for k in m.get('indexInfos'):
                temp_model = ModifyIndexPartitionRequestIndexInfos()
                self.index_infos.append(temp_model.from_map(k))
        return self


class ModifyIndexPartitionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # Map
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyIndexPartitionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyIndexPartitionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyIndexPartitionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyIndexVersionRequestBody(TeaModel):
    def __init__(
        self,
        build_deploy_id: str = None,
        index_name: str = None,
        version: str = None,
    ):
        # The ID of the index deployed in offline mode.
        self.build_deploy_id = build_deploy_id
        # The name of the index.
        self.index_name = index_name
        # The version of the index.
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.build_deploy_id is not None:
            result['buildDeployId'] = self.build_deploy_id
        if self.index_name is not None:
            result['indexName'] = self.index_name
        if self.version is not None:
            result['version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('buildDeployId') is not None:
            self.build_deploy_id = m.get('buildDeployId')
        if m.get('indexName') is not None:
            self.index_name = m.get('indexName')
        if m.get('version') is not None:
            self.version = m.get('version')
        return self


class ModifyIndexVersionRequest(TeaModel):
    def __init__(
        self,
        body: List[ModifyIndexVersionRequestBody] = None,
    ):
        # The keyword used to search for a version. Fuzzy match is supported.
        self.body = body

    def validate(self):
        if self.body:
            for k in self.body:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['body'] = []
        if self.body is not None:
            for k in self.body:
                result['body'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.body = []
        if m.get('body') is not None:
            for k in m.get('body'):
                temp_model = ModifyIndexVersionRequestBody()
                self.body.append(temp_model.from_map(k))
        return self


class ModifyIndexVersionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # result
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyIndexVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyIndexVersionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyIndexVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyNodeConfigRequest(TeaModel):
    def __init__(
        self,
        active: bool = None,
        data_duplicate_number: int = None,
        data_fragment_number: int = None,
        min_service_percent: int = None,
        published: bool = None,
        cluster_name: str = None,
        data_source_name: str = None,
        name: str = None,
        type: str = None,
    ):
        self.active = active
        self.data_duplicate_number = data_duplicate_number
        self.data_fragment_number = data_fragment_number
        self.min_service_percent = min_service_percent
        self.published = published
        # The ID of the cluster.
        self.cluster_name = cluster_name
        # The parameters in the request body.
        self.data_source_name = data_source_name
        # The name of the cluster.
        self.name = name
        # The original name of the node.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.active is not None:
            result['active'] = self.active
        if self.data_duplicate_number is not None:
            result['dataDuplicateNumber'] = self.data_duplicate_number
        if self.data_fragment_number is not None:
            result['dataFragmentNumber'] = self.data_fragment_number
        if self.min_service_percent is not None:
            result['minServicePercent'] = self.min_service_percent
        if self.published is not None:
            result['published'] = self.published
        if self.cluster_name is not None:
            result['clusterName'] = self.cluster_name
        if self.data_source_name is not None:
            result['dataSourceName'] = self.data_source_name
        if self.name is not None:
            result['name'] = self.name
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('active') is not None:
            self.active = m.get('active')
        if m.get('dataDuplicateNumber') is not None:
            self.data_duplicate_number = m.get('dataDuplicateNumber')
        if m.get('dataFragmentNumber') is not None:
            self.data_fragment_number = m.get('dataFragmentNumber')
        if m.get('minServicePercent') is not None:
            self.min_service_percent = m.get('minServicePercent')
        if m.get('published') is not None:
            self.published = m.get('published')
        if m.get('clusterName') is not None:
            self.cluster_name = m.get('clusterName')
        if m.get('dataSourceName') is not None:
            self.data_source_name = m.get('dataSourceName')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class ModifyNodeConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # auditing
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyNodeConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyNodeConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyNodeConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyOnlineConfigRequest(TeaModel):
    def __init__(
        self,
        body: Dict[str, str] = None,
    ):
        # ashortdescriptionofstruct
        self.body = body

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body is not None:
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class ModifyOnlineConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # Map
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyOnlineConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyOnlineConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyOnlineConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyPasswordRequest(TeaModel):
    def __init__(
        self,
        password: str = None,
        username: str = None,
    ):
        # The password
        self.password = password
        # The username
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.password is not None:
            result['password'] = self.password
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('password') is not None:
            self.password = m.get('password')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class ModifyPasswordResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request
        self.request_id = request_id
        # The result
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class ModifyPasswordResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ModifyPasswordResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ModifyPasswordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PublishAdvanceConfigRequest(TeaModel):
    def __init__(
        self,
        body: Dict[str, Any] = None,
    ):
        # The structure of the request
        self.body = body

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body is not None:
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class PublishAdvanceConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # The ID of the request
        self.request_id = request_id
        # The result returned
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class PublishAdvanceConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PublishAdvanceConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PublishAdvanceConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PublishIndexVersionRequest(TeaModel):
    def __init__(
        self,
        body: Dict[str, Any] = None,
    ):
        self.body = body

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body is not None:
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class PublishIndexVersionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class PublishIndexVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PublishIndexVersionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PublishIndexVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RecoverIndexRequest(TeaModel):
    def __init__(
        self,
        build_deploy_id: int = None,
        data_source_name: str = None,
        generation: str = None,
        index_name: str = None,
    ):
        # buildDeployId
        self.build_deploy_id = build_deploy_id
        # The name of the data source
        self.data_source_name = data_source_name
        # generation
        self.generation = generation
        # The name of the index
        self.index_name = index_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.build_deploy_id is not None:
            result['buildDeployId'] = self.build_deploy_id
        if self.data_source_name is not None:
            result['dataSourceName'] = self.data_source_name
        if self.generation is not None:
            result['generation'] = self.generation
        if self.index_name is not None:
            result['indexName'] = self.index_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('buildDeployId') is not None:
            self.build_deploy_id = m.get('buildDeployId')
        if m.get('dataSourceName') is not None:
            self.data_source_name = m.get('dataSourceName')
        if m.get('generation') is not None:
            self.generation = m.get('generation')
        if m.get('indexName') is not None:
            self.index_name = m.get('indexName')
        return self


class RecoverIndexResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # Map
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class RecoverIndexResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RecoverIndexResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RecoverIndexResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveClusterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class RemoveClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RemoveClusterResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RemoveClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: Dict[str, Any] = None,
    ):
        # id of request
        self.request_id = request_id
        # The information about the index
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            self.result = m.get('result')
        return self


class StopTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StopTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StopTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateInstanceRequestComponents(TeaModel):
    def __init__(
        self,
        code: str = None,
        value: str = None,
    ):
        # The name of the specification. The value must be the same as the name of a parameter on the buy page.
        self.code = code
        # The value of the specification.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['code'] = self.code
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('code') is not None:
            self.code = m.get('code')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class UpdateInstanceRequest(TeaModel):
    def __init__(
        self,
        components: List[UpdateInstanceRequestComponents] = None,
        description: str = None,
        order_type: str = None,
    ):
        # The information about the instance type.
        self.components = components
        # The description of the instance.
        self.description = description
        # The type of the order. Valid values: UPGRADE and DOWNGRADE. UPGRADE indicates the instance type is to be upgraded. DOWNGRADE indicates the instance type is to be downgraded.
        self.order_type = order_type

    def validate(self):
        if self.components:
            for k in self.components:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['components'] = []
        if self.components is not None:
            for k in self.components:
                result['components'].append(k.to_map() if k else None)
        if self.description is not None:
            result['description'] = self.description
        if self.order_type is not None:
            result['orderType'] = self.order_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.components = []
        if m.get('components') is not None:
            for k in m.get('components'):
                temp_model = UpdateInstanceRequestComponents()
                self.components.append(temp_model.from_map(k))
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('orderType') is not None:
            self.order_type = m.get('orderType')
        return self


class UpdateInstanceResponseBodyResult(TeaModel):
    def __init__(
        self,
        charge_type: str = None,
        commodity_code: str = None,
        create_time: str = None,
        description: str = None,
        expired_time: str = None,
        in_debt: bool = None,
        instance_id: str = None,
        lock_mode: str = None,
        resource_group_id: str = None,
        status: str = None,
        update_time: str = None,
    ):
        # The billing method of the instance.
        self.charge_type = charge_type
        # The service code.
        self.commodity_code = commodity_code
        # The time when the instance was created.
        self.create_time = create_time
        # The description of the instance.
        self.description = description
        # The time when the instance expires.
        self.expired_time = expired_time
        # Indicates whether an overdue payment is involved.
        self.in_debt = in_debt
        # The ID of the instance.
        self.instance_id = instance_id
        # The lock mode of the instance.
        self.lock_mode = lock_mode
        # The ID of the resource group.
        self.resource_group_id = resource_group_id
        # The state of the instance.
        self.status = status
        # The time when the instance was last updated.
        self.update_time = update_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.charge_type is not None:
            result['chargeType'] = self.charge_type
        if self.commodity_code is not None:
            result['commodityCode'] = self.commodity_code
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.expired_time is not None:
            result['expiredTime'] = self.expired_time
        if self.in_debt is not None:
            result['inDebt'] = self.in_debt
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.lock_mode is not None:
            result['lockMode'] = self.lock_mode
        if self.resource_group_id is not None:
            result['resourceGroupId'] = self.resource_group_id
        if self.status is not None:
            result['status'] = self.status
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('chargeType') is not None:
            self.charge_type = m.get('chargeType')
        if m.get('commodityCode') is not None:
            self.commodity_code = m.get('commodityCode')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('expiredTime') is not None:
            self.expired_time = m.get('expiredTime')
        if m.get('inDebt') is not None:
            self.in_debt = m.get('inDebt')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('lockMode') is not None:
            self.lock_mode = m.get('lockMode')
        if m.get('resourceGroupId') is not None:
            self.resource_group_id = m.get('resourceGroupId')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class UpdateInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: UpdateInstanceResponseBodyResult = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The result returned.
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.result is not None:
            result['result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('result') is not None:
            temp_model = UpdateInstanceResponseBodyResult()
            self.result = temp_model.from_map(m['result'])
        return self


class UpdateInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateInstanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


