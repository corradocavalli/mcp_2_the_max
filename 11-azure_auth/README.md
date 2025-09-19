# Azure Authentication - OAuth2 Integration with Microsoft Azure AD

Demonstrates secure MCP server implementation using Azure Active Directory OAuth2 authentication with Microsoft Graph API integration.

## Prerequisites

**⚠️ Azure App Registration Required**: Before running this example, you must set up an Azure App Registration as detailed in the [FastMCP Azure Integration Guide](https://gofastmcp.com/integrations/azure).

## Server Configuration

**Azure Provider Setup**: Configures OAuth2 authentication using Azure AD with environment-based credentials:
```python
from fastmcp.server.auth.providers.azure import AzureProvider

auth_provider = AzureProvider(
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"), 
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    base_url="http://localhost:8000",
    required_scopes=["User.Read", "email", "openid", "profile"],
)

mcp = FastMCP(name="Azure Secured App", auth=auth_provider)
```

**Environment Variables**: Requires the following variables in `.env` file:
```env
AZURE_CLIENT_ID=your-app-client-id
AZURE_CLIENT_SECRET=your-app-client-secret
AZURE_TENANT_ID=your-azure-tenant-id
```

**Microsoft Graph Permissions**: Server requests specific OAuth2 scopes for user data access:
- `User.Read` - Basic user profile information
- `email` - User's email address
- `openid` - OpenID Connect authentication
- `profile` - Extended profile information

## Available Tools

### Authentication-Protected Tools
- `get_user_info()` - Returns authenticated user's Azure AD profile data
  - Extracts claims from OAuth2 token using `get_access_token()`
  - Returns structured user information (ID, email, name, job title, office location)
  - Demonstrates secure access to Microsoft Graph user data

- `system_health_check()` - Basic health check endpoint
  - Simple tool to verify server functionality
  - Available to authenticated users only

## Client Behavior

**OAuth2 Authentication Flow**: Client initiates Azure AD authentication:
```python
async with Client("http://localhost:8000/mcp", auth="oauth") as client:
    # Client automatically handles OAuth2 flow
    # User will be redirected to Azure AD for authentication
    result = await client.call_tool("get_user_info")
```

**Authentication Process**:
1. Client connects with `auth="oauth"` parameter
2. Server redirects to Azure AD login page
3. User authenticates with Microsoft credentials
4. Azure AD redirects back with authorization code
5. Server exchanges code for access token
6. Subsequent tool calls include valid Bearer token

## Key Learning Points

- **Enterprise Authentication** - Integration with Azure AD for enterprise security
- **OAuth2 Flow** - Complete implementation of authorization code flow with PKCE
- **Environment Security** - Secure credential management using environment variables
- **Microsoft Graph Integration** - Access to rich user profile data from Azure AD
- **Token Claims Access** - Extracting user information from JWT token claims
- **Scope-Based Permissions** - Granular control over requested user data access
- **Production-Ready Security** - Enterprise-grade authentication suitable for production use
- **Redirect URI Configuration** - Proper callback handling for OAuth2 flow completion

## Azure Setup Requirements

1. **Create App Registration** in Azure Portal
2. **Configure Authentication** with redirect URI: `http://localhost:8000/auth/callback`
3. **Set API Permissions** for Microsoft Graph (User.Read, email, openid, profile)
4. **Generate Client Secret** and note the values
5. **Configure Environment Variables** with your App Registration details

For detailed setup instructions, visit: https://gofastmcp.com/integrations/azure