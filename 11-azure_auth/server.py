import os

from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
from fastmcp.server.dependencies import get_access_token

# Load environment variables from .env file
load_dotenv()

# The AzureProvider handles Azure's token format and validation
# Ensure you have correctly set up an App Registration in Azure AD: https://gofastmcp.com/integrations/azure
auth_provider = AzureProvider(
    client_id=os.getenv("AZURE_CLIENT_ID"),  # Your Azure App Client ID
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),  # Your Azure App Client Secret
    tenant_id=os.getenv("AZURE_TENANT_ID"),  # Your Azure Tenant ID (REQUIRED)
    base_url="http://localhost:8000",  # Must match your App registration
    required_scopes=[
        "User.Read",
        "email",
        "openid",
        "profile",
    ],  # Microsoft Graph permissions
    # redirect_path="/auth/callback"                                    # Default value, customize if needed
)

mcp = FastMCP(name="Azure Secured App", auth=auth_provider)


# Add a protected tool to test authentication
@mcp.tool
async def get_user_info():
    """Returns information about the authenticated Azure user."""

    token = get_access_token()
    # The AzureProvider stores user data in token claims
    return {
        "azure_id": token.claims.get("sub"),
        "email": token.claims.get("email"),
        "name": token.claims.get("name"),
        "job_title": token.claims.get("job_title"),
        "office_location": token.claims.get("office_location"),
    }


@mcp.tool()
async def system_health_check(ctx: Context) -> str:
    """Checks the health of the system."""
    return "I am alive and kicking!"


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
