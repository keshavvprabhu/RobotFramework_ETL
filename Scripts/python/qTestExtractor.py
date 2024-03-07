import requests

# Replace these values with your actual qTest parameters
base_url = "https://your-qtest-url.com"
api_token = "your-api-token"
project_id = "your-project-id"

def get_test_execution_stats():
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Get test runs for the project
    test_runs_url = f"{base_url}/api/v3/projects/{project_id}/test-runs"
    response = requests.get(test_runs_url, headers=headers)

    if response.status_code == 200:
        test_runs = response.json()
        total_executions = len(test_runs)
        passed_executions = sum(1 for run in test_runs if run["status"] == "PASSED")
        failed_executions = sum(1 for run in test_runs if run["status"] == "FAILED")
        print("Test Execution Stats:")
        print(f"Total Executions: {total_executions}")
        print(f"Passed Executions: {passed_executions}")
        print(f"Failed Executions: {failed_executions}")
    else:
        print(f"Failed to fetch test runs. Status code: {response.status_code}")

if __name__ == "__main__":
    get_test_execution_stats()
