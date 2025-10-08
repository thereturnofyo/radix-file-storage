A rudimentary file storage for Radix, just for fun as an experiment. Does nothing more than storing and retrieving bytes to and from a KeyValueStore.

**Note that Radix was not made for this.**

Example site that allows uploading of files and serves them based on their hashes: https://radix-files.vercel.app/ (Stokenet) or https://radix-files-mainnet.vercel.app/ (Mainnet)

A simple setup for serving files, made in Svelte, can be found here: https://github.com/thereturnofyo/radix-file-serving.

## Methods
### store_file
Stores a file's bytes in the KeyValueStore with the file's hash as the key. 

By default, files up to 500KB are allowed, depending on the transaction method used (see manifests below). The mobile-to-mobile connection seems to have trouble processing larger files, but at least about 150KB should work there.

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
`component_rdx1crlx9t5hdz2yx494zhcqyquyhdmwvnuryqt4lty2d6tcng3elxtuee`

## Usage
### Instantiate
You can use the deployed version, but can also instantiate your own, of course:
```
CALL_FUNCTION
    Address("package_tdx_2_1ph9m4alsknm4zyn0azwf6k2ejmh474075r3k5mpp7ze0vk068duvpy")
    "FileStorage"
    "instantiate"
```
### Store file with blob (recommended)
For this approach, you will have to add a blob to the transaction. This happens outside of the manifest, and instead you refer to its hash in the manifest. Tools you can use to do this are for example the dApp Toolkit and the Radix Engine Toolkit.

Using this method, you can store files using the full file size limit.

**Option 1: Using the Python script (upload_file.py)**

An example Python script using the Radix Engine Toolkit is included in this repository. To use it:

1. Install dependencies:
   ```bash
   pip install radix-engine-toolkit requests
   ```

2. Edit `upload_file.py` and configure:
   ```python
   FILE_TO_UPLOAD = "your_file.txt"  # Your file path
   private_key_list = [...]  # Your private key bytes
   NETWORK_ID = 0x01  # 0x01 for Mainnet, 0x02 for Stokenet
   ```

3. Run the script:
   ```bash
   python upload_file.py
   ```

The script automatically:
- Reads your file as bytes
- Calculates the Blake2b-256 hash (Radix standard)
- Creates a transaction manifest with the blob
- Submits the transaction to the network

**Option 2: Manual manifest with blob**

```
CALL_METHOD
    Address("COMPONENT_ADDRESS") # Replace with component address
    "store_file"
    Blob("BLOB_HASH") # Replace with a Blake2b-256 hash reference to the blob
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