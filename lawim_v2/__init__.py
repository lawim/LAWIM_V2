"""LAWIM_V2 executable baseline package entrypoint.

This top-level package bridges the repository root and the implementation code
stored under `code/lawim_v2` so the application can run directly from the
workspace without additional environment setup.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import extend_path

__version__ = "0.1.0"

__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]

_code_package = Path(__file__).resolve().parent.parent / "code" / "lawim_v2"
if _code_package.is_dir():
    code_path = str(_code_package)
    if code_path not in __path__:
        __path__.append(code_path)

from .conversation_registry import (
    ConversationArchiveManager,
    ConversationArchiveManifest,
    ConversationLifecycleEngine,
    ConversationRegistry,
    ConversationRestoreEngine,
    ConversationStorageProvider,
    OVHStorageOptimizer,
    StorageOrchestrator,
)
from .google_drive_connector import GoogleDriveOAuthCredentials, build_default_google_drive_connectors
from .security import (
    AADAuthResult,
    AADAuthenticator,
    AADAuthenticationProvider,
    AADConfig,
    AADAuditLogger,
    AADIdentityProvider,
    AADSession,
    AADSessionManager,
    AuthenticationResult,
    AuthorizationDecision,
    BaseAuthorizer,
    ClaimsBasedAuthorizer,
    ClaimsManager,
    ExternalSecretProvider,
    GroupMapper,
    Identity,
    IdentityGroup,
    IdentityProvider,
    IdentityProviderKind,
    IdentityValidator,
    LocalIdentityProvider,
    MockAccessToken,
    MockIDToken,
    MockRefreshToken,
    PolicyBasedAuthorizer,
    RoleBasedAuthorizer,
    RoleMapper,
    SecretProvider,
    resolve_aad_config,
)
from .storage_registry import (
    GoogleDriveConfigurationModel,
    GoogleDriveConnector,
    StorageResource,
    StorageResourceRegistry,
    StorageRoutingPolicy,
    StorageSetupWizard,
    StorageUsageThresholds,
)

__all__ = [
    "__version__",
    "AADAuthResult",
    "AADAuthenticator",
    "AADConfig",
    "AADAuditLogger",
    "AADIdentityProvider",
    "AADSession",
    "AADSessionManager",
    "AuthorizationDecision",
    "BaseAuthorizer",
    "ClaimsBasedAuthorizer",
    "ClaimsManager",
    "ExternalSecretProvider",
    "GroupMapper",
    "Identity",
    "IdentityGroup",
    "IdentityProvider",
    "IdentityProviderKind",
    "IdentityValidator",
    "LocalIdentityProvider",
    "MockAccessToken",
    "MockIDToken",
    "MockRefreshToken",
    "PolicyBasedAuthorizer",
    "RoleBasedAuthorizer",
    "RoleMapper",
    "SecretProvider",
    "ConversationArchiveManager",
    "ConversationArchiveManifest",
    "ConversationLifecycleEngine",
    "ConversationRegistry",
    "ConversationRestoreEngine",
    "ConversationStorageProvider",
    "GoogleDriveConfigurationModel",
    "GoogleDriveConnector",
    "GoogleDriveOAuthCredentials",
    "build_default_google_drive_connectors",
    "OVHStorageOptimizer",
    "StorageResource",
    "StorageResourceRegistry",
    "StorageRoutingPolicy",
    "StorageSetupWizard",
    "StorageUsageThresholds",
    "StorageOrchestrator",
    "resolve_aad_config",
]
