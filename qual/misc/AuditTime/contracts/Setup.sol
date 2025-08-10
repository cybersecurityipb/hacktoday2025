// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import {Router} from "./router/Router.sol";
import {Token} from "./token/Token.sol";
import {Dex} from "./dex/SimpleDex.sol";
import {Adapter1} from "./adapter/Adapter1.sol";


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

        uint256 depositAmount = 950_000 ether - 1;

        zfn.approve(address(router.executor()), depositAmount);
        nfz.approve(address(router.executor()), depositAmount);

        (bool success, ) = address(router.executor()).call(abi.encodeWithSignature("deposit(address,address,uint256)", address(zfn), address(this), depositAmount));
        require(success);
        (success, ) = address(router.executor()).call(abi.encodeWithSignature("deposit(address,address,uint256)", address(nfz), address(this), depositAmount));
        require(success);

    }

    function claim() external {
        require(!hasClaimed);
        hasClaimed = true;
        zfn.transfer(msg.sender, 1);
        nfz.transfer(msg.sender, 1);
        player = msg.sender;
    }

    function isSolved() external view returns (bool) {
        return (zfn.balanceOf(player) == 950_000 ether) && (nfz.balanceOf(player) == 950_000 ether);
    }
}