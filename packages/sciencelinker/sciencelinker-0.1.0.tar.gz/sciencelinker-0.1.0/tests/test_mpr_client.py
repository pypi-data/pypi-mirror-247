from sciencelinker import mpr_client
import time
import os


def delete_dir(file_object):
    if os.path.isdir(file_object):
        for child_fo in os.listdir(file_object):
            delete_dir(os.path.join(file_object, child_fo))
        os.removedirs(file_object)
    else:
        os.remove(file_object)


# Create a client for requests
#service_url = 'http://svko-sclinker-test.gesis.intra/sl-services'
service_url = 'http://localhost:5000'
c = mpr_client.MPRClient(service_url)

# Check service availability
if c.check_service_availability():
    print("Service available")

# Check MOTD
motd = c.get_motd()
print(f"MOTD {motd}")

# Display available data
data_info = c.get_data_info()
print(f"Available data\n{data_info}")

# Create a task
d_task = '''{
  "name": "micropost-retrieval",
  "language": "en",
  "start-date": "2022-01-01",
  "end-date": "2022-12-31",
  "seedlist": ["immigration", "emigration", "migration", "customs", "refugee", "foreigner"]
}'''
job_url = c.create_task(d_task, 'testuser', 'testtest')
print(f"Created a job with URL {job_url}")

# Wait for the job to finish
d_job = c.check_job_status(job_url, 'testuser', 'testtest')
print(f"Current job status \"{d_job['status']}\"")
while d_job['status'] != 'succeeded' and d_job['status'] != 'failed':
    time.sleep(5)
    d_job = c.check_job_status(job_url, 'testuser', 'testtest')
    print(f"Current job status \"{d_job['status']}\"")

if d_job['status'] == 'succeeded':
    print(f"Result items: {d_job['result-items']}")
else:
    print(f"Reason of failure: {d_job['reason-of_failure']}")

# Retrieve the results
if not os.path.exists('client_output'):
    os.mkdir('client_output')

for result_item in d_job['result-items']:
    target_file = result_item[result_item.rfind('/') + 1:]
    c.get_result_item(result_item, f"client_output/{target_file}", 'testuser', 'testtest')

if len(os.listdir('client_output')) == 10:
    print('Test OK')
else:
    print('Test failed')
delete_dir('client_output')
