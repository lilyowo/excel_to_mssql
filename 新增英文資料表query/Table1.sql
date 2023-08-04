CREATE TABLE AllMed(
	Med_id int NOT NULL,
	Med_name nvarchar(100) NOT NULL,
	Med_latin nvarchar(100),
	Med_en nvarchar(100),
	Med_base nvarchar(300),
	Med_content nvarchar(100),
	Med_use_class nvarchar(100),
	Med_character nvarchar(100),
	Med_efficacy nvarchar(300),
	Med_dosage nvarchar(100),
	Med_storage nvarchar(100),
	Med_mono int,
	Med_double int,
	Med_herb int,
	PRIMARY KEY(Med_id)
);