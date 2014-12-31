BEGIN;

-- create temporary table to store user ids and person ids
SELECT u.id INTO TEMPORARY TABLE user_ids
FROM auth_user u
WHERE lower(u.email) like 'f%qui@gmail.com';

SELECT p.id INTO TEMPORARY TABLE person_ids
FROM app_person p
INNER JOIN user_ids u on p.user_id = u.id
WHERE u.id IN (SELECT id FROM user_ids);

-- delete user information based on stored user ids and person ids
DELETE FROM app_companyuser cu
WHERE cu.user_id IN (SELECT id FROM user_ids);

DELETE FROM app_employmentauthorization ea
WHERE ea.user_id IN (SELECT id FROM user_ids);

DELETE FROM app_address a
WHERE a.person_id IN (SELECT id FROM person_ids);

DELETE FROM app_phone p
WHERE p.person_id IN (SELECT id FROM person_ids);

DELETE FROM app_enrolled e
WHERE e.person_id IN (SELECT id FROM person_ids);

DELETE FROM app_person p
WHERE p.user_id IN (SELECT id FROM user_ids);

DELETE FROM app_document d
WHERE d.signature_id IN (
    SELECT s.id FROM app_signature s
    WHERE s.user_id IN (SELECT id FROM user_ids)
);

DELETE FROM app_document d
WHERE d.user_id IN (SELECT id FROM user_ids);

DELETE FROM app_signature s
WHERE s.user_id IN (SELECT id FROM user_ids);

DELETE FROM app_usercompanybenefitplanoption ucb
WHERE ucb.user_id IN (SELECT id FROM user_ids);

DELETE FROM app_w4 w
WHERE w.user_id IN (SELECT id FROM user_ids);

DELETE FROM auth_user u
WHERE u.id IN (SELECT id FROM user_ids);

-- drop both temporary tables when all deletion was done
DROP TABLE user_ids;
DROP TABLE person_ids;

COMMIT;
