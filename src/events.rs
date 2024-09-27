use scrypto::prelude::*;

#[derive(ScryptoSbor, ScryptoEvent)]
pub struct FileStored {
    pub file_hash: String,
    pub file_name: String,
}

#[derive(ScryptoSbor, ScryptoEvent)]
pub struct FileRetrieved {
    pub file_hash: String,
    pub file_name: String,
}
