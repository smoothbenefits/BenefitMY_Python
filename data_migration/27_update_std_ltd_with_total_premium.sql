DO $$
BEGIN

UPDATE app_usercompanyltdinsuranceplan AS ltd
SET total_premium_per_month = LEAST(cltd.max_benefit_monthly, cltd.percentage_of_salary * ep.annual_base_salary / 100 / 12) * cltd.rate / 10
FROM app_usercompanyltdinsuranceplan ultd 
join app_person AS p ON p.user_id = ultd.user_id
JOIN app_employeeprofile AS ep ON ep.person_id = p.id
JOIN app_companyltdinsuranceplan AS cltd ON cltd.id = ultd.company_ltd_insurance_id
WHERE ultd.id = ltd.id;

UPDATE app_usercompanystdinsuranceplan AS std
SET total_premium_per_month = LEAST(cstd.max_benefit_weekly, cstd.percentage_of_salary * ep.annual_base_salary / 100 / 52 ) * cstd.rate / 10
FROM app_usercompanystdinsuranceplan ustd 
join app_person AS p ON p.user_id = ustd.user_id
JOIN app_employeeprofile AS ep ON ep.person_id = p.id
JOIN app_companystdinsuranceplan AS cstd ON cstd.id = ustd.company_std_insurance_id
WHERE ustd.id = std.id;


END
$$
;