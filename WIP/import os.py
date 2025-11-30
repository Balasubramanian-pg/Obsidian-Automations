import os
import re

# List of terms and definitions extracted from the images
data = [
    ("TB", "Tuberculosis"),
    ("MSL", "Medical Science Liaison\nThe Medical Science Liaison (MSL) is a specialized role within the pharmaceutical, biotechnology, medical device, and related health-care fields. They concentrate on a specific therapeutic area or disease state (e.g., oncology, cardiology, gastroenterology, infectious diseases, rheumatology). Their primary role is to build and foster strong relationships with key external experts in their shared therapeutic category."),
    ("Closed loop marketing", "(CLM) in pharma means the act of capturing data from your marketing efforts to understand what's resonating with your audiences – and thereby deliver more relevant communications to healthcare professionals and other key stakeholders (payers, hospital management, administrate buyers)."),
    ("TRANSPARENCY REPORTING", "Any payment or benefit provided to a healthcare professional or a teaching institution directly or indirectly on behalf of pharma company must comply with (a) the policy and law for the country, region or state in which the healthcare professional/teaching institution resides and/or practices medicine, and (b) the specific requirements of any governmental agency which requires pharma company to publicly report certain payments and benefits."),
    ("HCP", "healthcare Provider (CEM- Clinical expert management)"),
    ("KOL/KEE", "Key Opinion Leader or KEE – Key External expert"),
    ("TAE", "Therapy Area Expert"),
    ("EE", "External expert"),
    ("TL", "Thought leaders"),
    ("Vitro", "Research performed outside the living organism"),
    ("Vivo", "Research performed and work is taking inside a living organism (human trials)"),
    ("CLM", "Closed loop marketing"),
    ("GMP", "Good Manufacturing Practices GMP are the guidelines recommended by agencies for the authorization and control of manufacturing of products such as drugs, medical devices, active pharmaceutical ingredients (APIs) etc. Adhering to these guidelines assure the agencies about the quality of the products and that the manufacturers have taken every possible measure to ensure the safety of the product."),
    ("GCP", "Good Clinical Practices GCP are international quality standards defined by the International Conference on Harmonization (ICH) that state the clinical trial regulations for the products that require testing on human subjects. The standards outline the requirements of a clinical trial and the roles and responsibilities of the officials involved in it. It ensures that no human experiments are performed just for the sake of medical advancement."),
    ("GLP", "Good Laboratory Practices These are the standards set by the FDA for non-clinical laboratory tests and studies conducted for assessing the safety and efficacy of the product. GLPs are a set of standards which define the framework for a non-clinical study and states how they should be performed, evaluated, reported etc."),
    ("GxP", "(G)Stands for good (X)Variable(P) Stands for practices."),
    ("KPI", "Key performance indicator"),
    ("REMS", "A Risk Evaluation and Mitigation Strategy (REMS) is a drug safety program that the U.S. Food and Drug Administration (FDA) can require for certain medications with serious safety concerns to help ensure the benefits of the medication outweigh its risks"),
    ("IQVIA OneKey", "Dataset\nThe new OneKey, the result of the integration of three premiere reference data brands, delivers insight into more than 9.7 million professionals and 708,000 organizations in the U.S., and the affiliations linking them together. A single, validated source, OneKey can help your organization:\nExtend its coverage of healthcare professionals, organizations and affiliations"),
    ("DDD", "Drug distribution data (DDD) lets you track the distribution of your branded products to retailers and non-retail buyers in case units. For example, when Drug X comes off the manufacturing line, it's delivered to pharmacies and hospitals around the country.\n\nIQVIA DDD provides zip-code and account-level sales of prescription products sold into retail, non-retail and mail channels.\n-APLD: APLD is IQVIA's Anonymized Patient Level Data – the lowest level of granularity of transactional patient data containing longitudinal prescription (LRx) and medical claims (Dx) data.\n\nIMS DDD – Sales of drugs by the wholesalers to non-retail (hospitals, institutes, etc.) and retail (pharmacies, mail order, etc.). Retail data is available at the zip-code level whereas the non-retail sales data is available at an outlet/account level and is not the actual sales made."),
    ("Fingertip Formulary", "Dataset\nMarket access Fingertip Formulary™ Suite offers an enterprise level market access platform for today’s healthcare environment that offers rich, comprehensive views of the data required to analyse and navigate barriers to access.\n\nGet a complete view of formulary status\nFind out where your brands sit on formularies—and benchmark the competition through our robust, comprehensive datasets and easy to use interface\nView our data from every angle"),
    ("Speaker Program", "Speaker and educational programs are common tools by which pharmaceutical companies pay healthcare providers, including doctors and nurse practitioners, to speak about the benefits, risks, and best practices of prescribing companies' drugs. Most frequently intended to educate the medical community."),
    ("AdBoard", "Scientific communications directors working on a global dermatology brand found that they urgently needed frequent and specific insight from thought leaders to determine and implement critical changes to communications, messaging, and clinical trial design. A digital forum allowed more frequent engagement across all regions."),
    ("Brand product", "Branded products are not generic drugs or products. A brand can be an innovator (first-in-class) or not. It is protected by a patent or has an expired patent. It is licensed under a New Drug Application by the US Food and Drug Administration (FDA)."),
    ("Generic drug", "Competitors to a branded product that has an expired patent. Generics are considered identical to the brand product. Licensed under an Abbreviated New Drug Application by the FDA."),
    ("Biologic", "A therapeutic drug or a vaccine, made from living organisms — human, animal, yeast, or microorganisms — licensed under a Biologic License Application by the FDA."),
    ("Biosimilar", "Competitors to the first-in-class biologic product that has an expired patent. These drugs are not currently considered to be identical to the original product (because of the nature of manufacturing with live products), but are considered to be therapeutic alternatives."),
    ("Retail drugs", "Any kind of drug typically available at a pharmacy counter. Usually billed on a pharmacy claim."),
    ("Physician-administered drugs", "Any kind of drug that cannot typically be self-administered. Usually billed on an office visit claim."),
    ("Specialty drug", "A drug that is costly, requires special supply chain features (such as freezing or cold storage), typically indicated for a small group of patients, and where the patients may need special case management services. This is the broadest definition. There is no single agreed-upon definition, so sometimes specialty drug will only mean high-cost. For instance, specialty drugs in the Medicare Part D program are only defined by cost – currently $670/month (2018) – and indexed annually.\n\nThere is no standard classification that defines a set of specialty drugs. Industry participants (e.g., PBMs and CMS) generally define them based on cost per patient and/or handling requirements. They are often not stocked in a typical retail pharmacy."),
    ("Innovator drug", "The drug from which generics or biosimilars are made – the first product of its type."),
    ("Multisource drugs", "Any and all the generic drugs (included the innovator) which are competing against each other."),
    ("Small molecule products", "These are capsules, tablets, powders, ointments, sprays – that are generally self-administered and available at retail pharmacies with no live ingredients."),
    ("Large molecule products", "These are known as ‘biologics’ – and contain live active ingredients. They are infused or injected and are not typically self-administered."),
    ("Pipeline drugs", "Drugs (small or large molecule) under development by a manufacturer."),
    ("In-line or post-market drugs", "Products that are licensed and in the market."),
    ("Wholesaler", "In a simple distribution system, the wholesaler is the first purchaser of a drug product – direct from the manufacturer. Wholesalers buy very large quantities and then resell either direct to provider-purchasers (like a large health system, pharmacy or pharmacy chain), or resell to smaller, regional distributors for regional or local distribution to retail pharmacies and hospitals."),
    ("Specialty pharmacy", "While retail pharmacies are for short-term illness, specialty pharmacies work with patients and physicians to provide medications for chronic and more severe illnesses.\n\nThese organizations may or may not take ownership of the drug product. Their clients are drug manufacturers that want or need limited distribution of specialty drugs. Specialty drugs are typically (but not always) high cost, require special shipping and storage (freezing or cold storage), are indicated for relatively small patient populations treated by physician specialists.\n\nManufacturers have been accused of using specialty pharmacies to limit access to a drug by potential generic or biosimilar competitors (limited distribution can make it difficult to obtain a drug sample if the entity is not a treating provider on a list approved by the manufacturer).\n\nSpecialty pharmacy can deliver ‘just in time’ products by working with treating providers to supply the appropriate drug in time for a patient visit at the location where the drug will be used."),
    ("Health plan", "Health insurance coverage provided by an individual or group that provides or pays the cost of medical care. Health plans can be provided by public (Medicaid) or private (an employer) entities."),
    ("Payers", "The entity responsible for processing insurance claims. It can handle eligibility, enrollment, and premium payment oversight."),
    ("Pharmacy benefit manager (PBM)", "PBM clients are health plans. PBMs handle some or all of the pharmacy benefit for health plans (formulary design, cost sharing and tiers, pharmacist networks and contracts, price concession negotiation with manufacturers). PBMs may own mail order pharmacies and/or specialty pharmacies. Unless the PBM owns a pharmacy, it is not part of the drug distribution/supply chain."),
    ("Group purchasing organization (GPO)", "These entities represent groups of drug purchasers, such as hospitals and health systems. A GPO negotiates on behalf of its clients for either up-front, on-invoice discounts or back-end rebates. Importantly, GPOs do not take ownership of a drug; they are not part of the supply chain. GPOs essentially negotiate a purchase-order from which members of the buying group can purchase in whatever quantities needed. Wholesalers supplying to GPO members typically provide the drug at the discounted price on the invoice and then are compensated by the manufacturer after the fact. GPOs may provide additional client administrative services as well."),
    ("Pharmacy services administration organization (PSAO)", "Similar to a GPO, but it serves independent pharmacies. In addition to price negotiation with PBMs, PSAOs offer a variety of administrative services to pharmacies. PSAOs are often owned by wholesalers or PBMs."),
    ("Wholesale acquisition cost (WAC)", "The price the wholesaler pays the manufacturer. Generally considered the ‘list’ price. This price is under the control of a manufacturer."),
    ("Average wholesale price (AWP)", "The price at which a wholesaler sells product to others in the supply chain (hospitals or pharmacies for example). AWP is independent of whatever price concession deals a manufacturer might make with hospitals or other purchasers. AWP is generally estimated by companies that provide “pricing files” to insurers or PBMs so they can know how much to reimburse pharmacies, hospitals, clinics, etc. for dispensed drugs. AWP of the pricing files is thought to be higher than what dispensers actually pay. Therefore, many payers reimburse pharmacies something like AWP-17 percent or lower – reflecting what they believe to be the cost that needs to be reimbursed."),
    ("Actual acquisition cost (AAC)", "Increasingly health plans and other large payers are trying to ascertain what pharmacies and other dispensers actually paid to get the drug in stock. Payers want to reduce the extent to which dispensers profit on the drug price and move profit or revenue to the professional fees associated with the dispensing of the drug."),
    ("Rebates", "These are provided by manufacturers and are typically based on the ability of a payer to move market share for the manufacturer’s product. Rebates are confidential. Rebates are billed periodically by the insurer or PBM based on drug utilization subject to the rebate. Rebates allow the manufacturer to retain a high list price (which can be important to the manufacturer so any US price that might wind up in the reference pricing system of another country is high)."),
    ("On-invoice discounts", "Whatever price concession agreement a manufacturer has with a purchaser, the discount is on the invoice (rather than a post-sale rebate)."),
    ("Coupons", "These are given to consumers for use at the point of service (the pharmacy counter). Coupons mitigate the impact of insurance coverage cost sharing for a manufacturer’s product. A coupon might cover the full deductible cost, copays or coinsurance. Pharmacies redeem the coupons with the manufacturer or its coupon administration vendor. There are different views about coupons. They provide patient out of pocket cost relief for drugs where insurance benefits require significant cost sharing on high cost drugs. They also can undermine insurer efforts to control utilization (and costs) by encouraging a patient to move to less costly generics or alternative branded treatments. Coupons are not permitted in Medicaid or Medicare because of the effect on program costs. They are restricted in the commercial markets of California and Massachusetts."),
    ("Average manufacturer price (AMP)", "This is a Medicaid term and does not have any meaning or use outside the Medicaid program at this time. It is calculated by the manufacturer and provided to CMS, which uses it to let state Medicaid programs know the unit rebate amount for billing manufacturers. It is the average of manufacturer prices to the wholesale and retail class of trade (does not include sales from wholesalers to retailers but only the prices in any direct agreement between manufacturer and a retail seller). The Medicaid rebate is 23.1% of the AMP. AMP is confidential and not publicly available."),
    ("Best price (BP)", "Is a Medicaid term and does not have any meaning or use outside the Medicaid program at this time. It is the best price the manufacturer offers to any purchaser in the U.S.; this could be a clinic, a hospital, a health plan, a PBM, and so on. Generally speaking, if the BP is greater than 23.1% of the AMP, all state programs will get the BP rebate. BP is confidential and not publicly available."),
    ("Average sales price (ASP)", "This is a Medicare Part B reimbursement term used to pay for Medicare Part B drugs (which are typically physician-administered drugs). This is the weighted average manufacturer price for a product in the market. This applies to multi source drugs and patented products. Medicare reimburses physicians ASP+ 6 percent for Part B drugs."),
    ("Maximum allowable cost (MAC) and federal upper limits (FUL)", "Briefly, these payment limit methods apply only to multisource drugs (including the off-patent brand). The approach appears to be used by almost all payers. MAC/FUL is the average price of all the multisource drugs in a group. The frequency the MAC/FUL is recalculated is at the discretion of the payer. The multi-source drugs to which a MAC is applied is also at the discretion of the payer."),
    ("Reference price", "This is generally not used in the US at this time for drugs. A reference price limits the amount the insurer will pay for one product to the price of a similar product in the market. There are a number of ways to structure reference pricing, an example would be to tie the amount an insurer will pay (to a doctor or pharmacy for instance) to the lowest price of any drug in the therapeutic class, or limit the insurer payment to the average price of drugs in a class. If the consumer choses a product that exceeds the reference price, the consumer pays — to the provider or pharmacy— the difference between what the insurer will reimburse the pharmacy and the pharmacy’s costs/charge of the more expensive drug."),
    ("Dispensing fee/Professional fee", "There are two parts to pharmacy payment: ingredient cost and dispensing fee. The ingredient cost is where payers apply MAC, AWP, AAC etc. The dispensing fee remunerates for the professional services of the pharmacist. Dispensing fees have trended upward in recent years as payers try to move from pharmacy profits on the ingredient cost to profits on the dispensing fee and as pharmacists have taken on a greater role in case management type services for some health plans."),
    ("AAC", "Actual Acquisition Cost. Usually a surveyed pharmacy drug acquisition cost. It is used by some state Medicaid agencies as a basis for reimbursement."),
    ("ABLA", "Abbreviated Biologics License Application. The pathway for FDA approval of biosimilar products."),
    ("ADR", "Adverse Drug Reaction. An adverse drug reaction (ADR) can be defined as 'an appreciably harmful or unpleasant reaction resulting from an intervention related to the use of a medicinal product'."),
    ("AMP", "Average Manufacturer Price. A statutorily defined average price measure for drug products distributed to the retail class of trade that is used to determine Medicaid rebates and WAMP for generic drugs. It measures prices charged by manufacturers, net of discounts and rebates (excluding certain federal programs). Although it is reported by manufacturers to CMS, it is not publicly available."),
    ("ANDA", "Abbreviated New Drug Application. The pathway for FDA approval that is generally used for generic drugs. See also NDA."),
    ("API", "Active Pharmaceutical Ingredient. Also referred to as “Active Ingredient.”"),
    ("ASP", "Average Sales Price. A statutorily defined price measure used to determine reimbursement for Medicare Part B covered drugs (i.e., physician-administered drugs). It measures average prices charged by manufacturers to all purchasers, net of discounts and rebates (excluding certain federal programs) and is reported by manufacturers to CMS. The payment limits derived from the ASPs are publicly available."),
    ("At-Risk Launch", "Typically refers to a situation where a manufacturer that is a defendant in a patent infringement lawsuit launches its product prior to full resolution of pending litigation."),
    ("Authorized Generic (AG)", "A brand name drug with an approved NDA that is marketed as a generic."),
    ("AWP", "Average Wholesale Price. A reference benchmark that may be used in determining the reimbursement amount for a drug."),
    ("Batch", "A specific quantity of material produced in a process such that it is expected to be homogenous within specified limits."),
    ("Best Price", "A statutorily defined measure of a minimum price for drug products distributed to the retail class of trade that is used to determine Medicaid rebates. It measures the lowest prices charged by manufacturers, net of discounts and rebates (excluding certain nominal transactions and federal programs). Although it is reported by manufacturers to CMS, it is not publicly available."),
    ("Biologic", "A drug product produced from or by biological (living) organisms. These products are often referred to as large molecule drugs because of the complexity of their chemical makeup."),
    ("Biosimilar", "A biologic that is demonstrated to be similar to a reference biologic product. There is an abbreviated approval pathway for these products. See aBLA. These products may not be considered interchangeable with the reference biologic."),
    ("BLA", "Biologic License Application. The pathway for FDA approval of biologic drugs. See also aBLA."),
    ("BPCIA", "Biologics Price Competition and Innovation Act (2009). Created the abbreviated pathway for FDA approval of biosimilar products. See aBLA."),
    ("Branded Product", "A drug marketed under a brand name. Typically refers to products approved under an NDA or BLA/aBLA, though products approved under an ANDA may also be marketed with a brand name."),
    ("CBER", "Center for Biologics Evaluation and Research."),
    ("CDER", "Center for Drug Evaluation and Research."),
    ("CGMP", "Current Good Manufacturing Practices. FDA regulations that govern drug manufacturing processes."),
    ("Chargeback", "Typically a payment made by a manufacturer to a wholesaler to reimburse the wholesaler for a discount that a manufacturer is contractually obligated to provide to the wholesaler’s customer."),
    ("Clinical Trial", "Testing of an IND in human subjects."),
    ("CMS", "Centers for Medicare and Medicaid Services."),
    ("Compounding", "Practice in which a pharmacist combines, mixes, or alters ingredients of a drug to create a medication."),
    ("Contract Price", "A negotiated price for a drug product."),
    ("Coinsurance", "A fixed percentage of the cost of a prescription drug at the point of sale that a pharmacy benefit plan requires the patient to pay."),
    ("Copay Coupon", "A voucher distributed to patients by the manufacturer of a drug that can be redeemed to cover at least some of the patients' out-of-pocket costs for the drug."),
    ("Copayment", "A flat payment amount required by a pharmacy benefit plan that the patient is responsible for paying at the pharmacy point of sale when obtaining a prescription. These generally vary by formulary tier."),
    ("CRO", "Contract Research Organization"),
    ("DAW", "Dispense as Written. A notation by a prescriber that can dictate whether generic substitution will occur when a prescription is filled."),
    ("Detailing", "Efforts by sales representatives for drug manufacturers to educate prescribers about their products."),
    ("Direct Contract", "Contract between a drug manufacturer and a customer (such as a retail pharmacy) where the product does not pass through an intermediary wholesaler."),
    ("Dispensing Fee", "A contracted fee paid to a pharmacy for the service of dispensing/filling a prescription and advising patients. It does not include the drug cost, which is often referred to as the ingredient cost."),
    ("Distributor", "Similar to a wholesaler, but generally does not manage indirect contracts and chargebacks, or run source programs."),
    ("DTC", "Direct to Consumer Advertising (also called DTCA)."),
    ("EAC", "Estimated Acquisition Cost. Used in Medicaid statutes to refer to prices to be used in pharmacy reimbursement (e.g., the AAC or NADAC can be used by a state as its EAC)."),
    ("FDA", "US Food and Drug Administration."),
    ("Fill/Finish", "Manufacturing step involving putting a drug into a container/delivery system under aseptic conditions."),
    ("Formulary", "A list of covered drugs provided by a pharmacy benefit plan describing the level of coverage for each product, and any limits, restrictions, or exclusions to that coverage."),
    ("FUL", "Federal Upper Limit. A statutorily defined upper limit for Medicaid reimbursement of generic drugs."),
    ("Generic Product", "A drug marketed under its chemical name; generally refers to small molecule products approved by the FDA under an ANDA."),
    ("GPO", "Group Purchasing Organization. An entity that aggregates the purchases of health care providers (e.g., hospitals) and contracts with suppliers on their behalf to enable price discounts and efficiencies."),
    ("Hatch-Waxman Act", "Also known as the Drug Price Competition and Patent Term Restoration Act (1984). Among other provisions, created an abbreviated pathway for FDA approval of generic drug products, statutory exclusivity provisions for new and patented drug products, and a 180-day exclusivity period for ANDA filers that challenge patents listed in the Orange Book."),
    ("HCPCS", "Healthcare Common Procedure Coding Sytem. A coding system used by CMS for Medicare to identify drugs and procedures for reimbursement. In this system, drugs are typically listed with a “J” or “Q” followed by a four-digit number."),
    ("IND", "Investigational New Drug."),
    ("Indirect Contract", "Contract between a manufacturer and a customer (such as a retail pharmacy) where product passes through intermediary wholesaler."),
    ("J-Code", "Common term for Medicare HCPCS billing codes for Medicare Part B drugs."),
    ("IRB", "Institutional Review Board."),
    ("Label", "FDA-required labeling provided with medicines. Provides prescribing information such as approved indications, contra-indications, common side effects, and recommended dosing."),
    ("Labeler", "The entity that manufacturers, repacks, or distributes a drug product. See NDC."),
    ("MAC", "Maximum Allowable Cost. Upper limit set by an insurer (Medicaid or private plans) for the reimbursement of multiple-source generic drugs."),
    ("MCO", "Managed Care Organization."),
    ("Medicaid", "A state/federal system of health insurance for those requiring financial assistance. Each state is responsible for its Medicaid program design, operation, and partial funding within federal guidelines managed by the CMS."),
    ("Medicare Part A", "Federal hospital insurance program for the elderly (qualifying age is generally 65)."),
    ("Medicare Part B", "A federal health insurance program for the elderly (qualifying age is generally 65). Covers non-hospital medical services and supplies, including injectable drugs delivered in an office setting."),
    ("Medicare Part D", "Optional additional Medicare coverage for prescription drugs. Covers the costs of medications not covered by Medicare Part B (e.g., oral medications obtained through a pharmacy)."),
    ("NADAC", "National Average Drug Acquisition Cost. A surveyed pharmacy drug invoice cost provided by CMS for use in drug reimbursement by state Medicaid programs."),
    ("NDA", "New Drug Application. The pathway for FDA approval generally used for small molecule drugs."),
    ("NDC", "National Drug Code. A numeric code that uniquely identifies drug products. The code includes three segments that identify the labeler, the product, and the packaging."),
    ("NRx", "New Prescriptions."),
    ("Orange Book", "The FDA's list of Approved Drug Products with Therapeutic Equivalence Evaluations."),
    ("OTC", "Over-the-counter. Typically refers to a drug product that can be purchased without a prescription."),
    ("OOP Cost", "Out-of-pocket cost. The cost that the patient pays at the pharmacy point of sale. For an insured patient being dispensed a covered drug, this cost will include any coinsurance amount or copayment."),
    ("P&T Committee", "Pharmacy and Therapeutics Committee. A group of health care providers and other professionals working on behalf of a managed care plan, hospital, or pharmacy benefit manager to evaluate and manage a drug formulary."),
    ("Paragraph IV Certification", "A certification from an ANDA applicant that a patent (or patents) listed in the Orange Book for the brand-name reference product is invalid, unenforceable, or will not be infringed by the product for which the ANDA was submitted."),
    ("Patient Support Program", "A program that may be offered by a drug's manufacturer to provide personalized support (including financial support) to patients to improve health outcomes."),
    ("PBM", "Pharmacy Benefit Manager. Manages pharmacy benefit plans on behalf of insurers and third-party payors, including, e.g., negotiation of network pharmacy discounts, drug manufacturer rebate contracts, and formulary management."),
    ("Pharmacodynamics", "The study of the biochemical and physiological effects of drugs and the mechanisms of their actions, including the correlation of their actions and effects with their chemical structures."),
    ("Pharmacokinetics", "The study of the movement of drugs in the body, including the processes of absorption, distribution, and localization in tissues."),
    ("Pharmacy Network", "A contracted network of pharmacies that receive business from patients covered by a pharmacy benefit plan in exchange for discounts provided to the PBM or third-party payor."),
    ("Prior Authorization", "A formulary restriction that requires a patient or the patient's physician to obtain approval from the pharmacy benefit manager before reimbursement for the product will be provided."),
    ("Purple Book", "A compendium identifying biological products, including any biosimilar and interchangeable biological products, licensed by the FDA under the Public Health Service Act. Comparable to the Orange Book."),
    ("Rebate", "A post-sale payment or discount that may take various forms in the supply chain for a drug."),
    ("Sampling", "Practice by which pharmaceutical companies and affiliates provide health care"),
    ("Small Molecules (SMOLs)", "Small, chemically manufactured molecules."),
    ("SMD", "Small Molecule Drugs."),
    ("Source Program", "Generic drug purchasing programs provided by wholesalers to small chain and independent pharmacies as an alternative to having to order from (or contract with) manufacturers directly."),
    ("Step Therapy", "A formulary restriction that requires a patient to try and fail on one or more preferred products before a given product will be covered by the pharmacy benefit plan. Also known as a fail-first or step edit restriction."),
    ("Therapeutic Equivalence (TE)", "Drugs classified by the FDA to be therapeutically equivalent can be substituted for one another. For example, generic drugs are typically given “AB” TE codes, which indicate substitutability with a reference product has been demonstrated through evidence supplied via the ANDA."),
    ("Tier", "Drugs listed on a formulary are typically separated into groups or tiers. Lower formulary tiers are typically associated with lower out-of-pocket costs for the patient (see Formulary)."),
    ("TPP", "Third-party payor. An entity, other than the patient, that pays health care expenses."),
    ("TRx", "Total Prescriptions."),
    ("U&C Price", "Usual and Customary Price. In the context of pharmacy reimbursement, this is generally a price submitted by the pharmacy to be used in the absence of a contracted price."),
    ("WAC", "Wholesaler Acquisition Cost. The list price of a pharmaceutical product."),
    ("WAMP", "Weighted AMP. Statutorily defined average of submitted AMPs computed by CMS for the computation of FUL."),
    ("ACIP", "Advisory Committee on Immunization Practices. The Advisory Committee on Immunization Practices (ACIP) is a group of medical and public health experts that develop recommendations on how to use vaccines"),
    ("ADA", "Americans with Disabilities Act. The Americans with Disabilities Act (ADA) prohibits discrimination against people with disabilities in several areas, including employment, transportation, public accommodations, communications and access to state and local government' programs and services."),
    ("CDC", "Centers for Disease Control and Prevention. The Centers for Disease Control and Prevention is the national public health agency of the United States."),
    ("CMS", "Centers for Medicare & Medicaid Services. The Centers for Medicare & Medicaid Services (CMS), is a federal agency within the United States Department of Health and Human Services (HHS) that administers the Medicare program and works in partnership with state governments to administer Medicaid, the Children's Health Insurance Program (CHIP), and health insurance portability standards."),
    ("CoP", "Conditions of Participation"),
    ("EHR", "Electronic Health Record"),
    ("FMLA", "Family and Medical Leave Act (of 1993)"),
    ("HCO", "Healthcare Organization"),
    ("HCP", "Healthcare Personnel\n\n(Also defined in other contexts as: healthcare Provider)"),
    ("HICPAC", "Healthcare Infection Control Practices Advisory Committee"),
    ("HIPPA", "Health Insurance Portability and Accountability Act"),
    ("HIV", "Human Immunodeficiency Virus"),
    ("IIS", "Immunization Information Systems"),
    ("IPC", "Infection Prevention and Control"),
    ("NHSN", "National Healthcare Safety Network"),
    ("NIOSH", "National Institute for Occupational Safety and Health"),
    ("OHS", "Occupational Health Services"),
    ("OSHA", "Occupational Safety and Health Administration"),
    ("PPE", "Personal Protective Equipment"),
    ("PPME", "Pre-Placement Medical Evaluation"),
    ("SESIP", "Sharps with Engineered Sharps Injury Protection")
]

# Create output directory
output_dir = "C:/Videos/glossary_files"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Helper to clean filenames
def clean_filename(s):
    # Replace special chars with underscore, strip leading/trailing underscores
    cleaned = re.sub(r'[^\w\d-]', '_', s).strip('_')
    # Collapse multiple underscores
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned + ".md"

# Dictionary to handle duplicate terms (appending content if needed)
processed_data = {}

for term, definition in data:
    if term in processed_data:
        processed_data[term] += "\n\n" + definition
    else:
        processed_data[term] = definition

# Write files
count = 0
for term, definition in processed_data.items():
    filename = clean_filename(term)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        # Writing Term as Header and Definition as body
        f.write(f"# {term}\n\n{definition}\n")
    count += 1

print(f"Successfully created {count} Markdown files in the '{output_dir}' directory.")