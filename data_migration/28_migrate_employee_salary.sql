DO $$
BEGIN

INSERT INTO app_employeecompensation
  (annual_base_salary, increase_percentage, effective_date, company_id, person_id, reason_id, created_at, updated_at)
SELECT ep.annual_base_salary, NULL, ep.created_at, ep.company_id, ep.person_id, NULL, now(), now()
FROM app_employeeprofile ep
LEFT OUTER JOIN app_employeecompensation ec ON ep.person_id = ec.person_id AND ep.company_id = ec.company_id
  AND ep.annual_base_salary = ec.annual_base_salary
WHERE ec.id IS NULL;

END
$$
;
