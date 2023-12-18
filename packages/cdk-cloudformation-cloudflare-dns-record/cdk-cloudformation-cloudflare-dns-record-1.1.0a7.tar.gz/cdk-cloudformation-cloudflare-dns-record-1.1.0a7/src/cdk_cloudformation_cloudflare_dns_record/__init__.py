'''
# cloudflare-dns-record

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Cloudflare::Dns::Record` v1.1.0.

## Description

A Cloudflare resource for managing a single DNS record

## References

* [Documentation](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Cloudflare::Dns::Record \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Cloudflare-Dns-Record \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Cloudflare::Dns::Record`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fcloudflare-dns-record+v1.1.0).
* Issues related to `Cloudflare::Dns::Record` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers).

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


class CfnRecord(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/cloudflare-dns-record.CfnRecord",
):
    '''A CloudFormation ``Cloudflare::Dns::Record``.

    :cloudformationResource: Cloudflare::Dns::Record
    :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        content: builtins.str,
        name: builtins.str,
        ttl: jsii.Number,
        type: "CfnRecordPropsType",
        zone_id: builtins.str,
        meta: typing.Any = None,
        proxied: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``Cloudflare::Dns::Record``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: A valid IPv4 address.
        :param name: DNS record name (or @ for the zone apex).
        :param ttl: Time to live, in seconds, of the DNS record. Must be between 60 and 86400, or 1 for 'automatic'
        :param type: Record type.
        :param zone_id: Zone identifier tag.
        :param meta: Extra Cloudflare-specific information about the record.
        :param proxied: Whether the record is receiving the performance and security benefits of Cloudflare.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf15612040aae427fb9d0819f32099f3ad6f305f80861fe3bb7b32ddecf2acb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRecordProps(
            content=content,
            name=name,
            ttl=ttl,
            type=type,
            zone_id=zone_id,
            meta=meta,
            proxied=proxied,
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
        '''Attribute ``Cloudflare::Dns::Record.CreatedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedOn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Cloudflare::Dns::Record.Id``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLocked")
    def attr_locked(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''Attribute ``Cloudflare::Dns::Record.Locked``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "attrLocked"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedOn")
    def attr_modified_on(self) -> builtins.str:
        '''Attribute ``Cloudflare::Dns::Record.ModifiedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="attrProxiable")
    def attr_proxiable(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''Attribute ``Cloudflare::Dns::Record.Proxiable``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "attrProxiable"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneName")
    def attr_zone_name(self) -> builtins.str:
        '''Attribute ``Cloudflare::Dns::Record.ZoneName``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrZoneName"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnRecordProps":
        '''Resource props.'''
        return typing.cast("CfnRecordProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-dns-record.CfnRecordProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "name": "name",
        "ttl": "ttl",
        "type": "type",
        "zone_id": "zoneId",
        "meta": "meta",
        "proxied": "proxied",
    },
)
class CfnRecordProps:
    def __init__(
        self,
        *,
        content: builtins.str,
        name: builtins.str,
        ttl: jsii.Number,
        type: "CfnRecordPropsType",
        zone_id: builtins.str,
        meta: typing.Any = None,
        proxied: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''A Cloudflare resource for managing a single DNS record.

        :param content: A valid IPv4 address.
        :param name: DNS record name (or @ for the zone apex).
        :param ttl: Time to live, in seconds, of the DNS record. Must be between 60 and 86400, or 1 for 'automatic'
        :param type: Record type.
        :param zone_id: Zone identifier tag.
        :param meta: Extra Cloudflare-specific information about the record.
        :param proxied: Whether the record is receiving the performance and security benefits of Cloudflare.

        :schema: CfnRecordProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096f4e7a54aa0a219901827b6f47aa6eb508f0270760378b2a1d9931dbc916b1)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument meta", value=meta, expected_type=type_hints["meta"])
            check_type(argname="argument proxied", value=proxied, expected_type=type_hints["proxied"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "name": name,
            "ttl": ttl,
            "type": type,
            "zone_id": zone_id,
        }
        if meta is not None:
            self._values["meta"] = meta
        if proxied is not None:
            self._values["proxied"] = proxied

    @builtins.property
    def content(self) -> builtins.str:
        '''A valid IPv4 address.

        :schema: CfnRecordProps#Content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''DNS record name (or @ for the zone apex).

        :schema: CfnRecordProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ttl(self) -> jsii.Number:
        '''Time to live, in seconds, of the DNS record.

        Must be between 60 and 86400, or 1 for 'automatic'

        :schema: CfnRecordProps#Ttl
        '''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> "CfnRecordPropsType":
        '''Record type.

        :schema: CfnRecordProps#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("CfnRecordPropsType", result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''Zone identifier tag.

        :schema: CfnRecordProps#ZoneId
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def meta(self) -> typing.Any:
        '''Extra Cloudflare-specific information about the record.

        :schema: CfnRecordProps#Meta
        '''
        result = self._values.get("meta")
        return typing.cast(typing.Any, result)

    @builtins.property
    def proxied(self) -> typing.Optional[builtins.bool]:
        '''Whether the record is receiving the performance and security benefits of Cloudflare.

        :schema: CfnRecordProps#Proxied
        '''
        result = self._values.get("proxied")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecordProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/cloudflare-dns-record.CfnRecordPropsType")
class CfnRecordPropsType(enum.Enum):
    '''Record type.

    :schema: CfnRecordPropsType
    '''

    A = "A"
    '''A.'''
    AAAA = "AAAA"
    '''AAAA.'''
    CERT = "CERT"
    '''CERT.'''
    CNAME = "CNAME"
    '''CNAME.'''
    DNSKEY = "DNSKEY"
    '''DNSKEY.'''
    DS = "DS"
    '''DS.'''
    HTTPS = "HTTPS"
    '''HTTPS.'''
    LOC = "LOC"
    '''LOC.'''
    MX = "MX"
    '''MX.'''
    NAPTR = "NAPTR"
    '''NAPTR.'''
    NS = "NS"
    '''NS.'''
    SMIMEA = "SMIMEA"
    '''SMIMEA.'''
    SRV = "SRV"
    '''SRV.'''
    SSHFP = "SSHFP"
    '''SSHFP.'''
    SVCB = "SVCB"
    '''SVCB.'''
    TLSA = "TLSA"
    '''TLSA.'''
    TXT = "TXT"
    '''TXT.'''
    URI = "URI"
    '''URI.'''


__all__ = [
    "CfnRecord",
    "CfnRecordProps",
    "CfnRecordPropsType",
]

publication.publish()

def _typecheckingstub__caf15612040aae427fb9d0819f32099f3ad6f305f80861fe3bb7b32ddecf2acb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content: builtins.str,
    name: builtins.str,
    ttl: jsii.Number,
    type: CfnRecordPropsType,
    zone_id: builtins.str,
    meta: typing.Any = None,
    proxied: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096f4e7a54aa0a219901827b6f47aa6eb508f0270760378b2a1d9931dbc916b1(
    *,
    content: builtins.str,
    name: builtins.str,
    ttl: jsii.Number,
    type: CfnRecordPropsType,
    zone_id: builtins.str,
    meta: typing.Any = None,
    proxied: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
