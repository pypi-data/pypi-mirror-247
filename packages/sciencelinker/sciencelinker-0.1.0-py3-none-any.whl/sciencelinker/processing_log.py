from datetime import datetime
import hashlib
from collections import OrderedDict
import json

d_logs = {}


def es(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'",
                                                                                                               '&#39;')


class DataItem:
    """
    Used to store information about data item. The items can be used for input or output in processing log records.
    The item does not need to correspond to an actual data object but can be virtual.
    """

    def __init__(self, name, value, description=None):
        """
        Constructor. Can be used to instiantiate a DataItem.

        :param name: The name of the data item
        :type name: str
        :param value: The value of the data item. (Should correspond to an actual data object because this value is used to create a hash of the object, so data item can be tracked accross processing steps.
        :type value: any
        :param description: A brief the description of what is stored in the object
        :type description: str
        """
        self.name = name
        self.type = None
        self.value = value
        self.hash = None
        self.description = description
        self.__eval__()

    def __eval__(self):
        self.type = str(type(self.value))
        as_string = str(self.value)
        self.hash = hash(as_string)
        if len(as_string) < 30:
            self.value = as_string
        else:
            self.value = as_string[0:15] + '...' + as_string[-15:]

    def clone(self, name: str = None, value=None, description: str = None):
        """Creates a copy of a data item.

        This method can be used to quickly generate a new DataItem based on an already existing one.
        Use one of the parameters to change a value on the walk.

        :param name: Use this parameter to change the name during copying.
        :type name: str
        :param value: Use this parameter to change the value during copying. Dependant values such as the hash will be automatically recomputed.
        :type values: any
        :param description: Use this paramter to change the description during copying.
        :type description: str
        """
        c = DataItem(name=self.name, value=self.value, description=self.description)
        if name is not None:
            c.name = name
        if value is not None:
            c.value = value
        if description is not None:
            c.description = description
        c.__eval__()
        return c

    def as_dict(self):
        d = OrderedDict({'name': self.name, 'type': self.type, 'value': self.value, 'hash': self.hash,
                         'description': self.description})
        return d

    def as_html(self):
        s = f"<b>Name:</b> {es(self.name)}, <b>type:</b> {es(self.type)}, <b>value:</b> {es(str(self.value))}, <b>hash:</b> {self.hash}, <b>description:</b> {es(self.description)}"
        return s


class Note:
    def __init__(self, text):
        self.text = text
        self.utc_timestamp = datetime.utcnow()

    def as_dict(self):
        d = OrderedDict({'text': self.text, 'utc-timestamp': str(self.utc_timestamp)})
        return d

    def as_html(self):
        s = f"<b>{self.utc_timestamp}:</b> {self.text}"
        return s


def get_bg_color(level):
    colors = ['ffffff', 'dddddd', 'bbbbbb', '999999']
    if level > 3:
        return '777777'
    else:
        return colors[level]


class Procedure:
    def __init__(self, name, l_inputs, method_url=None):
        self.name = name
        self.l_inputs = l_inputs
        self.l_outputs = []
        self.l_events = []
        self.utc_timestamp_start = datetime.utcnow()
        self.utc_timestamp_end = None
        self.method_url = method_url
        self.open_status = 'open'

    def get_last_open(self):
        if self.open_status == 'closed':
            return None
        if len(self.l_events) > 0:
            last_event = self.l_events[-1]
            if type(last_event) == Procedure:
                if last_event.open_status == 'open':
                    return last_event.get_last_open()
        return self

    def close(self, l_outputs):
        self.l_outputs = l_outputs
        self.open_status = 'closed'
        self.utc_timestamp_end = datetime.utcnow()

    def as_dict(self):
        d = OrderedDict({'name': self.name})
        d['method_url'] = self.method_url
        d['utc-timestamp-start'] = str(self.utc_timestamp_start)
        d['inputs'] = [inpot.as_dict() for inpot in self.l_inputs]
        d['events'] = [event.as_dict() for event in self.l_events]
        d['utc-timestamp-end'] = str(self.utc_timestamp_end)
        d['outputs'] = [output.as_dict() for output in self.l_outputs]
        return d

    def as_html(self, level=0):
        if level == 0:
            s = f"<table style=\"background-color: #{get_bg_color(level)}; border:1px black solid; margin: 20px 0px 20px 0px;\">\n"
        else:
            s = f"<table style=\"background-color: #{get_bg_color(level)}; margin: 20px 0px 20px 20px;\">\n"
        s += f"<tr style=\"vertical-align:top\"><td>Name</td><td>{es(self.name)}</td></tr>\n"
        s += f"<tr style=\"vertical-align:top\"><td>Method documentation</td><td><a href=\"{es(self.method_url)}\">{es(self.method_url)}</a></td></tr>\n"
        s += f"<tr style=\"vertical-align:top\"><td>Start time</td><td>{self.utc_timestamp_start}</td></tr>\n"
        if len(self.l_inputs) > 0:
            s_input_table = f"<table>\n"
            for inp in self.l_inputs:
                s_input_table += f"<tr><td>{inp.as_html()}</td></tr>\n"
            s_input_table += f"</table>\n"
            s += f"<tr style=\"vertical-align:top\"><td>Inputs</td><td>\n{s_input_table}</td></tr>\n"

        for event in self.l_events:
            if type(event) == Note:
                s += f"<tr style=\"vertical-align:top\"><td>Note</td><td>{event.as_html()}</td></tr>\n"
            else:  # Event is a sub procedure call
                s += f"<tr style=\"vertical-align:top\"><td>Sub procedure call</td><td>\n{event.as_html(level=level + 1)}</td></tr>\n"

        s += f"<tr><td>End time</td><td>{self.utc_timestamp_end}</td></tr>\n"
        if len(self.l_outputs) > 0:
            s_output_table = f"<table>\n"
            for outp in self.l_outputs:
                s_output_table += f"<tr><td>\n{outp.as_html()}</td></tr>\n"
            s_output_table += f"</table>\n"
            s += f"<tr style=\"vertical-align:top\"><td>Outputs</td><td>{s_output_table}</td></tr>\n"

        s += f"</table>\n"
        return s


class Log:
    def __init__(self, log_name):
        self.log_name = log_name
        self.date_of_creation = datetime.utcnow()
        self.created_with = 'ScienceLinker'
        self.version = 'v0.0.1'
        self.technical_documentation_url = 'http://sciencelinker.git.gesis.org/docs/'
        self.project_home_url = 'https://sciencelinker.git.gesis.org/sciencelinker-development'
        self.pypi = 'https://pypi.org/project/sciencelinker/'
        self.notes = ['ScienceLinker is a prototype and as such needs to be treated with caution.']
        self.l_events = []

    def get_last_open(self):
        if len(self.l_events) > 0:
            last_event = self.l_events[-1]
            if type(last_event) == Procedure:
                return last_event.get_last_open()
        return None

    def as_dict(self):
        d = OrderedDict({'log-name': self.log_name, 'date-of-creation': str(self.date_of_creation),
                         'created-with': self.created_with,
                         'version': self.version, 'technical-documentation-url': self.technical_documentation_url,
                         'project-home-url': self.project_home_url,
                         'pypi': self.pypi, 'notes': self.notes,
                         'events': [event.as_dict() for event in self.l_events]})
        return d

    def as_html(self):
        html = '<!DOCTYPE html>\n<html>\n<body>\n\n'
        html += '<h1>Processing Log</h1>\n\n'
        html += '<table style=\"max-width:800px;\">\n'
        html += f"<tr><td style=\"min-width:300px;\">Log name</td><td>{es(self.log_name)}</td></tr>\n"
        html += f"<tr><td style=\"min-width:300px;\">Date of creation</td><td>{self.date_of_creation}</td></tr>\n"
        html += f"<tr><td style=\"min-width:300px;\">Created with</td><td>{self.created_with}</td></tr>\n"
        html += f"<tr><td style=\"min-width:300px;\">Version</td><td>{self.version}</td></tr>\n"
        html += f"<tr><td style=\"min-width:300px;\">Technical documentation</td><td><a href=\"{self.technical_documentation_url}\">{self.technical_documentation_url}</a></td></tr>\n"
        html += f"<tr><td style=\"min-width:300px;\">Project home</td><td><a href=\"{self.project_home_url}\">{self.project_home_url}</a></td></tr>\n"
        html += f"<tr><td style=\"min-width:300px;\">PyPi</td><td><a href=\"{self.pypi}\">{self.pypi}</a></td></tr>\n"
        html += '</table>\n\n'
        html += '<h2>Notes</h2>\n'
        html += '<ol>\n'
        for note in self.notes:
            html += f"<li>{es(note)}</li>\n"
        html += '</ol>\n\n'
        html += '<h2>Log</h2>\n'
        html += '<table style="max-width:800px;">\n'
        for event in self.l_events:
            html += f"<tr><td>{event.as_html(level=0)}</td></tr>\n"
        html += '</table>\n'
        html += '</body>\n</html>\n'
        return html


def start_procedure(name='No name', l_inputs=None, method_url=None, log_name='default'):
    """Logs the start of  a processing step. A procedure describes a logical step in the data processing. It must not necessarily align with the names of
    used functions or methods. This method is used by ScienceLinker modules to record processing steps but it is also available to users who want to add
    their own processing effort to the log.

    :param name: The name of the processing step. This should be name that is descriptive to the processing step.
    :type name: str
    :param l_inputs: A list describing the input into the processing step
    :type l_inputs: list of sciencelinker.processing_log.DataItem
    :param method_url: A URL referencing the documentation of the processing step
    :type method_url: str
    :param log_name: The name of the processing log to use. If a log with the given name does not exist it will be created. 'Default' will be used if nonen is given.
    :type log_name: str
    """
    if log_name not in d_logs:
        new_log = Log(log_name)
        d_logs[log_name] = new_log
    log = d_logs[log_name]

    p = Procedure(name, l_inputs, method_url)
    parent_call = log.get_last_open()
    if parent_call is None:
        log.l_events.append(p)
    else:
        parent_call.l_events.append(p)


def end_procedure(l_outputs, log_name='default'):
    """Logs the end of a processing step. Calling this function must correspond to a call to ``start_procedure(...)``.

    :param l_outputs: A list describing the output in from the processing step
    :type l_outputs: list of sciencelinker.processing_log.DataItem
    :param log_name: The name of the processing log to use. If a log with the given name does not exist it will be created. 'Default' will be used if nonen is given.
    :type log_name: str
    """
    if log_name not in d_logs:
        raise Exception(f"No log with name {log_name}")
    log = d_logs[log_name]
    open_call = log.get_last_open()
    if open_call is None:
        raise Exception(f"Cannot end procedure. No open call in {log_name}")
    else:
        open_call.close(l_outputs)


def add_note(text, log_name='default'):
    """
    Add a note to the processing log. The note will appear in the current context level.

    :param text: The text of the note
    :type text: str
    :param log_name: The name of the processing log to use. If a log with the given name does not exist it will be created. 'Default' will be used if nonen is given.
    :type log_name: str
    """
    if log_name not in d_logs:
        new_log = Log(log_name)
        d_logs[log_name] = new_log
    log = d_logs[log_name]
    parent_call = log.get_last_open()
    if parent_call is None:
        log.l_events.append(Note(text))
    else:
        parent_call.l_events.append(Note(text))


def write_log(output_format: str, file=None, log_name: str = 'default'):
    """
    Write the processing log to str or to a file.

    :param output_format: The format to use. ``json`` or ``html`` is available.
    :type output_format: str
    :param file: If given the output will be written to this file, otherwise it is returned as str.
    :type file: str
    :param log_name: The log to be written. If not used, the ``default`` named log will be used.
    :type log_name: str
    :return: The processing log as str in the specified format or None
    :rtype: str or None
    """
    if log_name not in d_logs:
        raise Exception(f"Unknown log {log_name}")
    log = d_logs[log_name]
    if output_format.lower() == 'json':
        s = json.dumps(log.as_dict(), indent='  ')
    elif output_format.lower() == 'html' or output_format.lower() == 'htm':
        s = log.as_html()
    if file is None:
        return s
    else:
        with open(file, 'w') as fd:
            fd.write(s)


def hash_a_file(fname):
    BLOCK_SIZE = 65536  # The size of each read from the file

    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
    with open(fname, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = f.read(BLOCK_SIZE)  # Read the next block from the file
    return file_hash.hexdigest()
