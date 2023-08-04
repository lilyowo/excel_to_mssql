CREATE TABLE SampleData(
	Med_name nvarchar(30) NOT NULL,
	Med_id int,
	Source_id int,
	Sample_id int,
	Standard_id int,
	PRIMARY KEY(Med_id, Source_id, Sample_id),
	FOREIGN KEY(Med_id) REFERENCES AllMed (Med_id) ON DELETE CASCADE,
	FOREIGN KEY(Source_id) REFERENCES MedSource(Source_id) ON DELETE CASCADE,
	FOREIGN KEY(Standard_id) REFERENCES StandardData (Standard_id) ON DELETE CASCADE,
	SS_fingerpring nvarchar(500),
	SS_med_source nvarchar(500),
	SS_used_part nvarchar(500),
	SS_process nvarchar(500),
	SS_extract nvarchar(500),
	SS_ratio nvarchar(1000),
	SS_hplc_instrument nvarchar(500),
	SS_hplc_detect nvarchar(500),

	SS_col_brand nvarchar(500),
	SS_col_type nvarchar(500),
	SS_col_length float,
	SS_col_width float,
	SS_col_particle_size float,
	SS_col_temperature float,

	SS_ch_mobileA nvarchar(500),
	SS_ch_mobileB nvarchar(500),
	SS_ch_mobileC nvarchar(500),

	SS_ch_detect_wavelength float,
	SS_ch_flow_rate float,
	SS_ch_Injection float
);