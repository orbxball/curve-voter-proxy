def state_of_strategy(strategy, currency, vault):
    scale = 10 ** currency.decimals()
    state = vault.strategies(strategy).dict()
    print(f"\n--- state of {strategy.name()} ---")
    print("Want:", currency.balanceOf(strategy) / scale)
    print("Total assets estimate:", strategy.estimatedTotalAssets() / scale)
    print(f"Total Strategy Debt: {state['totalDebt'] / scale}")
    print(f"Strategy Debt Ratio: {state['debtRatio']}")
    print(f"Total Strategy Gain: {state['totalGain'] / scale}")
    print(f"Total Strategy Loss: {state['totalLoss'] / scale}")
    print(f"Balance in gauge: {strategy.balanceOfPool() / scale}")
    print("Harvest Trigger:", strategy.harvestTrigger(1000000 * 30 * 1e9))
    print("Tend Trigger:", strategy.tendTrigger(1000000 * 30 * 1e9))
    print("Emergency Exit:", strategy.emergencyExit())


def state_of_vault(vault, currency):
    scale = 10 ** currency.decimals()
    print(f"\n--- state of {vault.name()} vault ---")
    print(f"Total Assets: {vault.totalAssets() / scale}")
    print(f"Loose balance in vault: {currency.balanceOf(vault) / scale}")
    print(f"Total Debt: {vault.totalDebt() / scale}")
    print(f"Price per share: {vault.pricePerShare() / scale}")
    print(f"Vault share totalSupply: {vault.totalSupply() / scale}")
