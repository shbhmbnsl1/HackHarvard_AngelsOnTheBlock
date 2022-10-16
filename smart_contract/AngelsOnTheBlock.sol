// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "./ERC721.sol";

contract AngelsOnTheBlock is ERC721 {
    event Mint(address indexed from, uint256 indexed tokenId);

    modifier callerIsUser() {
        require(tx.origin == msg.sender, "The caller is another contract");
        _;
    }

    modifier claimActive() {
        require(
            isClaimActive == true, "Claim is not active"
        );
        _;
    }

    uint256 public totalMintedTokens = 0;

    bool public isClaimActive = true;

    uint256 private maxTokensPerTransaction = 50;
    
    string private baseURI = "https://minervaequity.s3.amazonaws.com/";

    uint256 public pricePerToken = 150000000000000000;
    
    mapping(address => uint256) private claimedBlockCrunchTokenPerWallet;

    uint16[] availableBlockCrunchTokens;

    constructor() ERC721("AngelsOnTheBlock", "ANGBLCK") {}

    // ONLY OWNER

    /**
     * @dev Allows to withdraw the Ether in the contract
     */
    function withdraw() external onlyOwner {
        uint256 totalBalance = address(this).balance;
        payable(owner()).transfer(totalBalance);
    }

    /**
     * @dev Sets the base URI for the API that provides the NFT data.
     */
    function setBaseTokenURI(string memory _uri) external onlyOwner {
        baseURI = _uri;
    }


    /**
     * @dev Populates the available blockCrunch tokens
     */
    function addAvailableblockCrunchTokens(uint16 from, uint16 to)
        external
        onlyOwner
    {
        for (uint16 i = from; i <= to; i++) {
            availableBlockCrunchTokens.push(i);
        }
    }

    /**
     * @dev Checks if a blockCrunch token is in the available list
     */
    function isBlockCrunchTokenAvailable(uint16 tokenId)
        external
        view
        onlyOwner
        returns (bool)
    {
        for (uint16 i; i < availableBlockCrunchTokens.length; i++) {
            if (availableBlockCrunchTokens[i] == tokenId) {
                return true;
            }
        }

        return false;
    }

    /**
    * @dev Sets max tokens per transaction
     */
    function setMaxTokensPerTransaction(uint256 _maxTokensPerTransaction)
        external
        onlyOwner
    {
        maxTokensPerTransaction = _maxTokensPerTransaction;
    }

    /**
    @dev Enables the claim
     */
    function enableClaim() external onlyOwner {
        isClaimActive = true;
    }

    /**
    @dev Disables the claim
     */
    function disableClaim() external onlyOwner {
        isClaimActive = true;
    }

    /**
    @dev Sets the price per nft
     */
    function setPricePerToken(uint256 _pricePerToken) external onlyOwner {
        pricePerToken = _pricePerToken;
    }



    // END ONLY COLLABORATORS

    /**
     * @dev Claim upto 50 blockCrunch tokens in public sale
     */
    function claimblockCrunchTokens(uint256 quantity)
        external
        payable
        callerIsUser
        claimActive
        returns (uint256[] memory)
    {
        require(
            msg.value >= pricePerToken * quantity,
            "Not enough Ether to claim the blockCrunchTokens"
        );
        require(quantity <= maxTokensPerTransaction, "Max tokens per transaction can be 50");
        require(availableBlockCrunchTokens.length >= quantity, "Not enough blockCrunch tokens left");

        uint256[] memory tokenIds = new uint256[](quantity);

        claimedBlockCrunchTokenPerWallet[msg.sender] += quantity;
        totalMintedTokens += quantity;

        for (uint256 i; i < quantity; i++) {
            tokenIds[i] = getblockCrunchTokenToBeClaimed();
        }

        _batchMint(msg.sender, tokenIds);
        return tokenIds;
    }

    /**
     * @dev Returns the tokenId by index
     */
    function tokenByIndex(uint256 tokenId) external view returns (uint256) {
        require(
            _exists(tokenId),
            "ERC721: operator query for nonexistent token"
        );

        return tokenId;
    }

    /**
     * @dev Returns the base URI for the tokens API.
     */
    function baseTokenURI() external view returns (string memory) {
        return baseURI;
    }

    /**
     * @dev Returns how many blockCrunchTokens are still available to be claimed
     */
    function getAvailableblockCrunchTokens() external view returns (uint256) {
        return availableBlockCrunchTokens.length;
    }

    /**
     * @dev Returns the total supply
     */
    function totalSupply() external view virtual returns (uint256) {
        return totalMintedTokens;
    }


    // Private and Internal functions

    /**
     * @dev Returns a random available blockCrunchToken to be claimed
     */
    function getblockCrunchTokenToBeClaimed() private returns (uint256) {
        uint256 random = _getRandomNumber(availableBlockCrunchTokens.length);
        uint256 tokenId = uint256(availableBlockCrunchTokens[random]);

        availableBlockCrunchTokens[random] = availableBlockCrunchTokens[availableBlockCrunchTokens.length - 1];
        availableBlockCrunchTokens.pop();

        return tokenId;
    }

    /**
     * @dev Generates a pseudo-random number.
     */
    function _getRandomNumber(uint256 _upper) private view returns (uint256) {
        uint256 random = uint256(
            keccak256(
                abi.encodePacked(
                    availableBlockCrunchTokens.length,
                    blockhash(block.number - 1),
                    block.coinbase,
                    block.difficulty,
                    msg.sender
                )
            )
        );

        return random % _upper;
    }

    /**
     * @dev See {ERC721}.
     */
    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }
}