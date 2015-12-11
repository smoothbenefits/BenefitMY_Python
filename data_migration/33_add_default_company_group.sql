DO $$
BEGIN

CREATE TABLE company (company_id INT NOT NULL);

INSERT INTO company (company_id)
SELECT c.id FROM app_company c
LEFT OUTER JOIN app_companygroup cg ON c.id = cg.company_id
WHERE cg.id IS NULL;

INSERT INTO app_companygroup (company_id, name, created, updated)
SELECT c.company_id, 'Default Group', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM company c;

INSERT INTO app_companygroupmember (user_id, company_group_id, created)
SELECT cu.user_id, cg.id, CURRENT_TIMESTAMP FROM company c
INNER JOIN app_companygroup cg ON cg.company_id = c.company_id
INNER JOIN app_companyuser cu ON cu.company_id = c.company_id AND cu.company_user_type = 'employee';

DROP TABLE company;

END
$$
