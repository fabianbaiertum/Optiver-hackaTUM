params = {}   #dictionary with our tuned parameters

def microprice_calculation():
    return 0


#some other signals we used for pricing calculation: order book imbalance, volatility, inventory risk, etc.

def pricing_calculation():
    return 0,0

def execution_logic():
    return 0,0,0

def position_sizing_calculation():
    return 0



# our bid/ask is the currently quoted prices by us.
def market_making(best_bid, best_bid_volume, best_ask, best_ask_volume, history_microprices, current_position, our_bid, our_ask, our_bid_volume, our_ask_volume,params):
    # to exclude our current bid ask prices and volumes! for this we input our current prices, we exclude only, if we are at the Top of the Book, as we only use TOB data.
    if our_bid == best_bid:
        best_bid_volume -= our_bid_volume
    if our_ask == best_ask:
        best_ask_volume -= our_ask_volume

    tick_size = params["tick_size"]
    microprice = microprice_calculation(best_bid, best_bid_volume, best_ask, best_ask_volume,
                                        method=params["microprice"])
    history_microprices.append(microprice)
    if len(history_microprices) > 100:
        history_microprices.pop(0)

    bid_price,ask_price = pricing_calculation(best_bid, best_bid_volume, best_ask, best_ask_volume, history_microprices, current_position, params)

    ### execution logic

    bid_price, bid_action1, bid_action2 = execution_logic()

    ask_price, ask_action1, ask_action2 = execution_logic()

    ### position sizing logic

    bid_volume = position_sizing_calculation()

    ask_volume = position_sizing_calculation()


    # Disable quoting on one side if we're near the position limit
    position_threshold = 0.95 * params["position_limit"] #if we have 95 percent of a position limit in one direction don't quote on this side

    if current_position >= position_threshold:
        # Too long — stop quoting bids
        bid_volume = 0
    elif current_position <= -position_threshold:
        # Too short — stop quoting asks
        ask_volume = 0

    return bid_price, bid_volume, ask_price, ask_volume, bid_action1, ask_action1, bid_action2, ask_action2