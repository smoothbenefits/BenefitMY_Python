update app_documenttype
set default_content='
                      {{CompanyName}}
Offer Letter
{{TodayDate}}
{{EmployeeName}}

Dear {{EmployeeName}}:
{{CompanyName}}, (the “Company”), is pleased to offer you employment with the Company on the terms described below.
1.  Position.  You will start in a full-time position as  {{EmployeeTitle}}.
2.  Duties.  You will be responsible for such duties as are normally associated with such position. 
3.  Compensation.  You will be paid a starting salary at the rate of {{EmployeeAnnualSalary}}/year, payable on the Company’s regular payroll dates.  
4.  Benefits.  As a regular employee of the Company you will be eligible to participate in a number of Company-sponsored benefits, which are described in the employee benefit summary that I have attached hereto as Exhibit A. 
5.  Confidential Information and Invention Assignment Agreement.  As a condition of employment, you will be required to sign and comply with a Confidentiality and Invention Assignment Agreement, which among other things, prohibits unauthorized use or disclosure of Company proprietary information.
6.      Company Policies.  As a Company employee, you will be expected to abide by the Company''s rules and standards. [Specifically, you will be required to sign an acknowledgment that you have read and that you understand the Company''s rules of conduct which are included in the Company Handbook.
7.  I-9 Condition to Employment.  As a condition of employment, you will be required to sign and return a satisfactory I-9 Immigration form providing sufficient documentation establishing your employment eligibility in the United States, and provide satisfactory proof of your identity as required by United States law. 
8.  Background Check.  Your employment is further subject to satisfactory completion of a background check.
9.  Representation.  By signing below, you represent that your performance of services to the Company will not violate any duty which you may have to any other person or entity (such as a present or former employer), including obligations concerning providing services (whether or not competitive) to others, confidentiality of proprietary information and assignment of inventions, ideas, patents or copyrights, and you agree that you will not do anything in the performance of services hereunder that would violate any such duty.
10. Employment Relationship. Notwithstanding any of the above, your employment with the Company is “at will”.  This means you may terminate your employment with the Company at any time and for any reason whatsoever simply by notifying the Company.  Likewise, the Company may terminate your employment at any time and for any reason whatsoever, with or without cause or advance notice.  Although your job duties, title, compensation and benefits, as well as the Company’s personnel policies and procedures, may change from time to time, the “at will” nature of your employment may only be changed in an express written agreement signed by you and the Company’s Chief Executive Officer.
11.     Dispute Resolution. In the event of any dispute or claim relating to or arising out of our employment relationship, you and the Company agree that (i) any and all disputes between you and the Company shall be fully and finally resolved by binding arbitration, (ii) you are waiving any and all rights to a jury trial but all court remedies will be available in arbitration, (iii) all disputes shall be resolved by a neutral arbitrator who shall issue a written opinion, (iv) the arbitration shall provide for adequate discovery, and (v) the Company shall pay all but the first $125 of the arbitration fees. Please note that we must receive your signed Agreement before your first day of employment.
13. Outside Activities.  While you render services to the Company, you agree that you will not engage in any other employment, consulting or other business activity without the written consent of the Company.  In addition, while you render services to the company, you will not assist any person or entity in competing with the Company, in preparing to compete with the Company or in hiring any employees or consultants of the Company.
14. Withholding Taxes.  All forms of compensation referred to in this letter are subject to applicable withholding and payroll taxes.
15. Entire Agreement.   If you accept this offer, this letter and the Confidential Information and Invention Assignment Agreement shall constitute the complete agreement between you and Company with respect to the terms and conditions of your employment.  Any prior or contemporaneous representations (whether oral or written) not contained in this letter or the Confidential Information and Invention Assignment Agreement or contrary to those contained in this letter or the Confidential Information and Invention Assignment Agreement, that may have been made to you are expressly cancelled and superseded by this offer. 

[Signature Page Follows]

If you wish to accept this offer, please sign and date this letter, and the attached Confidentiality and Invention Assignment Agreement and return it to the Company by [date] along with a signed and satisfactory I-9 Immigration form    
We look forward to having you join us no later than {{EmployeeStartDate}}.
Very truly yours,
{{CompanyName}}

By: {{CompanyHRManagerName}}    
Title:{{CompanyHRTitle}}

ACCEPTED AND AGREED:
    
Employee Name Printed: {{EmployeeName}}
    
    

EXHIBIT A
EMPLOYEE BENEFITS SUMMARY
(if none then leave blank)'
where name='Offer Letter';