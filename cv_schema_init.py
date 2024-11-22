CREATE_SCHEMA = """
CREATE SCHEMA IF NOT EXISTS `mydb`;
"""

Create_users_Table = """
CREATE TABLE IF NOT EXISTS mydb.Users( 
        name VARCHAR(45) NOT NULL, 
        email Varchar(120) Not NULL,   
        type VARCHAR(45) NOT NULL,
        password VARCHAR(45) NULL,  
        UNIQUE INDEX email_UNIQUE (email), 
        CHECK (type in ('Recruiter','Client')),
        PRIMARY KEY (email)   );
  """
Create_recruiter_Table = """
CREATE TABLE IF NOT EXISTS mydb.Recruiter(
  RID INT NOT NULL AUTO_INCREMENT,
  RName VARCHAR(45) NOT NULL,
  REmail VARCHAR(45) NOT NULL,
  CompanyName VARCHAR(45) NOT NULL,
  CompanyLocation VARCHAR(45) NOT NULL,
  RGender VARCHAR(2) NOT NULL,
   PRIMARY KEY (RID),
   UNIQUE (REmail)
   );
  """
Create_client_Table = """
CREATE TABLE IF NOT EXISTS mydb.Client (
  CID INT NOT NULL AUTO_INCREMENT,
  CName VARCHAR(45) NOT NULL,
  CEmail VARCHAR(45) NOT NULL,
  CAge INT NOT NULL,
  CLocation VARCHAR(45) NOT NULL,
  CGender VARCHAR(2) NOT NULL,
  CExp INT NOT NULL,
  CSkills VARCHAR(45) NOT NULL,
  CQualification VARCHAR(45) NOT NULL,
  CResume LONGBLOB,
  CResumeFileName VARCHAR(255),
  UNIQUE (CEmail),
  PRIMARY KEY (CID)
  );
  """

Create_Job_Table = """
CREATE TABLE IF NOT EXISTS mydb.Job (
  RID INT NOT NULL,
  JID INT NOT NULL AUTO_INCREMENT,
  JobRole VARCHAR(45) NOT NULL,
  JobType VARCHAR(45) NOT NULL,
  Qualification VARCHAR(45) NOT NULL,
  MinExp INT NOT NULL,
  Salary INT NOT NULL,
  FOREIGN KEY (RID) REFERENCES mydb.Recruiter(RID),
  PRIMARY KEY (JID)
  );
  """

Create_Application_Table="""
CREATE TABLE IF NOT EXISTS mydb.Application(
    AID INT NOT NULL AUTO_INCREMENT,
    RID INT NOT NULL,
    JID INT NOT NULL,
    CID INT NOT NULL,
    Status VARCHAR(20) DEFAULT 'Pending',
    PRIMARY KEY(AID),
    FOREIGN KEY(RID) REFERENCES mydb.Recruiter(RID),
    FOREIGN KEY(JID) REFERENCES mydb.Job(JID),
    FOREIGN KEY(CID) REFERENCES mydb.Client(CID),
    CHECK (Status in ('Pending', 'Accepted', 'Rejected'))
);
"""

Create_Trigger_Prevent_Duplicate = """
DELIMITER //

CREATE TRIGGER prevent_duplicate_job_posting
BEFORE INSERT ON mydb.Job
FOR EACH ROW
BEGIN
    DECLARE job_count INT;
    SELECT COUNT(*) INTO job_count
    FROM mydb.Job
    WHERE RID = NEW.RID AND JobRole = NEW.JobRole;
    
    IF job_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate job role posting is not allowed';
    END IF;
END //

DELIMITER ;
"""

Create_Trigger_Update_Client = """
DELIMITER //

CREATE TRIGGER update_client_last_application
AFTER INSERT ON mydb.Application
FOR EACH ROW
BEGIN
    UPDATE mydb.Client
    SET LastApplicationDate = NOW()
    WHERE CID = NEW.CID;
END //

DELIMITER ;
"""

