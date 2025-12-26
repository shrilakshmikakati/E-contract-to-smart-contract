pragma solidity ^0.8.16;

/**
 * Fixed Rental Agreement Smart Contract
 * - Removed reserved keyword usage
 * - Added proper error handling
 * - Enhanced functionality for comparison testing
 */
contract RentalAgreementContract {
    // Parties (fixed: "contract" is reserved keyword)
    address public tenant;
    address public landlord;
    address public contractOwner;  // Fixed: was "contract"
    
    // Financial terms
    uint256 public monthlyRent;
    uint256 public securityDeposit;
    uint256 public totalPayments;
    
    // Property details
    string public propertyAddress;
    string public propertyDescription;
    
    // Contract status
    bool public isActive;
    bool public isTerminated;
    uint256 public contractStartDate;
    uint256 public contractEndDate;
    
    // Payment tracking
    mapping(uint256 => bool) public monthlyPayments;
    uint256 public currentMonth;
    
    // Events for business logic tracking
    event RentPaid(address indexed tenant, uint256 amount, uint256 month);
    event ContractActivated(address indexed tenant, address indexed landlord);
    event ContractTerminated(string reason);
    event SecurityDepositReturned(address indexed tenant, uint256 amount);
    
    // Modifiers
    modifier onlyTenant() {
        require(msg.sender == tenant, "Only tenant can call this function");
        _;
    }
    
    modifier onlyLandlord() {
        require(msg.sender == landlord, "Only landlord can call this function");
        _;
    }
    
    modifier contractActive() {
        require(isActive && !isTerminated, "Contract is not active");
        _;
    }
    
    constructor(
        address _tenant,
        address _landlord,
        uint256 _monthlyRent,
        uint256 _securityDeposit,
        string memory _propertyAddress,
        uint256 _contractDuration
    ) {
        tenant = _tenant;
        landlord = _landlord;
        contractOwner = msg.sender;
        monthlyRent = _monthlyRent;
        securityDeposit = _securityDeposit;
        propertyAddress = _propertyAddress;
        contractStartDate = block.timestamp;
        contractEndDate = block.timestamp + _contractDuration;
        currentMonth = 1;
        isActive = true;
        isTerminated = false;
        
        emit ContractActivated(_tenant, _landlord);
    }
    
    // Pay monthly rent
    function payRent() external payable onlyTenant contractActive {
        require(msg.value == monthlyRent, "Incorrect rent amount");
        require(!monthlyPayments[currentMonth], "Rent already paid for this month");
        
        monthlyPayments[currentMonth] = true;
        totalPayments += msg.value;
        
        // Transfer to landlord
        payable(landlord).transfer(msg.value);
        
        emit RentPaid(tenant, msg.value, currentMonth);
        currentMonth++;
    }
    
    // Terminate contract
    function terminateContract(string memory reason) external {
        require(msg.sender == tenant || msg.sender == landlord || msg.sender == contractOwner, 
                "Not authorized to terminate");
        require(!isTerminated, "Contract already terminated");
        
        isTerminated = true;
        isActive = false;
        
        emit ContractTerminated(reason);
    }
    
    // Return security deposit (landlord only)
    function returnSecurityDeposit() external onlyLandlord {
        require(isTerminated, "Contract must be terminated first");
        require(address(this).balance >= securityDeposit, "Insufficient balance for deposit");
        
        payable(tenant).transfer(securityDeposit);
        emit SecurityDepositReturned(tenant, securityDeposit);
    }
    
    // Check if rent is paid for specific month
    function isRentPaid(uint256 month) external view returns (bool) {
        return monthlyPayments[month];
    }
    
    // Get contract details
    function getContractDetails() external view returns (
        address _tenant,
        address _landlord,
        uint256 _monthlyRent,
        uint256 _securityDeposit,
        string memory _propertyAddress,
        bool _isActive,
        uint256 _currentMonth
    ) {
        return (tenant, landlord, monthlyRent, securityDeposit, propertyAddress, isActive, currentMonth);
    }
    
    // Fallback to receive security deposit
    receive() external payable {
        require(msg.value == securityDeposit, "Must send exact security deposit amount");
    }
}