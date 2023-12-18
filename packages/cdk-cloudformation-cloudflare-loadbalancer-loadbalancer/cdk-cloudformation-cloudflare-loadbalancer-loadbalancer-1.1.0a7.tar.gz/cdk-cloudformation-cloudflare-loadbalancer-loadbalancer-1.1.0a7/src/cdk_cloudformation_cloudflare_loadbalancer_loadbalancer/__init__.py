'''
# cloudflare-loadbalancer-loadbalancer

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Cloudflare::LoadBalancer::LoadBalancer` v1.1.0.

## Description

A Cloudflare resource for managing load-balancing across pools

## References

* [Documentation](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Cloudflare::LoadBalancer::LoadBalancer \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Cloudflare-LoadBalancer-LoadBalancer \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Cloudflare::LoadBalancer::LoadBalancer`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fcloudflare-loadbalancer-loadbalancer+v1.1.0).
* Issues related to `Cloudflare::LoadBalancer::LoadBalancer` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-cloudflare-resource-providers).

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


class CfnLoadBalancer(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-loadbalancer.CfnLoadBalancer",
):
    '''A CloudFormation ``Cloudflare::LoadBalancer::LoadBalancer``.

    :cloudformationResource: Cloudflare::LoadBalancer::LoadBalancer
    :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        zone_id: builtins.str,
        country_pools: typing.Any = None,
        default_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        fallback_pool: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pop_pools: typing.Any = None,
        proxied: typing.Optional[builtins.bool] = None,
        random_steering: typing.Optional[typing.Union["CfnLoadBalancerPropsRandomSteering", typing.Dict[builtins.str, typing.Any]]] = None,
        region_pools: typing.Any = None,
        rules: typing.Optional[typing.Sequence[typing.Any]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_attributes: typing.Any = None,
        session_affinity_ttl: typing.Optional[jsii.Number] = None,
        steering_policy: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Cloudflare::LoadBalancer::LoadBalancer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param zone_id: The zone ID to add the load balancer to.
        :param country_pools: A set containing mappings of country codes to a list of pool IDs (ordered by their failover priority) for the given country.
        :param default_pools: A list of pool IDs ordered by their failover priority. Pools defined here are used by default, or when region_pools are not configured for a given region
        :param description: Free text description.
        :param enabled: Enable or disable the load balancer. Defaults to true (enabled). Default: true (enabled).
        :param fallback_pool: he pool ID to use when all other pools are detected as unhealthy.
        :param name: The DNS name (FQDN, including the zone) to associate with the load balancer.
        :param pop_pools: A set containing mappings of Cloudflare Point-of-Presence (PoP) identifiers to a list of pool IDs (ordered by their failover priority) for the PoP (datacenter). This feature is only available to enterprise customers
        :param proxied: Whether the hostname gets Cloudflare's origin protection. Defaults to false. Default: false.
        :param random_steering: Configures pool weights for random steering. When steering_policy is 'random', a random pool is selected with probability proportional to these pool weights
        :param region_pools: A set containing mappings of region codes to a list of pool IDs (ordered by their failover priority) for the given region.
        :param rules: A list of conditions and overrides for each load balancer operation.
        :param session_affinity: Associates all requests coming from an end-user with a single origin. Cloudflare will set a cookie on the initial response to the client, such that consequent requests with the cookie in the request will go to the same origin, so long as it is available
        :param session_affinity_attributes: Configure cookie attributes for session affinity cookie.
        :param session_affinity_ttl: Time, in seconds, until this load balancers session affinity cookie expires after being created. This parameter is ignored unless a supported session affinity policy is set. The current default of 23 hours will be used unless session_affinity_ttl is explicitly set. Once the expiry time has been reached, subsequent requests may get sent to a different origin server. Valid values are between 1800 and 604800.
        :param steering_policy: Determine which method the load balancer uses to determine the fastest route to your origin.
        :param ttl: Time to live (TTL) of this load balancer's DNS name. Conflicts with proxied - this cannot be set for proxied load balancers. Default is 30. Default: 30.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3cc73b306f86eff54cb5a5acd6a92373b636705e6043a28208154ac19f5813)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoadBalancerProps(
            zone_id=zone_id,
            country_pools=country_pools,
            default_pools=default_pools,
            description=description,
            enabled=enabled,
            fallback_pool=fallback_pool,
            name=name,
            pop_pools=pop_pools,
            proxied=proxied,
            random_steering=random_steering,
            region_pools=region_pools,
            rules=rules,
            session_affinity=session_affinity,
            session_affinity_attributes=session_affinity_attributes,
            session_affinity_ttl=session_affinity_ttl,
            steering_policy=steering_policy,
            ttl=ttl,
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
        '''Attribute ``Cloudflare::LoadBalancer::LoadBalancer.CreatedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedOn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Cloudflare::LoadBalancer::LoadBalancer.Id``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedOn")
    def attr_modified_on(self) -> builtins.str:
        '''Attribute ``Cloudflare::LoadBalancer::LoadBalancer.ModifiedOn``.

        :link: https://github.com/aws-ia/cloudformation-cloudflare-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnLoadBalancerProps":
        '''Resource props.'''
        return typing.cast("CfnLoadBalancerProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-loadbalancer.CfnLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "zone_id": "zoneId",
        "country_pools": "countryPools",
        "default_pools": "defaultPools",
        "description": "description",
        "enabled": "enabled",
        "fallback_pool": "fallbackPool",
        "name": "name",
        "pop_pools": "popPools",
        "proxied": "proxied",
        "random_steering": "randomSteering",
        "region_pools": "regionPools",
        "rules": "rules",
        "session_affinity": "sessionAffinity",
        "session_affinity_attributes": "sessionAffinityAttributes",
        "session_affinity_ttl": "sessionAffinityTtl",
        "steering_policy": "steeringPolicy",
        "ttl": "ttl",
    },
)
class CfnLoadBalancerProps:
    def __init__(
        self,
        *,
        zone_id: builtins.str,
        country_pools: typing.Any = None,
        default_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        fallback_pool: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pop_pools: typing.Any = None,
        proxied: typing.Optional[builtins.bool] = None,
        random_steering: typing.Optional[typing.Union["CfnLoadBalancerPropsRandomSteering", typing.Dict[builtins.str, typing.Any]]] = None,
        region_pools: typing.Any = None,
        rules: typing.Optional[typing.Sequence[typing.Any]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_attributes: typing.Any = None,
        session_affinity_ttl: typing.Optional[jsii.Number] = None,
        steering_policy: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''A Cloudflare resource for managing load-balancing across pools.

        :param zone_id: The zone ID to add the load balancer to.
        :param country_pools: A set containing mappings of country codes to a list of pool IDs (ordered by their failover priority) for the given country.
        :param default_pools: A list of pool IDs ordered by their failover priority. Pools defined here are used by default, or when region_pools are not configured for a given region
        :param description: Free text description.
        :param enabled: Enable or disable the load balancer. Defaults to true (enabled). Default: true (enabled).
        :param fallback_pool: he pool ID to use when all other pools are detected as unhealthy.
        :param name: The DNS name (FQDN, including the zone) to associate with the load balancer.
        :param pop_pools: A set containing mappings of Cloudflare Point-of-Presence (PoP) identifiers to a list of pool IDs (ordered by their failover priority) for the PoP (datacenter). This feature is only available to enterprise customers
        :param proxied: Whether the hostname gets Cloudflare's origin protection. Defaults to false. Default: false.
        :param random_steering: Configures pool weights for random steering. When steering_policy is 'random', a random pool is selected with probability proportional to these pool weights
        :param region_pools: A set containing mappings of region codes to a list of pool IDs (ordered by their failover priority) for the given region.
        :param rules: A list of conditions and overrides for each load balancer operation.
        :param session_affinity: Associates all requests coming from an end-user with a single origin. Cloudflare will set a cookie on the initial response to the client, such that consequent requests with the cookie in the request will go to the same origin, so long as it is available
        :param session_affinity_attributes: Configure cookie attributes for session affinity cookie.
        :param session_affinity_ttl: Time, in seconds, until this load balancers session affinity cookie expires after being created. This parameter is ignored unless a supported session affinity policy is set. The current default of 23 hours will be used unless session_affinity_ttl is explicitly set. Once the expiry time has been reached, subsequent requests may get sent to a different origin server. Valid values are between 1800 and 604800.
        :param steering_policy: Determine which method the load balancer uses to determine the fastest route to your origin.
        :param ttl: Time to live (TTL) of this load balancer's DNS name. Conflicts with proxied - this cannot be set for proxied load balancers. Default is 30. Default: 30.

        :schema: CfnLoadBalancerProps
        '''
        if isinstance(random_steering, dict):
            random_steering = CfnLoadBalancerPropsRandomSteering(**random_steering)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0ae9efebf8d40d7f23afd439fe4b89bc425ffee15d86c08448ca6d231de228)
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument country_pools", value=country_pools, expected_type=type_hints["country_pools"])
            check_type(argname="argument default_pools", value=default_pools, expected_type=type_hints["default_pools"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument fallback_pool", value=fallback_pool, expected_type=type_hints["fallback_pool"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pop_pools", value=pop_pools, expected_type=type_hints["pop_pools"])
            check_type(argname="argument proxied", value=proxied, expected_type=type_hints["proxied"])
            check_type(argname="argument random_steering", value=random_steering, expected_type=type_hints["random_steering"])
            check_type(argname="argument region_pools", value=region_pools, expected_type=type_hints["region_pools"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument session_affinity_attributes", value=session_affinity_attributes, expected_type=type_hints["session_affinity_attributes"])
            check_type(argname="argument session_affinity_ttl", value=session_affinity_ttl, expected_type=type_hints["session_affinity_ttl"])
            check_type(argname="argument steering_policy", value=steering_policy, expected_type=type_hints["steering_policy"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "zone_id": zone_id,
        }
        if country_pools is not None:
            self._values["country_pools"] = country_pools
        if default_pools is not None:
            self._values["default_pools"] = default_pools
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if fallback_pool is not None:
            self._values["fallback_pool"] = fallback_pool
        if name is not None:
            self._values["name"] = name
        if pop_pools is not None:
            self._values["pop_pools"] = pop_pools
        if proxied is not None:
            self._values["proxied"] = proxied
        if random_steering is not None:
            self._values["random_steering"] = random_steering
        if region_pools is not None:
            self._values["region_pools"] = region_pools
        if rules is not None:
            self._values["rules"] = rules
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if session_affinity_attributes is not None:
            self._values["session_affinity_attributes"] = session_affinity_attributes
        if session_affinity_ttl is not None:
            self._values["session_affinity_ttl"] = session_affinity_ttl
        if steering_policy is not None:
            self._values["steering_policy"] = steering_policy
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone ID to add the load balancer to.

        :schema: CfnLoadBalancerProps#ZoneId
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def country_pools(self) -> typing.Any:
        '''A set containing mappings of country codes to a list of pool IDs (ordered by their failover priority) for the given country.

        :schema: CfnLoadBalancerProps#CountryPools
        '''
        result = self._values.get("country_pools")
        return typing.cast(typing.Any, result)

    @builtins.property
    def default_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of pool IDs ordered by their failover priority.

        Pools defined here are used by default, or when region_pools are not configured for a given region

        :schema: CfnLoadBalancerProps#DefaultPools
        '''
        result = self._values.get("default_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Free text description.

        :schema: CfnLoadBalancerProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable the load balancer.

        Defaults to true (enabled).

        :default: true (enabled).

        :schema: CfnLoadBalancerProps#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fallback_pool(self) -> typing.Optional[builtins.str]:
        '''he pool ID to use when all other pools are detected as unhealthy.

        :schema: CfnLoadBalancerProps#FallbackPool
        '''
        result = self._values.get("fallback_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The DNS name (FQDN, including the zone) to associate with the load balancer.

        :schema: CfnLoadBalancerProps#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pop_pools(self) -> typing.Any:
        '''A set containing mappings of Cloudflare Point-of-Presence (PoP) identifiers to a list of pool IDs (ordered by their failover priority) for the PoP (datacenter).

        This feature is only available to enterprise customers

        :schema: CfnLoadBalancerProps#PopPools
        '''
        result = self._values.get("pop_pools")
        return typing.cast(typing.Any, result)

    @builtins.property
    def proxied(self) -> typing.Optional[builtins.bool]:
        '''Whether the hostname gets Cloudflare's origin protection.

        Defaults to false.

        :default: false.

        :schema: CfnLoadBalancerProps#Proxied
        '''
        result = self._values.get("proxied")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def random_steering(self) -> typing.Optional["CfnLoadBalancerPropsRandomSteering"]:
        '''Configures pool weights for random steering.

        When steering_policy is 'random', a random pool is selected with probability proportional to these pool weights

        :schema: CfnLoadBalancerProps#RandomSteering
        '''
        result = self._values.get("random_steering")
        return typing.cast(typing.Optional["CfnLoadBalancerPropsRandomSteering"], result)

    @builtins.property
    def region_pools(self) -> typing.Any:
        '''A set containing mappings of region codes to a list of pool IDs (ordered by their failover priority) for the given region.

        :schema: CfnLoadBalancerProps#RegionPools
        '''
        result = self._values.get("region_pools")
        return typing.cast(typing.Any, result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List[typing.Any]]:
        '''A list of conditions and overrides for each load balancer operation.

        :schema: CfnLoadBalancerProps#Rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Associates all requests coming from an end-user with a single origin.

        Cloudflare will set a cookie on the initial response to the client, such that consequent requests with the cookie in the request will go to the same origin, so long as it is available

        :schema: CfnLoadBalancerProps#SessionAffinity
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity_attributes(self) -> typing.Any:
        '''Configure cookie attributes for session affinity cookie.

        :schema: CfnLoadBalancerProps#SessionAffinityAttributes
        '''
        result = self._values.get("session_affinity_attributes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def session_affinity_ttl(self) -> typing.Optional[jsii.Number]:
        '''Time, in seconds, until this load balancers session affinity cookie expires after being created.

        This parameter is ignored unless a supported session affinity policy is set. The current default of 23 hours will be used unless session_affinity_ttl is explicitly set. Once the expiry time has been reached, subsequent requests may get sent to a different origin server. Valid values are between 1800 and 604800.

        :schema: CfnLoadBalancerProps#SessionAffinityTtl
        '''
        result = self._values.get("session_affinity_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def steering_policy(self) -> typing.Optional[builtins.str]:
        '''Determine which method the load balancer uses to determine the fastest route to your origin.

        :schema: CfnLoadBalancerProps#SteeringPolicy
        '''
        result = self._values.get("steering_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''Time to live (TTL) of this load balancer's DNS name.

        Conflicts with proxied - this cannot be set for proxied load balancers. Default is 30.

        :default: 30.

        :schema: CfnLoadBalancerProps#Ttl
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cloudflare-loadbalancer-loadbalancer.CfnLoadBalancerPropsRandomSteering",
    jsii_struct_bases=[],
    name_mapping={"default_weight": "defaultWeight"},
)
class CfnLoadBalancerPropsRandomSteering:
    def __init__(self, *, default_weight: typing.Optional[jsii.Number] = None) -> None:
        '''Configures pool weights for random steering.

        When steering_policy is 'random', a random pool is selected with probability proportional to these pool weights

        :param default_weight: 

        :schema: CfnLoadBalancerPropsRandomSteering
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da48fa302472e4790a8cc530770c38c7669db906776a9137e78c817072e0604)
            check_type(argname="argument default_weight", value=default_weight, expected_type=type_hints["default_weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_weight is not None:
            self._values["default_weight"] = default_weight

    @builtins.property
    def default_weight(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnLoadBalancerPropsRandomSteering#DefaultWeight
        '''
        result = self._values.get("default_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerPropsRandomSteering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLoadBalancer",
    "CfnLoadBalancerProps",
    "CfnLoadBalancerPropsRandomSteering",
]

publication.publish()

def _typecheckingstub__0e3cc73b306f86eff54cb5a5acd6a92373b636705e6043a28208154ac19f5813(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    zone_id: builtins.str,
    country_pools: typing.Any = None,
    default_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    fallback_pool: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pop_pools: typing.Any = None,
    proxied: typing.Optional[builtins.bool] = None,
    random_steering: typing.Optional[typing.Union[CfnLoadBalancerPropsRandomSteering, typing.Dict[builtins.str, typing.Any]]] = None,
    region_pools: typing.Any = None,
    rules: typing.Optional[typing.Sequence[typing.Any]] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    session_affinity_attributes: typing.Any = None,
    session_affinity_ttl: typing.Optional[jsii.Number] = None,
    steering_policy: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0ae9efebf8d40d7f23afd439fe4b89bc425ffee15d86c08448ca6d231de228(
    *,
    zone_id: builtins.str,
    country_pools: typing.Any = None,
    default_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    fallback_pool: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pop_pools: typing.Any = None,
    proxied: typing.Optional[builtins.bool] = None,
    random_steering: typing.Optional[typing.Union[CfnLoadBalancerPropsRandomSteering, typing.Dict[builtins.str, typing.Any]]] = None,
    region_pools: typing.Any = None,
    rules: typing.Optional[typing.Sequence[typing.Any]] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    session_affinity_attributes: typing.Any = None,
    session_affinity_ttl: typing.Optional[jsii.Number] = None,
    steering_policy: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da48fa302472e4790a8cc530770c38c7669db906776a9137e78c817072e0604(
    *,
    default_weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
