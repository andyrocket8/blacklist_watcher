from src.schemas.address_dedup_info import AddressDedupInfo


def test_address_dedup_info():
    # test add operation
    test_element_1 = AddressDedupInfo(source_agent='agent_one')
    assert test_element_1.source_agent == 'agent_one', '"source_agent" attribute value must be equal "agent_one"'
    assert test_element_1.count == 0, '"count" attribute value must be equal 0'

    test_element_1 += AddressDedupInfo(source_agent='agent_two', count=10)
    assert test_element_1.source_agent == 'agent_two', '"source_agent" attribute value must be equal "agent_two"'
    assert test_element_1.count == 10, '"count" attribute value must be equal 10'

    # test subtract operation
    test_element_2 = AddressDedupInfo(count=-1)
    assert test_element_2.source_agent == '', '"source_agent" attribute value must be equal ""'
    assert test_element_2.count == -1, '"count" attribute value must be equal -1'

    test_element_2 -= AddressDedupInfo(source_agent='agent_three', count=-2)
    assert test_element_2.source_agent == 'agent_three', '"source_agent" attribute value must be equal "agent_three"'
    assert test_element_2.count == 1, '"count" attribute value must be equal 1'

    # test direct __add__
    test_element_3 = test_element_1 + test_element_2
    assert (
        test_element_3.source_agent == test_element_2.source_agent
    ), '"source_agent" attribute value must be equal "agent_three"'
    assert (
        test_element_3.count == test_element_1.count + test_element_2.count
    ), '"count" attribute value must be equal sum of "test_element_1" and "test_element_2"'

    # test direct __sub__
    test_element_4 = test_element_3 - test_element_1
    assert (
        test_element_4.source_agent == test_element_1.source_agent
    ), '"source_agent" attribute value must be equal "agent_two"'
    assert (
        test_element_4.count == test_element_3.count - test_element_1.count
    ), '"count" attribute value must be equal sub of "test_element_3" and "test_element_1"'
