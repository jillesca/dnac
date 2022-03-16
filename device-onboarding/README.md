# PNP onboarding

The script will create a template config. It will create a network profile and assigned it to a site. Currently the script doesn't link the network profile and template.

Then the script will claim a device that already appears on the PNP as unclaimed.

The assigment is based on the serial number of the device

To claim a device to a site using `/dna/intent/api/v1/onboarding/pnp-device/site-claim` you need to send this payload.

```json
payload = {
    "siteId": siteId,
        "deviceId": deviceId,
        "type": "Default",
        "imageInfo": {"imageId": imageId, "skip": False},
        "configInfo": {"configId": configId, "configParameters": params}
} 
```

The documentation doesn't mention about `imageInfo` and `configInfo` but these are required.

The script will not also fill any configuration parameters defined on the template. If you want to do it, you need to defined `params` under `configPrameters` on `configInfo`

This script is based from:

- <https://github.com/cisco-en-programmability/usecases_sample_code/blob/master/device-onboarding/device-onboarding-functions.py>

- <https://developer.cisco.com/docs/dna-center/#!device-onboarding/site-profile-api>

## More examples

<https://github.com/CiscoDevNet/DNAC-onboarding-tools/tree/master/PnP-BulkConfig-128>
