DO $$
BEGIN

--Fill the Company pay_period_definition

UPDATE app_company SET pay_period_definition_id = 2;


--First do the health numbers

UPDATE app_companybenefitplanoption
SET employee_cost_per_period = employee_cost_per_period / 0.46153846153846;

-- Then do the basic life
UPDATE app_companylifeinsuranceplan 
SET employee_cost_per_period = employee_cost_per_period / 0.46153846153846 
WHERE employee_cost_per_period IS NOT NULL AND employee_cost_per_period > 0;

END
$$;