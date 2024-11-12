import pytest
from unittest.mock import patch, MagicMock

from fabric_automation_utils.fabric_capacity import FabricCapacityMGMT
from fabric_automation_utils.service_principal import ServicePrincipal
import json
from fabric_automation_utils.fabric_capacity import FabricCapacityMGMT, FabricCapacitiesBySubscription

# load config for testing using docs/tests_config.json
config_data = json.loads(open('docs/non-prod-spn-config.json').read())
spn = ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
)
subscription_id = '910ebf13-1058-405d-b6cf-eda03e5288d1'
rg = 'fabric-rg'
cap_name = 'fabricf2testrh'

@pytest.fixture
def fabric_capacity_mgmt():
    spn = ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
    )

    subscription_id = '910ebf13-1058-405d-b6cf-eda03e5288d1'
    resource_group = 'fabric-rg'
    capacity_name = 'fabricf2testrh'
    return FabricCapacityMGMT(
        spn=spn,
        subscription_id=subscription_id,
        resource_group=resource_group,
        capacity_name=capacity_name
    )

@pytest.fixture
def fabric_capacities_by_subscription():
    spn = ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
    )

    subscription_id = '910ebf13-1058-405d-b6cf-eda03e5288d1'
    return FabricCapacitiesBySubscription(
        spn=spn,
        subscription_id=subscription_id
    )


@patch('azure.mgmt.fabric.FabricMgmtClient')
@patch('azure.identity.DefaultAzureCredential')
def test_get_capacity(mock_credential, mock_client, fabric_capacity_mgmt):
    mock_response = MagicMock()
    mock_response.properties = {'provisioningState': 'Succeeded', 'state': 'Active', 'administration': {'members': ['admin@MngEnvMCAP372892.onmicrosoft.com']}}
    mock_response.id = '/subscriptions/910ebf13-1058-405d-b6cf-eda03e5288d1/resourceGroups/fabric-rg/providers/Microsoft.Fabric/capacities/fabricf2testrh'
    mock_response.location = 'East US 2'
    mock_response.name = 'fabricf2testrh'
    mock_response.sku = 'F2'
    mock_response.admins = {'members': ['admin@MngEnvMCAP372892.onmicrosoft.com']}

    mock_client.return_value.fabric_capacities.get.return_value = mock_response

    response = fabric_capacity_mgmt.get_capacity()

    # assert response == mock_response
    assert fabric_capacity_mgmt.capacity_id == mock_response.id
    assert fabric_capacity_mgmt.location == mock_response.location
    assert fabric_capacity_mgmt.name == mock_response.name
    assert fabric_capacity_mgmt.sku == mock_response.sku
    assert fabric_capacity_mgmt.admins == mock_response.admins

# @patch('azure.mgmt.fabric.FabricMgmtClient')
# @patch('azure.identity.DefaultAzureCredential')
# def test_resume_capacity(mock_begin_resume, mock_credential, mock_client, fabric_capacity_mgmt):
#     # Set up the mock return value
#     mock_operation = MagicMock()
#     mock_begin_resume.return_value.result.return_value = mock_operation

#     # Call the resume_capacity method
#     response = fabric_capacity_mgmt.resume_capacity()

#     # Verify that begin_resume was called with the correct parameters
#     mock_begin_resume.assert_called_once_with(
#         resource_group_name=fabric_capacity_mgmt.resource_group,
#         capacity_name=fabric_capacity_mgmt.capacity_name
#     )

#     # Verify the response
#     assert response == mock_operation

@patch('azure.mgmt.fabric.FabricMgmtClient')
@patch('azure.identity.DefaultAzureCredential')
def test_list_capacities_by_subscription(mock_credential, mock_client, fabric_capacities_by_subscription):
    mock_response = MagicMock()
    mock_response.value = [
        {
            'id': '/subscriptions/910ebf13-1058-405d-b6cf-eda03e5288d1/resourceGroups/fabric-rg/providers/Microsoft.Fabric/capacities/fabricf2testrh',
            'location': 'East US 2',
            'name': 'fabricf2testrh',
            'properties': {'state': 'Active', 'administration': {'members': ['admin@MngEnvMCAP372892.onmicrosoft.com']}},
            'sku': {'name': 'F2'}
        }
    ]

    mock_client.return_value.fabric_capacities.list_by_subscription.return_value = mock_response

    response = fabric_capacities_by_subscription.list_capacities_by_subscription()

    assert response == mock_response
    assert len(response.value) == 1
    assert response.value[0]['name'] == 'fabricf2testrh'
    assert response.value[0]['location'] == 'East US 2'
    assert response.value[0]['sku']['name'] == 'F2'
    assert response.value[0]['properties']['state'] == 'Active'
    assert response.value[0]['properties']['administration']['members'] == ['admin@MngEnvMCAP372892.onmicrosoft.com']

