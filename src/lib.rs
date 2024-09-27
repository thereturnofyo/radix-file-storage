use events::*;
use scrypto::prelude::*;

pub mod events;

pub type FileTuple = (String, Vec<u8>);

#[blueprint]
#[types(FileStorage, String, FileTuple)]
#[events(FileStored, FileRetrieved)]
mod file_storage {
    /// This blueprint creates a rudimentary file storage on Radix, just for fun.
    /// It stores bytes and returns bytes.
    struct FileStorage {
        storage: KeyValueStore<String, (String, Vec<u8>)>,
        file_size_limit: u32,
    }

    impl FileStorage {
        /// Instantiate the file storage component. It is permissionless and the only configurable
        /// thing is the file size limit, which is set to 500kb to ensure we don't run into
        /// transaction limits.
        pub fn instantiate() -> Global<FileStorage> {
            Self {
                storage: KeyValueStore::<String, (String, Vec<u8>)>::new_with_registered_type(),
                file_size_limit: 500000,
            }
            .instantiate()
            .prepare_to_globalize(OwnerRole::None)
            .globalize()
        }

        /// Stores a file in the KeyValueStore.
        pub fn store_file(&mut self, bytes: Vec<u8>, file_name: String) -> String {
            assert!(
                bytes.len().to_u32().unwrap() <= self.file_size_limit,
                "File larger than file size limit of {} bytes",
                self.file_size_limit
            );

            let file_hash = hash(&bytes).to_string();
            self.storage
                .insert(file_hash.clone(), (file_name.clone(), bytes));

            Runtime::emit_event(FileStored {
                file_hash: file_hash.clone(),
                file_name,
            });

            file_hash
        }

        // Gets a file from the KVS
        pub fn get_file(&self, file_hash: String) -> (String, Vec<u8>) {
            let (file_name, file) = match self.storage.get(&file_hash) {
                Some(value) => value.to_owned(),
                None => panic!("Nothing stored with this hash"),
            };

            Runtime::emit_event(FileRetrieved {
                file_hash: file_hash.clone(),
                file_name: file_name.clone(),
            });

            (file_name, file)
        }
    }
}
