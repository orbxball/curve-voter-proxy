from brownie import accounts, config, Contract, Wei, web3, GaugeCleaner
from eth_utils import is_checksum_address
import click


def main():
    user = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    gc = GaugeCleaner.deploy({"from": user})

    gov = accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)
    ctrl = Contract('0x9E65Ad11b299CA0Abefc2799dDB6314Ef2d91080', owner=gov)
    token = Contract("0xb19059ebb43466C323583928285a49f558E572Fd")
    voter = Contract("0xF147b8125d2ef93FB6965Db97D6746952a133934")
    strategy = Contract(ctrl.strategies(token), owner=gov)
    gauge = Contract.from_explorer(strategy.gauge())
    
    # switch gov
    voter.setGovernance(gc, {"from": gov})

    # migrate token from gauge to vault
    gc.clear(token, {"from": gov})

    assert gauge.balanceOf(voter) == 0
    print(f"gauge balance of voter: {gauge.balanceOf(voter)}")
    assert token.balanceOf(voter) == 0
    print(f"token balance on voter: {token.balanceOf(voter)}")

    # set voter back to vault
    print(f"voter gov: {voter.governance()}")
    gc.setVoterGovernance({"from": gov})
    print(f"voter gov: {voter.governance()}")
