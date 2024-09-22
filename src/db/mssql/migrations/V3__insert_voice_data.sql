USE VoiceDeviceDataDB;

BEGIN TRANSACTION;

INSERT INTO Users (userId) VALUES
('555666777'),
('472917482'),
('958482928');

INSERT INTO Phones (phone) VALUES
('SEP123123234234'),
('SEP234567890123'),
('SEP345678901234'),
('SEP456789012345'),
('SEP567890123456');

INSERT INTO Voicemails (voicemail) VALUES
('555666777VM'),
('111222333VM'),
('333444555VM');

INSERT INTO Clusters (clusterId) VALUES
('domainserver1'),
('domainserver2'),
('domainserver3'),
('domainserver4'),
('domainserver5'),
('domainserver6'),
('domainserver7');

INSERT INTO UsersToPhonesJunction (phoneJunctionId, userId, phone) VALUES
('00001', '555666777', 'SEP123123234234'),
('00002', '555666777', 'SEP234567890123'),
('00003', '472917482', 'SEP123123234234'),
('00004', '958482928', 'SEP345678901234'),
('00005', '958482928', 'SEP123123234234');

INSERT INTO UsersToVoicemailsJunction (voicemailJunctionId, userId, voicemail) VALUES
('00001', '555666777', '555666777VM'),
('00002', '472917482', '111222333VM'),
('00003', '958482928', '111222333VM');

INSERT INTO Records (id, originationTime, clusterId, userId, phoneJunctionId, voicemailJunctionId) VALUES
('12345', 1656788800, 'domainserver1', '555666777', '00001', '00001'),
('12346', 1622548800, 'domainserver1', '472917482', '00003', '00002'),
('12347', 1630454400, 'domainserver3', '555666777', '00002', '00001'),
('12348', 1640995200, 'domainserver2', '555666777', '00001', '00001'),
('12349', 1651363200, 'domainserver1', '958482928', '00004', '00003');

COMMIT TRANSACTION;
