// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ServiceContract
 * @dev Smart contract for managing service agreements between providers and clients
 */
contract ServiceContract {
    
    struct Agreement {
        address provider;
        address client;
        uint256 hourlyRate;
        uint256 totalAmount;
        uint256 startDate;
        uint256 endDate;
        bool isActive;
        bool isCompleted;
    }
    
    struct Payment {
        uint256 amount;
        uint256 timestamp;
        bool isPaid;
    }
    
    mapping(uint256 => Agreement) public agreements;
    mapping(uint256 => Payment[]) public payments;
    mapping(address => uint256[]) public providerAgreements;
    mapping(address => uint256[]) public clientAgreements;
    
    uint256 public nextAgreementId;
    address public owner;
    
    event AgreementCreated(uint256 indexed agreementId, address indexed provider, address indexed client);
    event PaymentMade(uint256 indexed agreementId, uint256 amount, uint256 timestamp);
    event AgreementCompleted(uint256 indexed agreementId);
    event AgreementTerminated(uint256 indexed agreementId, address terminatedBy);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }
    
    modifier onlyParties(uint256 agreementId) {
        Agreement memory agreement = agreements[agreementId];
        require(
            msg.sender == agreement.provider || msg.sender == agreement.client,
            "Only agreement parties can perform this action"
        );
        _;
    }
    
    modifier agreementExists(uint256 agreementId) {
        require(agreements[agreementId].provider != address(0), "Agreement does not exist");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        nextAgreementId = 1;
    }
    
    /**
     * @dev Create a new service agreement
     * @param _provider Address of the service provider
     * @param _client Address of the client
     * @param _hourlyRate Hourly rate in wei
     * @param _totalAmount Total contract amount in wei
     * @param _duration Duration of the contract in seconds
     */
    function createAgreement(
        address _provider,
        address _client,
        uint256 _hourlyRate,
        uint256 _totalAmount,
        uint256 _duration
    ) external returns (uint256) {
        require(_provider != address(0) && _client != address(0), "Invalid addresses");
        require(_hourlyRate > 0 && _totalAmount > 0, "Invalid rates or amounts");
        require(_duration > 0, "Invalid duration");
        
        uint256 agreementId = nextAgreementId++;
        
        agreements[agreementId] = Agreement({
            provider: _provider,
            client: _client,
            hourlyRate: _hourlyRate,
            totalAmount: _totalAmount,
            startDate: block.timestamp,
            endDate: block.timestamp + _duration,
            isActive: true,
            isCompleted: false
        });
        
        providerAgreements[_provider].push(agreementId);
        clientAgreements[_client].push(agreementId);
        
        emit AgreementCreated(agreementId, _provider, _client);
        return agreementId;
    }
    
    /**
     * @dev Make a payment for services
     * @param agreementId ID of the agreement
     */
    function makePayment(uint256 agreementId) 
        external 
        payable 
        agreementExists(agreementId) 
    {
        Agreement storage agreement = agreements[agreementId];
        require(msg.sender == agreement.client, "Only client can make payments");
        require(agreement.isActive, "Agreement is not active");
        require(msg.value > 0, "Payment amount must be greater than 0");
        
        payments[agreementId].push(Payment({
            amount: msg.value,
            timestamp: block.timestamp,
            isPaid: true
        }));
        
        // Transfer payment to provider
        payable(agreement.provider).transfer(msg.value);
        
        emit PaymentMade(agreementId, msg.value, block.timestamp);
        
        // Check if total amount is reached
        uint256 totalPaid = getTotalPaid(agreementId);
        if (totalPaid >= agreement.totalAmount) {
            agreement.isCompleted = true;
            agreement.isActive = false;
            emit AgreementCompleted(agreementId);
        }
    }
    
    /**
     * @dev Terminate an agreement
     * @param agreementId ID of the agreement to terminate
     */
    function terminateAgreement(uint256 agreementId) 
        external 
        agreementExists(agreementId) 
        onlyParties(agreementId) 
    {
        Agreement storage agreement = agreements[agreementId];
        require(agreement.isActive, "Agreement is already terminated");
        
        agreement.isActive = false;
        
        emit AgreementTerminated(agreementId, msg.sender);
    }
    
    /**
     * @dev Get total amount paid for an agreement
     * @param agreementId ID of the agreement
     * @return Total amount paid in wei
     */
    function getTotalPaid(uint256 agreementId) 
        public 
        view 
        agreementExists(agreementId) 
        returns (uint256) 
    {
        Payment[] memory agreementPayments = payments[agreementId];
        uint256 total = 0;
        
        for (uint256 i = 0; i < agreementPayments.length; i++) {
            if (agreementPayments[i].isPaid) {
                total += agreementPayments[i].amount;
            }
        }
        
        return total;
    }
    
    /**
     * @dev Get agreement details
     * @param agreementId ID of the agreement
     * @return Agreement details
     */
    function getAgreement(uint256 agreementId) 
        external 
        view 
        agreementExists(agreementId) 
        returns (Agreement memory) 
    {
        return agreements[agreementId];
    }
    
    /**
     * @dev Get all agreements for a provider
     * @param provider Address of the provider
     * @return Array of agreement IDs
     */
    function getProviderAgreements(address provider) 
        external 
        view 
        returns (uint256[] memory) 
    {
        return providerAgreements[provider];
    }
    
    /**
     * @dev Get all agreements for a client
     * @param client Address of the client
     * @return Array of agreement IDs
     */
    function getClientAgreements(address client) 
        external 
        view 
        returns (uint256[] memory) 
    {
        return clientAgreements[client];
    }
    
    /**
     * @dev Get payment history for an agreement
     * @param agreementId ID of the agreement
     * @return Array of payments
     */
    function getPaymentHistory(uint256 agreementId) 
        external 
        view 
        agreementExists(agreementId) 
        returns (Payment[] memory) 
    {
        return payments[agreementId];
    }
    
    /**
     * @dev Check if agreement is expired
     * @param agreementId ID of the agreement
     * @return True if expired, false otherwise
     */
    function isAgreementExpired(uint256 agreementId) 
        external 
        view 
        agreementExists(agreementId) 
        returns (bool) 
    {
        return block.timestamp > agreements[agreementId].endDate;
    }
}