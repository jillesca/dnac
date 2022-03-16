# Modules import
import requests
from requests.auth import HTTPBasicAuth
import time
import sys

# Disable SSL warnings. Not needed in production environments with valid certificates
import urllib3
urllib3.disable_warnings()

# Authentication
BASE_URL = 'https://dnac'
AUTH_URL = '/dna/system/api/v1/auth/token'
USERNAME = 'username'
PASSWORD = 'password'

# URLs
SITE_PROFILE_ADD_SITE_URL = '/api/v1/siteprofile/{site_profile_id}/site/{site_id}'
SITE_PROFILE_URL = '/api/v1/siteprofile'
SITE_URL = '/dna/intent/api/v1/site'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'
TEMPLATE_PROJECT_URL = '/dna/intent/api/v1/template-programmer/project'
TEMPLATE_URL = '/dna/intent/api/v1/template-programmer/project/{project_id}/template'
TEMPLATE_VERSION_URL = '/dna/intent/api/v1/template-programmer/template/version'
ONBOARDING_PNP_DEVICE_LIST = '/dna/intent/api/v1/onboarding/pnp-device'
ONBOARDING_PNP_IMPORT_URL = '/dna/intent/api/v1/onboarding/pnp-device/import'
ONBOARDING_CLAIM_DEVICE_URL = '/dna/intent/api/v1/onboarding/pnp-device/site-claim'

# Get Authentication token


def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get list of sites


def get_sites(headers):
    response = requests.get(BASE_URL + SITE_URL,
                            headers=headers, verify=False)
    return response.json()['response']

# Get template configuration project


def get_configuration_template_project(headers):
    response = requests.get(BASE_URL + TEMPLATE_PROJECT_URL,
                            headers=headers,
                            verify=False)
    return response.json()

# Create template


def create_configuration_template(headers, project_id, template):
    response = requests.post(BASE_URL + TEMPLATE_URL.format(project_id=project_id),
                             headers=headers, json=template,
                             verify=False)
    return response.json()['response']

# Create configuration template version


def create_configuration_template_version(headers, template_version):
    response = requests.post(BASE_URL + TEMPLATE_VERSION_URL,
                             headers=headers, json=template_version,
                             verify=False)
    return response.json()['response']

# Create site profile


def create_site_profile(headers, site_profile_info):
    response = requests.post(BASE_URL + SITE_PROFILE_URL,
                             headers=headers, json=site_profile_info,
                             verify=False)
    return response.json()['response']

# Assign Site to Site Profile


def assign_site_to_site_profile(headers, site_profile_id, site_id):
    response = requests.post(BASE_URL +
                             SITE_PROFILE_ADD_SITE_URL.format(site_profile_id=site_profile_id,
                                                              site_id=site_id),
                             headers=headers, verify=False)
    return response.json()

# Get list of devices in PNP


def get_device_pnp(headers):
    response = requests.get(BASE_URL + ONBOARDING_PNP_DEVICE_LIST,
                            headers=headers,
                            verify=False)
    return response.json()

# Import device to PnP process


def import_device_to_pnp(headers, pnp_import_info):
    response = requests.post(BASE_URL + ONBOARDING_PNP_IMPORT_URL,
                             headers=headers, json=pnp_import_info,
                             verify=False)
    return response.json()

# Import device to PnP process


def claim_device_to_site(headers, claim_info):
    response = requests.post(BASE_URL + ONBOARDING_CLAIM_DEVICE_URL,
                             headers=headers, json=claim_info,
                             verify=False)
    return response.json()

# Get Task result


def get_task(headers, task_id):
    response = requests.get(BASE_URL + TASK_BY_ID_URL.format(task_id=task_id),
                            headers=headers, verify=False)
    return response.json()['response']


def main():
    site_name = ''
    # # Get Device IP and Name using Serial Number
    device_serial = ''
    device_name = 'PNP-test'
    device_pid = 'C9300-24P'
    project_name = "Onboarding Configuration"
    template_name = 'API PNP Test Template'
    profile_name = 'API PNP Test Teamplate'

    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # Get Site ID
    response = get_sites(headers)
    site_id = ''
    for site in response:
        if site['name'] == site_name:
            site_id = site['id']

    print(f'Printing site name {site_name} site id {site_id}')

    # Get Project information
    response = get_configuration_template_project(headers)
    project_id = ''
    for project in response:
        if project['name'] == project_name:
            project_id = project['id']

    # Create Configuration Template
    template_info = {
        "name": template_name,
        "description": "Guide Configuration Template",
        "tags": [],
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs",
                "productSeries": "Cisco Catalyst 9300 Series Switches"
            }
        ],
        "softwareType": "IOS-XE",
        "softwareVariant": "XE",
        "templateContent": "ip access-list extended $permitACLName\npermit ip 10.0.0.0 0.255.255.25.0 any\npermit ip 172.16.0.0 0.15.255.255 any\npermit ip 192.168.0.0 0.0.255.255 any\n!\n\nip access-list extended $denyACLName\ndeny ip 10.0.0.0 0.255.255.25.0 any\ndeny ip 172.16.0.0 0.15.255.255 any\ndeny ip 192.168.0.0 0.0.255.255 any\n!\n",
        "rollbackTemplateContent": "",
        "templateParams": [
            {
                "parameterName": "permitACLName",
                "dataType": "STRING",
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 1,
                "selection": {
                    "selectionType": None,
                    "selectionValues": {},
                    "defaultSelectedValues": []
                },
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            },
            {
                "parameterName": "denyACLName",
                "dataType": "STRING",
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 2,
                "selection": {
                    "selectionType": None,
                    "selectionValues": {},
                    "defaultSelectedValues": []
                },
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            }
        ],
        "rollbackTemplateParams": [],
        "composite": False,
        "containingTemplates": []
    }

    response = create_configuration_template(
        headers, project_id, template_info)
    task_id = response['taskId']

    time.sleep(3)
    response = get_task(headers, task_id)
    template_id = response['data']

    # Create Template version
    template_version = {
        "comments": f"{template_name} Initial Version",
        "templateId": template_id
    }
    create_configuration_template_version(headers, template_version)

    # Create Configuration Template
    site_profile_info = {
        "name": profile_name,
        "namespace": "switching",
        "profileAttributes": [
            {
                "key": "day0.templates",
                "attribs": [
                    {
                        "key": "device.family",
                        "value": "Switches and Hubs",
                        "attribs": [
                            {
                                "key": "device.series",
                                "value": "Cisco Catalyst 9300 Series Switches",
                                "attribs": [
                                    {
                                        "key": "device.type",
                                        "attribs": [
                                            {
                                                "key": "template.id",
                                                "value": template_id,
                                            },
                                            {
                                                "key": "device.tag",
                                                "value": "",
                                                "attribs": [

                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    response = create_site_profile(headers, site_profile_info)
    task_id = response['taskId']
    time.sleep(3)
    response = get_task(headers, task_id)

    site_profile_id = response['progress'].split(" ")[2][1:-1]
    response = assign_site_to_site_profile(headers, site_profile_id, site_id)

    pnp_devices = get_device_pnp(headers)
    device_id = ''
    for device in pnp_devices:
        if device['deviceInfo']['serialNumber'] == device_serial:
            device_id = device['id']

    claim_info = {
        "siteId": site_id,
        "deviceId": device_id,
        "type": "Default",
        "imageInfo": {"imageId": "", "skip": True},
        "configInfo": {"configId": "", "skip": True}
    }

    claim_device_to_site(headers, claim_info)


if __name__ == "__main__":
    main()
