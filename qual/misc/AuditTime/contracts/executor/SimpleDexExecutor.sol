// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "../library/IERC20.sol";
import "../library/Utils.sol";
import "../interface/ISimpleDex.sol";

/// @notice sushiswapV3, uniswapV3, pancakeV3 router
abstract contract SimpleDexExecutor {

    struct SimpleDexData {
        address pool;
    }

    function swapSimpleDex(address fromToken, uint256 fromTokenAmount, bytes memory data) internal {
        SimpleDexData memory arg = abi.decode(data, (SimpleDexData));

        // approve
        IERC20(fromToken).approve(arg.pool, fromTokenAmount);
        // execute
        ISimpleDex(arg.pool).trade(fromToken, fromTokenAmount);
    }
}