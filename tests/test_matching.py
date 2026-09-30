from collector.matching import assess, match_text


def ids(text, entities):
    return [m.entity_id for m in match_text(text, entities)]


def test_institution_and_project_is_high(entities):
    text = ("The Clearing House Partners with Quant to Advance the On-Chain Money Initiative "
            "tokenized deposits")
    matches = match_text(text, entities)
    assert {"tch", "quant", "tokenized_deposits"} <= {m.entity_id for m in matches}
    result = assess(matches, "newswire")
    assert result.level == "high"
    assert result.tokens == ("QNT",)


def test_common_words_do_not_match(entities):
    assert "quant" not in ids("Quant Fund Manager Raises New Capital for Equity Strategy",
                              entities)
    assert "swift" not in ids("Taylor Swift Tour Boosts Local Payment Volumes", entities)
    assert "stellar" not in ids("Retailer Posts Stellar Results for the Quarter", entities)
    assert "us_bank" not in ids("U.S. Banks Rush to Cut Costs", entities)


def test_context_words_enable_ambiguous_names(entities):
    assert "swift" in ids("Swift opens its blockchain ledger to banks at Sibos", entities)
    assert "stellar" in ids("U.S. Bank tests stablecoin on the Stellar network", entities)
    assert "us_bank" in ids("U.S. Bank tests stablecoin on the Stellar network", entities)


def test_project_in_regulator_feed_is_medium(entities):
    matches = match_text("Statement on Tokenized Collateral Pilot Using Chainlink Data", entities)
    assert assess(matches, "regulator").level == "medium"
    assert assess(matches, "newswire").level is None


def test_theme_only_has_no_level(entities):
    matches = match_text("Banks Explore Tokenized Deposits for Cross-Border Payments", entities)
    result = assess(matches, "newswire")
    assert result.themes and not result.institutions and not result.projects
    assert result.level is None


def test_control_group_is_marked(entities):
    matches = match_text("Ripple expands RLUSD stablecoin custody with a bank", entities)
    ripple = [m for m in matches if m.entity_id == "ripple"]
    assert ripple and ripple[0].control


def test_project_feed_needs_more_than_the_project_itself(entities):
    own = match_text("Chainlink CCIP now live on a new chain, tokenization tooling", entities)
    assert not assess(own, "project", "chainlink").makes_event
    # The same text in a newswire is still an event.
    assert assess(own, "newswire").makes_event

    with_bank = match_text("Swift and Chainlink complete tokenized fund pilot with banks",
                           entities)
    result = assess(with_bank, "project", "chainlink")
    assert result.makes_event and result.level == "high"

    other_project = match_text("Chainlink data feeds now available on Hedera", entities)
    assert assess(other_project, "project", "chainlink").makes_event
