from __future__ import annotations


def dedupe_chain(chain: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in chain:
        provider = str(item or "").strip().lower()
        if not provider or provider in seen:
            continue
        seen.add(provider)
        ordered.append(provider)
    return tuple(ordered)


def build_provider_chain(*, complexity: str, primary_provider: str, complex_provider: str, fallback_chain: tuple[str, ...]) -> tuple[str, ...]:
    chain = [provider for provider in fallback_chain if provider != "internal"] if fallback_chain else [
        primary_provider,
        complex_provider,
        "gemini_primary",
        "gemini_secondary",
    ]
    if complexity == "complex":
        ordered = [complex_provider, primary_provider, *chain]
    else:
        ordered = [primary_provider, complex_provider, *chain]
    return dedupe_chain(ordered)
