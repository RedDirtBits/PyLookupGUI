import socket
import re
import threading
import queue
import ipaddress
import PySimpleGUI as sg


def validate(host):
    """Validates a hostname or IP address

    Parameters:
        host (str): Hostname or and IP address

    Returns:
        str: A hostname or IP address
    """

    host_regex = '[@_!#$%^&*()<>?\/\\|}{~:]'

    try:

        ipaddress.IPv4Address(host)
        return socket.gethostbyaddr(host)[0].split('.')[0]

    except socket.gaierror:

        return 'Unable to resolve.  Non-existent domain'

    except ipaddress.AddressValueError:

        if not bool(re.search(host_regex, host)):

            try:

                return socket.gethostbyname(host)

            except socket.gaierror:

                return 'Unable to resolve.  Non-existent domain'

        else:

            return ValueError('Hostname contains invalid characters')


def thread_start(host):

    cue = queue.Queue()

    thread = threading.Thread(target=lambda q, arg1: q.put(
        validate(arg1)), args=(cue, host, ), daemon=True)

    thread.start()

    thread.join()

    try:

        if thread.is_alive():

            raise TimeoutError('Query timed out')

        else:

            return cue.get()

    except TimeoutError as error:

        return error


# Tool Tips to be used
multi_host_tt = 'Enter multiple hostnames or IP addresses each on their own line'
checkbox_tt = 'Select to clear text field after host lookup is performed'

sg.theme('DarkGrey9')

# Define the multiple host lookup text field
multi_lookup = [
    [sg.Multiline(size=(80, 10), key='LOOKUP', tooltip=multi_host_tt)]
]

# Define the multiple output field
output_window = [
    [sg.MLine(key='OUTPUT' + sg.WRITE_ONLY_KEY, size=(80, 10))]
]

# Create the window layout
layout = [
    [sg.Frame('IPs or Hostnames', multi_lookup)],
    [sg.Checkbox('Clear IP/Hostnames After Lookup',
                 size=(30, 1), key='ClearInputs', tooltip=checkbox_tt, default=True)],
    # [sg.Text(' ', size=(45, 2))],
    [sg.Frame('Output', output_window)],
    [sg.Text(' ', size=(45, 2))],
    [sg.Button('Exit', size=(15, 1)), sg.Text(
        ' ' * 75), sg.Button('DNS Query', size=(15, 1))],
]

# Display the window
window = sg.Window('DNS Query Tool', layout)

# Start the event loop
while True:

    event, values = window.read()

    # If the user clicks on the 'X' or the Exit button, break out of the loop and close the window
    if event == sg.WIN_CLOSED or event == 'Exit':

        break

    # User clicks on 'Lookup' button
    if event == 'DNS Query':

        # Create a list from the hostnames provided
        # Host list can be line, comma, tab or space separated
        hosts = re.split('\\n|\\t|\\s|, |,', values['LOOKUP'].strip())

        # Clear the output window of any previous results
        window['OUTPUT' + sg.WRITE_ONLY_KEY].update('')

        # Loop over the hostname list and perform a DNS query for each
        for host in hosts:

            window['OUTPUT' +
                   sg.WRITE_ONLY_KEY].print(host + ':', thread_start(host))

            # sg.Print('{}: {}'.format(host, thread_start(host)))

        # By default, clear the input field after a query has been performed
        if values['ClearInputs']:

            window['LOOKUP'].update('')

# Close the GUI window
window.close()
