import os
import json
from datetime import datetime, timedelta


class RequestCache:

    def __init__(self, cache_directory='.request_cache'):
        self.cache_directory = cache_directory
        self.index_file_name = 'index.json'
        self.index_file = self.cache_directory + os.path.sep + self.index_file_name

        if not os.path.exists(self.cache_directory):
            os.makedirs(self.cache_directory)

    def _do_profiles_match(self, d_profile_a, d_profile_b):
        if len(d_profile_a) != len(d_profile_b):
            return False
        for key in d_profile_a:
            if key not in d_profile_b:
                return False
            if d_profile_a[key] != d_profile_b[key]:
                return False
        return True

    def get_entry(self, d_profile):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as fp:
                l_index_entries = json.load(fp)
        else:
            l_index_entries = []

        # Identify outdated entries
        l_valid_entries = []
        l_invalid_entries = []
        for d_entry in l_index_entries:
            dt_valid_until = datetime.fromisoformat(d_entry['meta']['valid_until'])
            if datetime.now() > dt_valid_until:
                l_invalid_entries.append(d_entry)
            else:
                l_valid_entries.append(d_entry)

        # Remove outdated entries
        for d_entry in l_invalid_entries:
            os.remove(self.cache_directory + os.path.sep + d_entry['meta']['cached_in_file'])
        with open(self.index_file, 'w') as fp:
            json.dump(l_valid_entries, fp)

        # Remove orphaned files
        l_orphaned_files = []
        for file in os.listdir(self.cache_directory):
            if file != self.index_file_name:
                found = False
                for entry in l_valid_entries:
                    if file == entry['meta']['cached_in_file']:
                        found = True
                        break
                if not found:
                    l_orphaned_files.append(file)
        for file in l_orphaned_files:
            os.remove(self.cache_directory + os.path.sep + file)

        # Find requested entry
        for d_entry in l_valid_entries:
            if self._do_profiles_match(d_entry['profile'], d_profile):
                return self.cache_directory + os.path.sep + d_entry['meta']['cached_in_file']
        return None

    def create_empty_entry(self, d_profile):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as fp:
                l_index_entries = json.load(fp)
        else:
            l_index_entries = []

        # Find a potential old entry
        for d_entry in l_index_entries:
            if self._do_profiles_match(d_entry['profile'], d_profile):
                os.remove(d_entry['meta']['cached_in_file'])
                del (l_index_entries, d_entry)
                break

        # Add empty entry
        valid_date = datetime.now() + timedelta(days=1)
        file_name = str(datetime.timestamp(datetime.now()))
        new_entry = {'meta': {'valid_until': str(valid_date), 'cached_in_file': file_name}, 'profile': d_profile}
        l_index_entries.append(new_entry)

        # Write new index
        with open(self.index_file, 'w') as fp:
            json.dump(l_index_entries, fp, indent='    ')
        return self.cache_directory + os.path.sep + new_entry['meta']['cached_in_file']
