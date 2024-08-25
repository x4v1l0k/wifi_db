CREATE TABLE IF NOT EXISTS AP
(
    bssid TEXT NOT NULL,
    ssid TEXT,
    cloaked BOOLEAN,
    manuf TEXT,
    channel int,
    frequency int,
    carrier TEXT,
    encryption TEXT,
    packetsTotal int,
    lat_t REAL,
    lon_t REAL,
    mfpc BOOLEAN,
    mfpr BOOLEAN,
    firstTimeSeen timestamp,
    CONSTRAINT Key1 PRIMARY KEY (bssid)
);

CREATE TABLE IF NOT EXISTS Client
(
    mac TEXT NOT NULL,
    ssid TEXT,
    manuf TEXT,
    type TEXT,
    packetsTotal int,
    device TEXT,
    firstTimeSeen timestamp,
    CONSTRAINT Key1 PRIMARY KEY (mac)
);


CREATE TABLE IF NOT EXISTS SeenClient
(
    mac TEXT NOT NULL,
    time datetime NOT NULL,
    tool TEXT,
    signal_rssi int,
    lat REAL,
    lon REAL,
    alt REAL,
    CONSTRAINT Key3 PRIMARY KEY (time,mac),
    CONSTRAINT SeenClients FOREIGN KEY (mac) REFERENCES Client (mac) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Connected
(
    bssid TEXT NOT NULL,
    mac TEXT NOT NULL,
    CONSTRAINT Key4 PRIMARY KEY (bssid,mac),
    CONSTRAINT Relationship2 FOREIGN KEY (bssid) REFERENCES AP (bssid) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT Relationship3 FOREIGN KEY (mac) REFERENCES Client (mac) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS WPS
(
    bssid TEXT NOT NULL,
    wlan_ssid TEXT NOT NULL,
    wps_version TEXT NOT NULL,
    wps_device_name TEXT NOT NULL,
    wps_model_name TEXT NOT NULL,
    wps_model_number TEXT NOT NULL,
    wps_config_methods TEXT NOT NULL,
    wps_config_methods_keypad TEXT NOT NULL,
    CONSTRAINT KeyWPS PRIMARY KEY (bssid),
    CONSTRAINT RelationshipWPS FOREIGN KEY (bssid) REFERENCES AP (bssid) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS SeenAp
(
    bssid TEXT NOT NULL,
    time datetime NOT NULL,
    tool TEXT,
    signal_rssi int,
    lat REAL,
    lon REAL,
    alt REAL,
    bsstimestamp timestamp,
    CONSTRAINT Key3 PRIMARY KEY (time,bssid),
    CONSTRAINT SeenAp FOREIGN KEY (bssid) REFERENCES AP (bssid) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Probe
(
    mac TEXT NOT NULL,
    ssid TEXT NOT NULL,
    time datetime,
    CONSTRAINT Key5 PRIMARY KEY (mac,ssid),
    CONSTRAINT ProbesSent FOREIGN KEY (mac) REFERENCES Client (mac) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Certificate
(
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    file TEXT NOT NULL,
    issuer_commonName TEXT NOT NULL,
    issuer_countryName TEXT NOT NULL,
    issuer_email TEXT NOT NULL,
    issuer_localityName TEXT NOT NULL,
    issuer_organizationName TEXT NOT NULL,
    issuer_stateOrProvinceName TEXT NOT NULL,
    subject_commonName TEXT NOT NULL,
    subject_countryName TEXT NOT NULL,
    subject_email TEXT NOT NULL,
    subject_localityName TEXT NOT NULL,
    subject_organizationName TEXT NOT NULL,
    subject_stateOrProvinceName TEXT NOT NULL,
    CONSTRAINT Key5 PRIMARY KEY (source,destination,file,issuer_commonName,issuer_countryName,issuer_email,issuer_localityName,issuer_organizationName,issuer_stateOrProvinceName,subject_commonName,subject_countryName,subject_email,subject_localityName,subject_organizationName,subject_stateOrProvinceName)
);


CREATE TABLE IF NOT EXISTS Handshake
(
    bssid TEXT NOT NULL,
    mac TEXT NOT NULL,
    file TEXT NOT NULL,
    hashSHA TEXT NOT NULL,
    hashcat TEXT,
    CONSTRAINT Key6 PRIMARY KEY (bssid,mac,file)
    CONSTRAINT FRelationship4 FOREIGN KEY (bssid) REFERENCES AP (bssid) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FRelationship5 FOREIGN KEY (mac) REFERENCES Client (mac) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FRelationship8 FOREIGN KEY (file,hashSHA) REFERENCES Files (file,hashSHA) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Identity
(
    bssid TEXT NOT NULL,
    mac TEXT NOT NULL,
    identity TEXT NOT NULL,
    method TEXT NOT NULL,
    CONSTRAINT Key7 PRIMARY KEY (bssid,mac,identity)
    CONSTRAINT FRelationship6 FOREIGN KEY (bssid) REFERENCES AP (bssid) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FRelationship7 FOREIGN KEY (mac) REFERENCES Client (mac) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Files
(
    file TEXT NOT NULL,
    processed BOOLEAN,
    hashSHA TEXT NOT NULL,
    time datetime,
    CONSTRAINT Key8 PRIMARY KEY (file,hashSHA)
);