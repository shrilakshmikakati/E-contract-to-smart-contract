// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

/**
 * @title Professional Smart Contract
 * @notice Production-ready contract implementing business logic
 * @dev Generated on 2025-12-27 18:51:10
 */
contract PurchaseAgreement {

    // ========== STATE VARIABLES ==========

    address public owner;
    bool public contractActive;
    uint256 public contractStartDate;
    uint256 public contractEndDate;
    uint256 public contractValue;
    uint256 public amountPaid;
    uint256 public amountDue;

    // Purchase contract variables
    address public buyer;
    address public seller;
    uint256 public purchasePrice;

    // Financial tracking
    mapping(address => uint256) public balances;
    mapping(address => uint256) public paymentHistory;
    mapping(bytes32 => bool) public obligationsFulfilled;
    mapping(bytes32 => address) public obligationResponsible;

    // ========== EVENTS ==========

    event ContractInitialized(address indexed owner, uint256 startDate, uint256 value);
    event ContractTerminated(address indexed by, string reason, uint256 timestamp);
    event PaymentReceived(address indexed from, uint256 amount, uint256 timestamp);
    event PaymentMade(address indexed to, uint256 amount, string description);
    event ObligationFulfilled(bytes32 indexed obligationId, address indexed responsible);
    event ObligationCreated(bytes32 indexed obligationId, address indexed responsible, string description);

    // ========== STRUCTS ==========

    struct Obligation {
        bytes32 id;
        string description;
        address responsible;
        uint256 deadline;
        bool fulfilled;
    }

    // ========== MODIFIERS ==========

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    modifier onlyActive() {
        require(contractActive, "Contract not active");
        _;
    }

    modifier onlyParty() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    // ========== CONSTRUCTOR ==========

    constructor(uint256 _contractValue) {
        require(_contractValue > 0, "Invalid contract value");

        owner = msg.sender;
        contractValue = _contractValue;
        contractActive = true;
        contractStartDate = block.timestamp;
        amountDue = _contractValue;

        emit ContractInitialized(owner, block.timestamp, _contractValue);
    }

    // ========== BUSINESS FUNCTIONS ==========

    function confirmDelivery() external onlyBuyer onlyActive {
        bytes32 obligationId = keccak256(abi.encodePacked("delivery_confirmation"));
        obligationsFulfilled[obligationId] = true;
        
        emit ObligationFulfilled(obligationId, buyer);
    }

    function transferOwnership() external onlySeller onlyActive {
        bytes32 obligationId = keccak256(abi.encodePacked("ownership_transfer"));
        obligationsFulfilled[obligationId] = true;
        
        emit ObligationFulfilled(obligationId, seller);
    }

    // ========== VIEW FUNCTIONS ==========

    function getContractStatus() external view returns (
        bool active,
        uint256 startDate,
        uint256 endDate,
        uint256 totalValue,
        uint256 paid,
        uint256 due
    ) {
        return (
            contractActive,
            contractStartDate,
            contractEndDate,
            contractValue,
            amountPaid,
            amountDue
        );
    }

    function isObligationFulfilled(bytes32 obligationId) external view returns (bool) {
        return obligationsFulfilled[obligationId];
    }

    function getPaymentHistory(address party) external view returns (uint256) {
        return paymentHistory[party];
    }

    function getBalance(address party) external view returns (uint256) {
        return balances[party];
    }

    // ========== UTILITY FUNCTIONS ==========

    function terminateContract(string memory reason) external onlyOwner {
        require(contractActive, "Already terminated");
        
        contractActive = false;
        contractEndDate = block.timestamp;
        
        emit ContractTerminated(msg.sender, reason, block.timestamp);
    }

    function createObligation(
        bytes32 obligationId,
        address responsible,
        string memory description
    ) external onlyOwner onlyActive {
        require(responsible != address(0), "Invalid address");
        require(!obligationsFulfilled[obligationId], "Already exists");
        
        obligationResponsible[obligationId] = responsible;
        emit ObligationCreated(obligationId, responsible, description);
    }

    // Allow contract to receive ETH
    receive() external payable {
        balances[address(this)] += msg.value;
    }
}