# coding: utf-8

from __future__ import absolute_import

import importlib
import warnings

from ctcloudsdkcore.client import Client, ClientBuilder
from ctcloudsdkcore.utils import http_utils
from ctcloudsdkcore.sdk_stream_request import SdkStreamRequest
try:
    from ctcloudsdkcore.invoker.invoker import SyncInvoker
except ImportError as e:
    warnings.warn(str(e) + ", please check if you are using the same versions of 'ctcloudsdkcore' and 'ctcloudsdkecs'")


class EcsClient(Client):
    def __init__(self):
        super(EcsClient, self).__init__()
        self.model_package = importlib.import_module("ctcloudsdkecs.v2.model")

    @classmethod
    def new_builder(cls, clazz=None):
        if not clazz:
            client_builder = ClientBuilder(cls)
        else:
            if clazz.__name__ != "EcsClient":
                raise TypeError("client type error, support client type is EcsClient")
            client_builder = ClientBuilder(clazz)

        

        return client_builder

    def add_server_group_member(self, request):
        """
        :param request: Request instance for AddServerGroupMember
        :type request: :class:`ctcloudsdkecs.v2.AddServerGroupMemberRequest`
        :rtype: :class:`ctcloudsdkecs.v2.AddServerGroupMemberResponse`
        """
        http_info = self._add_server_group_member_http_info(request)
        return self._call_api(**http_info)

    def add_server_group_member_invoker(self, request):
        http_info = self._add_server_group_member_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _add_server_group_member_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/os-server-groups/{server_group_id}/action",
            "request_type": request.__class__.__name__,
            "response_type": "AddServerGroupMemberResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_group_id' in local_var_params:
            path_params['server_group_id'] = local_var_params['server_group_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def associate_server_virtual_ip(self, request):
        """
        :param request: Request instance for AssociateServerVirtualIp
        :type request: :class:`ctcloudsdkecs.v2.AssociateServerVirtualIpRequest`
        :rtype: :class:`ctcloudsdkecs.v2.AssociateServerVirtualIpResponse`
        """
        http_info = self._associate_server_virtual_ip_http_info(request)
        return self._call_api(**http_info)

    def associate_server_virtual_ip_invoker(self, request):
        http_info = self._associate_server_virtual_ip_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _associate_server_virtual_ip_http_info(cls, request):
        http_info = {
            "method": "PUT",
            "resource_path": "/v1/{project_id}/cloudservers/nics/{nic_id}",
            "request_type": request.__class__.__name__,
            "response_type": "AssociateServerVirtualIpResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'nic_id' in local_var_params:
            path_params['nic_id'] = local_var_params['nic_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def attach_server_volume(self, request):
        """
        :param request: Request instance for AttachServerVolume
        :type request: :class:`ctcloudsdkecs.v2.AttachServerVolumeRequest`
        :rtype: :class:`ctcloudsdkecs.v2.AttachServerVolumeResponse`
        """
        http_info = self._attach_server_volume_http_info(request)
        return self._call_api(**http_info)

    def attach_server_volume_invoker(self, request):
        http_info = self._attach_server_volume_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _attach_server_volume_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/attachvolume",
            "request_type": request.__class__.__name__,
            "response_type": "AttachServerVolumeResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_add_server_nics(self, request):
        """
        :param request: Request instance for BatchAddServerNics
        :type request: :class:`ctcloudsdkecs.v2.BatchAddServerNicsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchAddServerNicsResponse`
        """
        http_info = self._batch_add_server_nics_http_info(request)
        return self._call_api(**http_info)

    def batch_add_server_nics_invoker(self, request):
        http_info = self._batch_add_server_nics_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_add_server_nics_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/nics",
            "request_type": request.__class__.__name__,
            "response_type": "BatchAddServerNicsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_attach_sharable_volumes(self, request):
        """
        :param request: Request instance for BatchAttachSharableVolumes
        :type request: :class:`ctcloudsdkecs.v2.BatchAttachSharableVolumesRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchAttachSharableVolumesResponse`
        """
        http_info = self._batch_attach_sharable_volumes_http_info(request)
        return self._call_api(**http_info)

    def batch_attach_sharable_volumes_invoker(self, request):
        http_info = self._batch_attach_sharable_volumes_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_attach_sharable_volumes_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/batchaction/attachvolumes/{volume_id}",
            "request_type": request.__class__.__name__,
            "response_type": "BatchAttachSharableVolumesResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'volume_id' in local_var_params:
            path_params['volume_id'] = local_var_params['volume_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_create_server_tags(self, request):
        """
        :param request: Request instance for BatchCreateServerTags
        :type request: :class:`ctcloudsdkecs.v2.BatchCreateServerTagsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchCreateServerTagsResponse`
        """
        http_info = self._batch_create_server_tags_http_info(request)
        return self._call_api(**http_info)

    def batch_create_server_tags_invoker(self, request):
        http_info = self._batch_create_server_tags_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_create_server_tags_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/tags/action",
            "request_type": request.__class__.__name__,
            "response_type": "BatchCreateServerTagsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_delete_server_nics(self, request):
        """
        :param request: Request instance for BatchDeleteServerNics
        :type request: :class:`ctcloudsdkecs.v2.BatchDeleteServerNicsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchDeleteServerNicsResponse`
        """
        http_info = self._batch_delete_server_nics_http_info(request)
        return self._call_api(**http_info)

    def batch_delete_server_nics_invoker(self, request):
        http_info = self._batch_delete_server_nics_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_delete_server_nics_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/nics/delete",
            "request_type": request.__class__.__name__,
            "response_type": "BatchDeleteServerNicsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_delete_server_tags(self, request):
        """
        :param request: Request instance for BatchDeleteServerTags
        :type request: :class:`ctcloudsdkecs.v2.BatchDeleteServerTagsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchDeleteServerTagsResponse`
        """
        http_info = self._batch_delete_server_tags_http_info(request)
        return self._call_api(**http_info)

    def batch_delete_server_tags_invoker(self, request):
        http_info = self._batch_delete_server_tags_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_delete_server_tags_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/tags/action",
            "request_type": request.__class__.__name__,
            "response_type": "BatchDeleteServerTagsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_reboot_servers(self, request):
        """
        :param request: Request instance for BatchRebootServers
        :type request: :class:`ctcloudsdkecs.v2.BatchRebootServersRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchRebootServersResponse`
        """
        http_info = self._batch_reboot_servers_http_info(request)
        return self._call_api(**http_info)

    def batch_reboot_servers_invoker(self, request):
        http_info = self._batch_reboot_servers_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_reboot_servers_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/action",
            "request_type": request.__class__.__name__,
            "response_type": "BatchRebootServersResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_reset_servers_password(self, request):
        """
        :param request: Request instance for BatchResetServersPassword
        :type request: :class:`ctcloudsdkecs.v2.BatchResetServersPasswordRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchResetServersPasswordResponse`
        """
        http_info = self._batch_reset_servers_password_http_info(request)
        return self._call_api(**http_info)

    def batch_reset_servers_password_invoker(self, request):
        http_info = self._batch_reset_servers_password_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_reset_servers_password_http_info(cls, request):
        http_info = {
            "method": "PUT",
            "resource_path": "/v1/{project_id}/cloudservers/os-reset-passwords",
            "request_type": request.__class__.__name__,
            "response_type": "BatchResetServersPasswordResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_start_servers(self, request):
        """
        :param request: Request instance for BatchStartServers
        :type request: :class:`ctcloudsdkecs.v2.BatchStartServersRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchStartServersResponse`
        """
        http_info = self._batch_start_servers_http_info(request)
        return self._call_api(**http_info)

    def batch_start_servers_invoker(self, request):
        http_info = self._batch_start_servers_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_start_servers_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/action",
            "request_type": request.__class__.__name__,
            "response_type": "BatchStartServersResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_stop_servers(self, request):
        """
        :param request: Request instance for BatchStopServers
        :type request: :class:`ctcloudsdkecs.v2.BatchStopServersRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchStopServersResponse`
        """
        http_info = self._batch_stop_servers_http_info(request)
        return self._call_api(**http_info)

    def batch_stop_servers_invoker(self, request):
        http_info = self._batch_stop_servers_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_stop_servers_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/action",
            "request_type": request.__class__.__name__,
            "response_type": "BatchStopServersResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def batch_update_servers_name(self, request):
        """
        :param request: Request instance for BatchUpdateServersName
        :type request: :class:`ctcloudsdkecs.v2.BatchUpdateServersNameRequest`
        :rtype: :class:`ctcloudsdkecs.v2.BatchUpdateServersNameResponse`
        """
        http_info = self._batch_update_servers_name_http_info(request)
        return self._call_api(**http_info)

    def batch_update_servers_name_invoker(self, request):
        http_info = self._batch_update_servers_name_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _batch_update_servers_name_http_info(cls, request):
        http_info = {
            "method": "PUT",
            "resource_path": "/v1/{project_id}/cloudservers/server-name",
            "request_type": request.__class__.__name__,
            "response_type": "BatchUpdateServersNameResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def change_server_os_with_cloud_init(self, request):
        """
        :param request: Request instance for ChangeServerOsWithCloudInit
        :type request: :class:`ctcloudsdkecs.v2.ChangeServerOsWithCloudInitRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ChangeServerOsWithCloudInitResponse`
        """
        http_info = self._change_server_os_with_cloud_init_http_info(request)
        return self._call_api(**http_info)

    def change_server_os_with_cloud_init_invoker(self, request):
        http_info = self._change_server_os_with_cloud_init_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _change_server_os_with_cloud_init_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v2/{project_id}/cloudservers/{server_id}/changeos",
            "request_type": request.__class__.__name__,
            "response_type": "ChangeServerOsWithCloudInitResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def change_server_os_without_cloud_init(self, request):
        """
        :param request: Request instance for ChangeServerOsWithoutCloudInit
        :type request: :class:`ctcloudsdkecs.v2.ChangeServerOsWithoutCloudInitRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ChangeServerOsWithoutCloudInitResponse`
        """
        http_info = self._change_server_os_without_cloud_init_http_info(request)
        return self._call_api(**http_info)

    def change_server_os_without_cloud_init_invoker(self, request):
        http_info = self._change_server_os_without_cloud_init_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _change_server_os_without_cloud_init_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/changeos",
            "request_type": request.__class__.__name__,
            "response_type": "ChangeServerOsWithoutCloudInitResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def create_post_paid_servers(self, request):
        """
        :param request: Request instance for CreatePostPaidServers
        :type request: :class:`ctcloudsdkecs.v2.CreatePostPaidServersRequest`
        :rtype: :class:`ctcloudsdkecs.v2.CreatePostPaidServersResponse`
        """
        http_info = self._create_post_paid_servers_http_info(request)
        return self._call_api(**http_info)

    def create_post_paid_servers_invoker(self, request):
        http_info = self._create_post_paid_servers_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _create_post_paid_servers_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers",
            "request_type": request.__class__.__name__,
            "response_type": "CreatePostPaidServersResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def create_server_group(self, request):
        """
        :param request: Request instance for CreateServerGroup
        :type request: :class:`ctcloudsdkecs.v2.CreateServerGroupRequest`
        :rtype: :class:`ctcloudsdkecs.v2.CreateServerGroupResponse`
        """
        http_info = self._create_server_group_http_info(request)
        return self._call_api(**http_info)

    def create_server_group_invoker(self, request):
        http_info = self._create_server_group_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _create_server_group_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/os-server-groups",
            "request_type": request.__class__.__name__,
            "response_type": "CreateServerGroupResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def create_servers(self, request):
        """
        :param request: Request instance for CreateServers
        :type request: :class:`ctcloudsdkecs.v2.CreateServersRequest`
        :rtype: :class:`ctcloudsdkecs.v2.CreateServersResponse`
        """
        http_info = self._create_servers_http_info(request)
        return self._call_api(**http_info)

    def create_servers_invoker(self, request):
        http_info = self._create_servers_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _create_servers_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.1/{project_id}/cloudservers",
            "request_type": request.__class__.__name__,
            "response_type": "CreateServersResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def delete_server_group(self, request):
        """
        :param request: Request instance for DeleteServerGroup
        :type request: :class:`ctcloudsdkecs.v2.DeleteServerGroupRequest`
        :rtype: :class:`ctcloudsdkecs.v2.DeleteServerGroupResponse`
        """
        http_info = self._delete_server_group_http_info(request)
        return self._call_api(**http_info)

    def delete_server_group_invoker(self, request):
        http_info = self._delete_server_group_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _delete_server_group_http_info(cls, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v1/{project_id}/cloudservers/os-server-groups/{server_group_id}",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteServerGroupResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_group_id' in local_var_params:
            path_params['server_group_id'] = local_var_params['server_group_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def delete_server_group_member(self, request):
        """
        :param request: Request instance for DeleteServerGroupMember
        :type request: :class:`ctcloudsdkecs.v2.DeleteServerGroupMemberRequest`
        :rtype: :class:`ctcloudsdkecs.v2.DeleteServerGroupMemberResponse`
        """
        http_info = self._delete_server_group_member_http_info(request)
        return self._call_api(**http_info)

    def delete_server_group_member_invoker(self, request):
        http_info = self._delete_server_group_member_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _delete_server_group_member_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/os-server-groups/{server_group_id}/action",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteServerGroupMemberResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_group_id' in local_var_params:
            path_params['server_group_id'] = local_var_params['server_group_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def delete_server_metadata(self, request):
        """
        :param request: Request instance for DeleteServerMetadata
        :type request: :class:`ctcloudsdkecs.v2.DeleteServerMetadataRequest`
        :rtype: :class:`ctcloudsdkecs.v2.DeleteServerMetadataResponse`
        """
        http_info = self._delete_server_metadata_http_info(request)
        return self._call_api(**http_info)

    def delete_server_metadata_invoker(self, request):
        http_info = self._delete_server_metadata_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _delete_server_metadata_http_info(cls, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/metadata/{key}",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteServerMetadataResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'key' in local_var_params:
            path_params['key'] = local_var_params['key']
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def delete_server_password(self, request):
        """
        :param request: Request instance for DeleteServerPassword
        :type request: :class:`ctcloudsdkecs.v2.DeleteServerPasswordRequest`
        :rtype: :class:`ctcloudsdkecs.v2.DeleteServerPasswordResponse`
        """
        http_info = self._delete_server_password_http_info(request)
        return self._call_api(**http_info)

    def delete_server_password_invoker(self, request):
        http_info = self._delete_server_password_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _delete_server_password_http_info(cls, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/os-server-password",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteServerPasswordResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def delete_servers(self, request):
        """
        :param request: Request instance for DeleteServers
        :type request: :class:`ctcloudsdkecs.v2.DeleteServersRequest`
        :rtype: :class:`ctcloudsdkecs.v2.DeleteServersResponse`
        """
        http_info = self._delete_servers_http_info(request)
        return self._call_api(**http_info)

    def delete_servers_invoker(self, request):
        http_info = self._delete_servers_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _delete_servers_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/delete",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteServersResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def detach_server_volume(self, request):
        """
        :param request: Request instance for DetachServerVolume
        :type request: :class:`ctcloudsdkecs.v2.DetachServerVolumeRequest`
        :rtype: :class:`ctcloudsdkecs.v2.DetachServerVolumeResponse`
        """
        http_info = self._detach_server_volume_http_info(request)
        return self._call_api(**http_info)

    def detach_server_volume_invoker(self, request):
        http_info = self._detach_server_volume_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _detach_server_volume_http_info(cls, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/detachvolume/{volume_id}",
            "request_type": request.__class__.__name__,
            "response_type": "DetachServerVolumeResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']
        if 'volume_id' in local_var_params:
            path_params['volume_id'] = local_var_params['volume_id']

        query_params = []
        if 'delete_flag' in local_var_params:
            query_params.append(('delete_flag', local_var_params['delete_flag']))

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def disassociate_server_virtual_ip(self, request):
        """
        :param request: Request instance for DisassociateServerVirtualIp
        :type request: :class:`ctcloudsdkecs.v2.DisassociateServerVirtualIpRequest`
        :rtype: :class:`ctcloudsdkecs.v2.DisassociateServerVirtualIpResponse`
        """
        http_info = self._disassociate_server_virtual_ip_http_info(request)
        return self._call_api(**http_info)

    def disassociate_server_virtual_ip_invoker(self, request):
        http_info = self._disassociate_server_virtual_ip_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _disassociate_server_virtual_ip_http_info(cls, request):
        http_info = {
            "method": "PUT",
            "resource_path": "/v1/{project_id}/cloudservers/nics/{nic_id}",
            "request_type": request.__class__.__name__,
            "response_type": "DisassociateServerVirtualIpResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'nic_id' in local_var_params:
            path_params['nic_id'] = local_var_params['nic_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def list_flavors(self, request):
        """
        :param request: Request instance for ListFlavors
        :type request: :class:`ctcloudsdkecs.v2.ListFlavorsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ListFlavorsResponse`
        """
        http_info = self._list_flavors_http_info(request)
        return self._call_api(**http_info)

    def list_flavors_invoker(self, request):
        http_info = self._list_flavors_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _list_flavors_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/flavors",
            "request_type": request.__class__.__name__,
            "response_type": "ListFlavorsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'availability_zone' in local_var_params:
            query_params.append(('availability_zone', local_var_params['availability_zone']))

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def list_resize_flavors(self, request):
        """
        :param request: Request instance for ListResizeFlavors
        :type request: :class:`ctcloudsdkecs.v2.ListResizeFlavorsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ListResizeFlavorsResponse`
        """
        http_info = self._list_resize_flavors_http_info(request)
        return self._call_api(**http_info)

    def list_resize_flavors_invoker(self, request):
        http_info = self._list_resize_flavors_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _list_resize_flavors_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/resize_flavors",
            "request_type": request.__class__.__name__,
            "response_type": "ListResizeFlavorsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'instance_uuid' in local_var_params:
            query_params.append(('instance_uuid', local_var_params['instance_uuid']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'sort_dir' in local_var_params:
            query_params.append(('sort_dir', local_var_params['sort_dir']))
        if 'sort_key' in local_var_params:
            query_params.append(('sort_key', local_var_params['sort_key']))
        if 'source_flavor_id' in local_var_params:
            query_params.append(('source_flavor_id', local_var_params['source_flavor_id']))
        if 'source_flavor_name' in local_var_params:
            query_params.append(('source_flavor_name', local_var_params['source_flavor_name']))

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def list_server_block_devices(self, request):
        """
        :param request: Request instance for ListServerBlockDevices
        :type request: :class:`ctcloudsdkecs.v2.ListServerBlockDevicesRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ListServerBlockDevicesResponse`
        """
        http_info = self._list_server_block_devices_http_info(request)
        return self._call_api(**http_info)

    def list_server_block_devices_invoker(self, request):
        http_info = self._list_server_block_devices_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _list_server_block_devices_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/block_device",
            "request_type": request.__class__.__name__,
            "response_type": "ListServerBlockDevicesResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def list_server_groups(self, request):
        """
        :param request: Request instance for ListServerGroups
        :type request: :class:`ctcloudsdkecs.v2.ListServerGroupsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ListServerGroupsResponse`
        """
        http_info = self._list_server_groups_http_info(request)
        return self._call_api(**http_info)

    def list_server_groups_invoker(self, request):
        http_info = self._list_server_groups_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _list_server_groups_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/os-server-groups",
            "request_type": request.__class__.__name__,
            "response_type": "ListServerGroupsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def list_server_interfaces(self, request):
        """
        :param request: Request instance for ListServerInterfaces
        :type request: :class:`ctcloudsdkecs.v2.ListServerInterfacesRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ListServerInterfacesResponse`
        """
        http_info = self._list_server_interfaces_http_info(request)
        return self._call_api(**http_info)

    def list_server_interfaces_invoker(self, request):
        http_info = self._list_server_interfaces_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _list_server_interfaces_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/os-interface",
            "request_type": request.__class__.__name__,
            "response_type": "ListServerInterfacesResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def list_server_tags(self, request):
        """
        :param request: Request instance for ListServerTags
        :type request: :class:`ctcloudsdkecs.v2.ListServerTagsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ListServerTagsResponse`
        """
        http_info = self._list_server_tags_http_info(request)
        return self._call_api(**http_info)

    def list_server_tags_invoker(self, request):
        http_info = self._list_server_tags_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _list_server_tags_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/tags",
            "request_type": request.__class__.__name__,
            "response_type": "ListServerTagsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def list_servers_details(self, request):
        """
        :param request: Request instance for ListServersDetails
        :type request: :class:`ctcloudsdkecs.v2.ListServersDetailsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ListServersDetailsResponse`
        """
        http_info = self._list_servers_details_http_info(request)
        return self._call_api(**http_info)

    def list_servers_details_invoker(self, request):
        http_info = self._list_servers_details_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _list_servers_details_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/detail",
            "request_type": request.__class__.__name__,
            "response_type": "ListServersDetailsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'enterprise_project_id' in local_var_params:
            query_params.append(('enterprise_project_id', local_var_params['enterprise_project_id']))
        if 'flavor' in local_var_params:
            query_params.append(('flavor', local_var_params['flavor']))
        if 'ip' in local_var_params:
            query_params.append(('ip', local_var_params['ip']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'name' in local_var_params:
            query_params.append(('name', local_var_params['name']))
        if 'not_tags' in local_var_params:
            query_params.append(('not-tags', local_var_params['not_tags']))
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))
        if 'reservation_id' in local_var_params:
            query_params.append(('reservation_id', local_var_params['reservation_id']))
        if 'status' in local_var_params:
            query_params.append(('status', local_var_params['status']))
        if 'tags' in local_var_params:
            query_params.append(('tags', local_var_params['tags']))
        if 'ip_eq' in local_var_params:
            query_params.append(('ip_eq', local_var_params['ip_eq']))

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def migrate_server(self, request):
        """
        :param request: Request instance for MigrateServer
        :type request: :class:`ctcloudsdkecs.v2.MigrateServerRequest`
        :rtype: :class:`ctcloudsdkecs.v2.MigrateServerResponse`
        """
        http_info = self._migrate_server_http_info(request)
        return self._call_api(**http_info)

    def migrate_server_invoker(self, request):
        http_info = self._migrate_server_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _migrate_server_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/migrate",
            "request_type": request.__class__.__name__,
            "response_type": "MigrateServerResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_associate_security_group(self, request):
        """
        :param request: Request instance for NovaAssociateSecurityGroup
        :type request: :class:`ctcloudsdkecs.v2.NovaAssociateSecurityGroupRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaAssociateSecurityGroupResponse`
        """
        http_info = self._nova_associate_security_group_http_info(request)
        return self._call_api(**http_info)

    def nova_associate_security_group_invoker(self, request):
        http_info = self._nova_associate_security_group_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_associate_security_group_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v2.1/{project_id}/servers/{server_id}/action",
            "request_type": request.__class__.__name__,
            "response_type": "NovaAssociateSecurityGroupResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_attach_interface(self, request):
        """
        :param request: Request instance for NovaAttachInterface
        :type request: :class:`ctcloudsdkecs.v2.NovaAttachInterfaceRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaAttachInterfaceResponse`
        """
        http_info = self._nova_attach_interface_http_info(request)
        return self._call_api(**http_info)

    def nova_attach_interface_invoker(self, request):
        http_info = self._nova_attach_interface_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_attach_interface_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v2.1/{project_id}/servers/{server_id}/os-interface",
            "request_type": request.__class__.__name__,
            "response_type": "NovaAttachInterfaceResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_create_keypair(self, request):
        """
        :param request: Request instance for NovaCreateKeypair
        :type request: :class:`ctcloudsdkecs.v2.NovaCreateKeypairRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaCreateKeypairResponse`
        """
        http_info = self._nova_create_keypair_http_info(request)
        return self._call_api(**http_info)

    def nova_create_keypair_invoker(self, request):
        http_info = self._nova_create_keypair_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_create_keypair_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v2.1/{project_id}/os-keypairs",
            "request_type": request.__class__.__name__,
            "response_type": "NovaCreateKeypairResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'open_stack_api_version' in local_var_params:
            header_params['OpenStack-API-Version'] = local_var_params['open_stack_api_version']

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_create_servers(self, request):
        """
        :param request: Request instance for NovaCreateServers
        :type request: :class:`ctcloudsdkecs.v2.NovaCreateServersRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaCreateServersResponse`
        """
        http_info = self._nova_create_servers_http_info(request)
        return self._call_api(**http_info)

    def nova_create_servers_invoker(self, request):
        http_info = self._nova_create_servers_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_create_servers_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v2.1/{project_id}/servers",
            "request_type": request.__class__.__name__,
            "response_type": "NovaCreateServersResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'open_stack_api_version' in local_var_params:
            header_params['OpenStack-API-Version'] = local_var_params['open_stack_api_version']

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_delete_keypair(self, request):
        """
        :param request: Request instance for NovaDeleteKeypair
        :type request: :class:`ctcloudsdkecs.v2.NovaDeleteKeypairRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaDeleteKeypairResponse`
        """
        http_info = self._nova_delete_keypair_http_info(request)
        return self._call_api(**http_info)

    def nova_delete_keypair_invoker(self, request):
        http_info = self._nova_delete_keypair_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_delete_keypair_http_info(cls, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v2.1/{project_id}/os-keypairs/{keypair_name}",
            "request_type": request.__class__.__name__,
            "response_type": "NovaDeleteKeypairResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'keypair_name' in local_var_params:
            path_params['keypair_name'] = local_var_params['keypair_name']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_delete_server(self, request):
        """
        :param request: Request instance for NovaDeleteServer
        :type request: :class:`ctcloudsdkecs.v2.NovaDeleteServerRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaDeleteServerResponse`
        """
        http_info = self._nova_delete_server_http_info(request)
        return self._call_api(**http_info)

    def nova_delete_server_invoker(self, request):
        http_info = self._nova_delete_server_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_delete_server_http_info(cls, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v2.1/{project_id}/servers/{server_id}",
            "request_type": request.__class__.__name__,
            "response_type": "NovaDeleteServerResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_disassociate_security_group(self, request):
        """
        :param request: Request instance for NovaDisassociateSecurityGroup
        :type request: :class:`ctcloudsdkecs.v2.NovaDisassociateSecurityGroupRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaDisassociateSecurityGroupResponse`
        """
        http_info = self._nova_disassociate_security_group_http_info(request)
        return self._call_api(**http_info)

    def nova_disassociate_security_group_invoker(self, request):
        http_info = self._nova_disassociate_security_group_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_disassociate_security_group_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v2.1/{project_id}/servers/{server_id}/action",
            "request_type": request.__class__.__name__,
            "response_type": "NovaDisassociateSecurityGroupResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_list_availability_zones(self, request):
        """
        :param request: Request instance for NovaListAvailabilityZones
        :type request: :class:`ctcloudsdkecs.v2.NovaListAvailabilityZonesRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaListAvailabilityZonesResponse`
        """
        http_info = self._nova_list_availability_zones_http_info(request)
        return self._call_api(**http_info)

    def nova_list_availability_zones_invoker(self, request):
        http_info = self._nova_list_availability_zones_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_list_availability_zones_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v2.1/{project_id}/os-availability-zone",
            "request_type": request.__class__.__name__,
            "response_type": "NovaListAvailabilityZonesResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_list_keypairs(self, request):
        """
        :param request: Request instance for NovaListKeypairs
        :type request: :class:`ctcloudsdkecs.v2.NovaListKeypairsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaListKeypairsResponse`
        """
        http_info = self._nova_list_keypairs_http_info(request)
        return self._call_api(**http_info)

    def nova_list_keypairs_invoker(self, request):
        http_info = self._nova_list_keypairs_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_list_keypairs_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v2.1/{project_id}/os-keypairs",
            "request_type": request.__class__.__name__,
            "response_type": "NovaListKeypairsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))

        header_params = {}
        if 'open_stack_api_version' in local_var_params:
            header_params['OpenStack-API-Version'] = local_var_params['open_stack_api_version']

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_list_server_security_groups(self, request):
        """
        :param request: Request instance for NovaListServerSecurityGroups
        :type request: :class:`ctcloudsdkecs.v2.NovaListServerSecurityGroupsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaListServerSecurityGroupsResponse`
        """
        http_info = self._nova_list_server_security_groups_http_info(request)
        return self._call_api(**http_info)

    def nova_list_server_security_groups_invoker(self, request):
        http_info = self._nova_list_server_security_groups_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_list_server_security_groups_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v2.1/{project_id}/servers/{server_id}/os-security-groups",
            "request_type": request.__class__.__name__,
            "response_type": "NovaListServerSecurityGroupsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_list_servers_details(self, request):
        """
        :param request: Request instance for NovaListServersDetails
        :type request: :class:`ctcloudsdkecs.v2.NovaListServersDetailsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaListServersDetailsResponse`
        """
        http_info = self._nova_list_servers_details_http_info(request)
        return self._call_api(**http_info)

    def nova_list_servers_details_invoker(self, request):
        http_info = self._nova_list_servers_details_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_list_servers_details_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v2.1/{project_id}/servers/detail",
            "request_type": request.__class__.__name__,
            "response_type": "NovaListServersDetailsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'changes_since' in local_var_params:
            query_params.append(('changes-since', local_var_params['changes_since']))
        if 'flavor' in local_var_params:
            query_params.append(('flavor', local_var_params['flavor']))
        if 'image' in local_var_params:
            query_params.append(('image', local_var_params['image']))
        if 'ip' in local_var_params:
            query_params.append(('ip', local_var_params['ip']))
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'marker' in local_var_params:
            query_params.append(('marker', local_var_params['marker']))
        if 'name' in local_var_params:
            query_params.append(('name', local_var_params['name']))
        if 'not_tags' in local_var_params:
            query_params.append(('not-tags', local_var_params['not_tags']))
        if 'reservation_id' in local_var_params:
            query_params.append(('reservation_id', local_var_params['reservation_id']))
        if 'sort_key' in local_var_params:
            query_params.append(('sort_key', local_var_params['sort_key']))
        if 'status' in local_var_params:
            query_params.append(('status', local_var_params['status']))
        if 'tags' in local_var_params:
            query_params.append(('tags', local_var_params['tags']))

        header_params = {}
        if 'open_stack_api_version' in local_var_params:
            header_params['OpenStack-API-Version'] = local_var_params['open_stack_api_version']

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_show_keypair(self, request):
        """
        :param request: Request instance for NovaShowKeypair
        :type request: :class:`ctcloudsdkecs.v2.NovaShowKeypairRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaShowKeypairResponse`
        """
        http_info = self._nova_show_keypair_http_info(request)
        return self._call_api(**http_info)

    def nova_show_keypair_invoker(self, request):
        http_info = self._nova_show_keypair_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_show_keypair_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v2.1/{project_id}/os-keypairs/{keypair_name}",
            "request_type": request.__class__.__name__,
            "response_type": "NovaShowKeypairResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'keypair_name' in local_var_params:
            path_params['keypair_name'] = local_var_params['keypair_name']

        query_params = []

        header_params = {}
        if 'open_stack_api_version' in local_var_params:
            header_params['OpenStack-API-Version'] = local_var_params['open_stack_api_version']

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def nova_show_server(self, request):
        """
        :param request: Request instance for NovaShowServer
        :type request: :class:`ctcloudsdkecs.v2.NovaShowServerRequest`
        :rtype: :class:`ctcloudsdkecs.v2.NovaShowServerResponse`
        """
        http_info = self._nova_show_server_http_info(request)
        return self._call_api(**http_info)

    def nova_show_server_invoker(self, request):
        http_info = self._nova_show_server_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _nova_show_server_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v2.1/{project_id}/servers/{server_id}",
            "request_type": request.__class__.__name__,
            "response_type": "NovaShowServerResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}
        if 'open_stack_api_version' in local_var_params:
            header_params['OpenStack-API-Version'] = local_var_params['open_stack_api_version']

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def register_server_auto_recovery(self, request):
        """
        :param request: Request instance for RegisterServerAutoRecovery
        :type request: :class:`ctcloudsdkecs.v2.RegisterServerAutoRecoveryRequest`
        :rtype: :class:`ctcloudsdkecs.v2.RegisterServerAutoRecoveryResponse`
        """
        http_info = self._register_server_auto_recovery_http_info(request)
        return self._call_api(**http_info)

    def register_server_auto_recovery_invoker(self, request):
        http_info = self._register_server_auto_recovery_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _register_server_auto_recovery_http_info(cls, request):
        http_info = {
            "method": "PUT",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/autorecovery",
            "request_type": request.__class__.__name__,
            "response_type": "RegisterServerAutoRecoveryResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def reinstall_server_with_cloud_init(self, request):
        """
        :param request: Request instance for ReinstallServerWithCloudInit
        :type request: :class:`ctcloudsdkecs.v2.ReinstallServerWithCloudInitRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ReinstallServerWithCloudInitResponse`
        """
        http_info = self._reinstall_server_with_cloud_init_http_info(request)
        return self._call_api(**http_info)

    def reinstall_server_with_cloud_init_invoker(self, request):
        http_info = self._reinstall_server_with_cloud_init_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _reinstall_server_with_cloud_init_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v2/{project_id}/cloudservers/{server_id}/reinstallos",
            "request_type": request.__class__.__name__,
            "response_type": "ReinstallServerWithCloudInitResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def reinstall_server_without_cloud_init(self, request):
        """
        :param request: Request instance for ReinstallServerWithoutCloudInit
        :type request: :class:`ctcloudsdkecs.v2.ReinstallServerWithoutCloudInitRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ReinstallServerWithoutCloudInitResponse`
        """
        http_info = self._reinstall_server_without_cloud_init_http_info(request)
        return self._call_api(**http_info)

    def reinstall_server_without_cloud_init_invoker(self, request):
        http_info = self._reinstall_server_without_cloud_init_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _reinstall_server_without_cloud_init_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/reinstallos",
            "request_type": request.__class__.__name__,
            "response_type": "ReinstallServerWithoutCloudInitResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def reset_server_password(self, request):
        """
        :param request: Request instance for ResetServerPassword
        :type request: :class:`ctcloudsdkecs.v2.ResetServerPasswordRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ResetServerPasswordResponse`
        """
        http_info = self._reset_server_password_http_info(request)
        return self._call_api(**http_info)

    def reset_server_password_invoker(self, request):
        http_info = self._reset_server_password_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _reset_server_password_http_info(cls, request):
        http_info = {
            "method": "PUT",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/os-reset-password",
            "request_type": request.__class__.__name__,
            "response_type": "ResetServerPasswordResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def resize_post_paid_server(self, request):
        """
        :param request: Request instance for ResizePostPaidServer
        :type request: :class:`ctcloudsdkecs.v2.ResizePostPaidServerRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ResizePostPaidServerResponse`
        """
        http_info = self._resize_post_paid_server_http_info(request)
        return self._call_api(**http_info)

    def resize_post_paid_server_invoker(self, request):
        http_info = self._resize_post_paid_server_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _resize_post_paid_server_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/resize",
            "request_type": request.__class__.__name__,
            "response_type": "ResizePostPaidServerResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def resize_server(self, request):
        """
        :param request: Request instance for ResizeServer
        :type request: :class:`ctcloudsdkecs.v2.ResizeServerRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ResizeServerResponse`
        """
        http_info = self._resize_server_http_info(request)
        return self._call_api(**http_info)

    def resize_server_invoker(self, request):
        http_info = self._resize_server_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _resize_server_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.1/{project_id}/cloudservers/{server_id}/resize",
            "request_type": request.__class__.__name__,
            "response_type": "ResizeServerResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_reset_password_flag(self, request):
        """
        :param request: Request instance for ShowResetPasswordFlag
        :type request: :class:`ctcloudsdkecs.v2.ShowResetPasswordFlagRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowResetPasswordFlagResponse`
        """
        http_info = self._show_reset_password_flag_http_info(request)
        return self._call_api(**http_info)

    def show_reset_password_flag_invoker(self, request):
        http_info = self._show_reset_password_flag_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_reset_password_flag_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/os-resetpwd-flag",
            "request_type": request.__class__.__name__,
            "response_type": "ShowResetPasswordFlagResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server(self, request):
        """
        :param request: Request instance for ShowServer
        :type request: :class:`ctcloudsdkecs.v2.ShowServerRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerResponse`
        """
        http_info = self._show_server_http_info(request)
        return self._call_api(**http_info)

    def show_server_invoker(self, request):
        http_info = self._show_server_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server_auto_recovery(self, request):
        """
        :param request: Request instance for ShowServerAutoRecovery
        :type request: :class:`ctcloudsdkecs.v2.ShowServerAutoRecoveryRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerAutoRecoveryResponse`
        """
        http_info = self._show_server_auto_recovery_http_info(request)
        return self._call_api(**http_info)

    def show_server_auto_recovery_invoker(self, request):
        http_info = self._show_server_auto_recovery_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_auto_recovery_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/autorecovery",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerAutoRecoveryResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server_block_device(self, request):
        """
        :param request: Request instance for ShowServerBlockDevice
        :type request: :class:`ctcloudsdkecs.v2.ShowServerBlockDeviceRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerBlockDeviceResponse`
        """
        http_info = self._show_server_block_device_http_info(request)
        return self._call_api(**http_info)

    def show_server_block_device_invoker(self, request):
        http_info = self._show_server_block_device_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_block_device_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/block_device/{volume_id}",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerBlockDeviceResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']
        if 'volume_id' in local_var_params:
            path_params['volume_id'] = local_var_params['volume_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server_group(self, request):
        """
        :param request: Request instance for ShowServerGroup
        :type request: :class:`ctcloudsdkecs.v2.ShowServerGroupRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerGroupResponse`
        """
        http_info = self._show_server_group_http_info(request)
        return self._call_api(**http_info)

    def show_server_group_invoker(self, request):
        http_info = self._show_server_group_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_group_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/os-server-groups/{server_group_id}",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerGroupResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_group_id' in local_var_params:
            path_params['server_group_id'] = local_var_params['server_group_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server_limits(self, request):
        """
        :param request: Request instance for ShowServerLimits
        :type request: :class:`ctcloudsdkecs.v2.ShowServerLimitsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerLimitsResponse`
        """
        http_info = self._show_server_limits_http_info(request)
        return self._call_api(**http_info)

    def show_server_limits_invoker(self, request):
        http_info = self._show_server_limits_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_limits_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/limits",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerLimitsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server_password(self, request):
        """
        :param request: Request instance for ShowServerPassword
        :type request: :class:`ctcloudsdkecs.v2.ShowServerPasswordRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerPasswordResponse`
        """
        http_info = self._show_server_password_http_info(request)
        return self._call_api(**http_info)

    def show_server_password_invoker(self, request):
        http_info = self._show_server_password_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_password_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/os-server-password",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerPasswordResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server_remote_console(self, request):
        """
        :param request: Request instance for ShowServerRemoteConsole
        :type request: :class:`ctcloudsdkecs.v2.ShowServerRemoteConsoleRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerRemoteConsoleResponse`
        """
        http_info = self._show_server_remote_console_http_info(request)
        return self._call_api(**http_info)

    def show_server_remote_console_invoker(self, request):
        http_info = self._show_server_remote_console_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_remote_console_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/remote_console",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerRemoteConsoleResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_server_tags(self, request):
        """
        :param request: Request instance for ShowServerTags
        :type request: :class:`ctcloudsdkecs.v2.ShowServerTagsRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowServerTagsResponse`
        """
        http_info = self._show_server_tags_http_info(request)
        return self._call_api(**http_info)

    def show_server_tags_invoker(self, request):
        http_info = self._show_server_tags_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_server_tags_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/tags",
            "request_type": request.__class__.__name__,
            "response_type": "ShowServerTagsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def update_server(self, request):
        """
        :param request: Request instance for UpdateServer
        :type request: :class:`ctcloudsdkecs.v2.UpdateServerRequest`
        :rtype: :class:`ctcloudsdkecs.v2.UpdateServerResponse`
        """
        http_info = self._update_server_http_info(request)
        return self._call_api(**http_info)

    def update_server_invoker(self, request):
        http_info = self._update_server_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _update_server_http_info(cls, request):
        http_info = {
            "method": "PUT",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}",
            "request_type": request.__class__.__name__,
            "response_type": "UpdateServerResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def update_server_auto_terminate_time(self, request):
        """
        :param request: Request instance for UpdateServerAutoTerminateTime
        :type request: :class:`ctcloudsdkecs.v2.UpdateServerAutoTerminateTimeRequest`
        :rtype: :class:`ctcloudsdkecs.v2.UpdateServerAutoTerminateTimeResponse`
        """
        http_info = self._update_server_auto_terminate_time_http_info(request)
        return self._call_api(**http_info)

    def update_server_auto_terminate_time_invoker(self, request):
        http_info = self._update_server_auto_terminate_time_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _update_server_auto_terminate_time_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/actions/update-auto-terminate-time",
            "request_type": request.__class__.__name__,
            "response_type": "UpdateServerAutoTerminateTimeResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def update_server_metadata(self, request):
        """
        :param request: Request instance for UpdateServerMetadata
        :type request: :class:`ctcloudsdkecs.v2.UpdateServerMetadataRequest`
        :rtype: :class:`ctcloudsdkecs.v2.UpdateServerMetadataResponse`
        """
        http_info = self._update_server_metadata_http_info(request)
        return self._call_api(**http_info)

    def update_server_metadata_invoker(self, request):
        http_info = self._update_server_metadata_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _update_server_metadata_http_info(cls, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1/{project_id}/cloudservers/{server_id}/metadata",
            "request_type": request.__class__.__name__,
            "response_type": "UpdateServerMetadataResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'server_id' in local_var_params:
            path_params['server_id'] = local_var_params['server_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if 'body' in local_var_params:
            body = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json;charset=UTF-8'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def show_job(self, request):
        """
        :param request: Request instance for ShowJob
        :type request: :class:`ctcloudsdkecs.v2.ShowJobRequest`
        :rtype: :class:`ctcloudsdkecs.v2.ShowJobResponse`
        """
        http_info = self._show_job_http_info(request)
        return self._call_api(**http_info)

    def show_job_invoker(self, request):
        http_info = self._show_job_http_info(request)
        return SyncInvoker(self, http_info)

    @classmethod
    def _show_job_http_info(cls, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1/{project_id}/jobs/{job_id}",
            "request_type": request.__class__.__name__,
            "response_type": "ShowJobResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'job_id' in local_var_params:
            path_params['job_id'] = local_var_params['job_id']

        query_params = []

        header_params = {}

        form_params = {}

        body = None
        if isinstance(request, SdkStreamRequest):
            body = request.get_file_stream()

        response_headers = []

        header_params['Content-Type'] = http_utils.select_header_content_type(
            ['application/json'])

        auth_settings = []

        http_info["cname"] = cname
        http_info["collection_formats"] = collection_formats
        http_info["path_params"] = path_params
        http_info["query_params"] = query_params
        http_info["header_params"] = header_params
        http_info["post_params"] = form_params
        http_info["body"] = body
        http_info["response_headers"] = response_headers

        return http_info

    def _call_api(self, **kwargs):
        try:
            return self.do_http_request(**kwargs)
        except TypeError:
            import inspect
            params = inspect.signature(self.do_http_request).parameters
            http_info = {param_name: kwargs.get(param_name) for param_name in params if param_name in kwargs}
            return self.do_http_request(**http_info)

    def call_api(self, resource_path, method, path_params=None, query_params=None, header_params=None, body=None,
                 post_params=None, cname=None, response_type=None, response_headers=None, auth_settings=None,
                 collection_formats=None, request_type=None):
        """Makes the HTTP request and returns deserialized data.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param path_params: Path parameters in the url.
        :param query_params: Query parameters in the url.
        :param header_params: Header parameters to be placed in the request header.
        :param body: Request body.
        :param post_params: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param cname: Used for obs endpoint.
        :param auth_settings: Auth Settings names for the request.
        :param response_type: Response data type.
        :param response_headers: Header should be added to response data.
        :param collection_formats: dict of collection formats for path, query,
            header, and post parameters.
        :param request_type: Request data type.
        :return:
            Return the response directly.
        """
        return self.do_http_request(
            method=method,
            resource_path=resource_path,
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
            post_params=post_params,
            cname=cname,
            response_type=response_type,
            response_headers=response_headers,
            collection_formats=collection_formats,
            request_type=request_type)
