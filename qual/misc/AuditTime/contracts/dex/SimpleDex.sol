// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import "../library/UniversalERC20.sol";
import "../library/Ownable.sol";


contract Dex is Ownable {

    using UniversalERC20 for IERC20;

    address public immutable token0;
    address public immutable token1;

    constructor(address _token0, address _token1) Ownable(msg.sender) {
        token0 = _token0;
        token1 = _token1;
    }

    function trade(address fromToken, uint256 amount) external onlyOwner {

        if (fromToken == token0) {
            IERC20(token0).transferFrom(msg.sender, address(this), amount);
            IERC20(token1).transfer(msg.sender, amount);
        }
        else if (fromToken == token1) {
            IERC20(token1).transferFrom(msg.sender, address(this), amount);
            IERC20(token0).transfer(msg.sender, amount);
        }
        else {
            revert("DEX: invalid from token");
        }
    }
}