# coding: utf-8

import types
import six

from ctcloudsdkcore.region.region import Region
from ctcloudsdkcore.region.provider import RegionProviderChain

class EcsRegion:
    _PROVIDER = RegionProviderChain.get_default_region_provider_chain("ECS")

    RU_MOSCOW_1 = Region("ru-moscow-1",
                        "https://ecs.ru-moscow-1.hc.sbercloud.ru")

    static_fields = {
        "ru-moscow-1": RU_MOSCOW_1,
    }

    @classmethod
    def value_of(cls, region_id, static_fields=None):
        if not region_id:
            raise KeyError("Unexpected empty parameter: region_id.")

        fields = static_fields if static_fields else cls.static_fields

        region = cls._PROVIDER.get_region(region_id)
        if region:
            return region

        if region_id in fields:
            return fields.get(region_id)

        raise KeyError("Unexpected region_id: " + region_id)


