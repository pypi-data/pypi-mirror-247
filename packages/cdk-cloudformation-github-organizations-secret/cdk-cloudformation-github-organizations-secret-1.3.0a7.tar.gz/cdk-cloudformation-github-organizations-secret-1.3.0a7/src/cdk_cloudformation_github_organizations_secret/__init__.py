'''
# github-organizations-secret

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Organizations::Secret` v1.3.0.

## Description

Manage the organization secret

## References

* [Source](https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Organizations::Secret \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Organizations-Secret \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Organizations::Secret`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-organizations-secret+v1.3.0).
* Issues related to `GitHub::Organizations::Secret` should be reported to the [publisher](https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git).

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


class CfnSecret(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-organizations-secret.CfnSecret",
):
    '''A CloudFormation ``GitHub::Organizations::Secret``.

    :cloudformationResource: GitHub::Organizations::Secret
    :link: https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        org: builtins.str,
        secret_name: builtins.str,
        visibility: "Visibility",
        created_at: typing.Optional[datetime.datetime] = None,
        name: typing.Optional[builtins.str] = None,
        secret_value: typing.Optional[builtins.str] = None,
        selected_repository_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''Create a new ``GitHub::Organizations::Secret``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param org: 
        :param secret_name: 
        :param visibility: 
        :param created_at: 
        :param name: 
        :param secret_value: 
        :param selected_repository_ids: 
        :param updated_at: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c90c9c64f3a5878af3bb2c0bb1c373651958343c54f242d1ec0c095b6cf093)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecretProps(
            org=org,
            secret_name=secret_name,
            visibility=visibility,
            created_at=created_at,
            name=name,
            secret_value=secret_value,
            selected_repository_ids=selected_repository_ids,
            updated_at=updated_at,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSelectedRepositoriesUrl")
    def attr_selected_repositories_url(self) -> builtins.str:
        '''Attribute ``GitHub::Organizations::Secret.SelectedRepositoriesUrl``.

        :link: https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSelectedRepositoriesUrl"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSecretProps":
        '''Resource props.'''
        return typing.cast("CfnSecretProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-organizations-secret.CfnSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "org": "org",
        "secret_name": "secretName",
        "visibility": "visibility",
        "created_at": "createdAt",
        "name": "name",
        "secret_value": "secretValue",
        "selected_repository_ids": "selectedRepositoryIds",
        "updated_at": "updatedAt",
    },
)
class CfnSecretProps:
    def __init__(
        self,
        *,
        org: builtins.str,
        secret_name: builtins.str,
        visibility: "Visibility",
        created_at: typing.Optional[datetime.datetime] = None,
        name: typing.Optional[builtins.str] = None,
        secret_value: typing.Optional[builtins.str] = None,
        selected_repository_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''Manage the organization secret.

        :param org: 
        :param secret_name: 
        :param visibility: 
        :param created_at: 
        :param name: 
        :param secret_value: 
        :param selected_repository_ids: 
        :param updated_at: 

        :schema: CfnSecretProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e74172d886e4a35f66274d88a282fbd50cdbc9ec37102d4464bfa96a5aff897)
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
            check_type(argname="argument selected_repository_ids", value=selected_repository_ids, expected_type=type_hints["selected_repository_ids"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "org": org,
            "secret_name": secret_name,
            "visibility": visibility,
        }
        if created_at is not None:
            self._values["created_at"] = created_at
        if name is not None:
            self._values["name"] = name
        if secret_value is not None:
            self._values["secret_value"] = secret_value
        if selected_repository_ids is not None:
            self._values["selected_repository_ids"] = selected_repository_ids
        if updated_at is not None:
            self._values["updated_at"] = updated_at

    @builtins.property
    def org(self) -> builtins.str:
        '''
        :schema: CfnSecretProps#Org
        '''
        result = self._values.get("org")
        assert result is not None, "Required property 'org' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''
        :schema: CfnSecretProps#SecretName
        '''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def visibility(self) -> "Visibility":
        '''
        :schema: CfnSecretProps#Visibility
        '''
        result = self._values.get("visibility")
        assert result is not None, "Required property 'visibility' is missing"
        return typing.cast("Visibility", result)

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnSecretProps#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnSecretProps#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_value(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnSecretProps#SecretValue
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selected_repository_ids(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''
        :schema: CfnSecretProps#SelectedRepositoryIds
        '''
        result = self._values.get("selected_repository_ids")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnSecretProps#UpdatedAt
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/github-organizations-secret.Visibility")
class Visibility(enum.Enum):
    '''Which type of organization repositories have access to the organization secret.

    selected means only the repositories specified by selected_repository_ids can access the secret.

    :schema: Visibility
    '''

    ALL = "ALL"
    '''all.'''
    PRIVATE = "PRIVATE"
    '''private.'''
    SELECTED = "SELECTED"
    '''selected.'''


__all__ = [
    "CfnSecret",
    "CfnSecretProps",
    "Visibility",
]

publication.publish()

def _typecheckingstub__95c90c9c64f3a5878af3bb2c0bb1c373651958343c54f242d1ec0c095b6cf093(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    org: builtins.str,
    secret_name: builtins.str,
    visibility: Visibility,
    created_at: typing.Optional[datetime.datetime] = None,
    name: typing.Optional[builtins.str] = None,
    secret_value: typing.Optional[builtins.str] = None,
    selected_repository_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e74172d886e4a35f66274d88a282fbd50cdbc9ec37102d4464bfa96a5aff897(
    *,
    org: builtins.str,
    secret_name: builtins.str,
    visibility: Visibility,
    created_at: typing.Optional[datetime.datetime] = None,
    name: typing.Optional[builtins.str] = None,
    secret_value: typing.Optional[builtins.str] = None,
    selected_repository_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass
