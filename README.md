A rudimentary file storage for Radix, just for fun as an experiment. Does nothing more than storing and retrieving bytes to and from a KeyValueStore.

Example site that allows uploading of files and serves them based on their hashes: https://radix-files.vercel.app/

## Methods
### store_file
Stores a file's bytes in the KeyValueStore with the file's hash as the key. 

By default, files up to 500KB are allowed, depending on the transaction method used (see manifests below).

Accepts:
* Vec\<u8\>: hex-encoded file bytes
* String: file name

Returns:
* String: the file's hash

### get_file
Gets a file's bytes from the KeyValueStore via the provided hash.

Accepts:
* String: file hash

Returns:
* (String, Vec\<u8\>): a tuple containing the file name and file bytes

## Events
### FileStored
Emitted by the `store_file` method. 

Fields:
* `file_hash: String`: the file's hash
* `file_name: String`: the file's name

### FileRetrieved
Emitted by the `get_file` method. 

Fields:
* `file_hash: String`: the file's hash
* `file_name: String`: the file's name

## Component addresses
### Stokenet
`component_tdx_2_1cpd8dr5lza00jyk28npcu9qknn4j7ug26nmnhzwtsa6qhmr99enex6`

### Mainnet
Currently not deployed to mainnet.

## Usage
### Instantiate
You can use the deployed version, but can also instantiate your own, of course:
```
CALL_FUNCTION
    Address("package_tdx_2_1p4vtw2k07r2h7nt3lnkjssccphyjdhhmweq5594hw8jskj43vgfxe0")
    "FileStorage"
    "instantiate"
```
### Store file with blob (recommended)
For this approach, you will have to add a blob to the transaction. This happens outside of the manifest, and instead you refer to its hash in the manifest. The Radix Engine Toolkit is capable of this, for example.

Using this method, you can store files using the full file size limit.
```
CALL_METHOD
    Address("COMPONENT_ADDRESS") # Replace with component address
    "store_file"
    Blob("BLOB_HASH") # Replace with a hash reference to the blob
    "filename.png"
```
### Store file with bytes in manifest
You can use something like https://tomeko.net/online_tools/file_to_hex.php?lang=en to get the hex of a file for testing purposes. 

**Uncheck the two options:**
* Use 0x and comma as separator (C-like)
* Insert newlines after each 16B

**Note**: if you use this method, you can only use half the file size limit, as each byte is hex-encoded to two characters, which doubles the transaction size.

```
CALL_METHOD
    Address("COMPONENT_ADDRESS") # Replace with component address
    "store_file"
    Bytes("HEX_ENCODED_BYTES") # Replace with hex-encoded bytes
    "filename.png"
```

### Get file with hash
```
    Address("COMPONENT_ADDRESS") # Replace with component address
    "get_file"
    "HASH" # Replace with file hash
```