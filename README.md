# OWA-Password-Sprayer
OWA Password Sprayer


This Python script facilitates password spraying against Outlook Web Access (OWA) endpoints. Password spraying is a technique used to test a single password against multiple usernames, aiming to find valid credentials for accessing the OWA.
Features:

* Supports authentication using NTLM for OWA endpoints.
* Multi-threaded execution for efficient username and password spraying.
* Integration with asyncio for asynchronous task execution.
* Detailed logging and debug options to aid in troubleshooting.

## Usage:

* Clone the repository.
* Install necessary dependencies (requests, requests_ntlm, docopt).
* Customize the script with your target OWA URL, user list, and password.
* Run the script with appropriate command-line arguments to initiate password spraying.

## Command-line Arguments:

* `target`: URL of the OWA endpoint.
* `password`: Password to be sprayed against user list.
* `userfile`: File containing usernames (one per line).
* `--threads`: Number of concurrent threads to use (default: 3).
* `--debug`: Enable debug mode for detailed logging.

## Example:

bash
```
python3 owa_password_sprayer.py owa owa http://autodiscover.example.com Password /home/kali/Tools/user.txt --threads 3 --debug
```
## Result Summary:

Upon completion, the script provides a summary of successful authentication attempts, if any, along with detailed logging for each authentication request.

## Author

This script was developed by Dilanka Kaushal Hewage (**n3rdh4x0r**).

## License:

* This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer:

* Use this tool responsibly and only with proper authorization. Unauthorized use is strictly prohibited.
