// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import "../library/Utils.sol";

interface IExecutor {
    /**
     * @notice Execute a mega swap
     * @param fromToken The address of the token to swap from
     * @param toToken The address of the token to swap to
     * @param paths The array of paths to swap
     */
    function executeMegaSwap(address fromToken, address toToken, address user, Utils.MultiPath[] calldata paths) external payable;

    function updateAdaptor(address _adapter, bool isAdd) external;

    function getAdapters() external view returns (address[] memory);
}