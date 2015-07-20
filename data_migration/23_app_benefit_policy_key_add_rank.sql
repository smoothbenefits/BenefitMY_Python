DO $$
DECLARE
    item varchar[];
    item_array varchar[] := ARRAY[
        ['Individual Deductible', '100'],
        ['Family Deductible', '200'],
        ['Hospital-Inpatient', '600'],
        ['Out-patient Day Surgery', '700'],
        ['MRI/CT/PET Scans', '500'],
        ['Lab work/X-Ray', '400'],
        ['Chiropractic', '300'],
        ['Prescription Drugs - 30 days', '1000'],
        ['Mail order drugs - 90 days', '1100'],
        ['Annual Rx out of Pocket Maximum - single/family', '900'],
        ['Annual Medical out of Pocket Maximum - single/family', '800'],
        ['Primary Care Physician required', '1200'],
        ['Office Visit Copay (PCP/Specialist)', '230'],
        ['Preventative Office Visits, including related tests', '240'],
        ['Routine Vision Exams', '250'],
        ['Emergency Room Copay', '260']
    ];
BEGIN

    -- First update names where appliable
    update app_benefitpolicykey
    set name = 'Prescription Drugs - 30 days'
    where name = 'Prescription Drugs-30 days';

    update app_benefitpolicykey
    set name = 'Mail order drugs - 90 days'
    where name = 'Mail order drugs-90 days';

    update app_benefitpolicykey
    set name = 'Annual Rx out of Pocket Maximum - single/family'
    where name = 'Annual Rx out of Pocket Maximum';

    update app_benefitpolicykey
    set name = 'Annual Medical out of Pocket Maximum - single/family'
    where name = 'Annual Medical out of Pocket Maximum';

    -- Now, fill in the items where missing, and update items accoridngly
    FOREACH item SLICE 1 IN ARRAY item_array
    LOOP
        IF NOT EXISTS (select 1 from app_benefitpolicykey where trim(name) = item[1])
        THEN
            insert into app_benefitpolicykey (name, rank)
            values(item[1], item[2]::integer);
        ELSE
            update app_benefitpolicykey
            set rank = item[2] :: integer
            where name = item[1];
        END IF;
    End LOOP;

END
$$;
