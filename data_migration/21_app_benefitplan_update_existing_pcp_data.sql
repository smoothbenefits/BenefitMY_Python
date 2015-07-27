DO $$
BEGIN
update app_benefitplan set mandatory_pcp = 't' where name like '%Harvard Pilgrim HMO%' and benefit_type_id = 1;
update app_benefitplan set pcp_link='https://www.providerlookuponline.com/harvardpilgrim/po7/Search.aspx' where name like '%Harvard Pilgrim HMO%' and benefit_type_id = 1;

update app_benefitplan set mandatory_pcp = 't' where name like '%Neighborhood Health Plan (HMO)%' and benefit_type_id = 1;
update app_benefitplan set pcp_link='http://nhp.prismisp.com/' where name like '%Neighborhood Health Plan (HMO)%' and benefit_type_id = 1;

update app_benefitplan set mandatory_pcp = 't' where name like 'Harvard Pilgrim Best Buy HMO $1,500' and benefit_type_id = 1;
update app_benefitplan set pcp_link='https://www.providerlookuponline.com/harvardpilgrim/po7/Search.aspx' where name like 'Harvard Pilgrim Best Buy HMO $1,500' and benefit_type_id = 1;

update app_benefitplan set mandatory_pcp = 't' where name like 'HMO Blue New England $3,000 Deductible' and benefit_type_id = 1;
update app_benefitplan set pcp_link='https://www.bluecrossma.com/wps/portal/members/using-my-plan/doctors-hospitals/findadoctor/' where name like 'HMO Blue New England $3,000 Deductible' and benefit_type_id = 1;
END
$$
;
