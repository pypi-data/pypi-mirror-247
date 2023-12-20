import requests
from requests.auth import HTTPBasicAuth
import json


class MPRClient:
    """
    Client to perform micropost retrieval using the ScienceLinker Web Services (SLWS)
    """

    def __init__(self, service_url: str):
        """Create a client object

        :param service_url: Endpoint of a SLWS instance
        :type service_url: str
        """
        self.service_url = service_url

    def check_service_availability(self, verbose: bool = False) -> bool:
        """Checks if the SLWS are available.

        :param verbose: Prints additional information
        :type verbose: bool
        :return: True if the SLWS instance is available, otherwise false.
        :rtype: bool
        """
        r = requests.get(self.service_url)
        if verbose:
            print(f"Status code: {r.status_code}")
            print(f"Headers: {r.headers}")
            print(f"Body: {r.text}")
        if r.status_code == 200:
            return True
        else:
            return False

    def get_motd(self) -> str:
        """Retrieves the message of the day, from the connected SLWS instance.

        :return: The text of the message.
        :rtype: str
        """
        r = requests.get(self.service_url)
        if r.status_code == 200:
            return r.text
        else:
            raise Exception(f"Status_code {r.status_code}: {r.text}")

    def get_data_info(self) -> str:
        """Retrieves information about the provided dataset.

        :return: Information string.
        :rtype: str
        """
        r = requests.get(self.service_url + "/data-info")
        if r.status_code == 200:
            return r.text
        else:
            raise Exception(f"Status_code {r.status_code}: {r.text}")

    def create_task(self, task: str, user: str, pw: str, verbose: str = False) -> str:
        """Creates a job.

        :param task: Describes the task. See task descriptions.
        :type task: str
        :param user: The username for the SLWS.
        :type task: str
        :param pw: Password
        :type ps: str
        :param verbose: Print additional information
        :type verbose: bool
        :return: The ID of the newly created job
        :rtype: str
        """
        payload = {'task': task}
        basic = HTTPBasicAuth(user, pw)
        r = requests.get(self.service_url + "/micropost-retrieval/jobs/", params=payload, auth=basic)
        if verbose:
            print(f"Status code: {r.status_code}")
            print(f"Headers: {r.headers}")
            print(f"Body: {r.text}")
        if r.status_code == 201:
            return r.text
        else:
            raise Exception(f"Status_code {r.status_code}: {r.text}")

    def check_job_status(self, job_url: str, user: str, pw: str, verbose: bool = False) -> str:
        """Checks the status of a job.

        :param job_id: The job ID
        :type job_id: str
        :param user: Username for the SLWS
        :type user: str
        :param pw: Password
        :type pw: str
        :param verbose: Prints additional information
        :type verbose: bool
        :return: The job status. One of 'scheduled', 'executing', 'succeeded' or 'failed'
        :rtype: str
        """
        basic = HTTPBasicAuth(user, pw)
        r = requests.get(job_url, auth=basic)
        if verbose:
            print(f"Status code: {r.status_code}")
            print(f"Headers: {r.headers}")
            print(f"Body: {r.text}")
        if r.status_code == 200:
            d_job_status = json.loads(r.text)
            return d_job_status
        else:
            raise Exception(f"Status_code {r.status_code}: {r.text}")

    def get_result_item(self, item_url: str, target_file: str, user, pw, verbose: bool = False):
        """Retrieves result items.

        :param job_id: The job ID
        :type job_id: str
        :param item_id: The item ID
        :type item_id: str
        :param target_file: The file in which to store the result item
        :type target_file: str
        :param user: Username for SLWS
        :type user: str
        :param pw: Password
        :type pw: str
        :param verbose: Print additional information
        :type verbose: bool
        """
        basic = HTTPBasicAuth(user, pw)
        r = requests.get(item_url, auth=basic)
        if verbose:
            print(f"Status code: {r.status_code}")
            print(f"Headers: {r.headers}")
        if r.status_code == 200:
            fd = open(target_file, 'wb')
            fd.write(r.content)
            fd.close()
        else:
            raise Exception(f"Status_code {r.status_code}: {r.text}")
