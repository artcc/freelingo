import ipaddress

from fastapi import Request
from slowapi import Limiter

from app.core.config import settings


def _parse_networks(values: list[str]) -> list[ipaddress.IPv4Network | ipaddress.IPv6Network]:
    networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
    for value in values:
        candidate = value.strip()
        if not candidate:
            continue
        try:
            networks.append(ipaddress.ip_network(candidate, strict=False))
        except ValueError:
            continue
    return networks


def _is_trusted_proxy(host: str | None) -> bool:
    if not host:
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return any(address in network for network in _parse_networks(settings.TRUSTED_PROXY_IPS))


def _valid_ip(value: str) -> str | None:
    candidate = value.strip()
    try:
        ipaddress.ip_address(candidate)
    except ValueError:
        return None
    return candidate


def _get_real_ip(request: Request) -> str:
    """Return the client IP used as the rate-limit key.

    X-Real-IP / X-Forwarded-For are only honoured when the TCP peer is a
    trusted reverse proxy (TRUSTED_PROXY_IPS). A client connecting directly
    cannot change its rate-limit bucket by sending these headers.
    """
    peer = request.client.host if request.client else None
    if _is_trusted_proxy(peer):
        x_real_ip = _valid_ip(request.headers.get("X-Real-IP", ""))
        if x_real_ip:
            return x_real_ip
        forwarded_for = request.headers.get("X-Forwarded-For", "")
        if forwarded_for:
            # Walk from the right: the right-most untrusted hop is the client.
            hops = [hop for hop in (_valid_ip(part) for part in forwarded_for.split(",")) if hop]
            for hop in reversed(hops):
                if not _is_trusted_proxy(hop):
                    return hop
            if hops:
                return hops[0]
    return peer or "unknown"


# Desktop mode: disable rate limiting or use in-memory storage
if settings.DESKTOP_MODE or not settings.REDIS_ENABLED:
    # Use in-memory storage for desktop (single user doesn't need strict limits)
    limiter = Limiter(
        key_func=_get_real_ip,
        default_limits=["120/minute"] if settings.RATE_LIMIT_ENABLED else [],
        enabled=settings.RATE_LIMIT_ENABLED and not settings.DESKTOP_MODE,
        storage_uri="memory://",
    )
else:
    # Server mode: use Redis for distributed rate limiting
    limiter = Limiter(
        key_func=_get_real_ip,
        default_limits=["60/minute"] if settings.RATE_LIMIT_ENABLED else [],
        enabled=settings.RATE_LIMIT_ENABLED,
        storage_uri=settings.REDIS_URL,
    )
