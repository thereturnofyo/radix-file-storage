use scrypto_test::prelude::*;
use std::env;
use std::fs;

use storage::file_storage_test::*;

#[test]
fn test_store_and_get() -> Result<(), RuntimeError> {
    // Set up environment
    let (mut env, mut component) = setup_env()?;
    let file = fs::read("icon.svg");

    // Store file
    let file_hash = match file {
        Ok(bytes) => component.store_file(bytes, "icon_stored.svg".to_string(), &mut env)?,
        Err(e) => panic!("Could not read file due to {}", e),
    };

    // Get file
    let (file_name, file) = component.get_file(file_hash, &mut env)?;

    // Write file to disk
    let write_result = fs::write(file_name, file);

    assert!(write_result.is_ok());

    Ok(())
}

fn setup_env() -> Result<(TestEnvironment<InMemorySubstateDatabase>, FileStorage), RuntimeError> {
    let mut env = TestEnvironment::new();
    let package_address =
        PackageFactory::compile_and_publish(this_package!(), &mut env, CompileProfile::Fast)?;

    let component = FileStorage::instantiate(package_address, &mut env)?;

    Ok((env, component))
}
