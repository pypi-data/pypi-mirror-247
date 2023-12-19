import httpx
import pytest

from cashu.core.base import CheckSpendableRequest, CheckSpendableResponse, Proof

BASE_URL = "http://localhost:3337"


@pytest.mark.asyncio
async def test_info(ledger):
    response = httpx.get(f"{BASE_URL}/info")
    assert response.status_code == 200, f"{response.url} {response.status_code}"
    assert response.json()["pubkey"] == ledger.pubkey.serialize().hex()


@pytest.mark.asyncio
async def test_api_keys(ledger):
    response = httpx.get(f"{BASE_URL}/keys")
    assert response.status_code == 200, f"{response.url} {response.status_code}"
    assert response.json() == {
        str(k): v.serialize().hex() for k, v in ledger.keyset.public_keys.items()
    }


@pytest.mark.asyncio
async def test_api_keysets(ledger):
    response = httpx.get(f"{BASE_URL}/keysets")
    assert response.status_code == 200, f"{response.url} {response.status_code}"
    assert response.json()["keysets"] == list(ledger.keysets.keysets.keys())


@pytest.mark.asyncio
async def test_api_keyset_keys(ledger):
    response = httpx.get(
        f"{BASE_URL}/keys/{'1cCNIAZ2X/w1'.replace('/', '_').replace('+', '-')}"
    )
    assert response.status_code == 200, f"{response.url} {response.status_code}"
    assert response.json() == {
        str(k): v.serialize().hex() for k, v in ledger.keyset.public_keys.items()
    }


@pytest.mark.asyncio
async def test_api_mint_validation(ledger):
    response = httpx.get(f"{BASE_URL}/mint?amount=-21")
    assert "detail" in response.json()
    response = httpx.get(f"{BASE_URL}/mint?amount=0")
    assert "detail" in response.json()
    response = httpx.get(f"{BASE_URL}/mint?amount=2100000000000001")
    assert "detail" in response.json()
    response = httpx.get(f"{BASE_URL}/mint?amount=1")
    assert "detail" not in response.json()


@pytest.mark.asyncio
async def test_api_check_state(ledger):
    proofs = [
        Proof(id="1234", amount=0, secret="asdasdasd", C="asdasdasd"),
        Proof(id="1234", amount=0, secret="asdasdasd1", C="asdasdasd1"),
    ]
    payload = CheckSpendableRequest(proofs=proofs)
    response = httpx.post(
        f"{BASE_URL}/check",
        json=payload.dict(),
    )
    assert response.status_code == 200, f"{response.url} {response.status_code}"
    states = CheckSpendableResponse.parse_obj(response.json())
    assert states.spendable
    assert len(states.spendable) == 2
    assert states.pending
    assert len(states.pending) == 2
