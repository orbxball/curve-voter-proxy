import pytest
from brownie import chain


def test_emergency_exit(gov, vault, strategy, token, whale, amount):
    scale = 10 ** token.decimals()
    # Deposit to the vault
    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    vault.deposit(amount, {"from": whale})
    assert token.balanceOf(vault.address) == amount
    strategy.harvest({"from": gov})

    chain.sleep(86400)
    chain.mine(1)

    strategy.setEmergencyExit({"from": gov})
    strategy.harvest({"from": gov})

    assert vault.totalDebt() == 0
    assert vault.totalAssets() == token.balanceOf(vault)
