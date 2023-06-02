from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient

import os
import xlsxwriter

load_dotenv()
credential = DefaultAzureCredential()

subscription_id = os.getenv('SUBSCRIPTION_ID')
resource_group_name = os.getenv('RESOURCE_GROUP_NAME')
location = 'eastus2'

client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

workbook = xlsxwriter.Workbook('azure-resources-report.xlsx')
worksheet = workbook.add_worksheet()

resource_list_result = client.resources.list_by_resource_group(resource_group_name)

headersL1 = [
    "Resource",
    "Storage Account",
]
headersL2 = [
    # RESOURCE
    "Type".ljust(35),
    "Location".ljust(10),
    "Name".ljust(25),
    "Kind".ljust(10),
    # STORAGE ACCOUNT
    "Access tier",
    "Enable HTTPS traffic only",
    "Allow blob public access",
    "Minimum TLS version",
    "Allow shared key access",
    "Allow cross tenant replication",
    "Default to Oauth authentication",
    "Public network access"
]

print(headersL1[0].ljust(83), headersL1[1].ljust(200))
print("%35s" % (' '.join(headersL2)))
for resource in resource_list_result:
    if resource.kind is not None and resource.type == 'Microsoft.Storage/storageAccounts':
        storage_account = storage_client.storage_accounts.get_properties(resource_group_name, resource.name)
        print(
            resource.type.ljust(35),
            resource.location.ljust(10),
            resource.name.ljust(25),
            resource.kind.ljust(10),
            storage_account.access_tier.ljust(11),
            str(storage_account.enable_https_traffic_only).ljust(25),
            str(storage_account.allow_blob_public_access).ljust(24),
            storage_account.minimum_tls_version.ljust(19),
            str( storage_account.allow_shared_key_access).ljust(23),
            str(storage_account.allow_cross_tenant_replication).ljust(30),
            str(storage_account.default_to_o_auth_authentication).ljust(32),
            storage_account.public_network_access.ljust(10)

        )
    # else:
    #     print(resource.type,
    #         resource.location,resource.name,resource.kind)

workbook.close()

# compute_client = ComputeManagementClient(credential, subscription_id)
# vm_sizes = compute_client.virtual_machine_sizes.list(location)
#
# for size in vm_sizes:
#     print(size.as_dict())
