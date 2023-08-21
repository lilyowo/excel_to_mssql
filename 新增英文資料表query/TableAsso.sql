CREATE TABLE MedAssociate(
	Comp_id int,
	Med_id int,
	PRIMARY KEY(Med_id, Comp_id),
	FOREIGN KEY(Med_id) REFERENCES AllMed (Med_id) ON DELETE CASCADE,
	FOREIGN KEY(Comp_id) REFERENCES CompoundMed (Comp_id) ON DELETE CASCADE,
);