import requests
from radix_engine_toolkit import *
from typing import Tuple
import secrets
import hashlib

# Configuration
NETWORK_ID: int = 0x01  # Mainnet
FILE_STORAGE_COMPONENT = "component_rdx1crlx9t5hdz2yx494zhcqyquyhdmwvnuryqt4lty2d6tcng3elxtuee"  # Mainnet component
FILE_TO_UPLOAD = "my_file_name.txt"

# Replace with your private key bytes
private_key_list = [] # your private key

class GatewayApiClient:
    BASE_URL = "https://mainnet.radixdlt.com"

    @staticmethod
    def current_epoch() -> int:
        try:
            response = requests.post(f"{GatewayApiClient.BASE_URL}/status/gateway-status")
            response.raise_for_status()
            data = response.json()
            return data['ledger_state']['epoch']
        except Exception as e:
            print(f"Error fetching current epoch: {e}")
            raise

    @staticmethod
    def submit_transaction(transaction: NotarizedTransaction) -> dict:
        try:
            transaction_hex = transaction.compile().hex()
            payload = {"notarized_transaction_hex": transaction_hex}
            response = requests.post(f"{GatewayApiClient.BASE_URL}/transaction/submit", json=payload)
            if response.status_code != 200:
                print(f"Error response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error submitting transaction: {e}")
            raise

def account_from_keys(network_id: int) -> Tuple[PrivateKey, PublicKey, Address]:
    private_key_bytes = bytes(private_key_list)
    private_key: PrivateKey = PrivateKey.new_secp256k1(private_key_bytes)
    public_key: PublicKey = private_key.public_key()
    account: Address = derive_virtual_account_address_from_public_key(
        public_key, network_id
    )
    return (private_key, public_key, account)

def random_nonce() -> int:
    """
    Generates a random secure random number between 0 and 0xFFFFFFFF (u32::MAX)
    """
    return secrets.randbelow(0xFFFFFFFF)

def read_file_as_bytes(filename: str) -> bytes:
    """Read file and return as bytes"""
    with open(filename, 'rb') as f:
        return f.read()

def upload_file_to_radix(filename: str):
    try:
        # Setup account
        (private_key, public_key, account_address) = account_from_keys(NETWORK_ID)
        print(f"Account address: {account_address.as_str()}")

        # Read file
        file_data = read_file_as_bytes(filename)
        print(f"File size: {len(file_data)} bytes")

        # Calculate the blob hash using Blake2b-256 (Radix standard)
        import hashlib
        blob_hash = hashlib.blake2b(file_data, digest_size=32).hexdigest()
        print(f"Blob hash (blake2b): {blob_hash}")

        # Create manifest with blob reference
        manifest_string: str = f"""
            CALL_METHOD
                Address("{account_address.as_str()}")
                "lock_fee"
                Decimal("150")
            ;

            CALL_METHOD
                Address("{FILE_STORAGE_COMPONENT}")
                "store_file"
                Blob("{blob_hash}")
                "{filename}"
            ;
        """

        # Create manifest with blob
        manifest: TransactionManifest = TransactionManifest(
            Instructions.from_string(manifest_string, NETWORK_ID),
            [file_data]  # Add file data as blob
        )

        # Validate manifest
        manifest.statically_validate()
        print("Manifest validated successfully")

        # Get current epoch
        current_epoch: int = GatewayApiClient.current_epoch()
        print(f"Current epoch: {current_epoch}")

        # Build and notarize transaction
        transaction: NotarizedTransaction = (
            TransactionBuilder()
            .header(
                TransactionHeader(
                    NETWORK_ID,
                    current_epoch,
                    current_epoch + 10,
                    random_nonce(),
                    public_key,
                    True,
                    0,
                )
            )
            .manifest(manifest)
            .message(Message.NONE())
            .notarize_with_private_key(private_key)
        )

        transaction_id: TransactionHash = transaction.intent_hash()
        print(f"Transaction ID: {transaction_id.as_str()}")

        # Submit transaction
        response = GatewayApiClient.submit_transaction(transaction)
        print(f"Transaction submitted successfully!")
        print(f"Response: {response}")

        return {
            "Transaction ID": transaction_id.as_str(),
            "Response": response
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    result = upload_file_to_radix(FILE_TO_UPLOAD)
    print("\n=== Upload Complete ===")
    print(f"Transaction ID: {result['Transaction ID']}")
