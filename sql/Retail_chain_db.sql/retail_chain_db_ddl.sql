-- AUTHOR: SCOEY DERUS
-- DATE 11/25/25
-- DESCRIPTION - CREATION OF A RETAIL SALES DATABASE TO BE POPULATED WITH FAKE DATA AND CHARTED VIA MATPLOTLIB OR POWERBI

CREATE TABLE `Branch` (
    `BranchID` INT(6) NOT NULL PRIMARY KEY,
    `BranchName` VARCHAR(255) NOT NULL,
    `Country` VARCHAR(255) NOT NULL,
    `State` VARCHAR(255) NOT NULL,
    `City` VARCHAR(255) NOT NULL,
    `Address` VARCHAR(255) NOT NULL
);

CREATE TABLE `Customer` (
    `CustomerID` INT(11) NOT NULL AUTO_INCREMENT, -- Default starts at 1, anon sales will be CustomerID = 0
    `CustomerName` VARCHAR(255) DEFAULT NULL,   -- all fields will be default null except for CustomerID 0 if anon
    `PhoneNumber` VARCHAR(255) DEFAULT NULL,
    `Address` VARCHAR(255) DEFAULT NULL,
    `Email` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`CustomerID`)
);

INSERT INTO `Customer` VALUES(0);

CREATE TABLE `Product` (
    `ProductID` INT(11) NOT NULL AUTO_INCREMENT, -- Every new entry will just add to the last one
    `ProductName` VARCHAR(255) NOT NULL,
    `Description` VARCHAR(255) DEFAULT NULL,
    `Price` DECIMAL(19,4) NOT NULL,
    `Category` VARCHAR(255) DEFAULT 'MISC',
    PRIMARY KEY (`ProductID`)
);

CREATE TABLE `Transactions` (
    `TransactionID` INT(11) NOT NULL AUTO_INCREMENT,
    `CustomerID` INT(11),
    `Date` DATETIME NOT NULL,
    `ProductID` INT(11) NOT NULL,
    `BranchID` INT(6) NOT NULL,
    `SaleTotal` DECIMAL(19,4) NOT NULL,
    `UnitTotal` INT(6) NOT NULL,
    `Register` INT(4) DEFAULT NULL,
    PRIMARY KEY (`TransactionID`),
    FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`),
    FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`),
    FOREIGN KEY (`BranchID`) REFERENCES `Branch` (`BranchID`)
);

CREATE TABLE `Employee` (
    `EmployeeID` INT(11) NOT NULL AUTO_INCREMENT,
    `EmployeeName` VARCHAR(255) NOT NULL,
    `Address` VARCHAR(255) DEFAULT NULL,
    `Age` INT(11) DEFAULT NULL,
    `Position` VARCHAR(255) NOT NULL,
    `ManagerID` INT(11) DEFAULT NULL,
    `BranchID` INT(6) NOT NULL,
    `Status` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`EmployeeID`),
    FOREIGN KEY (`BranchID`) REFERENCES `Branch` (`BranchID`),
    FOREIGN KEY (`ManagerID`) REFERENCES `Employee` (`EmployeeID`) ON DELETE SET NULL
);