IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'VoiceDeviceDataDB')
BEGIN
    CREATE DATABASE VoiceDeviceDataDB;
END
