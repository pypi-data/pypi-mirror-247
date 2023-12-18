use crate::api::secrets::create_secret::create_secret_request;
use crate::error::Result;
use crate::helper::handle_authentication;
use crate::Client;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::Secret;
#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct CreateSecretOptions {
    pub environment: String,                   // environment
    pub secret_comment: Option<String>,        // secretComment
    pub path: Option<String>,                  // secretPath
    pub secret_value: String,                  // secretValue
    pub skip_multiline_encoding: Option<bool>, // skipMultilineEncoding
    pub r#type: Option<String>,                // shared / personal
    pub project_id: String,                    // workspaceId
    pub secret_name: String,                   // secretName (PASSED AS PARAMETER IN REQUEST)
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct CreateSecretResponse {
    pub secret: Secret,
}

pub async fn create_secret(
    client: &mut Client,
    input: &CreateSecretOptions,
) -> Result<CreateSecretResponse> {
    handle_authentication(client).await?;

    let secret = create_secret_request(client, input).await;

    match secret {
        Ok(secret) => Ok(secret),
        Err(e) => Err(e),
    }
}
