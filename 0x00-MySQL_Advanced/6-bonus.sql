-- SQL script to create a stored procedure AddBonus
DELIMITER $$

CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if the project exists, and if not, create it
    IF NOT EXISTS (SELECT 1 FROM projects WHERE name = p_project_name) THEN
        INSERT INTO projects (name) VALUES (p_project_name);
    END IF;

    -- Retrieve the project_id
    SELECT id INTO project_id FROM projects WHERE name = p_project_name;

    -- Add the bonus correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, project_id, p_score);
END $$

DELIMITER ;
