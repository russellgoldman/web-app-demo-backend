USE VoiceDeviceDataDB;

BEGIN TRANSACTION;

CREATE TABLE Users (
    userId NVARCHAR(9) PRIMARY KEY,
    CONSTRAINT chk_userId CHECK(LEN(userId) = 9)
);

CREATE TABLE Phones (
    phone NVARCHAR(15) PRIMARY KEY,
    CONSTRAINT chk_phone CHECK(LEFT(phone, 3) = 'SEP' AND LEN(phone) = 15)
);

CREATE TABLE Voicemails (
    voicemail NVARCHAR(11) PRIMARY KEY,
    CONSTRAINT chk_voicemail CHECK(RIGHT(voicemail, 2) = 'VM' AND LEN(voicemail) = 11)
);

CREATE TABLE Clusters (
    clusterId NVARCHAR(25) PRIMARY KEY,
    CONSTRAINT chk_clusterId CHECK(LEFT(clusterId, 12) = 'domainserver')
);

CREATE TABLE UsersToPhonesJunction (
    phoneJunctionId NVARCHAR(5),
    userId NVARCHAR(9) NOT NULL,
    phone NVARCHAR(15) NOT NULL,
    PRIMARY KEY (phoneJunctionId, userId),
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (phone) REFERENCES Phones(phone),
    CONSTRAINT uq_userId_phone UNIQUE (userId, phone),
    CONSTRAINT chk_phoneJunctionId CHECK(LEN(phoneJunctionId) = 5)
);

CREATE TABLE UsersToVoicemailsJunction (
    voicemailJunctionId NVARCHAR(5),
    userId NVARCHAR(9) NOT NULL,
    voicemail NVARCHAR(11) NOT NULL,
    PRIMARY KEY (voicemailJunctionId, userId),
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (voicemail) REFERENCES Voicemails(voicemail),
    CONSTRAINT uq_userId_voicemail UNIQUE (userId, voicemail),
    CONSTRAINT chk_voicemailJunctionId CHECK(LEN(voicemailJunctionId) = 5)
);

CREATE TABLE Records (
    id NVARCHAR(5) PRIMARY KEY,
    originationTime INT, -- The maximum value of a Unix epoch is equivalent to a 32-bit signed integer
    clusterId NVARCHAR(25),
    userId NVARCHAR(9),
    phoneJunctionId NVARCHAR(5),
    voicemailJunctionId NVARCHAR(5),
    FOREIGN KEY (clusterId) REFERENCES Clusters(clusterId),
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (phoneJunctionId, userId) REFERENCES UsersToPhonesJunction(phoneJunctionId, userId),
    FOREIGN KEY (voicemailJunctionId, userId) REFERENCES UsersToVoicemailsJunction(voicemailJunctionId, userId)
);

COMMIT TRANSACTION;
