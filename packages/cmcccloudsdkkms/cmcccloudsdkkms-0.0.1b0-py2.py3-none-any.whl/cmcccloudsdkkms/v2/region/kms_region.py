# coding: utf-8

import types
import six

from cmcccloudsdkcore.region.region import Region
from cmcccloudsdkcore.region.provider import RegionProviderChain

class KmsRegion:
    _PROVIDER = RegionProviderChain.get_default_region_provider_chain("KMS")

    CIDC_RP_11 = Region("CIDC-RP-11",
                        "https://kms.cidc-rp-11.joint.cmecloud.cn")
    CIDC_RP_12 = Region("CIDC-RP-12",
                        "https://kms.cidc-rp-12.joint.cmecloud.cn")
    CIDC_RP_13 = Region("CIDC-RP-13",
                        "https://kms.cidc-rp-13.joint.cmecloud.cn")
    CIDC_RP_19 = Region("CIDC-RP-19",
                        "https://kms.cidc-rp-19.joint.cmecloud.cn")
    CIDC_RP_2000 = Region("CIDC-RP-2000",
                        "https://kms.cidc-rp-2000.joint.cmecloud.cn")
    CIDC_RP_2005 = Region("CIDC-RP-2005",
                        "https://kms.cidc-rp-2005.joint.cmecloud.cn")
    CIDC_RP_2006 = Region("CIDC-RP-2006",
                        "https://kms.cidc-rp-2006.joint.cmecloud.cn")
    CIDC_RP_2011 = Region("CIDC-RP-2011",
                        "https://kms.cidc-rp-2011.joint.cmecloud.cn")

    static_fields = {
        "CIDC-RP-11": CIDC_RP_11,
        "CIDC-RP-12": CIDC_RP_12,
        "CIDC-RP-13": CIDC_RP_13,
        "CIDC-RP-19": CIDC_RP_19,
        "CIDC-RP-2000": CIDC_RP_2000,
        "CIDC-RP-2005": CIDC_RP_2005,
        "CIDC-RP-2006": CIDC_RP_2006,
        "CIDC-RP-2011": CIDC_RP_2011,
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


