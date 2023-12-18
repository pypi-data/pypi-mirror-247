pub(crate) mod create;
pub(crate) mod delete;
pub(crate) mod get;
pub(crate) mod list;
pub(crate) mod update;

pub use create::{CreateSecretOptions, CreateSecretResponse};
pub use delete::{DeleteSecretOptions, DeleteSecretResponse};
pub use get::{get_secret, GetSecretOptions, GetSecretResponse};
pub use list::{ListSecretsOptions, ListSecretsResponse};
pub use update::{UpdateSecretOptions, UpdateSecretResponse};

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Secret {
    #[serde(rename = "_id")]
    id: String,
    version: i32,
    workspace: String,
    r#type: String,
    environment: String,
    secret_key: String,
    secret_value: String,
    secret_comment: String,
}
