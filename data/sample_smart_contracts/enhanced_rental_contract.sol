// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

/**
 * @title Professional Smart Contract
 * @notice Production-ready contract implementing business logic
 * @dev Generated on 2025-12-27 18:50:36
 */
contract RentalAgreement {

    // ========== STATE VARIABLES ==========

    address public owner;
    bool public contractActive;
    uint256 public contractStartDate;
    uint256 public contractEndDate;
    uint256 public contractValue;
    uint256 public amountPaid;
    uint256 public amountDue;

    // Rental-specific variables
    address public landlord;
    address public tenant;
    uint256 public monthlyRent;
    uint256 public securityDeposit;

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

    modifier onlyLandlord() {
        require(msg.sender == landlord, "Only landlord");
        _;
    }

    modifier onlyTenant() {
        require(msg.sender == tenant, "Only tenant");
        _;
    }

    modifier onlyParty() {
        require(msg.sender == landlord || msg.sender == tenant || msg.sender == owner, "Not authorized");
        _;
    }

    // ========== CONSTRUCTOR ==========

    constructor(
        address _landlord,
        address _tenant,
        uint256 _contractValue,
        uint256 _monthlyRent,
        uint256 _securityDeposit
    ) {
        require(_landlord != address(0), "Invalid landlord");
        require(_tenant != address(0), "Invalid tenant");
        require(_contractValue > 0, "Invalid contract value");

        owner = msg.sender;
        landlord = _landlord;
        tenant = _tenant;
        contractValue = _contractValue;
        monthlyRent = _monthlyRent;
        securityDeposit = _securityDeposit;
        contractActive = true;
        contractStartDate = block.timestamp;
        amountDue = _contractValue;

        emit ContractInitialized(owner, block.timestamp, _contractValue);
    }

    // ========== BUSINESS FUNCTIONS ==========

    function makeRentPayment() external payable onlyTenant onlyActive {
        require(msg.value >= monthlyRent, "Insufficient payment");
        
        amountPaid += msg.value;
        if (amountDue >= msg.value) {
            amountDue -= msg.value;
        }
        
        paymentHistory[msg.sender] += msg.value;
        balances[landlord] += msg.value;
        
        emit PaymentReceived(msg.sender, msg.value, block.timestamp);
    }

    function paySecurityDeposit() external payable onlyTenant onlyActive {
        require(msg.value >= securityDeposit, "Insufficient deposit");
        
        balances[address(this)] += msg.value;
        paymentHistory[msg.sender] += msg.value;
        
        emit PaymentReceived(msg.sender, msg.value, block.timestamp);
    }

    function confirmPropertyHandover() external onlyLandlord onlyActive {
        bytes32 obligationId = keccak256(abi.encodePacked("property_handover"));
        obligationResponsible[obligationId] = landlord;
        obligationsFulfilled[obligationId] = true;
        
        emit ObligationFulfilled(obligationId, landlord);
    }

    function returnSecurityDeposit() external onlyLandlord {
        require(!contractActive || block.timestamp > contractEndDate, "Contract active");
        require(balances[address(this)] >= securityDeposit, "Insufficient balance");
        
        balances[address(this)] -= securityDeposit;
        payable(tenant).transfer(securityDeposit);
        
        emit PaymentMade(tenant, securityDeposit, "Security deposit return");
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