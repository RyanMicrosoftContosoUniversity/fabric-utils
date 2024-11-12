"""
Test file for performing etl on scan results
"""
import json
# import src.table as table   
import fabric_automation_utils.table as table


source_file = 'docs\sample_scan_response.json'

with open(source_file, 'r') as f:
    data = json.load(f)

# handle file workspaces -- ignore datasourceInstances and isconfiguredDatasourceInstances for now
for workspace in data['workspaces']:
    # create workspace object
    workspace_table = table.Workspace_table(name=workspace['name'], id=workspace['id'], type=workspace['type'], 
                                            isOnDedicatedCapacity=workspace['isOnDedicatedCapacity'], capacityId=workspace['capacityId'],
                                            defaultDatasetStorageFormat=workspace['defaultDatasetStorageFormat'], reports=workspace['reports'], dashboards=workspace['dashboards'],
                                            dataflows=workspace['dataflows'], datamarts=workspace['datamarts'], datasets=workspace['datasets'], users=workspace['users'])
