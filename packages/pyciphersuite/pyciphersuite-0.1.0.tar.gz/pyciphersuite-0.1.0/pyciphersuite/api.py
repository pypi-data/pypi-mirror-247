import logging

import requests

BASE = "https://ciphersuite.info/api"


def list_all_cs():
	"""
	List all available cipher suites.

	Method: GET
	Path: /cs

	:return: list
		A list of all available cipher suites.
	"""
	path = "/cs"

	try:
		response = requests.get(BASE + path)
		response.raise_for_status()
		return response.json()["ciphersuites"]
	except requests.exceptions.RequestException as e:
		logging.error(f"Error during request: {e}")
		return None


def display_cs(ciphersuite_name):
	"""
	Display cipher suite with the given (IANA) name.

	Method: GET
	Path: /cs/{ciphersuite_name}

	:param ciphersuite_name: str
		The cipher suite (IANA) name.

	:return: dict
		A dictionary containing the cipher suite information.
	"""
	path = f"/cs/{ciphersuite_name}"

	try:
		response = requests.get(BASE + path)
		response.raise_for_status()
		return response.json()
	except requests.exceptions.RequestException as e:
		logging.error(f"Error during request: {e}")
		return None


def display_cs_for_tls_version(tls_version):
	"""
	Display cipher suites supported by the given TLS version.

	Method: GET
	Path: /cs/tls/{10|11|12|13}

	:param tls_version: str
		The TLS version.

	:return: list
		A list of ciphersuites.
	"""
	if tls_version not in ["10", "11", "12", "13"]:
		raise ValueError("Invalid TLS version specified! Expected: 10|11|12|13")

	path = f"/cs/tls/{tls_version}"

	try:
		response = requests.get(BASE + path)
		response.raise_for_status()
		return response.json()["ciphersuites"]
	except requests.exceptions.RequestException as e:
		logging.error(f"Error during request: {e}")
		return None


def display_cs_for_security_lvl(security_lvl):
	"""
	Display cipher suites with the given security level.

	Method: GET
	Path: /cs/security/{recommended|secure|weak|insecure}

	:param security_lvl: str
		The security level.

	:return: list
		A list of ciphersuites.
	"""
	if security_lvl not in ["recommended", "secure", "weak", "insecure"]:
		raise ValueError("Invalid security level specified! Expected: recommended|secure|weak|insecure")

	path = f"/cs/security/{security_lvl}"

	try:
		response = requests.get(BASE + path)
		response.raise_for_status()
		return response.json()["ciphersuites"]
	except requests.exceptions.RequestException as e:
		logging.error(f"Error during request: {e}")
		return None


def display_cs_for_given_lib(library):
	"""
	Display cipher suites supported by the given library.

	Method: GET
	Path: /cs/software/{openssl|gnutls}

	:param library: str
		The library.

	:return: list
		A list of ciphersuites.
	"""
	if library not in ["openssl", "gnutls"]:
		raise ValueError("Invalid library specified! Expected: openssl|gnutls")

	path = f"/cs/software/{library}"

	try:
		response = requests.get(BASE + path)
		response.raise_for_status()
		return response.json()["ciphersuites"]
	except requests.exceptions.RequestException as e:
		logging.error(f"Error during request: {e}")
		return None


def list_all_rfcs():
	"""
	List all available RFCs.

	Method: GET
	Path: /rfc

	:return: list
		A list of RFCs.
	"""
	path = "/rfc"

	try:
		response = requests.get(BASE + path)
		response.raise_for_status()
		return response.json()["rfcs"]
	except requests.exceptions.RequestException as e:
		logging.error(f"Error during request: {e}")
		return None


def display_rfc(rfc_number):
	"""
	Display RFC with the given number.

	Method: GET
	Path: /rfc/{rfc_number}

	:param rfc_number: str
		The RFC number.

	:return: dict
		A dictionary containing the RFC information.
	"""
	path = f"/rfc/{rfc_number}"

	try:
		response = requests.get(BASE + path)
		response.raise_for_status()
		return response.json()
	except requests.exceptions.RequestException as e:
		logging.error(f"Error during request: {e}")
		return None
