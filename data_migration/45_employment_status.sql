DO $$
BEGIN

UPDATE app_employeeprofile SET employment_type = 'Active'
WHERE employment_type IS NULL;

END
$$
