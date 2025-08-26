"""
Industry-specific document classification categories and extraction prompts.
Each industry has tailored categories that reflect their unique document types and business needs.
"""

INDUSTRY_CATEGORIES = {
    "general": {
        "categories": [
            "Finance", "Legal", "Operations", "HR", "Product", "Engineering / Tech",
            "Sales", "Marketing / Communications", "Customer Success / Support",
            "Strategy / Corp Dev", "Compliance / Risk", "Other"
        ],
        "descriptions": {
            "Finance": "budgets, forecasts, invoices, audits",
            "Legal": "contracts, compliance, IP, regulatory",
            "Operations": "process docs, logistics, supply chain, facilities",
            "HR": "hiring, payroll, benefits, employee relations",
            "Product": "roadmaps, specs, R&D, design",
            "Engineering / Tech": "code, architecture, infrastructure, IT",
            "Sales": "pitches, deal flow, pipeline, CRM exports",
            "Marketing / Communications": "brand, PR, campaigns, content",
            "Customer Success / Support": "onboarding, training, help docs, feedback",
            "Strategy / Corp Dev": "M&A, partnerships, investor updates, OKRs",
            "Compliance / Risk": "audit reports, security, regulatory filings",
            "Other": "general documents that don't fit other categories"
        },
        "extraction_prompts": {
            "Finance": """
                Extract key financial information:
                - Document type (budget, forecast, invoice, audit report, financial statement)
                - Time period or fiscal year covered
                - Currency and monetary amounts (totals, line items, variances)
                - Budget categories or cost centers
                - Revenue, expenses, profit/loss figures
                - Key financial metrics or KPIs
                - Approval status and authorized personnel
                - Payment terms, due dates, or billing cycles
            """,
            "Legal": """
                Extract essential legal information:
                - Document type (contract, agreement, compliance doc, IP filing, regulation)
                - Parties involved (names, roles, entities)
                - Effective dates, terms, and expiration
                - Key obligations and rights
                - Jurisdiction and governing law
                - Dispute resolution mechanisms
                - Termination conditions and penalties
                - Compliance requirements and deadlines
            """,
            "Operations": """
                Extract operational information:
                - Process or operation name and scope
                - Standard operating procedures and workflows
                - Performance metrics and KPIs
                - Resource requirements (personnel, equipment, materials)
                - Quality standards and specifications
                - Timelines and scheduling requirements
                - Dependencies and critical path items
                - Risk factors and mitigation strategies
            """,
            "HR": """
                Extract human resources information:
                - Employee information (roles, departments, levels)
                - Compensation and benefits details
                - Policy requirements and procedures
                - Training and development programs
                - Performance evaluation criteria
                - Compliance and regulatory requirements
                - Organizational structure and reporting lines
                - Recruitment and retention strategies
            """,
            "Product": """
                Extract product information:
                - Product name, version, or release information
                - Features, capabilities, and specifications
                - Target market and user personas
                - Development timeline and milestones
                - Technical requirements and dependencies
                - Research findings and user feedback
                - Design principles and UI/UX guidelines
                - Competitive analysis and market positioning
            """,
            "Engineering / Tech": """
                Extract technical information:
                - System or application name
                - Technical architecture and infrastructure details
                - Code components, APIs, and integrations
                - Security requirements and protocols
                - Performance specifications and benchmarks
                - Development tools and frameworks
                - Deployment and configuration details
                - Monitoring and maintenance procedures
            """,
            "Sales": """
                Extract sales information:
                - Customer or prospect information
                - Deal size, value, and probability
                - Sales stage and next steps
                - Product or service offerings
                - Competitive landscape and positioning
                - Pricing and contract terms
                - Key stakeholders and decision makers
                - Timeline and closing expectations
            """,
            "Marketing / Communications": """
                Extract marketing and communications information:
                - Campaign name and objectives
                - Target audience and demographics
                - Messaging and positioning strategy
                - Marketing channels and tactics
                - Budget allocation and resource requirements
                - Success metrics and performance indicators
                - Timeline and key milestones
                - Brand guidelines and creative assets
            """,
            "Customer Success / Support": """
                Extract customer success and support information:
                - Customer information and account details
                - Issue or request description
                - Resolution steps and outcomes
                - Customer satisfaction metrics
                - Support channel and communication history
                - Escalation procedures and ownership
                - Knowledge base and documentation references
                - Training and onboarding requirements
            """,
            "Strategy / Corp Dev": """
                Extract strategic and corporate development information:
                - Strategic initiative or project name
                - Business objectives and success criteria
                - Market opportunity and competitive analysis
                - Resource requirements and investment needs
                - Timeline and key milestones
                - Risk assessment and mitigation strategies
                - Stakeholder alignment and communication plan
                - Expected outcomes and value creation
            """,
            "Compliance / Risk": """
                Extract compliance and risk information:
                - Regulatory framework and requirements
                - Risk assessment and impact analysis
                - Compliance status and audit findings
                - Mitigation strategies and control measures
                - Responsible parties and accountability
                - Reporting requirements and deadlines
                - Monitoring and review procedures
                - Escalation and incident response protocols
            """,
            "Other": """
                Extract general information:
                - Document type and primary purpose
                - Key stakeholders and organizations involved
                - Important dates and deadlines
                - Financial figures and cost estimates
                - Technical specifications or requirements
                - Action items and next steps
                - Risk factors and considerations
                - Decision points and approvals needed
            """
        }
    },
    
    "energy": {
        "categories": [
            "Exploration & Production", "Operations & Maintenance", "Environmental & Safety",
            "Regulatory & Compliance", "Finance & Trading", "Engineering & Infrastructure",
            "Supply Chain & Procurement", "Health & Safety", "Asset Management",
            "Market Analysis", "Sustainability & ESG", "Other"
        ],
        "descriptions": {
            "Exploration & Production": "geological surveys, drilling reports, reservoir analysis, production data",
            "Operations & Maintenance": "facility operations, maintenance schedules, equipment specs, outage reports",
            "Environmental & Safety": "environmental impact assessments, safety protocols, incident reports, permits",
            "Regulatory & Compliance": "permit applications, regulatory filings, compliance audits, government relations",
            "Finance & Trading": "commodity trading, hedging strategies, project financing, revenue forecasts",
            "Engineering & Infrastructure": "pipeline specs, facility design, technical drawings, capacity studies",
            "Supply Chain & Procurement": "equipment procurement, vendor contracts, logistics planning, inventory management",
            "Health & Safety": "safety training, emergency procedures, accident reports, HSE compliance",
            "Asset Management": "asset valuations, lifecycle management, investment decisions, portfolio analysis",
            "Market Analysis": "market forecasts, pricing analysis, demand studies, competitive intelligence",
            "Sustainability & ESG": "carbon reporting, sustainability initiatives, ESG metrics, renewable energy plans",
            "Other": "documents that don't fit other energy industry categories"
        },
        "extraction_prompts": {
            "Exploration & Production": """
                Extract key exploration and production information:
                - Field/block name and location (geographic coordinates, basin)
                - Resource type (oil, gas, condensate) and estimated reserves
                - Drilling program details (well count, depth, completion dates)
                - Production rates and decline curves
                - Recovery factors and extraction methods
                - Geological formations and reservoir characteristics
                - Environmental conditions and operational challenges
                - Investment amounts and project economics
                - Key personnel and operational partners
                - Regulatory permits and compliance status
            """,
            "Operations & Maintenance": """
                Extract operational and maintenance information:
                - Facility name and operational capacity
                - Maintenance schedules and equipment specifications
                - Downtime events and root cause analysis
                - Performance metrics (availability, reliability, efficiency)
                - Operational procedures and safety protocols
                - Equipment condition and remaining life assessments
                - Maintenance costs and budget allocations
                - Spare parts inventory and procurement needs
                - Workforce requirements and skill sets
                - Incident reports and corrective actions
            """,
            "Environmental & Safety": """
                Extract environmental and safety information:
                - Environmental impact assessment scope and findings
                - Emissions data (CO2, methane, NOx, particulates)
                - Water usage and waste management procedures
                - Biodiversity impact and mitigation measures
                - Safety incidents and near-miss reports
                - Emergency response procedures and equipment
                - Environmental permits and compliance status
                - Remediation activities and monitoring programs
                - Community engagement and stakeholder concerns
                - Regulatory requirements and inspection results
            """,
            "Regulatory & Compliance": """
                Extract regulatory and compliance information:
                - Regulatory body and jurisdiction
                - Permit types and application status
                - Compliance requirements and deadlines
                - Inspection results and findings
                - Violation notices and corrective actions
                - Regulatory fees and financial obligations
                - Environmental impact assessments required
                - Public consultation and stakeholder feedback
                - Appeal processes and legal proceedings
                - Regulatory changes and policy updates
            """,
            "Finance & Trading": """
                Extract financial and trading information:
                - Commodity type and trading volumes
                - Price benchmarks and hedging strategies
                - Contract terms and delivery specifications
                - Credit arrangements and counterparty risks
                - Revenue projections and market forecasts
                - Transportation and storage costs
                - Risk management strategies and instruments
                - Market analysis and price volatility
                - Regulatory capital requirements
                - Financial reporting and accounting treatments
            """,
            "Engineering & Infrastructure": """
                Extract engineering and infrastructure information:
                - Project name and technical specifications
                - Design parameters and capacity ratings
                - Construction timelines and milestones
                - Technical drawings and equipment lists
                - Safety factors and design standards
                - Materials specifications and sourcing
                - Installation procedures and testing protocols
                - Commissioning requirements and acceptance criteria
                - Operational parameters and control systems
                - Expansion capabilities and future modifications
            """,
            "Supply Chain & Procurement": """
                Extract supply chain and procurement information:
                - Vendor information and supplier qualifications
                - Equipment specifications and delivery schedules
                - Contract terms and pricing structures
                - Quality requirements and inspection procedures
                - Logistics arrangements and transportation modes
                - Inventory levels and reorder points
                - Lead times and critical path dependencies
                - Risk assessments and contingency plans
                - Payment terms and financial arrangements
                - Performance metrics and vendor evaluations
            """,
            "Health & Safety": """
                Extract health and safety information:
                - Safety training programs and certification requirements
                - Incident reports and injury statistics
                - Emergency response procedures and evacuation plans
                - Personal protective equipment specifications
                - Safety audits and inspection results
                - Risk assessments and hazard identification
                - Safety management systems and protocols
                - Contractor safety requirements and qualifications
                - Safety performance indicators and targets
                - Regulatory compliance and industry standards
            """,
            "Asset Management": """
                Extract asset management information:
                - Asset identification and classification
                - Valuation methods and current asset values
                - Depreciation schedules and remaining useful life
                - Performance metrics and condition assessments
                - Maintenance strategies and lifecycle costs
                - Investment decisions and capital allocation
                - Divestiture opportunities and market conditions
                - Risk factors and mitigation strategies
                - Portfolio optimization and strategic planning
                - Financial returns and value creation metrics
            """,
            "Market Analysis": """
                Extract market analysis information:
                - Market segments and geographic regions
                - Supply and demand fundamentals
                - Price forecasts and market drivers
                - Competitive landscape and market share
                - Regulatory impacts on market dynamics
                - Technology trends and disruptions
                - Economic indicators and correlation factors
                - Seasonal patterns and cyclical trends
                - Risk factors and uncertainty analysis
                - Investment opportunities and strategic recommendations
            """,
            "Sustainability & ESG": """
                Extract sustainability and ESG information:
                - Carbon emissions and reduction targets
                - Renewable energy initiatives and investments
                - Environmental management systems and certifications
                - Social impact programs and community investments
                - Governance structures and board composition
                - ESG performance metrics and reporting standards
                - Stakeholder engagement and materiality assessments
                - Sustainability goals and progress tracking
                - Climate risk assessments and adaptation strategies
                - Regulatory requirements and disclosure obligations
            """,
            "Other": """
                Extract general energy industry information:
                - Document type and primary purpose
                - Key stakeholders and organizations involved
                - Important dates and deadlines
                - Financial figures and cost estimates
                - Technical specifications or requirements
                - Geographical locations and facilities
                - Regulatory or compliance aspects
                - Risk factors and mitigation measures
                - Strategic objectives and outcomes
                - Next steps and follow-up actions required
            """
        }
    },
    
    "financial_services": {
        "categories": [
            "Credit & Risk", "Investment Management", "Regulatory & Compliance",
            "Client Services", "Operations & Technology", "Market Research",
            "Product Development", "Audit & Controls", "Trading & Markets",
            "Wealth Management", "Corporate Banking", "Other"
        ],
        "descriptions": {
            "Credit & Risk": "credit reports, risk assessments, loan documentation, default analysis",
            "Investment Management": "portfolio analysis, investment strategies, fund reports, performance metrics",
            "Regulatory & Compliance": "regulatory filings, compliance reports, KYC documentation, AML procedures",
            "Client Services": "client onboarding, account management, service agreements, complaint resolution",
            "Operations & Technology": "system documentation, process flows, technology infrastructure, data management",
            "Market Research": "market analysis, economic reports, sector studies, investment research",
            "Product Development": "product specifications, pricing models, launch plans, feature documentation",
            "Audit & Controls": "internal audits, control frameworks, SOX documentation, risk assessments",
            "Trading & Markets": "trading reports, market data, execution analysis, derivatives documentation",
            "Wealth Management": "financial plans, investment proposals, client portfolios, advisory reports",
            "Corporate Banking": "corporate lending, treasury services, trade finance, cash management",
            "Other": "documents that don't fit other financial services categories"
        },
        "extraction_prompts": {
            "Credit & Risk": """
                Extract credit and risk information:
                - Borrower or counterparty identification and credit rating
                - Loan or credit facility details (amount, term, interest rate)
                - Collateral and security arrangements
                - Risk assessment methodology and credit scoring
                - Default probability and loss given default estimates
                - Covenant requirements and compliance status
                - Regulatory capital requirements and provisioning
                - Credit limit and exposure calculations
                - Risk mitigation strategies and hedging instruments
                - Historical performance and delinquency rates
            """,
            "Investment Management": """
                Extract investment management information:
                - Fund or portfolio name and investment objective
                - Asset allocation and investment strategy
                - Performance metrics (returns, benchmark comparisons, Sharpe ratio)
                - Risk metrics (volatility, VaR, maximum drawdown)
                - Holdings and sector/geographic allocation
                - Fee structure and expense ratios
                - Investment committee decisions and rationale
                - Client mandates and investment restrictions
                - ESG considerations and sustainability metrics
                - Liquidity requirements and redemption terms
            """,
            "Regulatory & Compliance": """
                Extract regulatory and compliance information:
                - Regulatory authority and jurisdiction
                - Compliance framework and requirements
                - Filing deadlines and submission status
                - KYC/AML procedures and customer verification
                - Capital adequacy ratios and stress test results
                - Regulatory violations and remediation actions
                - Audit findings and management responses
                - Policy updates and implementation timelines
                - Training requirements and completion status
                - Reporting obligations and data requirements
            """,
            "Client Services": """
                Extract client services information:
                - Client identification and account details
                - Service request type and priority level
                - Resolution timeline and status updates
                - Client satisfaction scores and feedback
                - Service level agreements and performance metrics
                - Communication history and interaction logs
                - Escalation procedures and management involvement
                - Product or service recommendations
                - Account changes and maintenance requests
                - Cross-selling opportunities and referrals
            """,
            "Operations & Technology": """
                Extract operations and technology information:
                - System name and technical specifications
                - Process workflows and automation capabilities
                - Performance metrics (uptime, response time, throughput)
                - Data management and governance procedures
                - Security protocols and access controls
                - Integration points and API documentation
                - Change management and release procedures
                - Disaster recovery and business continuity plans
                - Vendor management and technology partnerships
                - Cost optimization and efficiency initiatives
            """,
            "Market Research": """
                Extract market research information:
                - Market segment and geographic scope
                - Research methodology and data sources
                - Market size, growth rates, and forecasts
                - Competitive landscape and market share analysis
                - Economic indicators and correlation factors
                - Consumer behavior and demand patterns
                - Regulatory changes and market implications
                - Technology trends and disruption risks
                - Investment themes and sector recommendations
                - Risk factors and uncertainty analysis
            """,
            "Product Development": """
                Extract product development information:
                - Product name and target market segment
                - Feature specifications and technical requirements
                - Pricing strategy and fee structure
                - Competitive analysis and differentiation factors
                - Regulatory approvals and compliance requirements
                - Launch timeline and go-to-market strategy
                - Revenue projections and profitability analysis
                - Risk assessment and mitigation strategies
                - Technology platform and infrastructure needs
                - Marketing and distribution channels
            """,
            "Audit & Controls": """
                Extract audit and controls information:
                - Audit scope and objectives
                - Control framework and testing procedures
                - Risk assessment and materiality thresholds
                - Audit findings and control deficiencies
                - Management responses and remediation plans
                - SOX compliance and internal control certification
                - Independent auditor opinions and recommendations
                - Regulatory examination results
                - Process improvements and control enhancements
                - Timeline for implementation and follow-up
            """,
            "Trading & Markets": """
                Extract trading and markets information:
                - Instrument type and trading venue
                - Trading strategy and execution methodology
                - Position sizes and risk limits
                - Market data and pricing information
                - Execution quality and transaction costs
                - Counterparty exposure and settlement details
                - Profit and loss attribution and performance metrics
                - Regulatory trade reporting and compliance
                - Market making and liquidity provision
                - Derivatives usage and hedging strategies
            """,
            "Wealth Management": """
                Extract wealth management information:
                - Client net worth and investment objectives
                - Risk tolerance and investment time horizon
                - Asset allocation recommendations and rationale
                - Investment product recommendations and alternatives
                - Financial planning goals and milestone tracking
                - Tax optimization strategies and implications
                - Estate planning and succession considerations
                - Insurance needs and coverage recommendations
                - Fee schedule and compensation structure
                - Performance reporting and client communication
            """,
            "Corporate Banking": """
                Extract corporate banking information:
                - Corporate client identification and industry sector
                - Banking relationship and service offerings
                - Credit facilities and loan structures
                - Cash management and treasury services
                - Trade finance and international banking
                - Foreign exchange and hedging solutions
                - Deposit accounts and liquidity management
                - Investment banking and capital markets services
                - Fee income and relationship profitability
                - Cross-selling opportunities and client needs
            """,
            "Other": """
                Extract general financial services information:
                - Document type and business purpose
                - Financial institutions and parties involved
                - Key financial metrics and performance indicators
                - Regulatory or compliance considerations
                - Risk factors and mitigation strategies
                - Timeline and critical deadlines
                - Decision points and approval requirements
                - Market conditions and economic factors
                - Technology and operational considerations
                - Strategic implications and next steps
            """
        }
    },
    
    "healthcare": {
        "categories": [
            "Clinical Operations", "Regulatory Affairs", "Research & Development",
            "Quality Assurance", "Patient Care", "Medical Affairs",
            "Pharmacovigilance", "Manufacturing", "Commercial Operations",
            "Health Economics", "Digital Health", "Other"
        ],
        "descriptions": {
            "Clinical Operations": "clinical protocols, trial reports, patient data, study designs",
            "Regulatory Affairs": "FDA submissions, regulatory approvals, compliance documentation, labeling",
            "Research & Development": "research protocols, lab reports, drug development, preclinical studies",
            "Quality Assurance": "quality control, validation protocols, batch records, deviation reports",
            "Patient Care": "medical records, treatment plans, care protocols, patient outcomes",
            "Medical Affairs": "medical communications, scientific publications, advisory boards, medical education",
            "Pharmacovigilance": "adverse event reports, safety data, risk management, surveillance studies",
            "Manufacturing": "manufacturing processes, facility specs, equipment validation, supply chain",
            "Commercial Operations": "marketing materials, sales training, market access, pricing strategies",
            "Health Economics": "cost-effectiveness studies, health outcomes research, reimbursement data",
            "Digital Health": "digital therapeutics, health apps, telemedicine, data analytics",
            "Other": "documents that don't fit other healthcare categories"
        },
        "extraction_prompts": {
            "Clinical Operations": """
                Extract clinical operations information:
                - Study title and protocol number
                - Primary and secondary endpoints
                - Patient inclusion/exclusion criteria
                - Study design and methodology (randomized, blinded, placebo-controlled)
                - Patient enrollment status and demographics
                - Treatment arms and dosing regimens
                - Safety monitoring and adverse event reporting
                - Study timelines and milestone completion
                - Investigator information and site locations
                - Regulatory status and approvals
            """,
            "Regulatory Affairs": """
                Extract regulatory affairs information:
                - Regulatory pathway and submission type (IND, NDA, BLA, 510(k))
                - Indication and therapeutic area
                - Regulatory authority and jurisdiction
                - Submission timelines and milestones
                - Clinical trial requirements and study endpoints
                - Manufacturing and quality specifications
                - Labeling and prescribing information
                - Post-market commitments and requirements
                - Advisory committee meetings and outcomes
                - Approval conditions and restrictions
            """,
            "Research & Development": """
                Extract research and development information:
                - Research program and therapeutic area
                - Compound or device identification and mechanism of action
                - Preclinical study results and safety profiles
                - Biomarker and companion diagnostic development
                - Intellectual property and patent landscape
                - Research collaboration and partnership agreements
                - Funding sources and investment requirements
                - Technology platform and development capabilities
                - Competitive landscape and differentiation
                - Development timeline and risk assessment
            """,
            "Quality Assurance": """
                Extract quality assurance information:
                - Quality management system and standards
                - Validation protocols and acceptance criteria
                - Batch records and manufacturing documentation
                - Deviation investigations and corrective actions
                - Quality control testing and specifications
                - Supplier qualification and audits
                - Change control and documentation
                - Training records and competency assessments
                - Quality metrics and trending analysis
                - Regulatory inspection findings and responses
            """,
            "Patient Care": """
                Extract patient care information:
                - Patient identification and demographics
                - Medical history and comorbidities
                - Diagnosis and disease staging
                - Treatment plans and therapeutic interventions
                - Medication administration and dosing
                - Monitoring parameters and laboratory values
                - Adverse events and side effect management
                - Patient outcomes and response to treatment
                - Care coordination and multidisciplinary team
                - Discharge planning and follow-up care
            """,
            "Medical Affairs": """
                Extract medical affairs information:
                - Medical strategy and therapeutic positioning
                - Key opinion leader relationships and activities
                - Scientific publications and medical communications
                - Medical education programs and training materials
                - Advisory board meetings and expert input
                - Medical information and inquiry responses
                - Evidence generation and real-world data studies
                - Medical review of promotional materials
                - Regulatory and compliance considerations
                - Cross-functional collaboration and support
            """,
            "Pharmacovigilance": """
                Extract pharmacovigilance information:
                - Adverse event description and classification
                - Patient information and concomitant medications
                - Event onset, duration, and outcome
                - Causality assessment and relationship to product
                - Reporting requirements and timelines
                - Risk management plans and mitigation strategies
                - Signal detection and safety monitoring
                - Periodic safety update reports
                - Regulatory communication and notifications
                - Safety database and data management
            """,
            "Manufacturing": """
                Extract manufacturing information:
                - Manufacturing site and facility specifications
                - Production processes and equipment requirements
                - Raw materials and component specifications
                - Batch size and production capacity
                - Quality control testing and release criteria
                - Supply chain and vendor management
                - Packaging and labeling requirements
                - Stability studies and shelf life determination
                - Technology transfer and process validation
                - Cost of goods and manufacturing economics
            """,
            "Commercial Operations": """
                Extract commercial operations information:
                - Product launch strategy and timeline
                - Market access and reimbursement strategy
                - Pricing and value proposition
                - Sales force training and deployment
                - Marketing campaigns and promotional materials
                - Key account management and contracting
                - Market research and competitive intelligence
                - Sales forecasting and revenue projections
                - Distribution channels and logistics
                - Performance metrics and KPI tracking
            """,
            "Health Economics": """
                Extract health economics information:
                - Economic evaluation methodology and perspective
                - Clinical outcomes and health-related quality of life
                - Cost components and resource utilization
                - Budget impact and affordability analysis
                - Comparative effectiveness and cost-effectiveness
                - Reimbursement and coverage decisions
                - Health technology assessment submissions
                - Real-world evidence and outcomes research
                - Value-based care and risk-sharing agreements
                - Pharmacoeconomic modeling and assumptions
            """,
            "Digital Health": """
                Extract digital health information:
                - Digital solution type and intended use
                - Clinical validation and evidence generation
                - User interface and patient experience
                - Data privacy and security measures
                - Regulatory pathway and approval status
                - Integration with healthcare systems
                - Clinical workflow and implementation
                - Outcomes measurement and analytics
                - Reimbursement and business model
                - Technology platform and scalability
            """,
            "Other": """
                Extract general healthcare information:
                - Document type and medical context
                - Healthcare organizations and stakeholders involved
                - Patient populations and therapeutic areas
                - Clinical or operational objectives
                - Regulatory and compliance considerations
                - Timeline and critical milestones
                - Risk factors and safety considerations
                - Quality standards and best practices
                - Economic and reimbursement implications
                - Innovation and technology applications
            """
        }
    },
    
    "insurance": {
        "categories": [
            "Underwriting", "Claims Management", "Actuarial", "Product Development",
            "Regulatory & Compliance", "Risk Management", "Customer Service",
            "Reinsurance", "Investment Management", "Technology & Operations",
            "Sales & Distribution", "Other"
        ],
        "descriptions": {
            "Underwriting": "underwriting guidelines, risk assessment, policy applications, coverage decisions",
            "Claims Management": "claims processing, damage assessments, settlement documentation, fraud investigation",
            "Actuarial": "actuarial reports, pricing models, reserve analysis, mortality studies",
            "Product Development": "product specifications, rate filings, policy forms, feature development",
            "Regulatory & Compliance": "regulatory filings, compliance reports, solvency requirements, examinations",
            "Risk Management": "risk assessments, catastrophe modeling, portfolio analysis, exposure management",
            "Customer Service": "customer communications, policy servicing, complaint resolution, retention strategies",
            "Reinsurance": "reinsurance treaties, cession reports, catastrophe coverage, risk transfer",
            "Investment Management": "investment portfolios, asset allocation, yield analysis, credit risk",
            "Technology & Operations": "system documentation, process automation, data management, digital transformation",
            "Sales & Distribution": "agent training, distribution strategies, commission structures, sales materials",
            "Other": "documents that don't fit other insurance categories"
        },
        "extraction_prompts": {
            "Underwriting": """
                Extract underwriting information:
                - Policy number and applicant information
                - Coverage type and limits requested
                - Risk assessment factors and scoring
                - Underwriting guidelines and criteria
                - Premium calculations and rating factors
                - Coverage decisions and conditions
                - Exclusions and policy limitations
                - Underwriter review and approval process
                - Risk mitigation requirements
                - Policy terms and effective dates
            """,
            "Claims Management": """
                Extract claims management information:
                - Claim number and policy details
                - Loss date, cause, and circumstances
                - Claimant information and coverage verification
                - Damage assessment and repair estimates
                - Investigation findings and documentation
                - Settlement amounts and payment details
                - Fraud indicators and investigation results
                - Legal proceedings and coverage disputes
                - Reserve adjustments and claim closure
                - Customer communications and satisfaction
            """,
            "Actuarial": """
                Extract actuarial information:
                - Analysis type and methodology
                - Data sources and statistical assumptions
                - Pricing models and rating factors
                - Loss projections and claim frequency
                - Reserve adequacy and development patterns
                - Mortality and morbidity assumptions
                - Catastrophe modeling and scenario analysis
                - Regulatory capital requirements
                - Profitability analysis and target returns
                - Model validation and sensitivity testing
            """,
            "Product Development": """
                Extract product development information:
                - Product name and target market
                - Coverage features and policy benefits
                - Pricing strategy and competitive analysis
                - Regulatory filing requirements and approvals
                - Distribution channels and sales strategy
                - Underwriting guidelines and risk appetite
                - Claims handling procedures and protocols
                - Technology platform and system requirements
                - Launch timeline and marketing plan
                - Performance metrics and success criteria
            """,
            "Regulatory & Compliance": """
                Extract regulatory and compliance information:
                - Regulatory authority and jurisdiction
                - Filing type and submission requirements
                - Compliance framework and standards
                - Solvency and capital adequacy ratios
                - Market conduct and examination findings
                - Consumer protection and fair practice requirements
                - Rate filing and approval status
                - Reporting obligations and deadlines
                - Regulatory changes and implementation impact
                - Enforcement actions and remediation plans
            """,
            "Risk Management": """
                Extract risk management information:
                - Risk type and exposure assessment
                - Portfolio analysis and concentration limits
                - Catastrophe modeling and stress testing
                - Risk appetite and tolerance levels
                - Mitigation strategies and controls
                - Reinsurance coverage and protection
                - Capital allocation and optimization
                - Risk monitoring and reporting systems
                - Emerging risks and scenario planning
                - Risk governance and oversight framework
            """,
            "Customer Service": """
                Extract customer service information:
                - Customer contact information and policy details
                - Service request type and resolution status
                - Communication history and interaction logs
                - Policy changes and endorsement requests
                - Billing inquiries and payment processing
                - Claims status and settlement communications
                - Complaint handling and escalation procedures
                - Customer satisfaction surveys and feedback
                - Retention strategies and loyalty programs
                - Cross-selling opportunities and referrals
            """,
            "Reinsurance": """
                Extract reinsurance information:
                - Reinsurance treaty type and structure
                - Coverage limits and retention levels
                - Ceding company and reinsurer details
                - Premium calculations and payment terms
                - Claims reporting and settlement procedures
                - Catastrophe coverage and aggregate limits
                - Risk transfer objectives and strategies
                - Contract terms and renewal negotiations
                - Performance monitoring and profitability analysis
                - Regulatory and accounting treatment
            """,
            "Investment Management": """
                Extract investment management information:
                - Investment portfolio composition and allocation
                - Asset classes and investment strategies
                - Performance metrics and benchmark comparisons
                - Risk metrics and duration matching
                - Credit quality and rating distributions
                - Yield analysis and income generation
                - Liquidity requirements and cash flow projections
                - Investment policies and guidelines
                - Market risk and sensitivity analysis
                - Regulatory capital and solvency considerations
            """,
            "Technology & Operations": """
                Extract technology and operations information:
                - System architecture and platform specifications
                - Process automation and workflow optimization
                - Data management and analytics capabilities
                - Digital transformation initiatives and roadmap
                - System integration and API connectivity
                - Performance metrics and operational efficiency
                - Disaster recovery and business continuity plans
                - Vendor management and technology partnerships
                - Security protocols and data protection measures
                - Cost optimization and operational excellence programs
            """,
            "Sales & Distribution": """
                Extract sales and distribution information:
                - Distribution channel strategy and partnerships
                - Agent and broker relationships and agreements
                - Commission structures and compensation plans
                - Sales training programs and certification requirements
                - Marketing campaigns and promotional materials
                - Lead generation and customer acquisition strategies
                - Sales performance metrics and targets
                - Territory management and market coverage
                - Product positioning and competitive differentiation
                - Customer segmentation and targeting strategies
            """,
            "Other": """
                Extract general insurance information:
                - Document type and business purpose
                - Insurance company and stakeholder information
                - Policy or product details and specifications
                - Financial metrics and performance indicators
                - Regulatory and compliance considerations
                - Risk factors and mitigation strategies
                - Timeline and critical deadlines
                - Technology and operational requirements
                - Market conditions and competitive factors
                - Strategic objectives and business impact
            """
        }
    },
    
    "legal": {
        "categories": [
            "Litigation", "Corporate Law", "Regulatory & Compliance", "Intellectual Property",
            "Employment Law", "Real Estate", "Tax Law", "Contract Management",
            "Mergers & Acquisitions", "Securities & Finance", "Client Relations", "Other"
        ],
        "descriptions": {
            "Litigation": "case files, court documents, discovery materials, settlement agreements",
            "Corporate Law": "corporate governance, board resolutions, bylaws, entity formation",
            "Regulatory & Compliance": "regulatory guidance, compliance programs, investigations, enforcement actions",
            "Intellectual Property": "patent applications, trademark registrations, licensing agreements, IP litigation",
            "Employment Law": "employment contracts, HR policies, discrimination cases, labor negotiations",
            "Real Estate": "property transactions, lease agreements, zoning issues, development projects",
            "Tax Law": "tax planning, audit defense, tax opinions, compliance documentation",
            "Contract Management": "contract templates, negotiations, amendments, renewals",
            "Mergers & Acquisitions": "due diligence, purchase agreements, regulatory approvals, integration planning",
            "Securities & Finance": "securities offerings, financing agreements, regulatory filings, investor relations",
            "Client Relations": "client agreements, billing, matter management, communication logs",
            "Other": "documents that don't fit other legal practice categories"
        },
        "extraction_prompts": {
            "Litigation": "Extract case information: case number, parties, court, cause of action, key facts, legal issues, procedural status, deadlines, damages claimed, settlement terms, attorney information",
            "Corporate Law": "Extract corporate details: entity name, jurisdiction, corporate action type, board resolutions, shareholder information, governance changes, compliance requirements, filing deadlines, authorized signatories",
            "Regulatory & Compliance": "Extract regulatory information: regulatory body, compliance framework, requirements, deadlines, violations, remediation actions, policies, training requirements, audit findings, enforcement actions",
            "Intellectual Property": "Extract IP details: IP type, application/registration numbers, inventors/creators, filing dates, claims/descriptions, prosecution status, licensing terms, infringement issues, maintenance requirements",
            "Employment Law": "Extract employment information: employee details, position, compensation, benefits, policies, violations, disciplinary actions, termination reasons, legal claims, settlement terms, compliance requirements",
            "Real Estate": "Extract property information: property address, transaction type, parties, purchase price, financing terms, closing date, title issues, zoning, environmental concerns, lease terms, development plans",
            "Tax Law": "Extract tax information: tax year/period, entity/individual, tax type, amounts owed/refunded, positions taken, audit issues, penalties, settlement terms, filing requirements, deadlines",
            "Contract Management": "Extract contract details: parties, contract type, key terms, obligations, payment terms, deadlines, termination provisions, renewal options, amendments, compliance requirements, risk factors",
            "Mergers & Acquisitions": "Extract M&A information: transaction type, parties, valuation, deal structure, due diligence findings, regulatory approvals, closing conditions, integration plans, key risks, timeline",
            "Securities & Finance": "Extract securities information: offering type, securities details, parties, amounts, regulatory filings, disclosure requirements, investor information, compliance obligations, risk factors",
            "Client Relations": "Extract client information: client details, matter description, fee arrangements, billing, communication logs, deliverables, deadlines, conflicts of interest, referral sources",
            "Other": "Extract legal information: document type, parties involved, legal issues, key terms, obligations, deadlines, risks, compliance requirements, next steps, contact information"
        }
    },
    
    "manufacturing": {
        "categories": [
            "Production Operations", "Quality Control", "Supply Chain", "Engineering & Design",
            "Maintenance & Reliability", "Safety & Environmental", "Product Development",
            "Procurement", "Inventory Management", "Process Improvement", "Regulatory Compliance", "Other"
        ],
        "descriptions": {
            "Production Operations": "production schedules, work orders, capacity planning, manufacturing processes",
            "Quality Control": "quality standards, inspection reports, testing procedures, defect analysis",
            "Supply Chain": "supplier agreements, logistics planning, demand forecasting, vendor management",
            "Engineering & Design": "product designs, technical specifications, CAD drawings, engineering changes",
            "Maintenance & Reliability": "maintenance schedules, equipment manuals, reliability analysis, downtime reports",
            "Safety & Environmental": "safety protocols, environmental compliance, incident reports, training materials",
            "Product Development": "product roadmaps, R&D projects, prototype testing, market requirements",
            "Procurement": "purchase orders, supplier evaluations, contract negotiations, cost analysis",
            "Inventory Management": "inventory levels, stock optimization, warehouse operations, cycle counting",
            "Process Improvement": "lean initiatives, process mapping, efficiency studies, continuous improvement",
            "Regulatory Compliance": "industry standards, regulatory certifications, compliance audits, documentation",
            "Other": "documents that don't fit other manufacturing categories"
        },
        "extraction_prompts": {
            "Production Operations": "Extract production details: product/part numbers, production schedules, capacity utilization, work orders, shift information, equipment used, output quantities, quality metrics, downtime incidents",
            "Quality Control": "Extract quality information: inspection criteria, test results, defect rates, corrective actions, quality standards, batch/lot numbers, supplier quality, customer complaints, certification status",
            "Supply Chain": "Extract supply chain details: supplier information, purchase orders, delivery schedules, inventory levels, lead times, logistics arrangements, cost analysis, supply disruptions, vendor performance",
            "Engineering & Design": "Extract engineering information: product specifications, design changes, CAD drawings, materials specifications, testing requirements, approval processes, version control, safety considerations",
            "Maintenance & Reliability": "Extract maintenance details: equipment ID, maintenance schedules, work orders, failure analysis, spare parts, downtime costs, reliability metrics, preventive maintenance programs",
            "Safety & Environmental": "Extract safety information: incident reports, safety procedures, training records, environmental compliance, permit requirements, waste management, safety audits, regulatory inspections",
            "Product Development": "Extract development details: project timelines, design specifications, testing results, market requirements, prototype status, regulatory approvals, launch plans, cost targets",
            "Procurement": "Extract procurement information: vendor details, contract terms, pricing agreements, purchase requisitions, supplier evaluations, cost savings initiatives, procurement policies",
            "Inventory Management": "Extract inventory details: stock levels, reorder points, inventory turnover, obsolete inventory, cycle counts, storage requirements, inventory valuation, demand forecasting",
            "Process Improvement": "Extract improvement details: process maps, efficiency metrics, waste reduction initiatives, lean projects, cost savings, implementation timelines, performance improvements",
            "Regulatory Compliance": "Extract compliance information: regulatory standards, audit findings, certification requirements, inspection reports, compliance training, corrective actions, regulatory submissions",
            "Other": "Extract manufacturing information: facility details, operational metrics, personnel information, equipment specifications, process documentation, performance indicators, improvement opportunities"
        }
    },
    
    "public_sector": {
        "categories": [
            "Policy & Legislation", "Public Services", "Budget & Finance", "Procurement",
            "Regulatory & Compliance", "Public Safety", "Infrastructure", "Human Resources",
            "Community Relations", "Legal Affairs", "Performance Management", "Other"
        ],
        "descriptions": {
            "Policy & Legislation": "policy documents, legislative proposals, regulatory frameworks, public consultations",
            "Public Services": "service delivery, citizen services, program administration, service standards",
            "Budget & Finance": "budget planning, financial reports, expenditure tracking, revenue analysis",
            "Procurement": "tender documents, contract awards, supplier management, procurement policies",
            "Regulatory & Compliance": "regulatory oversight, compliance monitoring, enforcement actions, audits",
            "Public Safety": "emergency planning, security protocols, safety assessments, incident response",
            "Infrastructure": "infrastructure planning, public works, facility management, capital projects",
            "Human Resources": "staffing plans, recruitment, training programs, performance evaluations",
            "Community Relations": "public engagement, stakeholder communications, community feedback, outreach programs",
            "Legal Affairs": "legal opinions, litigation management, contract review, regulatory interpretation",
            "Performance Management": "performance metrics, program evaluation, outcome reporting, quality assurance",
            "Other": "documents that don't fit other public sector categories"
        },
        "extraction_prompts": {
            "Policy & Legislation": "Extract policy details: policy title, objectives, implementation timeline, affected stakeholders, budget requirements, regulatory framework, public consultation, approval process",
            "Public Services": "Extract service information: service type, delivery methods, performance metrics, citizen feedback, resource requirements, service standards, accessibility provisions, improvement initiatives",
            "Budget & Finance": "Extract budget details: fiscal year, budget allocations, revenue sources, expenditure categories, variance analysis, financial performance, audit findings, funding requirements",
            "Procurement": "Extract procurement information: tender details, vendor selection, contract terms, pricing, delivery requirements, evaluation criteria, compliance requirements, performance metrics",
            "Regulatory & Compliance": "Extract regulatory details: regulatory framework, compliance requirements, monitoring procedures, enforcement actions, audit results, policy updates, training requirements",
            "Public Safety": "Extract safety information: incident reports, emergency procedures, response protocols, resource deployment, training programs, equipment specifications, performance metrics",
            "Infrastructure": "Extract infrastructure details: project scope, specifications, timelines, budget, contractors, maintenance requirements, performance standards, public impact, approval processes",
            "Human Resources": "Extract HR information: staffing levels, recruitment processes, training programs, performance management, compensation, benefits, policy compliance, employee relations",
            "Community Relations": "Extract community details: stakeholder groups, engagement activities, feedback mechanisms, communication strategies, public meetings, consultation results, partnership agreements",
            "Legal Affairs": "Extract legal information: legal issues, proceedings, compliance requirements, contract reviews, risk assessments, legal opinions, regulatory interpretations, litigation status",
            "Performance Management": "Extract performance details: KPIs, targets, achievement levels, improvement plans, benchmarking, citizen satisfaction, service delivery metrics, cost-effectiveness",
            "Other": "Extract public sector information: government entity, program details, citizen impact, regulatory requirements, stakeholder involvement, performance measures, accountability mechanisms"
        }
    },
    
    "retail": {
        "categories": [
            "Merchandising", "Supply Chain & Logistics", "Store Operations", "E-commerce",
            "Marketing & Promotions", "Customer Experience", "Inventory Management",
            "Vendor Relations", "Finance & Analytics", "Technology & Systems",
            "Real Estate & Facilities", "Other"
        ],
        "descriptions": {
            "Merchandising": "product selection, buying plans, category management, assortment planning",
            "Supply Chain & Logistics": "distribution, warehousing, transportation, fulfillment operations",
            "Store Operations": "store procedures, staff training, operational standards, performance metrics",
            "E-commerce": "online operations, digital marketing, website management, mobile commerce",
            "Marketing & Promotions": "advertising campaigns, promotional strategies, brand management, customer acquisition",
            "Customer Experience": "customer service, loyalty programs, feedback analysis, satisfaction surveys",
            "Inventory Management": "stock levels, replenishment, demand planning, inventory optimization",
            "Vendor Relations": "supplier agreements, vendor performance, product sourcing, negotiations",
            "Finance & Analytics": "sales analysis, financial planning, pricing strategies, profitability analysis",
            "Technology & Systems": "POS systems, inventory systems, technology infrastructure, digital transformation",
            "Real Estate & Facilities": "store locations, lease agreements, facility management, expansion planning",
            "Other": "documents that don't fit other retail categories"
        },
        "extraction_prompts": {
            "Merchandising": "Extract merchandising details: product categories, buying plans, vendor negotiations, pricing strategies, assortment planning, seasonal planning, inventory targets, margin analysis",
            "Supply Chain & Logistics": "Extract logistics information: distribution centers, transportation modes, delivery schedules, fulfillment metrics, warehouse operations, shipping costs, supply chain disruptions",
            "Store Operations": "Extract store details: store locations, operational procedures, staff schedules, sales performance, customer traffic, store layouts, maintenance requirements, security protocols",
            "E-commerce": "Extract e-commerce information: website performance, online sales, digital marketing, conversion rates, customer acquisition, mobile commerce, platform capabilities, technology integrations",
            "Marketing & Promotions": "Extract marketing details: campaign objectives, target demographics, promotional offers, media channels, campaign performance, brand positioning, customer engagement, ROI analysis",
            "Customer Experience": "Extract CX information: customer feedback, satisfaction scores, loyalty programs, service issues, customer journey, touchpoint analysis, experience improvements, retention strategies",
            "Inventory Management": "Extract inventory details: stock levels, turnover rates, demand forecasting, replenishment strategies, obsolete inventory, inventory costs, distribution planning, seasonal adjustments",
            "Vendor Relations": "Extract vendor information: supplier agreements, product sourcing, vendor performance, negotiation terms, quality standards, delivery performance, cost management, partnership strategies",
            "Finance & Analytics": "Extract financial details: sales analysis, profitability metrics, cost management, pricing optimization, financial forecasting, budget performance, investment analysis, performance dashboards",
            "Technology & Systems": "Extract technology information: system capabilities, POS systems, inventory systems, customer databases, technology upgrades, system performance, data analytics, integration requirements",
            "Real Estate & Facilities": "Extract facilities information: store locations, lease terms, facility management, space utilization, expansion plans, real estate costs, location analysis, site selection criteria",
            "Other": "Extract retail information: business operations, performance metrics, customer demographics, market trends, competitive analysis, strategic initiatives, operational challenges, growth opportunities"
        }
    },
    
    "transportation_logistics": {
        "categories": [
            "Fleet Management", "Operations & Scheduling", "Safety & Compliance",
            "Supply Chain Optimization", "Customer Service", "Technology & Systems",
            "Maintenance & Repair", "Freight & Cargo", "Route Planning",
            "Regulatory Affairs", "Finance & Costing", "Other"
        ],
        "descriptions": {
            "Fleet Management": "vehicle specifications, fleet planning, asset utilization, replacement schedules",
            "Operations & Scheduling": "route optimization, dispatch operations, capacity planning, service schedules",
            "Safety & Compliance": "safety protocols, DOT compliance, driver training, accident reports",
            "Supply Chain Optimization": "logistics planning, network design, distribution strategies, efficiency studies",
            "Customer Service": "service agreements, delivery confirmations, customer communications, issue resolution",
            "Technology & Systems": "tracking systems, logistics software, automation technologies, digital platforms",
            "Maintenance & Repair": "maintenance schedules, repair procedures, equipment specifications, downtime analysis",
            "Freight & Cargo": "shipping documentation, cargo manifests, freight agreements, handling procedures",
            "Route Planning": "route optimization, traffic analysis, delivery schedules, geographic planning",
            "Regulatory Affairs": "transportation regulations, permit applications, compliance documentation, inspections",
            "Finance & Costing": "cost analysis, pricing models, fuel management, profitability studies",
            "Other": "documents that don't fit other transportation and logistics categories"
        },
        "extraction_prompts": {
            "Fleet Management": "Extract fleet details: vehicle information, fleet size, utilization rates, maintenance schedules, fuel costs, driver assignments, vehicle specifications, replacement planning, performance metrics",
            "Operations & Scheduling": "Extract operations information: route schedules, dispatch operations, capacity planning, service levels, operational efficiency, resource allocation, performance targets, optimization strategies",
            "Safety & Compliance": "Extract safety details: safety incidents, compliance status, driver qualifications, safety training, vehicle inspections, regulatory requirements, safety protocols, accident reports",
            "Supply Chain Optimization": "Extract supply chain information: logistics networks, distribution strategies, optimization models, cost analysis, service improvements, capacity utilization, network design",
            "Customer Service": "Extract service details: customer requirements, service agreements, delivery confirmations, issue resolution, performance metrics, customer satisfaction, communication protocols",
            "Technology & Systems": "Extract technology information: tracking systems, logistics software, automation technologies, system capabilities, technology upgrades, data analytics, integration requirements",
            "Maintenance & Repair": "Extract maintenance details: maintenance schedules, repair procedures, equipment specifications, downtime analysis, maintenance costs, preventive maintenance, vendor relationships",
            "Freight & Cargo": "Extract cargo information: shipment details, cargo specifications, handling procedures, documentation requirements, freight rates, cargo security, special handling requirements",
            "Route Planning": "Extract routing details: route optimization, traffic analysis, delivery schedules, geographic coverage, route efficiency, planning algorithms, delivery windows, service areas",
            "Regulatory Affairs": "Extract regulatory information: transportation regulations, permit requirements, compliance documentation, regulatory inspections, licensing requirements, safety standards",
            "Finance & Costing": "Extract financial details: cost analysis, pricing models, revenue analysis, fuel management, operational costs, profitability analysis, budget planning, cost optimization",
            "Other": "Extract transportation information: operational details, performance metrics, service requirements, regulatory considerations, technology needs, strategic objectives, market conditions"
        }
    }
}

def get_categories_for_industry(industry: str) -> dict:
    """Get categories and descriptions for a specific industry"""
    return INDUSTRY_CATEGORIES.get(industry.lower(), INDUSTRY_CATEGORIES["general"])

def get_available_industries() -> list:
    """Get list of all available industries"""
    return list(INDUSTRY_CATEGORIES.keys())
