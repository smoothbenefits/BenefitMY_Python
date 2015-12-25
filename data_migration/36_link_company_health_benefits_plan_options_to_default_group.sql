DO $$
BEGIN

-- Find all company plans that currently are 
-- not linked to any company groups
CREATE TEMP TABLE orphan_company_plans AS
SELECT DISTINCT cp.id AS company_plan_id, cp.company_id
FROM app_companybenefitplanoption cp
LEFT OUTER JOIN app_companygroupbenefitplanoption cgp
ON cp.id = cgp.company_benefit_plan_option_id
WHERE cgp.company_benefit_plan_option_id IS NULL;

-- Get company to 'Default' company group mappings
CREATE TEMP TABLE default_company_groups AS
SELECT DISTINCT c.id AS company_id, cg.id AS company_default_group_id
FROM app_company c
LEFT OUTER JOIN app_companygroup cg ON c.id = cg.company_id AND cg.name = 'Default';

INSERT INTO app_companygroupbenefitplanoption(company_benefit_plan_option_id, company_group_id, created_at, updated_at)
SELECT DISTINCT ocp.company_plan_id, dcg.company_default_group_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM orphan_company_plans ocp
INNER JOIN default_company_groups dcg
ON ocp.company_id = dcg.company_id;

END
$$