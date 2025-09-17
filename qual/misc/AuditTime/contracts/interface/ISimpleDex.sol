// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

interface ISimpleDex {
    function trade(
        address fromToken,
        uint256 amount
    ) external;
}