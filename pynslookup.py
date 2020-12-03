import socket
import re
import threading
import queue
import PySimpleGUI as sg


def validate(host: str):
    """Validates a hostname or IP address

    Parameters:
        host (str): Hostname or and IP address

    Raises:
        socket.error: IP address fails vaildation
        ValueError: Hostname contains invalid characters

    Returns:
        str: A hostname or IP address
    """

    host_regex = '[@_!#$%^&*()<>?\/\\|}{~:]'

    # Check for three periods in the IP address.  Otherwise, assume its a hostname
    if host.count('.') == 3:

        try:

            # The first of two IP address validations
            socket.inet_pton(socket.AF_INET, host)

        except OSError:

            try:

                # The second IP address validation
                socket.inet_aton(host)

            except socket.error:

                # If the validation fails, return a message to the user
                return 'Invalid IP address'

        else:

            # If the host passes IP validation, perform a reverse DNS query
            return socket.gethostbyaddr(host)[0].split('.')[0]

    else:

        try:

            # Check that there are no invalid characters in the hostname
            if not bool(re.search(host_regex, host)):

                try:

                    # If the hostname validates, perform the DNS query
                    return socket.gethostbyname(host)

                except socket.gaierror:

                    return 'Unable to resolve.  Non-existent domain'

            else:

                # If the hostname fails validation throw an exception
                raise ValueError('Hostname contains invalid characters')

        except ValueError as error:

            # Hostname failed validation, let the user know
            return error


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

# Define the multiple host lookup text field and execution button
multi_lookup = [
    [sg.Multiline(size=(50, 10), key='LOOKUP', tooltip=multi_host_tt),
     sg.Button('Lookup', size=(10, 10))]
]

# Create the window layout
layout = [
    [sg.Frame('IPs or Hostnames', multi_lookup)],
    [sg.Checkbox('Clear IP/Hostnames After Lookup',
                 size=(25, 1), key='ClearInputs', tooltip=checkbox_tt, default=True)],
    [sg.Text(' ' * 55)],
    [sg.Button('Exit')]
]

# Display the window
window = sg.Window('Host Lookup Tool', layout)

# Start the event loop
while True:

    event, values = window.read()

    # If the user clicks on the 'X' or the Exit button, break out of the loop and close the window
    if event == sg.WIN_CLOSED or event == 'Exit':

        break

    # User clicks on 'Lookup' button
    if event == 'Lookup':

        # Create a list from the hostnames provided
        hosts = values['LOOKUP'].split()

        # Loop over the hostname list and perform a DNS query for each
        for host in hosts:

            sg.Print('{}: {}'.format(host, thread_start(host)))

        # By default, clear the input field after a query has been performed
        if values['ClearInputs']:

            window['LOOKUP'].update('')

# Close the GUI window
window.close()
