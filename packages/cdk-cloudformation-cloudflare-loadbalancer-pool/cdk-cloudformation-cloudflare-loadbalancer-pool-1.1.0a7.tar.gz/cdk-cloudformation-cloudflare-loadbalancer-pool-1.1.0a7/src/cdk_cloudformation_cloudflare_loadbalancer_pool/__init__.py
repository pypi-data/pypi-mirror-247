'''
# cloudflare-loadbalancer-pool

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Cloudflare::LoadBalancer::Pool` v1.1.0.

## Description

A resource to manage a pool of origin servers

## References

* [Documentation](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Cloudflare::LoadBalancer::Pool \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Cloudflare-LoadBalancer-Pool \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Cloudflare::LoadBalancer::Pool`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fcloudflare-loadbalancer-pool+v1.1.0).
* Issues related to `Cloudflare::LoadBalancer::Pool` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers).

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


class CfnPool(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.CfnPool",
):
    '''A CloudFormation ``Cloudflare::LoadBalancer::Pool``.

    :cloudformationResource: Cloudflare::LoadBalancer::Pool
    :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        origins: typing.Sequence[typing.Union["Origin", typing.Dict[builtins.str, typing.Any]]],
        account_identifier: typing.Optional[builtins.str] = None,
        check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        latitude: typing.Optional[jsii.Number] = None,
        load_shedding: typing.Optional[typing.Union["LoadShedding", typing.Dict[builtins.str, typing.Any]]] = None,
        longitude: typing.Optional[jsii.Number] = None,
        minimum_origins: typing.Optional[jsii.Number] = None,
        monitor: typing.Optional[builtins.str] = None,
        notification_email: typing.Optional[builtins.str] = None,
        notification_filter: typing.Optional[typing.Union["Filter", typing.Dict[builtins.str, typing.Any]]] = None,
        origin_steering: typing.Optional[typing.Union["CfnPoolPropsOriginSteering", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Cloudflare::LoadBalancer::Pool``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A short name (tag) for the pool. Only alphanumeric characters, hyphens, and underscores are allowed.
        :param origins: The list of origins within this pool. Traffic directed at this pool is balanced across all currently healthy origins, provided the pool itself is healthy
        :param account_identifier: The account identifier.
        :param check_regions: A list of regions (specified by region code) from which to run health checks. Empty means every Cloudflare data center (the default), but requires an Enterprise plan
        :param description: Free text description.
        :param enabled: Whether to enable (the default) this pool. Disabled pools will not receive traffic and are excluded from health checks. Disabling a pool will cause any load balancers using it to failover to the next pool (if any).
        :param latitude: The latitude this pool is physically located at; used for proximity steering. Values should be between -90 and 90.
        :param load_shedding: 
        :param longitude: The longitude this pool is physically located at; used for proximity steering. Values should be between -180 and 180.
        :param minimum_origins: The minimum number of origins that must be healthy for this pool to serve traffic. If the number of healthy origins falls below this number, the pool will be marked unhealthy and we will failover to the next available pool. Default: 1.
        :param monitor: The ID of the Monitor to use for health checking origins within this pool.
        :param notification_email: he email address to send health status notifications to. This can be an individual mailbox or a mailing list. Multiple emails can be supplied as a comma delimited list.
        :param notification_filter: Filter pool and origin health notifications by resource type or health status. Use null to reset
        :param origin_steering: Set an origin steering policy to control origin selection within a pool.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8147ea72c3bf5a2d14b1b48a0eb4f0df7d8cf18f217e476fd619bd5207ba1437)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPoolProps(
            name=name,
            origins=origins,
            account_identifier=account_identifier,
            check_regions=check_regions,
            description=description,
            enabled=enabled,
            latitude=latitude,
            load_shedding=load_shedding,
            longitude=longitude,
            minimum_origins=minimum_origins,
            monitor=monitor,
            notification_email=notification_email,
            notification_filter=notification_filter,
            origin_steering=origin_steering,
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
        '''Attribute ``Cloudflare::LoadBalancer::Pool.CreatedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedOn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Cloudflare::LoadBalancer::Pool.Id``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedOn")
    def attr_modified_on(self) -> builtins.str:
        '''Attribute ``Cloudflare::LoadBalancer::Pool.ModifiedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnPoolProps":
        '''Resource props.'''
        return typing.cast("CfnPoolProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.CfnPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "origins": "origins",
        "account_identifier": "accountIdentifier",
        "check_regions": "checkRegions",
        "description": "description",
        "enabled": "enabled",
        "latitude": "latitude",
        "load_shedding": "loadShedding",
        "longitude": "longitude",
        "minimum_origins": "minimumOrigins",
        "monitor": "monitor",
        "notification_email": "notificationEmail",
        "notification_filter": "notificationFilter",
        "origin_steering": "originSteering",
    },
)
class CfnPoolProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        origins: typing.Sequence[typing.Union["Origin", typing.Dict[builtins.str, typing.Any]]],
        account_identifier: typing.Optional[builtins.str] = None,
        check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        latitude: typing.Optional[jsii.Number] = None,
        load_shedding: typing.Optional[typing.Union["LoadShedding", typing.Dict[builtins.str, typing.Any]]] = None,
        longitude: typing.Optional[jsii.Number] = None,
        minimum_origins: typing.Optional[jsii.Number] = None,
        monitor: typing.Optional[builtins.str] = None,
        notification_email: typing.Optional[builtins.str] = None,
        notification_filter: typing.Optional[typing.Union["Filter", typing.Dict[builtins.str, typing.Any]]] = None,
        origin_steering: typing.Optional[typing.Union["CfnPoolPropsOriginSteering", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''A resource to manage a pool of origin servers.

        :param name: A short name (tag) for the pool. Only alphanumeric characters, hyphens, and underscores are allowed.
        :param origins: The list of origins within this pool. Traffic directed at this pool is balanced across all currently healthy origins, provided the pool itself is healthy
        :param account_identifier: The account identifier.
        :param check_regions: A list of regions (specified by region code) from which to run health checks. Empty means every Cloudflare data center (the default), but requires an Enterprise plan
        :param description: Free text description.
        :param enabled: Whether to enable (the default) this pool. Disabled pools will not receive traffic and are excluded from health checks. Disabling a pool will cause any load balancers using it to failover to the next pool (if any).
        :param latitude: The latitude this pool is physically located at; used for proximity steering. Values should be between -90 and 90.
        :param load_shedding: 
        :param longitude: The longitude this pool is physically located at; used for proximity steering. Values should be between -180 and 180.
        :param minimum_origins: The minimum number of origins that must be healthy for this pool to serve traffic. If the number of healthy origins falls below this number, the pool will be marked unhealthy and we will failover to the next available pool. Default: 1.
        :param monitor: The ID of the Monitor to use for health checking origins within this pool.
        :param notification_email: he email address to send health status notifications to. This can be an individual mailbox or a mailing list. Multiple emails can be supplied as a comma delimited list.
        :param notification_filter: Filter pool and origin health notifications by resource type or health status. Use null to reset
        :param origin_steering: Set an origin steering policy to control origin selection within a pool.

        :schema: CfnPoolProps
        '''
        if isinstance(load_shedding, dict):
            load_shedding = LoadShedding(**load_shedding)
        if isinstance(notification_filter, dict):
            notification_filter = Filter(**notification_filter)
        if isinstance(origin_steering, dict):
            origin_steering = CfnPoolPropsOriginSteering(**origin_steering)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e36b1f1c49690c0647395d80cc91f0c8bdaea8bd84934685e738c4cca23b06)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origins", value=origins, expected_type=type_hints["origins"])
            check_type(argname="argument account_identifier", value=account_identifier, expected_type=type_hints["account_identifier"])
            check_type(argname="argument check_regions", value=check_regions, expected_type=type_hints["check_regions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
            check_type(argname="argument load_shedding", value=load_shedding, expected_type=type_hints["load_shedding"])
            check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            check_type(argname="argument minimum_origins", value=minimum_origins, expected_type=type_hints["minimum_origins"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument notification_email", value=notification_email, expected_type=type_hints["notification_email"])
            check_type(argname="argument notification_filter", value=notification_filter, expected_type=type_hints["notification_filter"])
            check_type(argname="argument origin_steering", value=origin_steering, expected_type=type_hints["origin_steering"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "origins": origins,
        }
        if account_identifier is not None:
            self._values["account_identifier"] = account_identifier
        if check_regions is not None:
            self._values["check_regions"] = check_regions
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if latitude is not None:
            self._values["latitude"] = latitude
        if load_shedding is not None:
            self._values["load_shedding"] = load_shedding
        if longitude is not None:
            self._values["longitude"] = longitude
        if minimum_origins is not None:
            self._values["minimum_origins"] = minimum_origins
        if monitor is not None:
            self._values["monitor"] = monitor
        if notification_email is not None:
            self._values["notification_email"] = notification_email
        if notification_filter is not None:
            self._values["notification_filter"] = notification_filter
        if origin_steering is not None:
            self._values["origin_steering"] = origin_steering

    @builtins.property
    def name(self) -> builtins.str:
        '''A short name (tag) for the pool.

        Only alphanumeric characters, hyphens, and underscores are allowed.

        :schema: CfnPoolProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origins(self) -> typing.List["Origin"]:
        '''The list of origins within this pool.

        Traffic directed at this pool is balanced across all currently healthy origins, provided the pool itself is healthy

        :schema: CfnPoolProps#Origins
        '''
        result = self._values.get("origins")
        assert result is not None, "Required property 'origins' is missing"
        return typing.cast(typing.List["Origin"], result)

    @builtins.property
    def account_identifier(self) -> typing.Optional[builtins.str]:
        '''The account identifier.

        :schema: CfnPoolProps#AccountIdentifier
        '''
        result = self._values.get("account_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of regions (specified by region code) from which to run health checks.

        Empty means every Cloudflare data center (the default), but requires an Enterprise plan

        :schema: CfnPoolProps#CheckRegions
        '''
        result = self._values.get("check_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Free text description.

        :schema: CfnPoolProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable (the default) this pool.

        Disabled pools will not receive traffic and are excluded from health checks. Disabling a pool will cause any load balancers using it to failover to the next pool (if any).

        :schema: CfnPoolProps#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def latitude(self) -> typing.Optional[jsii.Number]:
        '''The latitude this pool is physically located at;

        used for proximity steering. Values should be between -90 and 90.

        :schema: CfnPoolProps#Latitude
        '''
        result = self._values.get("latitude")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_shedding(self) -> typing.Optional["LoadShedding"]:
        '''
        :schema: CfnPoolProps#LoadShedding
        '''
        result = self._values.get("load_shedding")
        return typing.cast(typing.Optional["LoadShedding"], result)

    @builtins.property
    def longitude(self) -> typing.Optional[jsii.Number]:
        '''The longitude this pool is physically located at;

        used for proximity steering. Values should be between -180 and 180.

        :schema: CfnPoolProps#Longitude
        '''
        result = self._values.get("longitude")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_origins(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of origins that must be healthy for this pool to serve traffic.

        If the number of healthy origins falls below this number, the pool will be marked unhealthy and we will failover to the next available pool. Default: 1.

        :schema: CfnPoolProps#MinimumOrigins
        '''
        result = self._values.get("minimum_origins")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor(self) -> typing.Optional[builtins.str]:
        '''The ID of the Monitor to use for health checking origins within this pool.

        :schema: CfnPoolProps#Monitor
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_email(self) -> typing.Optional[builtins.str]:
        '''he email address to send health status notifications to.

        This can be an individual mailbox or a mailing list. Multiple emails can be supplied as a comma delimited list.

        :schema: CfnPoolProps#NotificationEmail
        '''
        result = self._values.get("notification_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_filter(self) -> typing.Optional["Filter"]:
        '''Filter pool and origin health notifications by resource type or health status.

        Use null to reset

        :schema: CfnPoolProps#NotificationFilter
        '''
        result = self._values.get("notification_filter")
        return typing.cast(typing.Optional["Filter"], result)

    @builtins.property
    def origin_steering(self) -> typing.Optional["CfnPoolPropsOriginSteering"]:
        '''Set an origin steering policy to control origin selection within a pool.

        :schema: CfnPoolProps#OriginSteering
        '''
        result = self._values.get("origin_steering")
        return typing.cast(typing.Optional["CfnPoolPropsOriginSteering"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.CfnPoolPropsOriginSteering",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy"},
)
class CfnPoolPropsOriginSteering:
    def __init__(
        self,
        *,
        policy: typing.Optional["CfnPoolPropsOriginSteeringPolicy"] = None,
    ) -> None:
        '''Set an origin steering policy to control origin selection within a pool.

        :param policy: The type of origin steering policy to use, either random or hash (based on CF-Connecting-IP).

        :schema: CfnPoolPropsOriginSteering
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0030a2eb33023acedbb1cb9e0e6fad8f902565da356b817fcb99a5e58a1ffc2b)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def policy(self) -> typing.Optional["CfnPoolPropsOriginSteeringPolicy"]:
        '''The type of origin steering policy to use, either random or hash (based on CF-Connecting-IP).

        :schema: CfnPoolPropsOriginSteering#Policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional["CfnPoolPropsOriginSteeringPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPoolPropsOriginSteering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.CfnPoolPropsOriginSteeringPolicy"
)
class CfnPoolPropsOriginSteeringPolicy(enum.Enum):
    '''The type of origin steering policy to use, either random or hash (based on CF-Connecting-IP).

    :schema: CfnPoolPropsOriginSteeringPolicy
    '''

    HASH = "HASH"
    '''hash.'''
    RANDOM = "RANDOM"
    '''random.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.Filter",
    jsii_struct_bases=[],
    name_mapping={"pool": "pool"},
)
class Filter:
    def __init__(
        self,
        *,
        pool: typing.Optional[typing.Union["FilterPool", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Filter pool and origin health notifications by resource type or health status.

        Use null to reset

        :param pool: 

        :schema: Filter
        '''
        if isinstance(pool, dict):
            pool = FilterPool(**pool)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb980c57fa16f46075d9474f43f56b719185baa9afa8490a3d8f5f8ec04ffa20)
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pool is not None:
            self._values["pool"] = pool

    @builtins.property
    def pool(self) -> typing.Optional["FilterPool"]:
        '''
        :schema: Filter#Pool
        '''
        result = self._values.get("pool")
        return typing.cast(typing.Optional["FilterPool"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Filter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.FilterPool",
    jsii_struct_bases=[],
    name_mapping={"healthy": "healthy"},
)
class FilterPool:
    def __init__(self, *, healthy: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param healthy: 

        :schema: FilterPool
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64253a1ee111c5be5906021923add76598f07554d0c8609cca847ea7abfa7981)
            check_type(argname="argument healthy", value=healthy, expected_type=type_hints["healthy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if healthy is not None:
            self._values["healthy"] = healthy

    @builtins.property
    def healthy(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: FilterPool#Healthy
        '''
        result = self._values.get("healthy")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilterPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.LoadShedding",
    jsii_struct_bases=[],
    name_mapping={
        "default_percent": "defaultPercent",
        "default_policy": "defaultPolicy",
        "session_percent": "sessionPercent",
        "session_policy": "sessionPolicy",
    },
)
class LoadShedding:
    def __init__(
        self,
        *,
        default_percent: typing.Optional[jsii.Number] = None,
        default_policy: typing.Optional["LoadSheddingDefaultPolicy"] = None,
        session_percent: typing.Optional[jsii.Number] = None,
        session_policy: typing.Optional["LoadSheddingSessionPolicy"] = None,
    ) -> None:
        '''Configures load shedding policies and percentages for the pool.

        :param default_percent: The percent of traffic to shed from the pool, according to the default policy. Applies to new sessions and traffic without session affinity.
        :param default_policy: The default policy to use when load shedding. A random policy randomly sheds a given percent of requests. A hash policy computes a hash over the CF-Connecting-IP address and sheds all requests originating from a percent of IPs.
        :param session_percent: The percent of existing sessions to shed from the pool, according to the session policy.
        :param session_policy: Session Policy.

        :schema: LoadShedding
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c00ecef4c70106d8765d5bb5fe8fb85d2ff6af0ac5a12d2b1efde2c0b9ebfcd)
            check_type(argname="argument default_percent", value=default_percent, expected_type=type_hints["default_percent"])
            check_type(argname="argument default_policy", value=default_policy, expected_type=type_hints["default_policy"])
            check_type(argname="argument session_percent", value=session_percent, expected_type=type_hints["session_percent"])
            check_type(argname="argument session_policy", value=session_policy, expected_type=type_hints["session_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_percent is not None:
            self._values["default_percent"] = default_percent
        if default_policy is not None:
            self._values["default_policy"] = default_policy
        if session_percent is not None:
            self._values["session_percent"] = session_percent
        if session_policy is not None:
            self._values["session_policy"] = session_policy

    @builtins.property
    def default_percent(self) -> typing.Optional[jsii.Number]:
        '''The percent of traffic to shed from the pool, according to the default policy.

        Applies to new sessions and traffic without session affinity.

        :schema: LoadShedding#DefaultPercent
        '''
        result = self._values.get("default_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_policy(self) -> typing.Optional["LoadSheddingDefaultPolicy"]:
        '''The default policy to use when load shedding.

        A random policy randomly sheds a given percent of requests. A hash policy computes a hash over the CF-Connecting-IP address and sheds all requests originating from a percent of IPs.

        :schema: LoadShedding#DefaultPolicy
        '''
        result = self._values.get("default_policy")
        return typing.cast(typing.Optional["LoadSheddingDefaultPolicy"], result)

    @builtins.property
    def session_percent(self) -> typing.Optional[jsii.Number]:
        '''The percent of existing sessions to shed from the pool, according to the session policy.

        :schema: LoadShedding#SessionPercent
        '''
        result = self._values.get("session_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_policy(self) -> typing.Optional["LoadSheddingSessionPolicy"]:
        '''Session Policy.

        :schema: LoadShedding#SessionPolicy
        '''
        result = self._values.get("session_policy")
        return typing.cast(typing.Optional["LoadSheddingSessionPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadShedding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.LoadSheddingDefaultPolicy"
)
class LoadSheddingDefaultPolicy(enum.Enum):
    '''The default policy to use when load shedding.

    A random policy randomly sheds a given percent of requests. A hash policy computes a hash over the CF-Connecting-IP address and sheds all requests originating from a percent of IPs.

    :schema: LoadSheddingDefaultPolicy
    '''

    HASH = "HASH"
    '''hash.'''
    RANDOM = "RANDOM"
    '''random.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.LoadSheddingSessionPolicy"
)
class LoadSheddingSessionPolicy(enum.Enum):
    '''Session Policy.

    :schema: LoadSheddingSessionPolicy
    '''

    HASH = "HASH"
    '''hash.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-pool.Origin",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "enabled": "enabled",
        "name": "name",
        "weight": "weight",
    },
)
class Origin:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param address: 
        :param enabled: 
        :param name: 
        :param weight: 

        :schema: Origin
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805e0cf6c9c9be3b05d92d05ecff43e9ce3fdc8ab6c17f76905e156a4a8c496e)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if enabled is not None:
            self._values["enabled"] = enabled
        if name is not None:
            self._values["name"] = name
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Origin#Address
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Origin#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Origin#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Origin#Weight
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Origin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnPool",
    "CfnPoolProps",
    "CfnPoolPropsOriginSteering",
    "CfnPoolPropsOriginSteeringPolicy",
    "Filter",
    "FilterPool",
    "LoadShedding",
    "LoadSheddingDefaultPolicy",
    "LoadSheddingSessionPolicy",
    "Origin",
]

publication.publish()

def _typecheckingstub__8147ea72c3bf5a2d14b1b48a0eb4f0df7d8cf18f217e476fd619bd5207ba1437(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    origins: typing.Sequence[typing.Union[Origin, typing.Dict[builtins.str, typing.Any]]],
    account_identifier: typing.Optional[builtins.str] = None,
    check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    latitude: typing.Optional[jsii.Number] = None,
    load_shedding: typing.Optional[typing.Union[LoadShedding, typing.Dict[builtins.str, typing.Any]]] = None,
    longitude: typing.Optional[jsii.Number] = None,
    minimum_origins: typing.Optional[jsii.Number] = None,
    monitor: typing.Optional[builtins.str] = None,
    notification_email: typing.Optional[builtins.str] = None,
    notification_filter: typing.Optional[typing.Union[Filter, typing.Dict[builtins.str, typing.Any]]] = None,
    origin_steering: typing.Optional[typing.Union[CfnPoolPropsOriginSteering, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e36b1f1c49690c0647395d80cc91f0c8bdaea8bd84934685e738c4cca23b06(
    *,
    name: builtins.str,
    origins: typing.Sequence[typing.Union[Origin, typing.Dict[builtins.str, typing.Any]]],
    account_identifier: typing.Optional[builtins.str] = None,
    check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    latitude: typing.Optional[jsii.Number] = None,
    load_shedding: typing.Optional[typing.Union[LoadShedding, typing.Dict[builtins.str, typing.Any]]] = None,
    longitude: typing.Optional[jsii.Number] = None,
    minimum_origins: typing.Optional[jsii.Number] = None,
    monitor: typing.Optional[builtins.str] = None,
    notification_email: typing.Optional[builtins.str] = None,
    notification_filter: typing.Optional[typing.Union[Filter, typing.Dict[builtins.str, typing.Any]]] = None,
    origin_steering: typing.Optional[typing.Union[CfnPoolPropsOriginSteering, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0030a2eb33023acedbb1cb9e0e6fad8f902565da356b817fcb99a5e58a1ffc2b(
    *,
    policy: typing.Optional[CfnPoolPropsOriginSteeringPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb980c57fa16f46075d9474f43f56b719185baa9afa8490a3d8f5f8ec04ffa20(
    *,
    pool: typing.Optional[typing.Union[FilterPool, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64253a1ee111c5be5906021923add76598f07554d0c8609cca847ea7abfa7981(
    *,
    healthy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c00ecef4c70106d8765d5bb5fe8fb85d2ff6af0ac5a12d2b1efde2c0b9ebfcd(
    *,
    default_percent: typing.Optional[jsii.Number] = None,
    default_policy: typing.Optional[LoadSheddingDefaultPolicy] = None,
    session_percent: typing.Optional[jsii.Number] = None,
    session_policy: typing.Optional[LoadSheddingSessionPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805e0cf6c9c9be3b05d92d05ecff43e9ce3fdc8ab6c17f76905e156a4a8c496e(
    *,
    address: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
