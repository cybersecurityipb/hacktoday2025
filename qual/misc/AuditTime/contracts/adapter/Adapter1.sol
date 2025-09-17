// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import "../library/UniversalERC20.sol";
import "../library/SignedDecimalMath.sol";
import "../interface/IAdapter.sol";
import "../executor/SimpleDexExecutor.sol";

contract Adapter1 is
    IAdapter,
    SimpleDexExecutor
{
    using UniversalERC20 for IERC20;
    using SignedDecimalMath for uint256;

    constructor() {}

    /**
     * @notice Execute a simple swap
     * @param fromToken The address of the token to swap from
     * @param toToken The address of the token to swap to
     * @param fromTokenAmount The amount of the token to swap from
     * @param swaps The array of swaps to execute
     */
    function executeSimpleSwap(
        address fromToken,
        address toToken,
        uint256 fromTokenAmount,
        Utils.SimpleSwap[] memory swaps
    ) external payable {
        uint256 totalPercent;
        for (uint256 i = 0; i < swaps.length; i++) {
            Utils.SimpleSwap memory swap = swaps[i];
            totalPercent += swap.percent;
            if (swap.swapType == 1) {
                swapSimpleDex(fromToken, fromTokenAmount, swap.data);
            } else {
                revert("Executor: Invalid swap type");
            }
        }
        require(totalPercent == SignedDecimalMath.ONE, "Adaptor: Invalid total percent");
    }

    receive() external payable {}
}