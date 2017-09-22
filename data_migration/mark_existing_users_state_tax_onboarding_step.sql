DO $$
BEGIN

INSERT INTO app_useronboardingstepstate (step, state, user_id, updated_at)
SELECT 'state_tax_info', 'completed', cu.user_id, now()
FROM app_companyuser cu
WHERE cu.company_user_type='employee';

END
$$
