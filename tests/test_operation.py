from brownie import accounts, config, reverts, Wei, Contract
from useful_methods import state_of_vault, state_of_strategy
import brownie


def test_operation(web3, chain, vault, strategy, token, whale, gov, strategist, rewards, amount):
    scale = 10 ** token.decimals()
    # Deposit to the vault
    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    print(f"shares amount: {vault.balanceOf(whale)/scale}")
    vault.deposit(amount, {"from": whale})
    print(f"deposit amount: {amount/scale}")
    print(f"shares amount: {vault.balanceOf(whale)/scale}")
    assert token.balanceOf(vault.address) == amount
    print(f"token on strategy: {token.balanceOf(strategy)/scale}")

    print(f"\n****** Initial Status ******")
    print(f"\n****** State ******")
    state_of_strategy(strategy, token, vault)
    state_of_vault(vault, token)

    print(f"\n >>> call harvest")
    strategy.harvest()

    print(f"\n****** State ******")
    state_of_strategy(strategy, token, vault)
    state_of_vault(vault, token)

    print(f"\n >>> wait 1 day")
    chain.sleep(86400)
    chain.mine(1)

    print(f"\n >>> harvest to realized profit")
    strategy.harvest()

    print(f"\n****** State ******")
    state_of_strategy(strategy, token, vault)
    state_of_vault(vault, token)

    print(f"\n >>> wait 1 day to get the share price back")
    chain.sleep(86400)
    chain.mine(1)
    state_of_vault(vault, token)

    # withdraw
    print()
    print(f"shares amount: {vault.balanceOf(whale)/scale}")
    before = token.balanceOf(whale)
    vault.withdraw({"from": whale})
    print(f"withdraw amount: {(token.balanceOf(whale)-before)/scale}")
    print(f"shares amount: {vault.balanceOf(whale)/scale}")
    assert token.balanceOf(whale) != 0

    # all withdraw
    print()
    print(f"rewards+strategist withdraw")
    vault.withdraw({"from": rewards})
    vault.transfer(strategist, vault.balanceOf(strategy), {"from": strategy})
    vault.withdraw({"from": strategist})

    print(f"\n****** State ******")
    state_of_strategy(strategy, token, vault)
    state_of_vault(vault, token)

    print(f"\n >>> call tend")
    strategy.tend()
