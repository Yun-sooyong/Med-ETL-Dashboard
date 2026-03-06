CREATE TABLE patients(
    patient_id TEXT PRIMARY KEY,
    sex CHAR(1),
    birth_date DATE
    );

CREATE TABLE visits(
	visit_id TEXT PRIMARY KEY,
	patient_id TEXT NOT NULL,
	visit_date TIMESTAMP NOT NULL,
		CONSTRAINT fk_patient
		FOREIGN KEY (patient_id)
		REFERENCES patients(patient_id)
		ON DELETE CASCADE
    );

CREATE TABLE labs (
	lab_id TEXT PRIMARY KEY,
	visit_id TEXT NOT NULL
	test_name TEXT NOT NULL
	value NUMBERIC,
	unit CHAR(20),
	collected_at TIMESTAMP,
	flag_abnormal BOOLEAN
		CONSTRAINT fk_visit
		FOREIGN KEY (visit_id)
		REFERENCES visits(visit_id)
		ON DELETE CASCADE
    );


