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
        ['Prescription Drugs-30 days', '1000'],
        ['Mail order drugs-90 days', '1100'],
        ['Annual Rx out of Pocket Maximum', '900'],
        ['Annual Medical out of Pocket Maximum', '800'],
        ['Primary Care Physician required', '1200'],
        ['Office Visit Copay (PCP/Specialist)', '230'],
        ['Preventative Office Visits, including related tests', '240'],
        ['Routine Vision Exams', '250'],
        ['Emergency Room Copay', '260']
    ];
BEGIN

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
