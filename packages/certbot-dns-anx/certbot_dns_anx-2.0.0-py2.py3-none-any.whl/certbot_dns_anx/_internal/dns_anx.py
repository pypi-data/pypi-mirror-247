"""DNS Authenticator for DNSimple DNS."""
import logging
from typing import Any
from typing import Callable

from requests import HTTPError
from pyanxdns import Client, split_domain
from datetime import datetime, timedelta
from time import sleep

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)

class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for ANX

    This Authenticator uses the ANX API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are using ANX for DNS).'

    ttl = 30

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._client = None
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None],
                             default_propagation_seconds: int = 30) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='ANX credentials INI file.')

    def more_info(self) -> str:
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the ANX API.'

    def _validate_credentials(self, credentials: CredentialsConfiguration) -> None:
        key = credentials.conf('api-key')
        if not key:
            raise errors.PluginError('{}: dns_anx_api_key is required when using a '
                                        'Global API Key.'
                                        .format(credentials.confobj.filename))
    
    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            'credentials',
            'ANX credentials INI file',
            None,
            self._validate_credentials
        )
    
    def _get__client(self, domain):
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return Client(
            domain,
            self.credentials.conf("api-key")
        )
    
    def _perform(self, domain, validation_name, validation):
        domain_parts = split_domain(validation_name)
        client = self._get__client(domain_parts.domain)

        name = validation_name
        if not name.endswith('.'):
            name = name + '.'

        logger.debug(
            "Creating TXT record for {} on subdomain {}".format(*domain_parts))
        
        logger.debug(
            "Creating TXT record for {}".format(name ))

        client.add_txt_record(name, validation,ttl=self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        domain_parts = split_domain(validation_name)
        client = self._get__client(domain_parts.domain)

        msg = "Removing subdomain {1} on subdomain {0}"
        logger.debug(msg.format(*domain_parts))

        client.delete_by_txt(validation, name=validation_name + ".")
    

