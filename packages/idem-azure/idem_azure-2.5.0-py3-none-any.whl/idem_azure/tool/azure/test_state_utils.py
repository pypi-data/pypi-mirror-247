import copy
from typing import Any
from typing import Dict


def generate_test_state(
    hub,
    enforced_state: Dict[str, Any],
    desired_state: Dict[str, Any],
):
    """
    Giving the previous enforced state and desired state inputs, generate a test state,
     which can be used by idem state --test as the running result.

    Args:
        hub: The redistributed pop central hub.
        enforced_state: Previous enforced state.
        desired_state: A dictionary of desired state values. If any property's value is None,
         this property will be ignored. This is to match the behavior when a present() input is a None, Idem does not
         do an update.

    Returns:
        A result state.
    """
    desired_state_clean = {k: v for k, v in desired_state.items() if v is not None}
    if enforced_state:
        plan_state = copy.deepcopy(enforced_state)
        for parameter in desired_state_clean.keys():
            if plan_state.get(parameter) != desired_state_clean.get(parameter):
                plan_state[parameter] = desired_state_clean.get(parameter)
    else:
        plan_state = copy.deepcopy(desired_state_clean)
    return plan_state
