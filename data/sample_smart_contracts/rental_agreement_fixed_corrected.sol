// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

/**
 * @title Rental Agreement Smart Contract
 * @notice Production-ready smart contract implementing rental agreement logic
 * @dev Generated and corrected on 2025-12-27
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

    // Core contract parties
    address public landlord;
    address public tenant;
    address public propertyAddress;
    
    // Contract terms
    uint256 public monthlyRent;
    uint256 public securityDeposit;
    
    // Financial tracking
    mapping(address => uint256) public balances;
    mapping(address => uint256) public paymentHistory;
    mapping(uint256 => bool) public paymentsMade;
    uint256 public totalPayments;
    uint256 public nextPaymentDue;

    // Obligation tracking
    mapping(bytes32 => bool) public obligationsFulfilled;
    mapping(bytes32 => address) public obligationResponsible;
    mapping(address => mapping(uint256 => bool)) public partyObligations;
    uint256 public constant TOTAL_OBLIGATIONS = 8;

    // ========== EVENTS ==========

    event ContractInitialized(address indexed owner, uint256 startDate, uint256 value);
    event ContractTerminated(address indexed by, string reason, uint256 timestamp);

    // Payment events
    event PaymentReceived(address indexed from, uint256 amount, uint256 timestamp);
    event PaymentMade(address indexed to, uint256 amount, string description);
    event BalanceUpdated(address indexed party, uint256 newBalance);

    // Obligation events
    event ObligationFulfilled(bytes32 indexed obligationId, address indexed responsible);
    event ObligationCreated(bytes32 indexed obligationId, address indexed responsible, string description);
    event ObligationBreach(address indexed responsible, bytes32 obligationId, string reason);

    // Party events
    event PartyAdded(address indexed party, string role, uint256 timestamp);
    event PartyRemoved(address indexed party, string reason);
    event RoleAssigned(address indexed party, string role);

    // ========== STRUCTS ==========

    struct Party {
        address addr;
        string name;
        bool isActive;
        uint256 paymentsMade;
    }

    struct Obligation {
        bytes32 id;
        string description;
        address responsible;
        uint256 deadline;
        bool fulfilled;
    }

    // ========== MODIFIERS ==========

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    modifier onlyActive() {
        require(contractActive, "Contract is not active");
        _;
    }

    modifier onlyParty() {
        require(
            msg.sender == landlord || msg.sender == tenant || msg.sender == owner,
            "Not authorized party"
        );
        _;
    }

    modifier onlyLandlord() {
        require(msg.sender == landlord, "Only landlord can perform this action");
        _;
    }

    modifier onlyTenant() {
        require(msg.sender == tenant, "Only tenant can perform this action");
        _;
    }

    // ========== CONSTRUCTOR ==========

    constructor(
        address _landlord,
        address _tenant,
        uint256 _contractValue,
        uint256 _monthlyRent,
        uint256 _securityDeposit,
        uint256 _contractDuration
    ) {
        require(_landlord != address(0), "Invalid landlord address");
        require(_tenant != address(0), "Invalid tenant address");
        require(_contractValue > 0, "Contract value must be positive");
        require(_monthlyRent > 0, "Monthly rent must be positive");
        
        owner = msg.sender;
        landlord = _landlord;
        tenant = _tenant;
        contractValue = _contractValue;
        monthlyRent = _monthlyRent;
        securityDeposit = _securityDeposit;
        contractActive = true;
        contractStartDate = block.timestamp;
        contractEndDate = block.timestamp + _contractDuration;
        amountDue = _contractValue;

        emit ContractInitialized(owner, block.timestamp, _contractValue);
    }

    // ========== CORE BUSINESS FUNCTIONS ==========

    /**
     * @notice Make a rent payment
     */
    function makeRentPayment() external payable onlyTenant onlyActive {
        require(msg.value >= monthlyRent, "Insufficient payment amount");
        
        amountPaid += msg.value;
        if (amountDue >= msg.value) {
            amountDue -= msg.value;
        } else {
            amountDue = 0;
        }
        
        paymentHistory[msg.sender] += msg.value;
        balances[landlord] += msg.value;
        totalPayments++;

        emit PaymentReceived(msg.sender, msg.value, block.timestamp);
    }

    /**
     * @notice Pay security deposit
     */
    function paySecurityDeposit() external payable onlyTenant onlyActive {
        require(msg.value >= securityDeposit, "Insufficient security deposit");
        
        balances[address(this)] += msg.value;
        paymentHistory[msg.sender] += msg.value;

        emit PaymentReceived(msg.sender, msg.value, block.timestamp);
    }

    /**
     * @notice Landlord confirms property handover to tenant
     */
    function confirmPropertyHandover() external onlyLandlord onlyActive {
        bytes32 obligationId = keccak256(abi.encodePacked("property_handover"));
        obligationResponsible[obligationId] = landlord;
        obligationsFulfilled[obligationId] = true;
        
        emit ObligationFulfilled(obligationId, landlord);
    }

    /**
     * @notice Tenant confirms property receipt
     */
    function confirmPropertyReceipt() external onlyTenant onlyActive {
        bytes32 obligationId = keccak256(abi.encodePacked("property_receipt"));
        obligationResponsible[obligationId] = tenant;
        obligationsFulfilled[obligationId] = true;
        
        emit ObligationFulfilled(obligationId, tenant);
    }

    /**
     * @notice Fulfill a general obligation
     */
    function fulfillObligation(bytes32 obligationId) external onlyParty onlyActive {
        require(!obligationsFulfilled[obligationId], "Obligation already fulfilled");
        require(obligationResponsible[obligationId] == msg.sender, "Not responsible for this obligation");

        obligationsFulfilled[obligationId] = true;
        emit ObligationFulfilled(obligationId, msg.sender);
    }

    /**
     * @notice Create a new obligation
     */
    function createObligation(
        bytes32 obligationId, 
        address responsible, 
        string memory description
    ) external onlyOwner onlyActive {
        require(responsible == landlord || responsible == tenant, "Invalid responsible party");
        require(!obligationsFulfilled[obligationId], "Obligation already exists");
        
        obligationResponsible[obligationId] = responsible;
        emit ObligationCreated(obligationId, responsible, description);
    }

    /**
     * @notice Terminate contract early
     */
    function terminateContract(string memory reason) external onlyOwner {
        require(contractActive, "Contract already terminated");
        
        contractActive = false;
        contractEndDate = block.timestamp;
        
        emit ContractTerminated(msg.sender, reason, block.timestamp);
    }

    /**
     * @notice Return security deposit (only after contract end)
     */
    function returnSecurityDeposit() external onlyLandlord {
        require(!contractActive || block.timestamp > contractEndDate, "Contract still active");
        require(balances[address(this)] >= securityDeposit, "Insufficient deposit balance");
        
        balances[address(this)] -= securityDeposit;
        payable(tenant).transfer(securityDeposit);
        
        emit PaymentMade(tenant, securityDeposit, "Security deposit return");
    }

    /**
     * @notice Withdraw accumulated rent payments
     */
    function withdrawRent() external onlyLandlord {
        uint256 amount = balances[landlord];
        require(amount > 0, "No balance to withdraw");
        
        balances[landlord] = 0;
        payable(landlord).transfer(amount);
        
        emit PaymentMade(landlord, amount, "Rent withdrawal");
    }

    // ========== VIEW FUNCTIONS ==========

    /**
     * @notice Get contract status overview
     */
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

    /**
     * @notice Get party information
     */
    function getPartyInfo() external view returns (
        address landlordAddr,
        address tenantAddr,
        uint256 rent,
        uint256 deposit
    ) {
        return (landlord, tenant, monthlyRent, securityDeposit);
    }

    /**
     * @notice Check if obligation is fulfilled
     */
    function isObligationFulfilled(bytes32 obligationId) external view returns (bool) {
        return obligationsFulfilled[obligationId];
    }

    /**
     * @notice Get responsible party for obligation
     */
    function getObligationResponsible(bytes32 obligationId) external view returns (address) {
        return obligationResponsible[obligationId];
    }

    /**
     * @notice Check if contract is valid and active
     */
    function isContractValid() external view returns (bool) {
        return contractActive && 
               block.timestamp >= contractStartDate && 
               block.timestamp <= contractEndDate;
    }

    /**
     * @notice Get payment history for a party
     */
    function getPaymentHistory(address party) external view returns (uint256) {
        return paymentHistory[party];
    }

    /**
     * @notice Get balance for a party
     */
    function getBalance(address party) external view returns (uint256) {
        return balances[party];
    }

    // ========== EMERGENCY FUNCTIONS ==========

    /**
     * @notice Emergency withdrawal (only owner)
     */
    function emergencyWithdraw() external onlyOwner {
        require(!contractActive, "Contract must be terminated first");
        payable(owner).transfer(address(this).balance);
    }

    /**
     * @notice Update contract end date (only owner, only extend)
     */
    function extendContract(uint256 additionalDays) external onlyOwner onlyActive {
        require(additionalDays > 0, "Extension must be positive");
        contractEndDate += additionalDays * 1 days;
    }

    // Allow contract to receive ETH
    receive() external payable {
        balances[address(this)] += msg.value;
    }

    fallback() external payable {
        balances[address(this)] += msg.value;
    }
}