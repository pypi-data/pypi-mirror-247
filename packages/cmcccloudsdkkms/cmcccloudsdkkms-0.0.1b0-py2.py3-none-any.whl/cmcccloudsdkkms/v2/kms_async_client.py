# coding: utf-8

from __future__ import absolute_import

import importlib
import warnings

from cmcccloudsdkcore.client import Client, ClientBuilder
from cmcccloudsdkcore.utils import http_utils
from cmcccloudsdkcore.sdk_stream_request import SdkStreamRequest
try:
    from cmcccloudsdkcore.invoker.invoker import AsyncInvoker
except ImportError as e:
    warnings.warn(str(e) + ", please check if you are using the same versions of 'cmcccloudsdkcore' and 'cmcccloudsdkkms'")


class KmsAsyncClient(Client):
    def __init__(self):
        super(KmsAsyncClient, self).__init__()
        self.model_package = importlib.import_module("cmcccloudsdkkms.v2.model")

    @classmethod
    def new_builder(cls, clazz=None):
        if not clazz:
            client_builder = ClientBuilder(cls)
        else:
            if clazz.__name__ != "KmsAsyncClient":
                raise TypeError("client type error, support client type is KmsAsyncClient")
            client_builder = ClientBuilder(clazz)

        

        return client_builder

    def batch_create_kms_tags_async(self, request):
        """

        :param request: Request instance for BatchCreateKmsTags
        :type request: :class:`cmcccloudsdkkms.v2.BatchCreateKmsTagsRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.BatchCreateKmsTagsResponse`
        """
        http_info = self._batch_create_kms_tags_http_info(request)
        return self._call_api(**http_info)

    def batch_create_kms_tags_async_invoker(self, request):
        http_info = self._batch_create_kms_tags_http_info(request)
        return AsyncInvoker(self, http_info)

    def _batch_create_kms_tags_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/{key_id}/tags/action",
            "request_type": request.__class__.__name__,
            "response_type": "BatchCreateKmsTagsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'key_id' in local_var_params:
            path_params['key_id'] = local_var_params['key_id']

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

    def cancel_grant_async(self, request):
        """

        :param request: Request instance for CancelGrant
        :type request: :class:`cmcccloudsdkkms.v2.CancelGrantRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CancelGrantResponse`
        """
        http_info = self._cancel_grant_http_info(request)
        return self._call_api(**http_info)

    def cancel_grant_async_invoker(self, request):
        http_info = self._cancel_grant_http_info(request)
        return AsyncInvoker(self, http_info)

    def _cancel_grant_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/revoke-grant",
            "request_type": request.__class__.__name__,
            "response_type": "CancelGrantResponse"
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

    def cancel_key_deletion_async(self, request):
        """

        :param request: Request instance for CancelKeyDeletion
        :type request: :class:`cmcccloudsdkkms.v2.CancelKeyDeletionRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CancelKeyDeletionResponse`
        """
        http_info = self._cancel_key_deletion_http_info(request)
        return self._call_api(**http_info)

    def cancel_key_deletion_async_invoker(self, request):
        http_info = self._cancel_key_deletion_http_info(request)
        return AsyncInvoker(self, http_info)

    def _cancel_key_deletion_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/cancel-key-deletion",
            "request_type": request.__class__.__name__,
            "response_type": "CancelKeyDeletionResponse"
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

    def cancel_self_grant_async(self, request):
        """

        :param request: Request instance for CancelSelfGrant
        :type request: :class:`cmcccloudsdkkms.v2.CancelSelfGrantRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CancelSelfGrantResponse`
        """
        http_info = self._cancel_self_grant_http_info(request)
        return self._call_api(**http_info)

    def cancel_self_grant_async_invoker(self, request):
        http_info = self._cancel_self_grant_http_info(request)
        return AsyncInvoker(self, http_info)

    def _cancel_self_grant_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/retire-grant",
            "request_type": request.__class__.__name__,
            "response_type": "CancelSelfGrantResponse"
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

    def create_datakey_async(self, request):
        """

        :param request: Request instance for CreateDatakey
        :type request: :class:`cmcccloudsdkkms.v2.CreateDatakeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateDatakeyResponse`
        """
        http_info = self._create_datakey_http_info(request)
        return self._call_api(**http_info)

    def create_datakey_async_invoker(self, request):
        http_info = self._create_datakey_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_datakey_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/create-datakey",
            "request_type": request.__class__.__name__,
            "response_type": "CreateDatakeyResponse"
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

    def create_datakey_without_plaintext_async(self, request):
        """

        :param request: Request instance for CreateDatakeyWithoutPlaintext
        :type request: :class:`cmcccloudsdkkms.v2.CreateDatakeyWithoutPlaintextRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateDatakeyWithoutPlaintextResponse`
        """
        http_info = self._create_datakey_without_plaintext_http_info(request)
        return self._call_api(**http_info)

    def create_datakey_without_plaintext_async_invoker(self, request):
        http_info = self._create_datakey_without_plaintext_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_datakey_without_plaintext_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/create-datakey-without-plaintext",
            "request_type": request.__class__.__name__,
            "response_type": "CreateDatakeyWithoutPlaintextResponse"
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

    def create_grant_async(self, request):
        """

        :param request: Request instance for CreateGrant
        :type request: :class:`cmcccloudsdkkms.v2.CreateGrantRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateGrantResponse`
        """
        http_info = self._create_grant_http_info(request)
        return self._call_api(**http_info)

    def create_grant_async_invoker(self, request):
        http_info = self._create_grant_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_grant_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/create-grant",
            "request_type": request.__class__.__name__,
            "response_type": "CreateGrantResponse"
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

    def create_key_async(self, request):
        """

        :param request: Request instance for CreateKey
        :type request: :class:`cmcccloudsdkkms.v2.CreateKeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateKeyResponse`
        """
        http_info = self._create_key_http_info(request)
        return self._call_api(**http_info)

    def create_key_async_invoker(self, request):
        http_info = self._create_key_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_key_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/create-key",
            "request_type": request.__class__.__name__,
            "response_type": "CreateKeyResponse"
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

    def create_key_store_async(self, request):
        """

        :param request: Request instance for CreateKeyStore
        :type request: :class:`cmcccloudsdkkms.v2.CreateKeyStoreRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateKeyStoreResponse`
        """
        http_info = self._create_key_store_http_info(request)
        return self._call_api(**http_info)

    def create_key_store_async_invoker(self, request):
        http_info = self._create_key_store_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_key_store_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/keystores",
            "request_type": request.__class__.__name__,
            "response_type": "CreateKeyStoreResponse"
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

    def create_kms_tag_async(self, request):
        """

        :param request: Request instance for CreateKmsTag
        :type request: :class:`cmcccloudsdkkms.v2.CreateKmsTagRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateKmsTagResponse`
        """
        http_info = self._create_kms_tag_http_info(request)
        return self._call_api(**http_info)

    def create_kms_tag_async_invoker(self, request):
        http_info = self._create_kms_tag_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_kms_tag_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/{key_id}/tags",
            "request_type": request.__class__.__name__,
            "response_type": "CreateKmsTagResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'key_id' in local_var_params:
            path_params['key_id'] = local_var_params['key_id']

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

    def create_parameters_for_import_async(self, request):
        """

        :param request: Request instance for CreateParametersForImport
        :type request: :class:`cmcccloudsdkkms.v2.CreateParametersForImportRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateParametersForImportResponse`
        """
        http_info = self._create_parameters_for_import_http_info(request)
        return self._call_api(**http_info)

    def create_parameters_for_import_async_invoker(self, request):
        http_info = self._create_parameters_for_import_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_parameters_for_import_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/get-parameters-for-import",
            "request_type": request.__class__.__name__,
            "response_type": "CreateParametersForImportResponse"
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

    def create_random_async(self, request):
        """

        :param request: Request instance for CreateRandom
        :type request: :class:`cmcccloudsdkkms.v2.CreateRandomRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.CreateRandomResponse`
        """
        http_info = self._create_random_http_info(request)
        return self._call_api(**http_info)

    def create_random_async_invoker(self, request):
        http_info = self._create_random_http_info(request)
        return AsyncInvoker(self, http_info)

    def _create_random_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/gen-random",
            "request_type": request.__class__.__name__,
            "response_type": "CreateRandomResponse"
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

    def decrypt_data_async(self, request):
        """

        :param request: Request instance for DecryptData
        :type request: :class:`cmcccloudsdkkms.v2.DecryptDataRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DecryptDataResponse`
        """
        http_info = self._decrypt_data_http_info(request)
        return self._call_api(**http_info)

    def decrypt_data_async_invoker(self, request):
        http_info = self._decrypt_data_http_info(request)
        return AsyncInvoker(self, http_info)

    def _decrypt_data_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/decrypt-data",
            "request_type": request.__class__.__name__,
            "response_type": "DecryptDataResponse"
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

    def decrypt_datakey_async(self, request):
        """

        :param request: Request instance for DecryptDatakey
        :type request: :class:`cmcccloudsdkkms.v2.DecryptDatakeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DecryptDatakeyResponse`
        """
        http_info = self._decrypt_datakey_http_info(request)
        return self._call_api(**http_info)

    def decrypt_datakey_async_invoker(self, request):
        http_info = self._decrypt_datakey_http_info(request)
        return AsyncInvoker(self, http_info)

    def _decrypt_datakey_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/decrypt-datakey",
            "request_type": request.__class__.__name__,
            "response_type": "DecryptDatakeyResponse"
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

    def delete_imported_key_material_async(self, request):
        """

        :param request: Request instance for DeleteImportedKeyMaterial
        :type request: :class:`cmcccloudsdkkms.v2.DeleteImportedKeyMaterialRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DeleteImportedKeyMaterialResponse`
        """
        http_info = self._delete_imported_key_material_http_info(request)
        return self._call_api(**http_info)

    def delete_imported_key_material_async_invoker(self, request):
        http_info = self._delete_imported_key_material_http_info(request)
        return AsyncInvoker(self, http_info)

    def _delete_imported_key_material_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/delete-imported-key-material",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteImportedKeyMaterialResponse"
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

    def delete_key_async(self, request):
        """

        :param request: Request instance for DeleteKey
        :type request: :class:`cmcccloudsdkkms.v2.DeleteKeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DeleteKeyResponse`
        """
        http_info = self._delete_key_http_info(request)
        return self._call_api(**http_info)

    def delete_key_async_invoker(self, request):
        http_info = self._delete_key_http_info(request)
        return AsyncInvoker(self, http_info)

    def _delete_key_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/schedule-key-deletion",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteKeyResponse"
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

    def delete_key_store_async(self, request):
        """

        :param request: Request instance for DeleteKeyStore
        :type request: :class:`cmcccloudsdkkms.v2.DeleteKeyStoreRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DeleteKeyStoreResponse`
        """
        http_info = self._delete_key_store_http_info(request)
        return self._call_api(**http_info)

    def delete_key_store_async_invoker(self, request):
        http_info = self._delete_key_store_http_info(request)
        return AsyncInvoker(self, http_info)

    def _delete_key_store_http_info(self, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v1.0/{project_id}/keystores/{keystore_id}",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteKeyStoreResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'keystore_id' in local_var_params:
            path_params['keystore_id'] = local_var_params['keystore_id']

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

    def delete_tag_async(self, request):
        """

        :param request: Request instance for DeleteTag
        :type request: :class:`cmcccloudsdkkms.v2.DeleteTagRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DeleteTagResponse`
        """
        http_info = self._delete_tag_http_info(request)
        return self._call_api(**http_info)

    def delete_tag_async_invoker(self, request):
        http_info = self._delete_tag_http_info(request)
        return AsyncInvoker(self, http_info)

    def _delete_tag_http_info(self, request):
        http_info = {
            "method": "DELETE",
            "resource_path": "/v1.0/{project_id}/kms/{key_id}/tags/{key}",
            "request_type": request.__class__.__name__,
            "response_type": "DeleteTagResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'key_id' in local_var_params:
            path_params['key_id'] = local_var_params['key_id']
        if 'key' in local_var_params:
            path_params['key'] = local_var_params['key']

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

    def disable_key_async(self, request):
        """

        :param request: Request instance for DisableKey
        :type request: :class:`cmcccloudsdkkms.v2.DisableKeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DisableKeyResponse`
        """
        http_info = self._disable_key_http_info(request)
        return self._call_api(**http_info)

    def disable_key_async_invoker(self, request):
        http_info = self._disable_key_http_info(request)
        return AsyncInvoker(self, http_info)

    def _disable_key_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/disable-key",
            "request_type": request.__class__.__name__,
            "response_type": "DisableKeyResponse"
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

    def disable_key_rotation_async(self, request):
        """

        :param request: Request instance for DisableKeyRotation
        :type request: :class:`cmcccloudsdkkms.v2.DisableKeyRotationRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DisableKeyRotationResponse`
        """
        http_info = self._disable_key_rotation_http_info(request)
        return self._call_api(**http_info)

    def disable_key_rotation_async_invoker(self, request):
        http_info = self._disable_key_rotation_http_info(request)
        return AsyncInvoker(self, http_info)

    def _disable_key_rotation_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/disable-key-rotation",
            "request_type": request.__class__.__name__,
            "response_type": "DisableKeyRotationResponse"
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

    def disable_key_store_async(self, request):
        """

        :param request: Request instance for DisableKeyStore
        :type request: :class:`cmcccloudsdkkms.v2.DisableKeyStoreRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.DisableKeyStoreResponse`
        """
        http_info = self._disable_key_store_http_info(request)
        return self._call_api(**http_info)

    def disable_key_store_async_invoker(self, request):
        http_info = self._disable_key_store_http_info(request)
        return AsyncInvoker(self, http_info)

    def _disable_key_store_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/keystores/{keystore_id}/disable",
            "request_type": request.__class__.__name__,
            "response_type": "DisableKeyStoreResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'keystore_id' in local_var_params:
            path_params['keystore_id'] = local_var_params['keystore_id']

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

    def enable_key_async(self, request):
        """

        :param request: Request instance for EnableKey
        :type request: :class:`cmcccloudsdkkms.v2.EnableKeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.EnableKeyResponse`
        """
        http_info = self._enable_key_http_info(request)
        return self._call_api(**http_info)

    def enable_key_async_invoker(self, request):
        http_info = self._enable_key_http_info(request)
        return AsyncInvoker(self, http_info)

    def _enable_key_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/enable-key",
            "request_type": request.__class__.__name__,
            "response_type": "EnableKeyResponse"
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

    def enable_key_rotation_async(self, request):
        """

        :param request: Request instance for EnableKeyRotation
        :type request: :class:`cmcccloudsdkkms.v2.EnableKeyRotationRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.EnableKeyRotationResponse`
        """
        http_info = self._enable_key_rotation_http_info(request)
        return self._call_api(**http_info)

    def enable_key_rotation_async_invoker(self, request):
        http_info = self._enable_key_rotation_http_info(request)
        return AsyncInvoker(self, http_info)

    def _enable_key_rotation_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/enable-key-rotation",
            "request_type": request.__class__.__name__,
            "response_type": "EnableKeyRotationResponse"
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

    def enable_key_store_async(self, request):
        """

        :param request: Request instance for EnableKeyStore
        :type request: :class:`cmcccloudsdkkms.v2.EnableKeyStoreRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.EnableKeyStoreResponse`
        """
        http_info = self._enable_key_store_http_info(request)
        return self._call_api(**http_info)

    def enable_key_store_async_invoker(self, request):
        http_info = self._enable_key_store_http_info(request)
        return AsyncInvoker(self, http_info)

    def _enable_key_store_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/keystores/{keystore_id}/enable",
            "request_type": request.__class__.__name__,
            "response_type": "EnableKeyStoreResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'keystore_id' in local_var_params:
            path_params['keystore_id'] = local_var_params['keystore_id']

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

    def encrypt_data_async(self, request):
        """

        :param request: Request instance for EncryptData
        :type request: :class:`cmcccloudsdkkms.v2.EncryptDataRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.EncryptDataResponse`
        """
        http_info = self._encrypt_data_http_info(request)
        return self._call_api(**http_info)

    def encrypt_data_async_invoker(self, request):
        http_info = self._encrypt_data_http_info(request)
        return AsyncInvoker(self, http_info)

    def _encrypt_data_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/encrypt-data",
            "request_type": request.__class__.__name__,
            "response_type": "EncryptDataResponse"
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

    def encrypt_datakey_async(self, request):
        """

        :param request: Request instance for EncryptDatakey
        :type request: :class:`cmcccloudsdkkms.v2.EncryptDatakeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.EncryptDatakeyResponse`
        """
        http_info = self._encrypt_datakey_http_info(request)
        return self._call_api(**http_info)

    def encrypt_datakey_async_invoker(self, request):
        http_info = self._encrypt_datakey_http_info(request)
        return AsyncInvoker(self, http_info)

    def _encrypt_datakey_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/encrypt-datakey",
            "request_type": request.__class__.__name__,
            "response_type": "EncryptDatakeyResponse"
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

    def import_key_material_async(self, request):
        """

        :param request: Request instance for ImportKeyMaterial
        :type request: :class:`cmcccloudsdkkms.v2.ImportKeyMaterialRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ImportKeyMaterialResponse`
        """
        http_info = self._import_key_material_http_info(request)
        return self._call_api(**http_info)

    def import_key_material_async_invoker(self, request):
        http_info = self._import_key_material_http_info(request)
        return AsyncInvoker(self, http_info)

    def _import_key_material_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/import-key-material",
            "request_type": request.__class__.__name__,
            "response_type": "ImportKeyMaterialResponse"
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

    def list_grants_async(self, request):
        """

        :param request: Request instance for ListGrants
        :type request: :class:`cmcccloudsdkkms.v2.ListGrantsRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ListGrantsResponse`
        """
        http_info = self._list_grants_http_info(request)
        return self._call_api(**http_info)

    def list_grants_async_invoker(self, request):
        http_info = self._list_grants_http_info(request)
        return AsyncInvoker(self, http_info)

    def _list_grants_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/list-grants",
            "request_type": request.__class__.__name__,
            "response_type": "ListGrantsResponse"
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

    def list_key_detail_async(self, request):
        """

        :param request: Request instance for ListKeyDetail
        :type request: :class:`cmcccloudsdkkms.v2.ListKeyDetailRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ListKeyDetailResponse`
        """
        http_info = self._list_key_detail_http_info(request)
        return self._call_api(**http_info)

    def list_key_detail_async_invoker(self, request):
        http_info = self._list_key_detail_http_info(request)
        return AsyncInvoker(self, http_info)

    def _list_key_detail_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/describe-key",
            "request_type": request.__class__.__name__,
            "response_type": "ListKeyDetailResponse"
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

    def list_key_stores_async(self, request):
        """

        :param request: Request instance for ListKeyStores
        :type request: :class:`cmcccloudsdkkms.v2.ListKeyStoresRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ListKeyStoresResponse`
        """
        http_info = self._list_key_stores_http_info(request)
        return self._call_api(**http_info)

    def list_key_stores_async_invoker(self, request):
        http_info = self._list_key_stores_http_info(request)
        return AsyncInvoker(self, http_info)

    def _list_key_stores_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1.0/{project_id}/keystores",
            "request_type": request.__class__.__name__,
            "response_type": "ListKeyStoresResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))

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

    def list_keys_async(self, request):
        """

        :param request: Request instance for ListKeys
        :type request: :class:`cmcccloudsdkkms.v2.ListKeysRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ListKeysResponse`
        """
        http_info = self._list_keys_http_info(request)
        return self._call_api(**http_info)

    def list_keys_async_invoker(self, request):
        http_info = self._list_keys_http_info(request)
        return AsyncInvoker(self, http_info)

    def _list_keys_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/list-keys",
            "request_type": request.__class__.__name__,
            "response_type": "ListKeysResponse"
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

    def list_kms_by_tags_async(self, request):
        """

        :param request: Request instance for ListKmsByTags
        :type request: :class:`cmcccloudsdkkms.v2.ListKmsByTagsRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ListKmsByTagsResponse`
        """
        http_info = self._list_kms_by_tags_http_info(request)
        return self._call_api(**http_info)

    def list_kms_by_tags_async_invoker(self, request):
        http_info = self._list_kms_by_tags_http_info(request)
        return AsyncInvoker(self, http_info)

    def _list_kms_by_tags_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/{resource_instances}/action",
            "request_type": request.__class__.__name__,
            "response_type": "ListKmsByTagsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'resource_instances' in local_var_params:
            path_params['resource_instances'] = local_var_params['resource_instances']

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

    def list_kms_tags_async(self, request):
        """

        :param request: Request instance for ListKmsTags
        :type request: :class:`cmcccloudsdkkms.v2.ListKmsTagsRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ListKmsTagsResponse`
        """
        http_info = self._list_kms_tags_http_info(request)
        return self._call_api(**http_info)

    def list_kms_tags_async_invoker(self, request):
        http_info = self._list_kms_tags_http_info(request)
        return AsyncInvoker(self, http_info)

    def _list_kms_tags_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1.0/{project_id}/kms/tags",
            "request_type": request.__class__.__name__,
            "response_type": "ListKmsTagsResponse"
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

    def list_retirable_grants_async(self, request):
        """

        :param request: Request instance for ListRetirableGrants
        :type request: :class:`cmcccloudsdkkms.v2.ListRetirableGrantsRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ListRetirableGrantsResponse`
        """
        http_info = self._list_retirable_grants_http_info(request)
        return self._call_api(**http_info)

    def list_retirable_grants_async_invoker(self, request):
        http_info = self._list_retirable_grants_http_info(request)
        return AsyncInvoker(self, http_info)

    def _list_retirable_grants_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/list-retirable-grants",
            "request_type": request.__class__.__name__,
            "response_type": "ListRetirableGrantsResponse"
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

    def show_key_rotation_status_async(self, request):
        """

        :param request: Request instance for ShowKeyRotationStatus
        :type request: :class:`cmcccloudsdkkms.v2.ShowKeyRotationStatusRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowKeyRotationStatusResponse`
        """
        http_info = self._show_key_rotation_status_http_info(request)
        return self._call_api(**http_info)

    def show_key_rotation_status_async_invoker(self, request):
        http_info = self._show_key_rotation_status_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_key_rotation_status_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/get-key-rotation-status",
            "request_type": request.__class__.__name__,
            "response_type": "ShowKeyRotationStatusResponse"
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

    def show_key_store_async(self, request):
        """

        :param request: Request instance for ShowKeyStore
        :type request: :class:`cmcccloudsdkkms.v2.ShowKeyStoreRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowKeyStoreResponse`
        """
        http_info = self._show_key_store_http_info(request)
        return self._call_api(**http_info)

    def show_key_store_async_invoker(self, request):
        http_info = self._show_key_store_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_key_store_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1.0/{project_id}/keystores/{keystore_id}",
            "request_type": request.__class__.__name__,
            "response_type": "ShowKeyStoreResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'keystore_id' in local_var_params:
            path_params['keystore_id'] = local_var_params['keystore_id']

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

    def show_kms_tags_async(self, request):
        """

        :param request: Request instance for ShowKmsTags
        :type request: :class:`cmcccloudsdkkms.v2.ShowKmsTagsRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowKmsTagsResponse`
        """
        http_info = self._show_kms_tags_http_info(request)
        return self._call_api(**http_info)

    def show_kms_tags_async_invoker(self, request):
        http_info = self._show_kms_tags_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_kms_tags_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1.0/{project_id}/kms/{key_id}/tags",
            "request_type": request.__class__.__name__,
            "response_type": "ShowKmsTagsResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'key_id' in local_var_params:
            path_params['key_id'] = local_var_params['key_id']

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

    def show_public_key_async(self, request):
        """

        :param request: Request instance for ShowPublicKey
        :type request: :class:`cmcccloudsdkkms.v2.ShowPublicKeyRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowPublicKeyResponse`
        """
        http_info = self._show_public_key_http_info(request)
        return self._call_api(**http_info)

    def show_public_key_async_invoker(self, request):
        http_info = self._show_public_key_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_public_key_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/get-publickey",
            "request_type": request.__class__.__name__,
            "response_type": "ShowPublicKeyResponse"
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

    def show_user_instances_async(self, request):
        """

        :param request: Request instance for ShowUserInstances
        :type request: :class:`cmcccloudsdkkms.v2.ShowUserInstancesRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowUserInstancesResponse`
        """
        http_info = self._show_user_instances_http_info(request)
        return self._call_api(**http_info)

    def show_user_instances_async_invoker(self, request):
        http_info = self._show_user_instances_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_user_instances_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1.0/{project_id}/kms/user-instances",
            "request_type": request.__class__.__name__,
            "response_type": "ShowUserInstancesResponse"
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

    def show_user_quotas_async(self, request):
        """

        :param request: Request instance for ShowUserQuotas
        :type request: :class:`cmcccloudsdkkms.v2.ShowUserQuotasRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowUserQuotasResponse`
        """
        http_info = self._show_user_quotas_http_info(request)
        return self._call_api(**http_info)

    def show_user_quotas_async_invoker(self, request):
        http_info = self._show_user_quotas_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_user_quotas_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/v1.0/{project_id}/kms/user-quotas",
            "request_type": request.__class__.__name__,
            "response_type": "ShowUserQuotasResponse"
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

    def sign_async(self, request):
        """

        :param request: Request instance for Sign
        :type request: :class:`cmcccloudsdkkms.v2.SignRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.SignResponse`
        """
        http_info = self._sign_http_info(request)
        return self._call_api(**http_info)

    def sign_async_invoker(self, request):
        http_info = self._sign_http_info(request)
        return AsyncInvoker(self, http_info)

    def _sign_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/sign",
            "request_type": request.__class__.__name__,
            "response_type": "SignResponse"
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

    def update_key_alias_async(self, request):
        """

        :param request: Request instance for UpdateKeyAlias
        :type request: :class:`cmcccloudsdkkms.v2.UpdateKeyAliasRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.UpdateKeyAliasResponse`
        """
        http_info = self._update_key_alias_http_info(request)
        return self._call_api(**http_info)

    def update_key_alias_async_invoker(self, request):
        http_info = self._update_key_alias_http_info(request)
        return AsyncInvoker(self, http_info)

    def _update_key_alias_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/update-key-alias",
            "request_type": request.__class__.__name__,
            "response_type": "UpdateKeyAliasResponse"
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

    def update_key_description_async(self, request):
        """

        :param request: Request instance for UpdateKeyDescription
        :type request: :class:`cmcccloudsdkkms.v2.UpdateKeyDescriptionRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.UpdateKeyDescriptionResponse`
        """
        http_info = self._update_key_description_http_info(request)
        return self._call_api(**http_info)

    def update_key_description_async_invoker(self, request):
        http_info = self._update_key_description_http_info(request)
        return AsyncInvoker(self, http_info)

    def _update_key_description_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/update-key-description",
            "request_type": request.__class__.__name__,
            "response_type": "UpdateKeyDescriptionResponse"
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

    def update_key_rotation_interval_async(self, request):
        """

        :param request: Request instance for UpdateKeyRotationInterval
        :type request: :class:`cmcccloudsdkkms.v2.UpdateKeyRotationIntervalRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.UpdateKeyRotationIntervalResponse`
        """
        http_info = self._update_key_rotation_interval_http_info(request)
        return self._call_api(**http_info)

    def update_key_rotation_interval_async_invoker(self, request):
        http_info = self._update_key_rotation_interval_http_info(request)
        return AsyncInvoker(self, http_info)

    def _update_key_rotation_interval_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/update-key-rotation-interval",
            "request_type": request.__class__.__name__,
            "response_type": "UpdateKeyRotationIntervalResponse"
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

    def validate_signature_async(self, request):
        """

        :param request: Request instance for ValidateSignature
        :type request: :class:`cmcccloudsdkkms.v2.ValidateSignatureRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ValidateSignatureResponse`
        """
        http_info = self._validate_signature_http_info(request)
        return self._call_api(**http_info)

    def validate_signature_async_invoker(self, request):
        http_info = self._validate_signature_http_info(request)
        return AsyncInvoker(self, http_info)

    def _validate_signature_http_info(self, request):
        http_info = {
            "method": "POST",
            "resource_path": "/v1.0/{project_id}/kms/verify",
            "request_type": request.__class__.__name__,
            "response_type": "ValidateSignatureResponse"
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

    def show_version_async(self, request):
        """

        :param request: Request instance for ShowVersion
        :type request: :class:`cmcccloudsdkkms.v2.ShowVersionRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowVersionResponse`
        """
        http_info = self._show_version_http_info(request)
        return self._call_api(**http_info)

    def show_version_async_invoker(self, request):
        http_info = self._show_version_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_version_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/{version_id}",
            "request_type": request.__class__.__name__,
            "response_type": "ShowVersionResponse"
            }

        local_var_params = {attr: getattr(request, attr) for attr in request.attribute_map if hasattr(request, attr)}

        cname = None

        collection_formats = {}

        path_params = {}
        if 'version_id' in local_var_params:
            path_params['version_id'] = local_var_params['version_id']

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

    def show_versions_async(self, request):
        """

        :param request: Request instance for ShowVersions
        :type request: :class:`cmcccloudsdkkms.v2.ShowVersionsRequest`
        :rtype: :class:`cmcccloudsdkkms.v2.ShowVersionsResponse`
        """
        http_info = self._show_versions_http_info(request)
        return self._call_api(**http_info)

    def show_versions_async_invoker(self, request):
        http_info = self._show_versions_http_info(request)
        return AsyncInvoker(self, http_info)

    def _show_versions_http_info(self, request):
        http_info = {
            "method": "GET",
            "resource_path": "/",
            "request_type": request.__class__.__name__,
            "response_type": "ShowVersionsResponse"
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

    def _call_api(self, **kwargs):
        try:
            kwargs["async_request"] = True
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
        :param header_params: Header parameters to be
            placed in the request header.
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
            request_type=request_type,
	        async_request=True)
