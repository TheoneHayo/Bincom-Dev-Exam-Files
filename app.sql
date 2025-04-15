-- Create the lga table
CREATE TABLE IF NOT EXISTS lga (
    lga_id SERIAL PRIMARY KEY,
    lga_name VARCHAR(255),
    state_id INT
);

-- Create the polling_unit table
CREATE TABLE IF NOT EXISTS polling_unit (
    uniqueid SERIAL PRIMARY KEY,
    polling_unit_name VARCHAR(255),
    lga_id INT,
    FOREIGN KEY (lga_id) REFERENCES lga(lga_id)
);

-- Create the announced_pu_results table
CREATE TABLE IF NOT EXISTS announced_pu_results (
    result_id SERIAL PRIMARY KEY,
    polling_unit_uniqueid INT,
    party_abbreviation VARCHAR(10),
    party_score INT,
    FOREIGN KEY (polling_unit_uniqueid) REFERENCES polling_unit(uniqueid)
);
