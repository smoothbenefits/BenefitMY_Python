DO $$
BEGIN

UPDATE app_employeeprofile SET employment_status = 'Active'
WHERE employment_status IS NULL;

END
$$
