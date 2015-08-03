DO $$
BEGIN

--First do the health numbers

UPDATE app_companybenefitplanoption AS cb
SET employee_cost_per_period = cb.employee_cost_per_period / p.month_factor
FROM app_company AS c
JOIN app_sysperioddefinition AS p ON p.id = c.pay_period_definition_id
WHERE c.id = cb.company_id;

-- Then do the basic life
UPDATE app_companylifeinsuranceplan AS ci
SET employee_cost_per_period = ci.employee_cost_per_period / p.month_factor
FROM app_company AS c
JOIN app_sysperioddefinition AS p ON p.id = c.pay_period_definition_id
WHERE c.id = ci.company_id AND ci.employee_cost_per_period IS NOT NULL AND ci.employee_cost_per_period > 0;

END
$$;