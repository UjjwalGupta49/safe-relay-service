import os
from logging import getLogger
from typing import Tuple

from ethereum.transactions import secpk1n
from faker import Factory as FakerFactory
from faker import Faker

from safe_relay_service.ether.tests.factories import get_eth_address_with_key
from safe_relay_service.safe.models import SafeCreation

fakerFactory = FakerFactory.create()
faker = Faker()

logger = getLogger(__name__)


def generate_valid_s():
    while True:
        s = int(os.urandom(31).hex(), 16)
        if s <= (secpk1n - 1):
            return s


def generate_random_safe(owners=None, number_owners=3) -> Tuple[str, str, int]:
    s = generate_valid_s()

    if not owners:
        owners = []
        for _ in range(number_owners):
            owner, _ = get_eth_address_with_key()
            owners.append(owner)

    threshold = len(owners)

    safe_creation = SafeCreation.objects.create_safe_tx(s, owners, threshold)
    return safe_creation.safe.address, safe_creation.deployer, safe_creation.payment


def generate_and_deploy_safe(w3, funder, master_copy, owners, threshold) -> str:
    s = generate_valid_s()
    safe_creation = SafeCreation.objects.create_safe_tx(s, owners, threshold, master_copy=master_copy)
    w3.eth.sendTransaction({
        'from': funder,
        'to': safe_creation.deployer,
        'value': safe_creation.payment
    })

    w3.eth.sendTransaction({
        'from': funder,
        'to': safe_creation.safe.address,
        'value': safe_creation.payment
    })

    tx_hash = w3.eth.sendRawTransaction(bytes(safe_creation.signed_tx))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert tx_receipt.contractAddress == safe_creation.safe.address
    assert tx_receipt.status

    return safe_creation.safe.address
