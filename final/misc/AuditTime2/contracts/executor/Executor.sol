// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import "../library/Ownable.sol";
import "../library/ReentrancyGuard.sol";
import "../interface/IExecutor.sol";
import "../interface/IAdapter.sol";
import {UniversalERC20} from "../library/UniversalERC20.sol";
import "../library/SignedDecimalMath.sol";
import "../library/IERC20.sol";

/**
 * @title Executor
 * @notice A delegatecall-based executor for split-route swaps
 * @dev Key features:
 * - Supports multi-path swaps with percentage splits
 * - Whitelisted adapter system
 * - Owner controlled adapter management
 * - Handles both ERC20 and ETH
 * - Protected against reentrancy
 *
 * Flow: split amount -> delegate to adapters ->
 * execute swaps -> aggregate results
 */
contract Executor is Ownable, ReentrancyGuard {
    using UniversalERC20 for IERC20;
    using SignedDecimalMath for uint256;

    mapping(address => bool) public whiteListAdapter;
    address[] public adapterList;
    mapping(address => mapping(address => uint256)) public balances;

    constructor() Ownable(msg.sender) {}


    function executeMegaSwap(address fromToken, address toToken, Utils.MultiPath[] calldata paths)
        external
        payable
        onlyOwner
        nonReentrant
    {
        uint256 totalPercent;
        uint256 fromTokenAmount = IERC20(fromToken).balanceOf(address(this));


        for (uint256 i = 0; i < paths.length; i++) {
            totalPercent += paths[i].percent;
            uint256 amount = fromTokenAmount.decimalMul(paths[i].percent);

            if (i == paths.length - 1) {
                amount = IERC20(fromToken).balanceOf(address(this));
            }
            executeMultiPath(address(fromToken), amount, paths[i].paths);
        }
        require(totalPercent == SignedDecimalMath.ONE, "Executor: Invalid MultiPath total percent");
        uint256 balance = IERC20(toToken).balanceOf(address(this));
        IERC20(toToken).transfer(payable(msg.sender), balance);
    }

    function executeMultiPath(address fromToken, uint256 fromTokenAmount, Utils.SinglePath[] calldata paths) internal {
        for (uint256 i = 0; i < paths.length; i++) {
            fromToken = i > 0 ? paths[i - 1].toToken : fromToken;
            
            // Record balance before swap (only if there are multiple paths)
            uint256 midTokenBalanceBefore;
            if (paths.length > 1 && i < paths.length - 1) {
                midTokenBalanceBefore = IERC20(paths[i].toToken).balanceOf(address(this));
            }
            
            uint256 totalPercent;
            for (uint256 j = 0; j < paths[i].adapters.length; j++) {
                Utils.Adapter memory adapter = paths[i].adapters[j];
                require(whiteListAdapter[adapter.adapter], "Executor: adapter not whitelist");
                totalPercent += adapter.percent;
                uint256 fromAmountSlice = fromTokenAmount.decimalMul(adapter.percent);


                //DELEGATING CALL TO THE ADAPTER
                (bool success,) = adapter.adapter.delegatecall(
                    abi.encodeWithSelector(
                        IAdapter.executeSimpleSwap.selector, fromToken, paths[i].toToken, fromAmountSlice, adapter.swaps
                    )
                );
                if (success == false) {
                    assembly {
                        let ptr := mload(0x40)
                        let size := returndatasize()
                        returndatacopy(ptr, 0, size)
                        revert(ptr, size)
                    }
                }
            }
            require(totalPercent == SignedDecimalMath.ONE, "Executor: Invalid adapter total percent");
            
            // Calculate the actual amount received from this swap (only if there are multiple paths)
            if (paths.length > 1 && i < paths.length - 1) {
                uint256 midTokenBalanceAfter = IERC20(paths[i].toToken).balanceOf(address(this));
                uint256 receivedAmount = midTokenBalanceAfter - midTokenBalanceBefore;
                fromTokenAmount = receivedAmount;
            }
        }
    }

    function updateAdaptor(address _adapter, bool isAdd) external onlyOwner {
        whiteListAdapter[_adapter] = isAdd;
        if (isAdd) {
            adapterList.push(_adapter);
        } else {
            for (uint256 i = 0; i < adapterList.length; i++) {
                if (adapterList[i] == _adapter) {
                    adapterList[i] = adapterList[adapterList.length - 1];
                    adapterList.pop();
                    break;
                }
            }
        }
    }

    function getAdapters() external view returns (address[] memory) {
        return adapterList;
    }

    receive() external payable {}
}