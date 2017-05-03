DO $$
BEGIN

UPDATE app_employeeprofile ep SET ep.pin = LPAD(ep.company_id, 2, '0') + LPAD(p.user_id, 4, '0')
INNER JOIN app_person p ON ep.person_id = p.id
WHERE ep.pin IS NULL;

END
$$
