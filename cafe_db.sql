CREATE TABLE `Customers` (
  `CustomerID` int(15) NOT NULL,
  `CustomerFirstName` varchar(30) DEFAULT NULL,
  `CustomerLastName` varchar(30) DEFAULT NULL,
  `CustomerUsername` varchar(30) DEFAULT NULL,
   PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Product` (
  `ProductID` int(15) NOT NULL,
  `ProductName` varchar(35) NOT NULL,
  `ProductLS` varchar(35) NOT NULL,
  `ProductPrice` int(10) NOT NULL,
  PRIMARY KEY (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Orders` (
  `OrderID` int(25) NOT NULL,
  `CustomerID` int(15) NOT NULL,
  `OrderDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`OrderID`),
  FOREIGN KEY (`CustomerID`) REFERENCES `Customers` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ProductInOrder` (
  `OrderDetailID` int NOT NULL AUTO_INCREMENT,
  `OrderID` int(25) NOT NULL,
  `ProductID` int(15) NOT NULL,
  PRIMARY KEY (`OrderDetailID`),
  FOREIGN KEY (`OrderID`) REFERENCES `Orders` (`OrderID`),
  FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;




