// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import {Router} from "./router/Router.sol";
import {Token} from "./token/Token.sol";
import {Dex} from "./dex/SimpleDex.sol";
import {Adapter1} from "./adapter/Adapter1.sol";
import "./library/Utils.sol";
import "./executor/SimpleDexExecutor.sol";


contract Setup {
    Router public router;

    Token public zfn;
    Token public nfz;

    Adapter1 public adapter;

    Dex public dex;

    bool public hasClaimed = false;

    address player;

    constructor() payable {
        zfn = new Token("zafin", "ZFN");
        nfz = new Token("nfz", "NFZ");

        address[3] memory admins = [address(this), address(this), address(this)];
        router = new Router(admins);

        adapter = new Adapter1();
        router.updateAdaptor(address(adapter), true);

        dex = new Dex(address(zfn), address(nfz));
        dex.transferOwnership(address(router.executor()));

        zfn.transfer(address(dex), 50_000 ether);
        nfz.transfer(address(dex), 50_000 ether);

        Utils.MultiPath memory multiPath;
        {
            Utils.SinglePath[] memory singlePaths = new Utils.SinglePath[](1);
            {
                Utils.SimpleSwap[] memory paths = new Utils.SimpleSwap[](1);

                SimpleDexExecutor.SimpleDexData memory arg = SimpleDexExecutor.SimpleDexData(address(dex));
                bytes memory payload = abi.encode(arg);
                Utils.SimpleSwap memory path = Utils.SimpleSwap(1e18, 1, payload);
                paths[0] = path;

                Utils.Adapter[] memory adapters = new Utils.Adapter[](1);
                Utils.Adapter memory adapterUtil = Utils.Adapter(payable(adapter), 1e18, paths);
                adapters[0] = adapterUtil;
                Utils.SinglePath memory singlePath =
                    Utils.SinglePath(address(zfn), adapters);
                singlePaths[0] = singlePath;
            }
            multiPath = Utils.MultiPath(1e18, singlePaths);
        }

        Utils.MultiPath[] memory multiPath_1 = new Utils.MultiPath[](1);
        multiPath_1[0] = multiPath;

        uint256 amountIn = 1000 ether;
        uint256 slippage = amountIn * 8 / 10;

        uint256 nfzBalanceBefore = nfz.balanceOf(address(this));

        zfn.approve(address(router), amountIn);
        router.swap(address(zfn), amountIn, address(nfz), slippage, true, multiPath_1);

        uint256 nfzBalanceAfter = nfz.balanceOf(address(this));

        uint256 amountOut = nfzBalanceAfter - nfzBalanceBefore;

        uint256 feeTaken = amountIn - amountOut;

        require(feeTaken > 0, "fee must be greater than zero");
    }

    function claim() external {
        require(!hasClaimed);
        hasClaimed = true;
        zfn.transfer(msg.sender, 1000 ether);
        player = msg.sender;
    }

    function isSolved() external view returns (bool) {
        return (nfz.balanceOf(player) == 1000 ether);
    }
}