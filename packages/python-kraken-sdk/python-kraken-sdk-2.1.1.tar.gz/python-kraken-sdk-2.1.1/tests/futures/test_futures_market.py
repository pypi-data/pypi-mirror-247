#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures market client."""

import pytest

from kraken.futures import Market

from .helper import is_not_error, is_success


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_ohlc(futures_market: Market) -> None:
    """
    Checks the ``get_ohlc`` endpoint.
    """
    assert isinstance(
        futures_market.get_ohlc(
            tick_type="trade",
            symbol="PI_XBTUSD",
            resolution="1m",
            from_="1668989233",
            to="1668999233",
        ),
        dict,
    )


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_ohlc_failing_wrong_tick_type(futures_market: Market) -> None:
    """
    Checks the ``get_ohlc`` function by passing an invalid tick type.
    """
    with pytest.raises(
        ValueError,
        match=r"tick_type must be in \('spot', 'mark', 'trade'\)",
    ):
        futures_market.get_ohlc(symbol="XBTUSDT", resolution="240", tick_type="fail")


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_ohlc_failing_wrong_resolution(futures_market: Market) -> None:
    """
    Checks the ``get_ohlc`` function by passing an invalid resolution.
    """
    with pytest.raises(
        ValueError,
        match=r"resolution must be in \('1m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w'\)",
    ):
        futures_market.get_ohlc(symbol="XBTUSDT", resolution="1234", tick_type="trade")


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_tick_types(futures_market: Market) -> None:
    assert isinstance(futures_market.get_tick_types(), list)


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_tradeable_products(futures_market: Market) -> None:
    """
    Checks the ``get_tradeable_products`` endpoint.
    """
    assert isinstance(futures_market.get_tradeable_products(tick_type="mark"), list)


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_resolutions(futures_market: Market) -> None:
    """
    Checks the ``get_resolutions`` endpoint.
    """
    assert isinstance(
        futures_market.get_resolutions(tick_type="trade", tradeable="PI_XBTUSD"),
        list,
    )


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_fee_schedules(futures_market: Market) -> None:
    """
    Checks the ``get_fee_schedules`` endpoint.
    """
    assert is_success(futures_market.get_fee_schedules())


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_market()
def test_get_fee_schedules_vol(futures_auth_market: Market) -> None:
    """
    Checks the ``get_fee_schedules_vol`` endpoint.
    """
    assert is_success(futures_auth_market.get_fee_schedules_vol())


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_orderbook(futures_market: Market) -> None:
    """
    Checks the ``get_orderbook`` endpoint.
    """
    # assert type(market.get_orderbook()) == dict # raises 500-INTERNAL_SERVER_ERROR on Kraken,
    # but symbol is optional as described in the API documentation (Dec, 2022)
    assert is_success(futures_market.get_orderbook(symbol="PI_XBTUSD"))


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_tickers(futures_market: Market) -> None:
    """
    Checks the ``get_tickers`` endpoint.
    """
    assert is_success(futures_market.get_tickers())


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_instruments(futures_market: Market) -> None:
    """
    Checks the ``get_instruments`` endpoint.
    """
    assert is_success(futures_market.get_instruments())


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_instruments_status(futures_market: Market) -> None:
    """
    Checks the ``get_instruments_status`` endpoint.
    """
    assert is_success(futures_market.get_instruments_status())
    assert is_success(futures_market.get_instruments_status(instrument="PI_XBTUSD"))


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_trade_history(futures_market: Market) -> None:
    """
    Checks the ``get_trade_history`` endpoint.
    """
    assert is_success(futures_market.get_trade_history(symbol="PI_XBTUSD"))


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_historical_funding_rates(futures_market: Market) -> None:
    """
    Checks the ``get_historical_funding_rates`` endpoint.
    """
    assert is_success(futures_market.get_historical_funding_rates(symbol="PI_XBTUSD"))


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_market()
def test_get_leverage_preference(futures_auth_market: Market) -> None:
    """
    Checks the ``get_leverage_preference`` endpoint.
    """
    assert is_not_error(futures_auth_market.get_leverage_preference())


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_market()
@pytest.mark.skip(reason="CI does not have trade permission")
def test_set_leverage_preference(futures_auth_market: Market) -> None:
    """
    Checks the ``set_leverage_preference`` endpoint.
    """
    old_leverage_preferences: dict = futures_auth_market.get_leverage_preference()
    assert "result" in old_leverage_preferences
    assert old_leverage_preferences["result"] == "success"
    assert is_success(
        futures_auth_market.set_leverage_preference(symbol="PF_XBTUSD", maxLeverage=2),
    )

    new_leverage_preferences: dict = futures_auth_market.get_leverage_preference()
    assert "result" in new_leverage_preferences
    assert new_leverage_preferences["result"] == "success"
    assert "leveragePreferences" in new_leverage_preferences
    assert {"symbol": "PF_XBTUSD", "maxLeverage": 2.0} in new_leverage_preferences[
        "leveragePreferences"
    ]

    if "leveragePreferences" in old_leverage_preferences:
        for setting in old_leverage_preferences["leveragePreferences"]:
            if "symbol" in setting and setting["symbol"] == "PF_XBTUSD":
                assert is_success(
                    futures_auth_market.set_leverage_preference(symbol="PF_XBTUSD"),
                )
                break


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_market()
def test_get_pnl_preference(futures_auth_market: Market) -> None:
    """
    Checks the ``get_pnl_preference`` endpoint.
    """
    assert is_not_error(futures_auth_market.get_pnl_preference())


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_market()
@pytest.mark.skip(reason="CI does not have trade permission")
def test_set_pnl_preference(futures_auth_market: Market) -> None:
    """
    Checks the ``set_pnl_preference`` endpoint.
    """
    old_pnl_preference: dict = futures_auth_market.get_pnl_preference()
    assert "result" in old_pnl_preference
    assert old_pnl_preference["result"] == "success"
    assert is_success(
        futures_auth_market.set_pnl_preference(symbol="PF_XBTUSD", pnlPreference="BTC"),
    )

    new_pnl_preference: dict = futures_auth_market.get_pnl_preference()
    assert "result" in new_pnl_preference
    assert new_pnl_preference["result"] == "success"
    assert "preferences" in new_pnl_preference
    assert {"symbol": "PF_XBTUSD", "pnlCurrency": "BTC"} in new_pnl_preference[
        "preferences"
    ]

    if "preferences" in old_pnl_preference:
        for setting in old_pnl_preference["preferences"]:
            if "symbol" in setting and setting["symbol"] == "PF_XBTUSD":
                assert is_success(
                    futures_auth_market.set_pnl_preference(
                        symbol="PF_XBTUSD",
                        pnlPreference=setting["pnlCurrency"],
                    ),
                )
                break


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_public_execution_events(futures_market: Market) -> None:
    """
    Checks the ``get_public_execution_events`` endpoint.
    """
    assert is_not_error(
        futures_market.get_public_execution_events(
            tradeable="PF_SOLUSD",
            since=1668989233,
            before=1668999999,
        ),
    )


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_public_order_events(futures_market: Market) -> None:
    """
    Checks the ``public_order_events`` endpoint.
    """
    assert is_not_error(
        futures_market.get_public_order_events(
            tradeable="PF_SOLUSD",
            since=1668989233,
            sort="asc",
        ),
    )


@pytest.mark.futures()
@pytest.mark.futures_market()
def test_get_public_mark_price_events(futures_market: Market) -> None:
    """
    Checks the ``get_public_mark_price_events`` endpoint.
    """
    assert is_not_error(
        futures_market.get_public_mark_price_events(
            tradeable="PF_SOLUSD",
            since=1668989233,
        ),
    )
