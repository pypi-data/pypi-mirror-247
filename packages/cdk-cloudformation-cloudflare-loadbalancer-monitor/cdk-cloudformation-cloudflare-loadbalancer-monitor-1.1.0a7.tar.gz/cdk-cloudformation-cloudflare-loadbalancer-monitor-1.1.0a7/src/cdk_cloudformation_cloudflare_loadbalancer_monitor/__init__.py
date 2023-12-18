'''
# cloudflare-loadbalancer-monitor

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Cloudflare::LoadBalancer::Monitor` v1.1.0.

## Description

A Monitor policy to configure monitoring of endpoint health

## References

* [Documentation](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Cloudflare::LoadBalancer::Monitor \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Cloudflare-LoadBalancer-Monitor \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Cloudflare::LoadBalancer::Monitor`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fcloudflare-loadbalancer-monitor+v1.1.0).
* Issues related to `Cloudflare::LoadBalancer::Monitor` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers).

## License

Distributed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnMonitor(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-monitor.CfnMonitor",
):
    '''A CloudFormation ``Cloudflare::LoadBalancer::Monitor``.

    :cloudformationResource: Cloudflare::LoadBalancer::Monitor
    :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        expected_codes: builtins.str,
        account_identifier: typing.Optional[builtins.str] = None,
        allow_insecure: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        expected_body: typing.Optional[builtins.str] = None,
        follow_redirects: typing.Optional[builtins.bool] = None,
        header: typing.Any = None,
        interval: typing.Optional[jsii.Number] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        probe_zone: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Cloudflare::LoadBalancer::Monitor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param expected_codes: The expected HTTP response code or code range of the health check. Eg 2xx. Only valid and required if type is "http" or "https".
        :param account_identifier: The account identifier.
        :param allow_insecure: Do not validate the certificate when monitor use HTTPS. Only valid if type is "http" or "https".
        :param description: Free text description.
        :param expected_body: A case-insensitive sub-string to look for in the response body. If this string is not found, the origin will be marked as unhealthy. Only valid if type is "http" or "https". Default: "".
        :param follow_redirects: Follow redirects if returned by the origin. Only valid if type is "http" or "https".
        :param header: The HTTP request headers to send in the health check. It is recommended you set a Host header by default. The User-Agent header cannot be overridden. Fields documented below. Only valid if type is "http" or "https".
        :param interval: The interval between each health check. Shorter intervals may improve failover time, but will increase load on the origins as we check from multiple locations. Default: 60.
        :param method: The method to use for the health check. Valid values are any valid HTTP verb if type is "http" or "https", or connection_established if type is "tcp". Default: "GET" if type is "http" or "https", "connection_established" if type is "tcp", and empty otherwise.
        :param path: The endpoint path to health check against. Default: "/". Only valid if type is "http" or "https".
        :param port: The port number to use for the healthcheck, required when creating a TCP monitor. Valid values are in the range 0-65535.
        :param probe_zone: Assign this monitor to emulate the specified zone while probing. Only valid if type is "http" or "https".
        :param retries: The number of retries to attempt in case of a timeout before marking the origin as unhealthy. Retries are attempted immediately. Default: 2.
        :param timeout: The timeout (in seconds) before marking the health check as failed. Default: 5.
        :param type: The protocol to use for the healthcheck. Currently supported protocols are 'HTTP', 'HTTPS', 'TCP', 'UDP-ICMP', 'ICMP-PING', and 'SMTP'. Default: "http".
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0132a9c464b634709ee7db51580671f7fdad4d65e5a10c4093c5547643dfd084)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMonitorProps(
            expected_codes=expected_codes,
            account_identifier=account_identifier,
            allow_insecure=allow_insecure,
            description=description,
            expected_body=expected_body,
            follow_redirects=follow_redirects,
            header=header,
            interval=interval,
            method=method,
            path=path,
            port=port,
            probe_zone=probe_zone,
            retries=retries,
            timeout=timeout,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedOn")
    def attr_created_on(self) -> builtins.str:
        '''Attribute ``Cloudflare::LoadBalancer::Monitor.CreatedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedOn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Cloudflare::LoadBalancer::Monitor.Id``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedOn")
    def attr_modified_on(self) -> builtins.str:
        '''Attribute ``Cloudflare::LoadBalancer::Monitor.ModifiedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnMonitorProps":
        '''Resource props.'''
        return typing.cast("CfnMonitorProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-monitor.CfnMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "expected_codes": "expectedCodes",
        "account_identifier": "accountIdentifier",
        "allow_insecure": "allowInsecure",
        "description": "description",
        "expected_body": "expectedBody",
        "follow_redirects": "followRedirects",
        "header": "header",
        "interval": "interval",
        "method": "method",
        "path": "path",
        "port": "port",
        "probe_zone": "probeZone",
        "retries": "retries",
        "timeout": "timeout",
        "type": "type",
    },
)
class CfnMonitorProps:
    def __init__(
        self,
        *,
        expected_codes: builtins.str,
        account_identifier: typing.Optional[builtins.str] = None,
        allow_insecure: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        expected_body: typing.Optional[builtins.str] = None,
        follow_redirects: typing.Optional[builtins.bool] = None,
        header: typing.Any = None,
        interval: typing.Optional[jsii.Number] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        probe_zone: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''A Monitor policy to configure monitoring of endpoint health.

        :param expected_codes: The expected HTTP response code or code range of the health check. Eg 2xx. Only valid and required if type is "http" or "https".
        :param account_identifier: The account identifier.
        :param allow_insecure: Do not validate the certificate when monitor use HTTPS. Only valid if type is "http" or "https".
        :param description: Free text description.
        :param expected_body: A case-insensitive sub-string to look for in the response body. If this string is not found, the origin will be marked as unhealthy. Only valid if type is "http" or "https". Default: "".
        :param follow_redirects: Follow redirects if returned by the origin. Only valid if type is "http" or "https".
        :param header: The HTTP request headers to send in the health check. It is recommended you set a Host header by default. The User-Agent header cannot be overridden. Fields documented below. Only valid if type is "http" or "https".
        :param interval: The interval between each health check. Shorter intervals may improve failover time, but will increase load on the origins as we check from multiple locations. Default: 60.
        :param method: The method to use for the health check. Valid values are any valid HTTP verb if type is "http" or "https", or connection_established if type is "tcp". Default: "GET" if type is "http" or "https", "connection_established" if type is "tcp", and empty otherwise.
        :param path: The endpoint path to health check against. Default: "/". Only valid if type is "http" or "https".
        :param port: The port number to use for the healthcheck, required when creating a TCP monitor. Valid values are in the range 0-65535.
        :param probe_zone: Assign this monitor to emulate the specified zone while probing. Only valid if type is "http" or "https".
        :param retries: The number of retries to attempt in case of a timeout before marking the origin as unhealthy. Retries are attempted immediately. Default: 2.
        :param timeout: The timeout (in seconds) before marking the health check as failed. Default: 5.
        :param type: The protocol to use for the healthcheck. Currently supported protocols are 'HTTP', 'HTTPS', 'TCP', 'UDP-ICMP', 'ICMP-PING', and 'SMTP'. Default: "http".

        :schema: CfnMonitorProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acef52423bc833b022b8c689066a3d751f44bc7310383872f2ff8c452c64fab8)
            check_type(argname="argument expected_codes", value=expected_codes, expected_type=type_hints["expected_codes"])
            check_type(argname="argument account_identifier", value=account_identifier, expected_type=type_hints["account_identifier"])
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expected_body", value=expected_body, expected_type=type_hints["expected_body"])
            check_type(argname="argument follow_redirects", value=follow_redirects, expected_type=type_hints["follow_redirects"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument probe_zone", value=probe_zone, expected_type=type_hints["probe_zone"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expected_codes": expected_codes,
        }
        if account_identifier is not None:
            self._values["account_identifier"] = account_identifier
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if description is not None:
            self._values["description"] = description
        if expected_body is not None:
            self._values["expected_body"] = expected_body
        if follow_redirects is not None:
            self._values["follow_redirects"] = follow_redirects
        if header is not None:
            self._values["header"] = header
        if interval is not None:
            self._values["interval"] = interval
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if probe_zone is not None:
            self._values["probe_zone"] = probe_zone
        if retries is not None:
            self._values["retries"] = retries
        if timeout is not None:
            self._values["timeout"] = timeout
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def expected_codes(self) -> builtins.str:
        '''The expected HTTP response code or code range of the health check.

        Eg 2xx. Only valid and required if type is "http" or "https".

        :schema: CfnMonitorProps#ExpectedCodes
        '''
        result = self._values.get("expected_codes")
        assert result is not None, "Required property 'expected_codes' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_identifier(self) -> typing.Optional[builtins.str]:
        '''The account identifier.

        :schema: CfnMonitorProps#AccountIdentifier
        '''
        result = self._values.get("account_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_insecure(self) -> typing.Optional[builtins.bool]:
        '''Do not validate the certificate when monitor use HTTPS.

        Only valid if type is "http" or "https".

        :schema: CfnMonitorProps#AllowInsecure
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Free text description.

        :schema: CfnMonitorProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_body(self) -> typing.Optional[builtins.str]:
        '''A case-insensitive sub-string to look for in the response body.

        If this string is not found, the origin will be marked as unhealthy. Only valid if type is "http" or "https". Default: "".

        :schema: CfnMonitorProps#ExpectedBody
        '''
        result = self._values.get("expected_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def follow_redirects(self) -> typing.Optional[builtins.bool]:
        '''Follow redirects if returned by the origin.

        Only valid if type is "http" or "https".

        :schema: CfnMonitorProps#FollowRedirects
        '''
        result = self._values.get("follow_redirects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def header(self) -> typing.Any:
        '''The HTTP request headers to send in the health check.

        It is recommended you set a Host header by default. The User-Agent header cannot be overridden. Fields documented below. Only valid if type is "http" or "https".

        :schema: CfnMonitorProps#Header
        '''
        result = self._values.get("header")
        return typing.cast(typing.Any, result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''The interval between each health check.

        Shorter intervals may improve failover time, but will increase load on the origins as we check from multiple locations. Default: 60.

        :schema: CfnMonitorProps#Interval
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''The method to use for the health check.

        Valid values are any valid HTTP verb if type is "http" or "https", or connection_established if type is "tcp". Default: "GET" if type is "http" or "https", "connection_established" if type is "tcp", and empty otherwise.

        :schema: CfnMonitorProps#Method
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The endpoint path to health check against.

        Default: "/". Only valid if type is "http" or "https".

        :schema: CfnMonitorProps#Path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number to use for the healthcheck, required when creating a TCP monitor.

        Valid values are in the range 0-65535.

        :schema: CfnMonitorProps#Port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def probe_zone(self) -> typing.Optional[builtins.str]:
        '''Assign this monitor to emulate the specified zone while probing.

        Only valid if type is "http" or "https".

        :schema: CfnMonitorProps#ProbeZone
        '''
        result = self._values.get("probe_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''The number of retries to attempt in case of a timeout before marking the origin as unhealthy.

        Retries are attempted immediately. Default: 2.

        :schema: CfnMonitorProps#Retries
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout (in seconds) before marking the health check as failed.

        Default: 5.

        :schema: CfnMonitorProps#Timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The protocol to use for the healthcheck.

        Currently supported protocols are 'HTTP', 'HTTPS', 'TCP', 'UDP-ICMP', 'ICMP-PING', and 'SMTP'. Default: "http".

        :schema: CfnMonitorProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMonitor",
    "CfnMonitorProps",
]

publication.publish()

def _typecheckingstub__0132a9c464b634709ee7db51580671f7fdad4d65e5a10c4093c5547643dfd084(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    expected_codes: builtins.str,
    account_identifier: typing.Optional[builtins.str] = None,
    allow_insecure: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    expected_body: typing.Optional[builtins.str] = None,
    follow_redirects: typing.Optional[builtins.bool] = None,
    header: typing.Any = None,
    interval: typing.Optional[jsii.Number] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    probe_zone: typing.Optional[builtins.str] = None,
    retries: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acef52423bc833b022b8c689066a3d751f44bc7310383872f2ff8c452c64fab8(
    *,
    expected_codes: builtins.str,
    account_identifier: typing.Optional[builtins.str] = None,
    allow_insecure: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    expected_body: typing.Optional[builtins.str] = None,
    follow_redirects: typing.Optional[builtins.bool] = None,
    header: typing.Any = None,
    interval: typing.Optional[jsii.Number] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    probe_zone: typing.Optional[builtins.str] = None,
    retries: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
