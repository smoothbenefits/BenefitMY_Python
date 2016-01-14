DO $$
BEGIN

-- Find all company STD plans that currently are 
-- not linked to any company groups
DROP TABLE IF EXISTS orphan_company_plans;

CREATE TEMP TABLE orphan_company_plans AS
SELECT DISTINCT csip.id AS company_plan_id, csip.company_id
FROM app_companystdinsuranceplan csip
LEFT OUTER JOIN app_companygroupstdinsuranceplan cgsip
ON csip.id = cgsip.company_std_insurance_plan_id
WHERE cgsip.company_std_insurance_plan_id IS NULL;

-- Get company to 'Default' company group mappings
DROP TABLE IF EXISTS default_company_groups;

CREATE TEMP TABLE default_company_groups AS
SELECT DISTINCT c.id AS company_id, cg.id AS company_default_group_id
FROM app_company c
LEFT OUTER JOIN app_companygroup cg ON c.id = cg.company_id AND cg.name = 'Default';

INSERT INTO app_companygroupstdinsuranceplan(company_std_insurance_plan_id, company_group_id, created_at, updated_at)
SELECT DISTINCT ocp.company_plan_id, dcg.company_default_group_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM orphan_company_plans ocp
INNER JOIN default_company_groups dcg
ON ocp.company_id = dcg.company_id;

END
$$