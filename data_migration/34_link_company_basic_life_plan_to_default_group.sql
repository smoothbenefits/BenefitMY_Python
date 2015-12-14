DO $$
BEGIN

-- Find all company basic life plans that currently are 
-- not linked to any company groups
CREATE TEMP TABLE orphan_company_plans AS
SELECT DISTINCT clip.id AS company_plan_id, clip.company_id
FROM app_companylifeinsuranceplan clip
LEFT OUTER JOIN app_companygroupbasiclifeinsuranceplan cgblip
ON clip.id = cgblip.company_basic_life_insurance_plan_id
LEFT OUTER JOIN app_lifeinsuranceplan lip
ON lip.id = clip.life_insurance_plan_id
WHERE cgblip.company_basic_life_insurance_plan_id IS NULL
    AND lip.insurance_type = 'Basic';

-- Get company to 'Default' company group mappings
CREATE TEMP TABLE default_company_groups AS
SELECT DISTINCT c.id AS company_id, cg.id AS company_default_group_id
FROM app_company c
LEFT OUTER JOIN app_companygroup cg ON c.id = cg.company_id AND cg.name = 'Default';

INSERT INTO app_companygroupbasiclifeinsuranceplan(company_basic_life_insurance_plan_id, company_group_id, created_at, updated_at)
SELECT DISTINCT ocp.company_plan_id, dcg.company_default_group_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM orphan_company_plans ocp
INNER JOIN default_company_groups dcg
ON ocp.company_id = dcg.company_id;

END
$$