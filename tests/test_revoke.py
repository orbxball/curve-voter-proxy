import pytest


def test_revoke(gov, vault, strategy, token, whale, amount):
    scale = 10 ** token.decimals()
    # Deposit to the vault
    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    vault.deposit(amount, {"from": whale})
    assert token.balanceOf(vault.address) == amount
    strategy.harvest({"from": gov})

    vault.revokeStrategy(strategy, {"from": gov})
    strategy.harvest({"from": gov})

    assert vault.totalDebt() == 0
    assert vault.totalAssets() == token.balanceOf(vault)

