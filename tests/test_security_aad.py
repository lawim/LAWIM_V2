from __future__ import annotations

from unittest import TestCase

from lawim_v2.security.aad import AADAuthResult, AADAuthenticator, AADConfig, resolve_aad_config
from lawim_v2.security.audit import AADAuditLogger
from lawim_v2.security.authorization import ClaimsBasedAuthorizer, PolicyBasedAuthorizer, RoleBasedAuthorizer
from lawim_v2.security.claims import ClaimsManager
from lawim_v2.security.groups import GroupMapper, IdentityGroup
from lawim_v2.security.identity import (
    AADAuthenticationProvider,
    AADIdentityProvider,
    AuthenticationResult,
    Identity,
    IdentityProviderKind,
    IdentityValidator,
    LocalIdentityProvider,
)
from lawim_v2.security.roles import RoleMapper
from lawim_v2.security.secrets import ExternalSecretProvider
from lawim_v2.security.session import AADSessionManager
from lawim_v2.security.tokens import MockAccessToken, MockIDToken, MockRefreshToken
from lawim_v2.services import LawimServices


class AADSecurityConfigTest(TestCase):
    def test_aad_config_defaults_to_disabled(self) -> None:
        config = resolve_aad_config({})
        self.assertFalse(config.enabled)
        self.assertEqual(config.secret_provider, "external")

    def test_aad_config_requires_tenant_and_client_when_enabled(self) -> None:
        with self.assertRaises(ValueError):
            resolve_aad_config({
                "LAWIM_AAD_ENABLED": "true",
                "LAWIM_AAD_CLIENT_ID": "client-id",
            })

    def test_aad_config_accepts_entra_profile(self) -> None:
        config = resolve_aad_config({
            "LAWIM_AAD_ENABLED": "true",
            "LAWIM_AAD_TENANT_ID": "tenant-id",
            "LAWIM_AAD_CLIENT_ID": "client-id",
            "LAWIM_AAD_SCOPES": "openid,profile",
            "LAWIM_AAD_REDIRECT_URI": "https://example.test/callback",
            "SECRET_PROVIDER": "entra",
        })
        self.assertTrue(config.enabled)
        self.assertEqual(config.tenant_id, "tenant-id")
        self.assertEqual(config.scopes, ("openid", "profile"))
        self.assertEqual(config.secret_provider, "entra")

    def test_aad_config_uses_default_secret_provider_when_missing(self) -> None:
        config = AADConfig(enabled=True, tenant_id="tenant-id", client_id="client-id", scopes=("openid",), redirect_uri=None)
        self.assertEqual(config.secret_provider, "external")

    def test_aad_authenticator_reports_disabled_by_default(self) -> None:
        authenticator = AADAuthenticator()
        result = authenticator.authenticate(email="user@example.com", password="secret")
        self.assertIsInstance(result, AADAuthResult)
        self.assertFalse(result.enabled)
        self.assertEqual(result.mode, "disabled")

    def test_aad_authenticator_reports_scaffold_when_enabled(self) -> None:
        authenticator = AADAuthenticator(AADConfig(enabled=True, tenant_id="tenant-id", client_id="client-id"))
        result = authenticator.authenticate(email="user@example.com", password="secret")
        self.assertTrue(result.enabled)
        self.assertEqual(result.mode, "scaffold")
        self.assertEqual(result.provider, "entra")

    def test_services_keep_local_auth_path_when_aad_is_disabled(self) -> None:
        class DummyRepository:
            def __init__(self) -> None:
                self.calls: list[tuple[str, str]] = []

            def authenticate(self, *, email: str, password: str) -> dict[str, object] | None:
                self.calls.append((email, password))
                return {"id": 7, "email": email}

        repository = DummyRepository()
        services = object.__new__(LawimServices)
        services.repository = repository
        services.aad_authenticator = AADAuthenticator()

        user = services._authenticate_with_optional_aad(email="user@example.com", password="secret")
        self.assertEqual(user["email"], "user@example.com")
        self.assertEqual(repository.calls, [("user@example.com", "secret")])


class AADArchitectureTest(TestCase):
    def test_identity_provider_selection_supports_local_and_aad(self) -> None:
        local_provider = LocalIdentityProvider()
        identity = local_provider.load_identity("local-user")
        self.assertEqual(identity.provider, "local")
        self.assertEqual(identity.username, "local-user")

        aad_provider = AADIdentityProvider(AADConfig(enabled=True, tenant_id="tenant-id", client_id="client-id"))
        aad_identity = aad_provider.load_identity("user@example.com")
        self.assertEqual(aad_identity.provider, "aad")
        self.assertEqual(aad_identity.authentication_method, "scaffold")

    def test_claims_manager_reads_validates_and_maps(self) -> None:
        manager = ClaimsManager()
        raw_claims = {"roles": ["admin"], "groups": ["Engineering"], "scope": "openid"}
        claims = manager.read_claims(raw_claims)
        self.assertEqual(claims["scope"], "openid")
        self.assertTrue(manager.validate_claims(claims, required=("scope",)))

        identity = Identity(
            tenant="tenant-id",
            object_id="object-1",
            username="ada",
            display_name="Ada",
            email="ada@example.com",
            groups=("Engineering",),
            roles=("admin",),
            scopes=("openid",),
            claims={"scope": "openid"},
            provider=IdentityProviderKind.AAD.value,
            authentication_method="scaffold",
        )
        mapped = manager.map_identity(identity)
        self.assertEqual(mapped["provider"], "aad")
        self.assertEqual(mapped["roles"], ("admin",))

    def test_role_and_group_mapping_is_configurable(self) -> None:
        role_mapper = RoleMapper({"Engineering": "manager", "Sales": "agent"})
        group_mapper = GroupMapper()
        groups = group_mapper.from_claims(("Engineering", "Sales"))
        self.assertEqual(groups[0].name, "Engineering")
        self.assertEqual(role_mapper.map_groups_to_roles(("Engineering", "Sales")), ("manager", "agent"))

    def test_authorization_layers_support_policy_role_and_claims(self) -> None:
        role_authorizer = RoleBasedAuthorizer()
        policy_authorizer = PolicyBasedAuthorizer(lambda actor, context: actor.get("role") == "admin")
        claims_authorizer = ClaimsBasedAuthorizer(required_claims=("scope",))
        actor = {"role": "admin"}
        self.assertTrue(role_authorizer.authorize(actor, {}).allowed)
        self.assertTrue(policy_authorizer.authorize(actor, {}).allowed)
        self.assertTrue(claims_authorizer.authorize({"claims": {"scope": "openid"}}, {}).allowed)

    def test_tokens_and_session_manager_are_mock_only(self) -> None:
        access = MockAccessToken("token-value")
        id_token = MockIDToken("id-value")
        refresh = MockRefreshToken("refresh-value")
        self.assertEqual(access.token_type, "access")
        self.assertEqual(id_token.token_type, "id")
        self.assertEqual(refresh.token_type, "refresh")

        session_manager = AADSessionManager()
        session = session_manager.create_session(
            Identity(
                tenant="tenant-id",
                object_id="object-1",
                username="ada",
                display_name="Ada",
                email="ada@example.com",
                groups=(),
                roles=(),
                scopes=(),
                claims={},
                provider=IdentityProviderKind.AAD.value,
                authentication_method="scaffold",
            ),
            ttl_seconds=60,
        )
        self.assertTrue(session_manager.is_active(session.session_id))
        self.assertEqual(session.identity.username, "ada")

    def test_audit_logger_sanitizes_sensitive_payloads(self) -> None:
        logger = AADAuditLogger()
        event = logger.log("Authentication Success", details={"token": "secret", "email": "user@example.com"})
        self.assertEqual(event.event, "Authentication Success")
        self.assertEqual(event.details["email"], "user@example.com")
        self.assertNotIn("token", event.details)

    def test_identity_validator_rejects_invalid_provider_and_claims(self) -> None:
        validator = IdentityValidator()
        identity = Identity(
            tenant="tenant-id",
            object_id="object-1",
            username="ada",
            display_name="Ada",
            email="ada@example.com",
            groups=(),
            roles=(),
            scopes=(),
            claims={},
            provider="unknown",
            authentication_method="scaffold",
        )
        with self.assertRaises(ValueError):
            validator.validate_provider(identity.provider)
        with self.assertRaises(ValueError):
            validator.validate_claims(identity, required=("scope",))

    def test_aad_authentication_provider_returns_mock_result(self) -> None:
        provider = AADAuthenticationProvider(AADConfig(enabled=True, tenant_id="tenant-id", client_id="client-id"))
        result = provider.authenticate(principal="user@example.com", credentials={"password": "secret"})
        self.assertIsInstance(result, AuthenticationResult)
        self.assertTrue(result.success)
        self.assertEqual(result.provider, "aad")
        self.assertEqual(result.identity.provider, "aad")

    def test_session_manager_supports_destroy_and_retrieval(self) -> None:
        manager = AADSessionManager()
        identity = Identity(
            tenant="tenant-id",
            object_id="object-1",
            username="ada",
            display_name="Ada",
            email="ada@example.com",
            groups=(),
            roles=(),
            scopes=(),
            claims={},
            provider=IdentityProviderKind.AAD.value,
            authentication_method="scaffold",
        )
        session = manager.create_session(identity, ttl_seconds=30)
        self.assertEqual(manager.get_session(session.session_id).session_id, session.session_id)
        self.assertTrue(manager.destroy_session(session.session_id))
        self.assertFalse(manager.destroy_session(session.session_id))
        self.assertIsNone(manager.get_session(session.session_id))

    def test_secret_provider_defaults_to_external_without_storing_secrets(self) -> None:
        provider = ExternalSecretProvider("external")
        self.assertEqual(provider.resolve_secret("client_secret"), None)
        self.assertEqual(provider.provider_name, "external")
        self.assertIsNone(provider.store_secret("client_secret", "ignored"))
